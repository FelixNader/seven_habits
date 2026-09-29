frappe.pages["sh-agenda"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({ parent: wrapper, title: __("Agenda"), single_column: true });
	const $body = $('<div class="frappe-card p-4" style="max-width: 900px;"></div>').appendTo(page.body);
	const $date = $('<input type="date" class="form-control" style="max-width: 220px; display: inline-block;">')
		.val(frappe.datetime.get_today()).appendTo($body);
	const $list = $('<div class="mt-4"></div>').appendTo($body);
	const render = () => frappe.call({
		method: "seven_habits.api.get_agenda",
		args: { day: $date.val() },
		callback: ({ message: items }) => {
			$list.empty();
			if (!items.length) { $list.append($("<p class='text-muted'>No hay tiempo planificado para este día.</p>")); return; }
			items.forEach((item) => {
				const time = `${frappe.datetime.str_to_user(item.start_datetime, false, false)} – ${frappe.datetime.str_to_user(item.end_datetime, false, false)}`;
				const $row = $('<div class="border-bottom py-3"></div>').appendTo($list);
				$("<span class='badge me-2'></span>").text(item.type).appendTo($row);
				$("<strong></strong>").text(item.title).appendTo($row);
				$("<div class='text-muted small mt-1'></div>").text(time).appendTo($row);
			});
		},
	});
	$('<button class="btn btn-primary ms-2">Actualizar</button>').appendTo($body).on("click", render);
	$date.on("change", render);
	render();
};
