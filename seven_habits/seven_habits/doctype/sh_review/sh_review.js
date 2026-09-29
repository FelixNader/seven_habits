frappe.ui.form.on("SH Review Observation", {
	subject_type(frm, cdt, cdn) {
		frappe.model.set_value(cdt, cdn, "subject_reference", "");
		frm.refresh_field("observations");
	}
});

frappe.ui.form.on("SH Adjustment Decision", {
	target_doctype(frm, cdt, cdn) {
		frappe.model.set_value(cdt, cdn, "target_name", "");
		frm.refresh_field("adjustment_decisions");
	}
});
