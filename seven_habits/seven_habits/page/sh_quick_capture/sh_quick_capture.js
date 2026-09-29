frappe.pages["sh-quick-capture"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({ parent: wrapper, title: __("Captura rápida"), single_column: true });
	const $form = $('<div class="frappe-card p-4" style="max-width: 720px;"></div>').appendTo(page.body);
	$('<label class="control-label">¿Qué ocurrió?</label>').appendTo($form);
	const $input = $('<input class="form-control" placeholder="Describe el hecho real">').appendTo($form);
	$('<label class="control-label mt-3">Fecha y hora efectiva</label>').appendTo($form);
	const initial_timestamp = frappe.datetime.now_datetime().replace(" ", "T").slice(0, 16);
	const $effectiveAt = $('<input type="datetime-local" class="form-control">').val(initial_timestamp).appendTo($form);
	const save = () => {
		const raw_text = $input.val().trim();
		if (!raw_text) return;
		frappe.call({
			method: "seven_habits.api.capture_activity_fact",
			args: { raw_text, effective_at: $effectiveAt.val().replace("T", " ") },
			freeze: false,
			callback: () => {
				$input.val("").focus();
				$effectiveAt.val(frappe.datetime.now_datetime().replace(" ", "T").slice(0, 16));
				frappe.show_alert({ message: __("Hecho registrado"), indicator: "green" });
			},
		});
	};
	$('<button class="btn btn-primary mt-3">Guardar</button>').appendTo($form).on("click", save);
	$input.on("keydown", (event) => { if ((event.ctrlKey || event.metaKey) && event.key === "Enter") save(); });
	$input.focus();
};
