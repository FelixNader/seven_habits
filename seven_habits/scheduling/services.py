from __future__ import annotations

import frappe
from frappe.utils import add_days, getdate


def schedule_commitment_as_task(commitment, title=None, planned_effort_min=None):
	doc = frappe.get_doc({"doctype": "SH Task", "commitment": commitment, "title": title,
		"planned_effort_min": planned_effort_min})
	doc.insert()
	return doc.name


def allocate_task_time(task, start_datetime, end_datetime):
	doc = frappe.get_doc("SH Task", task)
	doc.append("allocations", {"start_datetime": start_datetime, "end_datetime": end_datetime, "status": "Planned"})
	doc.save()
	return doc.name


def create_event(title, start_datetime, end_datetime, commitment=None, **kwargs):
	doc = frappe.get_doc({"doctype": "SH Event", "title": title, "start_datetime": start_datetime,
		"end_datetime": end_datetime, "commitment": commitment, **kwargs})
	doc.insert()
	return doc.name


def reschedule_event(event, start_datetime, end_datetime):
	"""Reschedule through a semantic operation; Frappe track_changes keeps the history."""
	doc = frappe.get_doc("SH Event", event)
	doc.start_datetime = start_datetime
	doc.end_datetime = end_datetime
	doc.save()
	return doc.name


def agenda_for_day(day: str | None = None) -> list[dict]:
	"""Project planned allocations and fixed events into one chronological agenda."""
	date = getdate(day)
	start = f"{date} 00:00:00"
	end = f"{add_days(date, 1)} 00:00:00"
	allocations = frappe.db.sql(
		"""
		SELECT allocation.name, allocation.parent AS task, task.title, task.commitment,
			allocation.start_datetime, allocation.end_datetime
		FROM `tabSH Time Allocation` allocation
		INNER JOIN `tabSH Task` task ON task.name = allocation.parent
		WHERE allocation.parenttype = 'SH Task'
			AND allocation.status = 'Planned'
			AND task.status != 'Cancelled'
			AND allocation.start_datetime < %(end)s
			AND allocation.end_datetime > %(start)s
		""",
		{"start": start, "end": end},
		as_dict=True,
	)
	events = frappe.db.sql(
		"""
		SELECT name, title, commitment, start_datetime, end_datetime
		FROM `tabSH Event`
		WHERE status != 'Cancelled'
			AND start_datetime < %(end)s
			AND end_datetime > %(start)s
		""",
		{"start": start, "end": end},
		as_dict=True,
	)
	items = [
		{
			"type": "Task",
			"name": row.task,
			"title": row.title,
			"commitment": row.commitment,
			"start_datetime": row.start_datetime,
			"end_datetime": row.end_datetime,
		}
		for row in allocations
	]
	items.extend(
		{
			"type": "Event",
			"name": row.name,
			"title": row.title,
			"commitment": row.commitment,
			"start_datetime": row.start_datetime,
			"end_datetime": row.end_datetime,
		}
		for row in events
	)
	return sorted(items, key=lambda item: item["start_datetime"])


