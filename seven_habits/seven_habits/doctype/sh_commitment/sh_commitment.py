from __future__ import annotations

import frappe
from frappe.model.document import Document

from seven_habits.commitment.domain import derive_quadrant


class SHCommitment(Document):
	def validate(self):
		# A commitment decides responsibility; it deliberately owns no time fields.
		self.quadrant = derive_quadrant(self.importance, self.urgency)
		if not self.created_at:
			from frappe.utils import now_datetime

			self.created_at = now_datetime()

	def on_trash(self):
		if self.status in {"Satisfied", "Released"}:
			frappe.throw("Los compromisos satisfechos o liberados se conservan como historial.")
