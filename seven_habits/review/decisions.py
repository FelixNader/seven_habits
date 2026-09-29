import frappe


def apply_adjustment_decision(decision_name: str) -> str:
	decision = frappe.get_doc("SH Adjustment Decision", decision_name)
	if decision.status != "Accepted":
		frappe.throw("Sólo se pueden aplicar decisiones Accepted.")
	target = frappe.get_doc(decision.target_doctype, decision.target_name)
	action = (decision.action or "").strip().lower()
	if action in {"cancel", "cancelar"} and hasattr(target, "status"):
		target.status = "Cancelled"
	elif action in {"suspend", "suspender"} and hasattr(target, "status"):
		target.status = "Suspended"
	elif action in {"complete", "completar"} and hasattr(target, "status"):
		target.status = "Completed"
	else:
		frappe.throw("Acción de ajuste no soportada para aplicación automática.")
	target.save()
	decision.status = "Applied"
	decision.save()
	return decision.name
