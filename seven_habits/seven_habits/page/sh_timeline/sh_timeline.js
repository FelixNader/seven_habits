frappe.pages["sh-timeline"].on_page_load = (wrapper) => {
	const page = frappe.ui.make_app_page({parent: wrapper, title: __("Bitácora"), single_column: true});
	const date = $('<input type="date" class="form-control" style="max-width:220px">').val(frappe.datetime.get_today()).appendTo(page.body);
	const list = $('<div class="mt-3"></div>').appendTo(page.body);
	const load = () => frappe.call({method:"seven_habits.api.get_timeline", args:{day:date.val()}, callback:({message}) => {list.empty(); message.forEach(x => list.append($('<div class="border-bottom py-2"></div>').text(`${x.effective_at} — ${x.raw_text}`)));}});
	date.on("change", load); load();
};
