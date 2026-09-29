import frappe
from frappe.model.document import Document

ALLOWED_TARGETS = {"SH Role", "SH Goal", "SH Project", "SH Habit", "SH Commitment", "SH Task", "SH Event"}


class SHAdjustmentDecision(Document):
	def validate(self):
		if self.target_doctype not in ALLOWED_TARGETS:
			frappe.throw("La decisión sólo puede apuntar a objetos de Seven Habits.")
		if self.target_name and not frappe.db.exists(self.target_doctype, self.target_name):
			frappe.throw("El objetivo de la decisión no existe.")
		if not self.reason and self.status in {"Accepted", "Applied"}:
			frappe.throw("Una decisión aceptada requiere un motivo.")
