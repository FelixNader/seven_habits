import frappe
from frappe.model.document import Document


class SHCommitmentAlignment(Document):
	def validate(self):
		expected_doctypes = {
			"Role": "SH Role",
			"Goal": "SH Goal",
			"Project": "SH Project",
			"Habit": "SH Habit",
		}
		expected = expected_doctypes.get(self.dimension_type)
		if expected and self.reference_doctype != expected:
			frappe.throw(f"{self.dimension_type} debe referenciar {expected}.")
