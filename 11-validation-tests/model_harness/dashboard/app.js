'use strict';
const $ = id => document.getElementById(id);
const names = {full_source:'Full source', no_context:'No context', truncated:'Truncated source', openai_blueprint:'OpenAI blueprint', jev_blueprint:'OpenAI + JEV'};
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pct = v => v == null ? '—' : `${(v*100).toFixed(1)}%`;
let runs = [], selected = null, mediaRuns = [], sceneRuns = [];
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
 $('lossless').innerHTML=(r.lossless_comparison?.rows||[]).map(m=>`<tr><td>${names[m.arm]}</td><td>${m.cases}/${m.attempted_cases}</td>${['raw','zip_deflate9','gzip9','xz6'].map(k=>`<td>${m.bytes[k]??'—'}</td>`).join('')}<td>${pct(m.reduction_vs_same_encoding.zip_deflate9)}</td></tr>`).join('');
 $('case-select').innerHTML=r.results.map((c,i)=>`<option value="${i}">${esc(c.case_id)}</option>`).join('');
 $('provenance').textContent=JSON.stringify({created_at:r.created_at,finished_at:r.finished_at,status:r.status,errata:r.errata,lossless_comparison:r.lossless_comparison,harness:r.harness,config:r.config,calls:r.calls},null,2);
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
$('refresh').onclick=()=>{refresh();refreshMedia();refreshScene();};$('filter').oninput=list;$('case-select').onchange=caseDetail;
$('download').onclick=()=>{if(!selected)return;const url=URL.createObjectURL(new Blob([JSON.stringify(selected,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`${selected.run_id}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
refresh();

function showMedia(){
 const r=mediaRuns[Number($('media-select').value)];if(!r)return;
 $('media-result').innerHTML=`<p>${esc(r.scene.title)} · <strong>${r.scene.width}×${r.scene.height} · ${r.scene.fps} fps</strong> · ${r.scene.start_seconds}–${r.scene.start_seconds+r.scene.duration_seconds}s · ${esc(r.status)} · ${esc(new Date(r.created_at).toLocaleString())} · harness v${esc(r.harness.version)} / ${esc(r.harness.source_sha256.slice(0,12))}</p><p class="footnote">${esc(r.scene.track)}. ${esc(r.scene.reference)} ${esc(r.scene.attribution)}</p>${r.rows.some(x=>x.file==='libx264.mp4')?`<video controls preload="metadata" width="640" src="/media-preview/${encodeURIComponent(r.run_id)}"></video>`:''}<div class="table-wrap"><table><thead><tr><th>Method</th><th>Bytes</th><th>Saved vs raw frames</th><th>Pixel exact?</th><th>SSIM</th><th>PSNR dB</th></tr></thead><tbody>${r.rows.map(x=>`<tr><td>${esc(x.method)}</td><td>${x.bytes.toLocaleString()}</td><td>${pct(x.reduction_vs_decoded_raw)}</td><td>${x.lossless_to_decoded_reference?'Yes':'No'}</td><td>${x.quality?.ssim?.toFixed(5)??'—'}</td><td>${esc(x.quality?.psnr??'—')}</td></tr>`).join('')}</tbody></table></div><div class="limitations"><ul>${r.limitations.map(x=>`<li>${esc(x.replace('No model or JEV was run on this scene.', 'No model or JEV was run in this codec experiment.'))}</li>`).join('')}</ul></div><details><summary>Codec commands, source hash and provenance</summary><pre>${esc(JSON.stringify(r,null,2))}</pre></details>`;
}
async function refreshMedia(){
 try{const response=await fetch('/api/media');if(!response.ok)throw new Error('media');mediaRuns=(await response.json()).sort((a,b)=>Date.parse(b.created_at)-Date.parse(a.created_at));$('media-notice').textContent=mediaRuns.length?'Saved offline codec runs; semantic QA is shown separately below.':'No saved media runs yet.';
 $('media-select').innerHTML=mediaRuns.map((r,i)=>`<option value="${i}">${esc(r.run_id)} · ${r.scene.width}×${r.scene.height} · ${esc(r.status)}</option>`).join('');showMedia();
 }catch(e){$('media-notice').textContent='Media reports unavailable; restart the server after a harness update.';}
}
$('media-select').onchange=showMedia;
refreshMedia();

function showScene(){
 const r=sceneRuns[Number($('scene-select').value)];if(!r)return;
 $('scene-result').innerHTML=`<p>${esc(r.scene.title)} · <strong>${r.scene.width}×${r.scene.height} · ${r.scene.fps} fps</strong> · ${esc(r.status)} · ${esc(new Date(r.created_at).toLocaleString())} · harness v${esc(r.harness.version)} / ${esc(r.harness.source_sha256.slice(0,12))}</p><p class="footnote">${esc(r.config.model)} + ${esc(r.config.jev_model)}. Control assessment: ${esc(r.validity?.status??"not predeclared")}. Actual frame inputs at 1 fps; no audio. QA uses agent-authored references. JSON is a description, not a playable reconstruction.</p><div class="table-wrap"><table><thead><tr><th>Method</th><th>Status</th><th>Video bytes</th><th>Raw JSON bytes</th><th>ZIP bytes</th><th>gzip bytes</th><th>QA correct</th><th>Visible facts</th><th>Unknowns</th></tr></thead><tbody>${r.rows.map(x=>`<tr><td>${esc(x.method)}</td><td>${esc(x.status)}</td><td>${x.video_bytes?.toLocaleString()??'—'}</td><td>${x.bytes?.raw??'—'}</td><td>${x.bytes?.zip_deflate9??'—'}</td><td>${x.bytes?.gzip9??'—'}</td><td>${x.correct_count==null?'—':`${x.correct_count}/${x.total}`}</td><td>${x.answerable_correct==null?'—':`${x.answerable_correct}/${x.answerable_total}`}</td><td>${x.unknown_correct==null?'—':`${x.unknown_correct}/${x.unknown_total}`}</td></tr>`).join('')}</tbody></table></div>${r.rows.filter(x=>x.payload).map(x=>`<details><summary>${esc(x.method)} · inspect semantic JSON</summary><pre>${esc(JSON.stringify(x.payload,null,2))}</pre></details>`).join('')}<div class="limitations"><ul>${r.limitations.map(x=>`<li>${esc(x.replace('No model or JEV was run on this scene.', 'No model or JEV was run in this codec experiment.'))}</li>`).join('')}</ul></div><details><summary>Questions, per-question answers, prompts and provenance</summary><pre>${esc(JSON.stringify(r,null,2))}</pre></details>`;
}
async function refreshScene(){
 try{const response=await fetch('/api/scene');if(!response.ok)throw new Error('scene');sceneRuns=(await response.json()).sort((a,b)=>Date.parse(b.created_at)-Date.parse(a.created_at));$('scene-notice').textContent=sceneRuns.length?'Saved live-model experiments; compare size with retained facts.':'No saved semantic scene experiments yet.';
 $('scene-select').innerHTML=sceneRuns.map((r,i)=>`<option value="${i}">${esc(r.run_id)} · ${r.scene.width}×${r.scene.height} · ${esc(r.status)}</option>`).join('');showScene();
 }catch(e){$('scene-notice').textContent='Semantic scene reports unavailable; restart the server after a harness update.';}
}
$('scene-select').onchange=showScene;
refreshScene();
