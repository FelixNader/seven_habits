from frappe.model.document import Document

from seven_habits.scheduling.domain import validate_interval


class SHEvent(Document):
	def validate(self):
		validate_interval(self.start_datetime, self.end_datetime)
