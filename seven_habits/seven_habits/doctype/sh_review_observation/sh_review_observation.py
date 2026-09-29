import frappe
from frappe.model.document import Document


class SHReviewObservation(Document):
	def validate(self):
		allowed = {"SH Task", "SH Event", "SH Activity Fact", "SH Commitment", "SH Role", "SH Goal", "SH Project", "SH Habit"}
		if self.subject_type not in allowed:
			frappe.throw("El tipo de subject debe pertenecer a Seven Habits.")
		if self.planned_minutes is not None and self.planned_minutes < 0:
			frappe.throw("Los minutos planificados no pueden ser negativos.")
		if self.actual_minutes is not None and self.actual_minutes < 0:
			frappe.throw("Los minutos reales no pueden ser negativos.")
		if self.subject_type and self.subject_reference and frappe.db.exists(self.subject_type, self.subject_reference) is None:
			frappe.throw("El subject de la observación no existe.")
		if self.actual_minutes is not None and self.planned_minutes is not None:
			self.variance_minutes = self.actual_minutes - self.planned_minutes
		else:
			self.variance_minutes = None
