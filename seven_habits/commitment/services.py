"""Application services for commitments.

Frappe DocTypes persist state; semantic actions remain explicit here.
"""

from __future__ import annotations

import frappe


def assume_commitment(statement: str, *, origin: str = "Manual") -> str:
	if not statement or not statement.strip():
		frappe.throw("A commitment needs a statement.")
	doc = frappe.get_doc({
		"doctype": "SH Commitment",
		"statement": statement.strip(),
		"origin": origin,
	})
	doc.insert()
	return doc.name