def plan_vs_real(day: str | None = None, commitment: str | None = None) -> list[dict]:
	"""Return planned minutes and evidence; real duration remains unknown unless derived reliably."""
	date = getdate(day)
	start, end = f"{date} 00:00:00", f"{add_days(date, 1)} 00:00:00"
	allocations = frappe.db.sql("""
		SELECT task.commitment,
			SUM(TIMESTAMPDIFF(MINUTE, GREATEST(allocation.start_datetime, %(start)s), LEAST(allocation.end_datetime, %(end)s))) minutes
		FROM `tabSH Time Allocation` allocation JOIN `tabSH Task` task ON task.name=allocation.parent
		WHERE allocation.parenttype='SH Task' AND allocation.status='Planned' AND task.status!='Cancelled'
		AND allocation.start_datetime < %(end)s AND allocation.end_datetime > %(start)s
		GROUP BY task.commitment
	""", {"start": start, "end": end}, as_dict=True)
	events = frappe.db.sql("""
		SELECT commitment,
			SUM(TIMESTAMPDIFF(MINUTE, GREATEST(start_datetime, %(start)s), LEAST(end_datetime, %(end)s))) minutes
		FROM `tabSH Event`
		WHERE status!='Cancelled' AND commitment IS NOT NULL AND commitment!=''
		AND start_datetime < %(end)s AND end_datetime > %(start)s
		GROUP BY commitment
	""", {"start": start, "end": end}, as_dict=True)
	planned_by_commitment = {}
	for row in allocations + events:
		planned_by_commitment[row.commitment] = planned_by_commitment.get(row.commitment, 0) + row.minutes
	planned = [frappe._dict(commitment=name, minutes=minutes) for name, minutes in planned_by_commitment.items()]
	if commitment:
		planned = [row for row in planned if row.commitment == commitment]
	result = [{"commitment": row.commitment, "commitment_text": frappe.db.get_value("SH Commitment", row.commitment, "statement") or row.commitment, "planned_minutes": row.minutes, "actual_minutes": None, "facts": []} for row in planned]
	by_commitment = {row["commitment"]: row for row in result}
	planned_items = frappe.db.sql("""
		SELECT task.commitment, task.title, allocation.start_datetime, allocation.end_datetime, 'Task' item_type
		FROM `tabSH Time Allocation` allocation JOIN `tabSH Task` task ON task.name=allocation.parent
		WHERE allocation.parenttype='SH Task' AND allocation.status='Planned' AND task.status!='Cancelled'
		AND allocation.start_datetime < %(end)s AND allocation.end_datetime > %(start)s
		UNION ALL
		SELECT commitment, title, start_datetime, end_datetime, 'Event' item_type
		FROM `tabSH Event`
		WHERE status!='Cancelled' AND commitment IS NOT NULL AND commitment!=''
		AND start_datetime < %(end)s AND end_datetime > %(start)s
	""", {"start": start, "end": end}, as_dict=True)
	for item in planned_items:
		if item.commitment in by_commitment:
			by_commitment[item.commitment].setdefault("planned_items", []).append(dict(item))
	facts = frappe.db.sql("""
		SELECT DISTINCT fact.name, fact.raw_text, fact.effective_at, classification.reference_name commitment, classification.dimension_type, classification.reference_doctype
		FROM `tabSH Activity Fact` fact
		JOIN `tabSH Interpretation` interpretation ON interpretation.subject_doctype='SH Activity Fact' AND interpretation.subject_name=fact.name
		JOIN `tabSH Classification` classification ON classification.parent=interpretation.name AND classification.parenttype='SH Interpretation'
		WHERE fact.voided=0 AND fact.effective_at BETWEEN %(start)s AND %(end)s
		AND classification.dimension_type IN ('Role','Goal','Project','Habit','Commitment','Task','Event') AND classification.accepted=1
	""", {"start": start, "end": end}, as_dict=True)
	for fact in facts:
		if commitment and fact.commitment != commitment: continue
		group_key = fact.commitment if fact.dimension_type == "Commitment" else f"{fact.dimension_type}:{fact.commitment}"
		title_field = frappe.get_meta(fact.reference_doctype).get_title_field() or "name"
		label = frappe.db.get_value(fact.reference_doctype, fact.commitment, title_field) or fact.commitment
		if fact.dimension_type != "Commitment": label = f"{fact.dimension_type}: {label}"
		row = by_commitment.setdefault(group_key, {"commitment": fact.commitment if fact.dimension_type == "Commitment" else None, "commitment_text": label, "planned_minutes": 0, "actual_minutes": None, "facts": [], "planned_items": []})
		row["facts"].append(dict(fact))
	for row in by_commitment.values():
		if row not in result:
			result.append(row)
	unclassified = frappe.db.sql("""
		SELECT fact.name, fact.raw_text, fact.effective_at
		FROM `tabSH Activity Fact` fact
		WHERE fact.voided=0 AND fact.effective_at BETWEEN %(start)s AND %(end)s
		AND NOT EXISTS (
			SELECT 1 FROM `tabSH Interpretation` interpretation
			JOIN `tabSH Classification` classification ON classification.parent=interpretation.name AND classification.parenttype='SH Interpretation'
			WHERE interpretation.subject_doctype='SH Activity Fact' AND interpretation.subject_name=fact.name
			AND classification.accepted=1
		)
	""", {"start": start, "end": end}, as_dict=True)
	if unclassified:
		result.append({"commitment": None, "commitment_text": "Hechos pendientes de interpretar", "planned_minutes": 0, "actual_minutes": None, "facts": [dict(f) for f in unclassified], "planned_items": []})
	return result
