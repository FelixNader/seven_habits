frappe.pages["sh-review"].on_page_load = (wrapper) => {
	const page = frappe.ui.make_app_page({ parent: wrapper, title: __("Review"), single_column: true });
	const controls = $("<div class='row g-2'></div>").appendTo(page.body);
	const type = $("<select class='form-control col' style='max-width:180px'><option>Weekly</option><option>Daily</option><option>Monthly</option></select>").appendTo(controls);
	const start = $("<input type='date' class='form-control col' style='max-width:180px'>").val(frappe.datetime.get_today()).appendTo(controls);
	const end = $("<input type='date' class='form-control col' style='max-width:180px'>").val(frappe.datetime.get_today()).appendTo(controls);
	const open = $("<button class='btn btn-primary ml-2'>Abrir revisión</button>").appendTo(controls);
	const message = $("<div class='mt-3'></div>").appendTo(page.body);
	open.on("click", () => {
		frappe.call({method: "seven_habits.api.start_review", args: {review_type: type.val(), period_start: start.val(), period_end: end.val()},
			callback: (r) => { if (r.message) { message.html(`<div class='alert alert-success'>Review ${r.message} creada. <a href='/app/sh-review/${r.message}'>Abrir detalle</a></div>`); } }
		});
	});
};
