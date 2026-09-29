const classificationDoctypes = {
	Role: "SH Role",
	Goal: "SH Goal",
	Project: "SH Project",
	Habit: "SH Habit",
	Commitment: "SH Commitment"
	,Task: "SH Task"
	,Event: "SH Event"
};

frappe.ui.form.on("SH Interpretation", {
	setup(frm) {
		frm.set_query("reference_name", "classifications", (_doc, cdt, cdn) => {
			const row = frappe.get_doc(cdt, cdn);
			const doctype = classificationDoctypes[row.dimension_type];
			return doctype ? { filters: { name: ["is", "set"] } } : {};
		});
	},
});

frappe.ui.form.on("SH Classification", {
	dimension_type(frm, cdt, cdn) {
		const row = frappe.get_doc(cdt, cdn);
		const expected = classificationDoctypes[row.dimension_type];
		frappe.model.set_value(cdt, cdn, "reference_doctype", expected || "");
		frappe.model.set_value(cdt, cdn, "reference_name", "");
		frm.refresh_field("classifications");
	},
});
