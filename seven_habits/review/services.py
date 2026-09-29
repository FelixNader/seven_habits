import frappe
from frappe.utils import add_days, getdate
from seven_habits.scheduling.services import plan_vs_real


def start_review(review_type, period_start, period_end):
	period_start, period_end = getdate(period_start), getdate(period_end)
	if period_end < period_start:
		frappe.throw("El final del período no puede ser anterior al inicio.")
	doc = frappe.get_doc({"doctype": "SH Review", "review_type": review_type,
		"period_start": period_start, "period_end": period_end, "status": "Open"})
	doc.insert()
	day = period_start
	while day <= period_end:
		for row in plan_vs_real(day):
			doc.append("observations", {
				"subject_type": "SH Commitment",
				"subject_reference": row.commitment,
				"planned_minutes": row.planned_minutes,
				"actual_minutes": row.actual_minutes,
				"note": f"{len(row.facts)} hecho(s) relacionado(s)" if row.facts else "",
			})
		day = add_days(day, 1)
	if doc.observations:
		doc.save()
	return doc.name


def close_review(review_name, summary=""):
	doc = frappe.get_doc("SH Review", review_name)
	if doc.status == "Closed":
		frappe.throw("La revisión ya está cerrada.")
	for decision in doc.adjustment_decisions or []:
		if decision.status == "Accepted" and (not decision.target_doctype or not decision.target_name):
			frappe.throw("Toda decisión Accepted debe tener un objetivo válido antes de cerrar.")
	doc.status = "Closed"
	doc.summary = summary
	doc.save()
	return doc.name
