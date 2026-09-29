import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class SHActivityFact(Document):
	def before_insert(self):
		self.recorded_at = now_datetime()

	def validate(self):
		if not self.effective_at:
			self.effective_at = now_datetime()

	def before_save(self):
		if self.is_new():
			return
		previous = self.get_doc_before_save()
		if not previous:
			return
		protected = ("raw_text", "effective_at", "fact_kind", "source")
		if any(self.get(field) != previous.get(field) for field in protected):
			frappe.throw("Los hechos no se editan directamente; agrega una corrección auditada.")
