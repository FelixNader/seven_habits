const alignmentDoctypes = {
	Role: "SH Role",
	Goal: "SH Goal",
	Project: "SH Project",
	Habit: "SH Habit",
};

frappe.ui.form.on("SH Commitment Alignment", {
	dimension_type(frm, cdt, cdn) {
		const row = frappe.get_doc(cdt, cdn);
		const expected = alignmentDoctypes[row.dimension_type];
		if (expected && row.reference_doctype !== expected) {
			frappe.model.set_value(cdt, cdn, "reference_doctype", expected);
			frappe.model.set_value(cdt, cdn, "reference_name", "");
		}
	},
});
