"""Thin Frappe API adapters. Domain work belongs in bounded-context services."""

from __future__ import annotations

import frappe

from seven_habits.commitment.services import assume_commitment as _assume_commitment
from seven_habits.ledger.services import capture_fact as _capture_fact
from seven_habits.ledger.services import correct_fact as _correct_fact
from seven_habits.scheduling.services import agenda_for_day as _agenda_for_day, plan_vs_real as _plan_vs_real, schedule_commitment_as_task as _schedule_task, allocate_task_time as _allocate_time, create_event as _create_event, reschedule_event as _reschedule_event
from seven_habits.interpretation.services import classify_subject as _classify_subject
from seven_habits.review.services import start_review as _start_review
from seven_habits.review.services import close_review as _close_review
from seven_habits.review.decisions import apply_adjustment_decision as _apply_adjustment_decision


def has_app_permission() -> bool:
	"""Show the app to authenticated users; DocType permissions remain authoritative."""
	return frappe.session.user not in {"Guest", "Administrator"} or frappe.session.user == "Administrator"


@frappe.whitelist()
def assume_commitment(statement: str, origin: str = "Manual") -> str:
	return _assume_commitment(statement, origin=origin)


@frappe.whitelist()
def capture_activity_fact(
	raw_text: str,
	effective_at: str | None = None,
	fact_kind: str = "Unknown",
	source: str = "Quick Capture",
) -> str:
	"""Record a real-world fact without requiring prior classification."""
	return _capture_fact(raw_text, effective_at, fact_kind, source)


@frappe.whitelist()
def correct_activity_fact(fact_name: str, field_name: str, corrected_value: str, reason: str) -> str:
	"""Append an audit correction; the original fact remains intact."""
	return _correct_fact(fact_name, field_name, corrected_value, reason)


@frappe.whitelist()
def get_agenda(day: str | None = None) -> list[dict]:
	"""Return the Agenda projection; Task and Event remain its source of truth."""
	return _agenda_for_day(day)


@frappe.whitelist()
def classify_subject(subject_doctype, subject_name, classifications, status="Draft"):
	return _classify_subject(subject_doctype, subject_name, frappe.parse_json(classifications), status)


@frappe.whitelist()
def start_review(review_type, period_start, period_end):
	return _start_review(review_type, period_start, period_end)


@frappe.whitelist()
def close_review(review_name, summary=""):
	return _close_review(review_name, summary)


@frappe.whitelist()
def apply_adjustment_decision(decision_name):
	return _apply_adjustment_decision(decision_name)


@frappe.whitelist()
def get_timeline(day=None):
	filters = {"voided": 0}
	if day:
		filters["effective_at"] = ["between", [f"{day} 00:00:00", f"{day} 23:59:59"]]
	return frappe.get_all("SH Activity Fact", filters=filters, fields=["name", "raw_text", "effective_at", "fact_kind"], order_by="effective_at desc")

@frappe.whitelist()
def get_plan_vs_real(day=None, commitment=None):
	return _plan_vs_real(day, commitment)

@frappe.whitelist()
def schedule_as_task(commitment, title=None, planned_effort_min=None):
	return _schedule_task(commitment, title, planned_effort_min)

@frappe.whitelist()
def allocate_task_time(task, start_datetime, end_datetime):
	return _allocate_time(task, start_datetime, end_datetime)

@frappe.whitelist()
def create_event(title, start_datetime, end_datetime, commitment=None, **kwargs):
	return _create_event(title, start_datetime, end_datetime, commitment, **kwargs)

@frappe.whitelist()
def reschedule_event(event, start_datetime, end_datetime):
	return _reschedule_event(event, start_datetime, end_datetime)
