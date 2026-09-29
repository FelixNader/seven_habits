from __future__ import annotations

import frappe
from frappe.utils import now_datetime

from seven_habits.ledger.domain import validate_correction


def capture_fact(raw_text: str, effective_at=None, fact_kind: str = "Unknown", source: str = "Quick Capture") -> str:
	if not raw_text or not raw_text.strip():
		frappe.throw("El hecho requiere texto.")
	fact = frappe.get_doc({
		"doctype": "SH Activity Fact",
		"raw_text": raw_text.strip(),
		"effective_at": effective_at or now_datetime(),
		"fact_kind": fact_kind,
		"source": source,
	})
	fact.insert()
	return fact.name


def correct_fact(fact_name: str, field_name: str, corrected_value: str, reason: str) -> str:
	fact = frappe.get_doc("SH Activity Fact", fact_name)
	previous_value = fact.get(field_name)
	validate_correction(field_name, previous_value, corrected_value, reason)
	fact.append("corrections", {
		"field_name": field_name,
		"previous_value": str(previous_value),
		"corrected_value": corrected_value,
		"reason": reason.strip(),
		"corrected_at": now_datetime(),
	})
	fact.save()
	return fact.name
