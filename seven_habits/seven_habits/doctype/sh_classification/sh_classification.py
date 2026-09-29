import frappe
from frappe.model.document import Document

DIMENSION_DOCTYPES = {
	"Role": "SH Role",
	"Goal": "SH Goal",
	"Project": "SH Project",
	"Habit": "SH Habit",
	"Commitment": "SH Commitment",
	"Task": "SH Task",
	"Event": "SH Event",
}


class SHClassification(Document):
	def validate(self):
		expected = DIMENSION_DOCTYPES.get(self.dimension_type)
		if expected and self.reference_doctype != expected:
			frappe.throw(f"{self.dimension_type} debe referenciar {expected}.")
		if expected and self.reference_name and not frappe.db.exists(expected, self.reference_name):
			frappe.throw("La referencia seleccionada no existe.")
