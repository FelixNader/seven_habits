import frappe
from frappe.model.document import Document


class SHMission(Document):
	def validate(self):
		if self.active and frappe.db.exists("SH Mission", {"active": 1, "name": ["!=", self.name]}):
			frappe.throw("Sólo puede existir una misión activa.")
