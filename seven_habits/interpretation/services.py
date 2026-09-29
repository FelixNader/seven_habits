import frappe


def classify_subject(subject_doctype, subject_name, classifications, status="Draft"):
	"""Attach evolving meaning to a subject without changing the subject itself."""
	doc = frappe.get_doc({"doctype": "SH Interpretation", "subject_doctype": subject_doctype,
		"subject_name": subject_name, "status": status, "classifications": classifications})
	doc.insert()
	return doc.name
