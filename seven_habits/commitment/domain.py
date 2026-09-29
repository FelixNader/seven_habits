"""Pure domain rules for the Commitment bounded context."""

from __future__ import annotations


def derive_quadrant(importance: str | None, urgency: str | None) -> str:
	"""Return the Eisenhower quadrant; unclassified inputs have no quadrant."""
	if importance == "Important" and urgency == "Urgent":
		return "Q1"
	if importance == "Important" and urgency == "Not Urgent":
		return "Q2"
	if importance == "Not Important" and urgency == "Urgent":
		return "Q3"
	if importance == "Not Important" and urgency == "Not Urgent":
		return "Q4"
	return ""
