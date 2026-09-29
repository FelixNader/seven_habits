import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class SHReview(Document):
	def validate(self):
		if getdate(self.period_end) < getdate(self.period_start):
			frappe.throw("El final del período no puede ser anterior al inicio.")
		if self.status not in {"Open", "Closed"}:
			frappe.throw("Estado de revisión inválido.")
		if not self.is_new() and frappe.db.get_value(self.doctype, self.name, "status") == "Closed":
			frappe.throw("Una revisión cerrada no puede modificarse.")

	def on_trash(self):
		if self.status == "Closed":
			frappe.throw("Una revisión cerrada no puede eliminarse.")
