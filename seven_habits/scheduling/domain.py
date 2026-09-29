from __future__ import annotations

from datetime import datetime


def validate_interval(start_datetime: datetime, end_datetime: datetime) -> None:
	"""A scheduled item must have a strictly positive time interval."""
	if end_datetime <= start_datetime:
		raise ValueError("La fecha final debe ser posterior a la fecha inicial.")


def validate_no_overlapping_allocations(allocations: list[object]) -> None:
	"""Validate allocations belonging to one task, ignoring cancelled ones."""
	active = sorted(
		(
			allocation
			for allocation in allocations
			if getattr(allocation, "status", "Planned") != "Cancelled"
		),
		key=lambda allocation: allocation.start_datetime,
	)
	for previous, current in zip(active, active[1:]):
		if current.start_datetime < previous.end_datetime:
			raise ValueError("Las asignaciones de una misma tarea no pueden solaparse.")
