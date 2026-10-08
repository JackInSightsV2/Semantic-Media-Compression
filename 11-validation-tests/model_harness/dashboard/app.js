'use strict';
const $ = id => document.getElementById(id);
const names = {full_source:'Full source', no_context:'No context', truncated:'Truncated source', openai_blueprint:'OpenAI blueprint', jev_blueprint:'OpenAI + JEV'};
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pct = v => v == null ? '—' : `${(v*100).toFixed(1)}%`;
let runs = [], selected = null;
function list() {
 const filter = $('filter').value.toLowerCase();
 $('runs').replaceChildren();
 runs.filter(r=>JSON.stringify([r.run_id,r.created_at,r.dataset_id,r.config,r.harness.version,r.harness.source_sha256]).toLowerCase().includes(filter)).forEach(r=>{
  const b=document.createElement('button'); b.className='run'+(selected?.run_id===r.run_id?' active':'');
  b.innerHTML=`<strong>${esc(r.dataset_id)}</strong><small>${esc(new Date(r.created_at).toLocaleString())}</small><small>${esc(r.config.openai_model)}</small><small>v${esc(r.harness.version)} · ${esc(r.harness.source_sha256.slice(0,10))}</small><span class="badge ${esc(r.status)}">${esc(r.status)} · ${r.results.length} cases</span>`;
  b.onclick=()=>show(r); $('runs').append(b);
 });
}
function show(r) {
 selected=r; list(); $('empty').hidden=true; $('detail').hidden=false;
 $('run-title').textContent=r.dataset_id;
 const used=(r.calls||[]).filter(c=>c.status==='ok').map(c=>c.resolved_model||c.requested_model);
 $('meta').innerHTML=[r.run_id, `Harness v${r.harness.version}`,`Build ${r.harness.source_sha256.slice(0,12)}`,`Dataset ${r.dataset_sha256.slice(0,12)}`, ...new Set(used)].map(x=>`<span>${esc(x)}</span>`).join('');
 $('bars').innerHTML=Object.entries(names).map(([key,name])=>{const m=r.summary?.[key];return `<div class="bar-row ${key==='jev_blueprint'?'hybrid':key.includes('blueprint')?'':'control'}"><span>${name}</span><progress class="bar-track" max="1" value="${m?.accuracy_all_questions??0}" aria-label="${name} accuracy"></progress><b>${pct(m?.accuracy_all_questions)}</b></div>`}).join('');
 $('comparison').innerHTML=Object.entries(names).map(([key,name])=>{const m=r.summary?.[key];return `<tr><td>${name}</td><td>${pct(m?.accuracy_all_questions)}</td><td>${pct(m?.retention_on_full_source_correct)}</td><td>${pct(m?.byte_reduction)}</td><td>${m?.valid_cases??0}/${m?.attempted_cases??r.results.length}</td><td>${m?.within_budget_cases==null?'—':`${m.within_budget_cases}/${m.valid_cases}`}</td></tr>`}).join('');
 $('case-select').innerHTML=r.results.map((c,i)=>`<option value="${i}">${esc(c.case_id)}</option>`).join('');
 $('provenance').textContent=JSON.stringify({created_at:r.created_at,finished_at:r.finished_at,status:r.status,errata:r.errata,harness:r.harness,config:r.config,calls:r.calls},null,2);
 $('limitations').innerHTML='<strong>Interpretation limits</strong><ul>'+r.limitations.map(t=>`<li>${esc(t)}</li>`).join('')+'</ul>';
 caseDetail();
}
function caseDetail(){
 const c=selected?.results[Number($('case-select').value)]; if(!c){$('case-detail').textContent='Run in progress; no cases yet.';return;}
 const source=selected.dataset.cases.find(x=>x.id===c.case_id)?.source;
 $('case-detail').innerHTML=`<details><summary>Original source · ${new TextEncoder().encode(source||'').length} bytes</summary><pre>${esc(source)}</pre></details><div class="payloads">${['openai_blueprint','jev_blueprint'].map(key=>{const a=c.arms[key];return `<div class="payload"><h3>${names[key]}</h3><small>${a?.size?.blueprint_bytes??'—'} bytes / ${c.byte_budget} budget · ${esc(a?.status??'pending')}</small><pre>${esc(a?.context??a?.error_type??'Waiting for output')}</pre></div>`}).join('')}</div><div class="table-wrap"><table><thead><tr><th>Question / reference</th><th>Full</th><th>OpenAI</th><th>+ JEV</th><th>Truncated</th><th>No source</th></tr></thead><tbody>${c.questions.map(q=>`<tr><td title="${esc(q.prompt)}">${esc(q.prompt)}<br><small>Reference: ${esc(q.options[q.expected])}</small></td>${['full_source','openai_blueprint','jev_blueprint','truncated','no_context'].map(key=>{const a=c.arms[key],answer=a?.answers?.[q.id];return `<td class="${a?.correct?.[q.id]?'correct':'wrong'}" title="${esc(q.options[answer]??a?.error_type??'Not evaluated')}">${answer?`${a.correct[q.id]?'✓':'×'} ${esc(answer)}`:'—'}</td>`}).join('')}</tr>`).join('')}</tbody></table></div><details><summary>Extracted facts and JEV decisions</summary><pre>${esc(JSON.stringify(c.jev_selection??{},null,2))}</pre></details>`;
}
async function refresh(){
 try{const response=await fetch('/api/runs');if(!response.ok)throw new Error(`HTTP ${response.status}`);runs=await response.json();
 const complete=runs.filter(r=>r.status==='completed').length;
 const calls=runs.reduce((n,r)=>n+(r.calls?.length??0),0),builds=new Set(runs.map(r=>r.harness.source_sha256)).size;
 $('stats').innerHTML=[[runs.length,'Recorded runs'],[complete,'Complete experiments'],[builds,'Exact harness builds'],[calls,'Recorded API calls']].map(([n,s])=>`<div class="stat"><b>${n}</b><span>${s}</span></div>`).join('');
 $('notice').textContent='';const target=runs.find(r=>r.run_id===selected?.run_id)||runs[0];if(target)show(target);else{list();$('detail').hidden=true;$('empty').hidden=false;}
 }catch(error){$('notice').textContent='Unable to load saved runs. Check the local dashboard server.';}
}
$('refresh').onclick=refresh;$('filter').oninput=list;$('case-select').onchange=caseDetail;
$('download').onclick=()=>{if(!selected)return;const url=URL.createObjectURL(new Blob([JSON.stringify(selected,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`${selected.run_id}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
refresh();
