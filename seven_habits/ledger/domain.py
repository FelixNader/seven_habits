from __future__ import annotations


CORRECTABLE_FACT_FIELDS = frozenset({"raw_text", "effective_at", "fact_kind"})


def validate_correction(field_name: str, previous_value: object, corrected_value: object, reason: str) -> None:
	if field_name not in CORRECTABLE_FACT_FIELDS:
		raise ValueError(f"El campo {field_name} no admite correcciones auditadas.")
	if str(previous_value) == str(corrected_value):
		raise ValueError("La corrección debe cambiar el valor efectivo.")
	if not reason or not reason.strip():
		raise ValueError("Una corrección requiere motivo.")
