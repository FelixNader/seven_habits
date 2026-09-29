from frappe.model.document import Document
import frappe

ALLOWED_SUBJECTS = {"SH Task", "SH Event", "SH Activity Fact", "SH Commitment"}


class SHInterpretation(Document):
	def validate(self):
		if self.subject_doctype not in ALLOWED_SUBJECTS:
			frappe.throw("Subject debe ser un objeto de Seven Habits (Task, Event, Activity Fact o Commitment).")
		if self.subject_name and not frappe.db.exists(self.subject_doctype, self.subject_name):
			frappe.throw("El Subject seleccionado no existe.")
