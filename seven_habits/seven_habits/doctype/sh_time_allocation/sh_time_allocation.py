import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_datetime

from seven_habits.scheduling.domain import validate_interval


class SHTimeAllocation(Document):
	def validate(self):
		validate_interval(self.start_datetime, self.end_datetime)
		if get_datetime(self.start_datetime) <= now_datetime():
			frappe.throw("Start debe ser posterior a la hora actual.")
