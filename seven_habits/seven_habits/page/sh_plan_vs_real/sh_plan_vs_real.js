frappe.pages["sh-plan-vs-real"].on_page_load = (wrapper) => {
 const page=frappe.ui.make_app_page({parent:wrapper,title:__("Plan vs Real"),single_column:true});
 const controls=$("<div class='mb-3'></div>").appendTo(page.body);
 const date=$("<input type='date' class='form-control' style='max-width:220px'>").val(frappe.datetime.get_today()).appendTo(controls);
 const content=$("<div></div>").appendTo(page.body);
 const load=()=>frappe.call({method:"seven_habits.api.get_plan_vs_real",args:{day:date.val()},callback:({message=[]})=>{
  content.empty(); const planned=[],facts=[];
  message.forEach(g=>{(g.planned_items||[]).forEach(i=>planned.push(i));(g.facts||[]).forEach(f=>facts.push({...f,group:g.commitment_text,classified:g.commitment_text!=="Hechos pendientes de interpretar"}));});
  planned.sort((a,b)=>String(a.start_datetime).localeCompare(String(b.start_datetime))); facts.sort((a,b)=>String(a.effective_at).localeCompare(String(b.effective_at)));
  const plan=message.reduce((n,x)=>n+(x.planned_minutes||0),0), pending=facts.filter(x=>!x.classified).length;
  content.append($('<div class="alert alert-info"></div>').text(`Resumen del día · Plan: ${plan} min · Real registrado: ${facts.length} hechos · Clasificados: ${facts.length-pending} · Pendientes: ${pending}`));
  const cols=$("<div class='row'></div>").appendTo(content), pc=$("<div class='col-md-6 mb-3'><h4>Así lo planeaste</h4></div>").appendTo(cols), rc=$("<div class='col-md-6 mb-3'><h4>Así transcurrió</h4></div>").appendTo(cols);
  if(!planned.length) pc.append($('<div class="text-muted p-3">No hay Tasks o Events planificados.</div>')); planned.forEach(i=>pc.append($('<div class="frappe-card p-3 mb-2 border-left-primary"></div>').append($('<div class="font-weight-bold"></div>').text(i.title)).append($('<div class="small text-muted"></div>').text(`${i.item_type} · ${frappe.datetime.str_to_user(i.start_datetime)} → ${frappe.datetime.str_to_user(i.end_datetime)}`))));
  if(!facts.length) rc.append($('<div class="text-muted p-3">No hay hechos registrados.</div>')); facts.forEach(f=>{const c=$('<div class="frappe-card p-3 mb-2"></div>').append($('<div class="font-weight-bold"></div>').text(f.raw_text)).append($('<div class="small text-muted"></div>').text(`${frappe.datetime.str_to_user(f.effective_at)} · ${f.classified?f.group:"Pendiente de interpretar"}`)); if(!f.classified)c.append($('<a class="btn btn-xs btn-secondary mt-2">Interpretar</a>').attr('href',`/app/sh-interpretation/new-sh-interpretation?subject_doctype=SH%20Activity%20Fact&subject_name=${f.name}`)); rc.append(c);});
  content.append($('<hr><h4>Comparación por resultado</h4>')); message.forEach(g=>content.append($('<div class="frappe-card p-3 mb-2"></div>').append($('<div class="font-weight-bold"></div>').text(g.commitment_text||"Sin compromiso")).append($('<div></div>').text(`Plan: ${g.planned_minutes||0} min · Evidencia: ${(g.facts||[]).length} hechos · Real: ${g.actual_minutes==null?"duración no disponible":g.actual_minutes+" min"}`))));
 }}); date.on("change",load); load();
};
