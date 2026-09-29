import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class SHReflection(Document):
	def before_insert(self):
		self.created_at = now_datetime()
		self.author = frappe.session.user

	def validate(self):
		if self.parent and frappe.db.get_value("SH Review", self.parent, "status") == "Closed":
			frappe.throw("No se pueden modificar reflexiones de una revisión cerrada.")
