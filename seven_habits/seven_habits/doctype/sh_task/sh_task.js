frappe.ui.form.on("SH Task", {
	allocations_add(frm, cdt, cdn) {
		const row = frappe.get_doc(cdt, cdn);
		const start = frappe.datetime.add_minutes(frappe.datetime.now_datetime(), 5);
		frappe.model.set_value(cdt, cdn, "start_datetime", start);
		frappe.model.set_value(cdt, cdn, "end_datetime", frappe.datetime.add_minutes(start, 60));
	}
});
