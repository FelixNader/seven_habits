const alignmentDoctypes = {
	Role: "SH Role",
	Goal: "SH Goal",
	Project: "SH Project",
	Habit: "SH Habit",
};

frappe.ui.form.on("SH Commitment", {
	setup(frm) {
		frm.set_query("reference_doctype", "alignments", (_doc, _cdt, cdn) => {
			const row = frappe.get_doc(_cdt, cdn);
			const allowed = alignmentDoctypes[row.dimension_type];
			return allowed ? { filters: { name: allowed } } : { filters: { name: ["in", Object.values(alignmentDoctypes)] } };
		});
	},
});

frappe.ui.form.on("SH Commitment Alignment", {
	 dimension_type(frm, cdt, cdn) {
		const row = frappe.get_doc(cdt, cdn);
		const expected = alignmentDoctypes[row.dimension_type];
		if (!expected) return;
		// The doctype is derived from Dimension Type; the hidden technical
		// field drives the Dynamic Link shown to the user.
		frappe.model.set_value(cdt, cdn, "reference_doctype", expected);
		frappe.model.set_value(cdt, cdn, "reference_name", "");
		frm.refresh_field("alignments");
	},
});
