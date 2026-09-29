import frappe
from frappe.model.document import Document

from seven_habits.scheduling.domain import validate_no_overlapping_allocations


class SHTask(Document):
	def before_validate(self):
		if not self.title and self.commitment:
			self.title = frappe.db.get_value("SH Commitment", self.commitment, "statement")

	def validate(self):
		validate_no_overlapping_allocations(self.allocations or [])
