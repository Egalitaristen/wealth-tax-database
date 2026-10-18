'use strict';
const REPO = 'Egalitaristen/wealth-tax-map';
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const enc = encodeURIComponent;
const safeUrl = u => /^https?:\/\//.test(u) ? u : '';
const issueUrl = (title, fields = {}) =>
  `https://github.com/${REPO}/issues/new?template=data-report.yml&title=${enc(title)}` +
  Object.entries(fields).map(([k, v]) => `&${k}=${enc(v)}`).join('');
$('#report-top').href = issueUrl('Report: ');
$('#repo-link').href = `https://github.com/${REPO}`;

const TYPE = {politician:'Politician',party:'Party',government_body:'Council or body',academic:'Academic',economist:'Economist',think_tank:'Think tank',ngo_campaign:'Campaign group',union:'Union',union_official:'Union official',journalist:'Commentator',media_outlet:'Media outlet',legal_tax_professional:'Legal or tax',wealthy_individual:'Wealthy individual',business_leader:'Business leader',faith:'Faith',cultural_figure:'Cultural figure',campaigner:'Campaigner or NGO leader',international_body:'International body',funder:'Funder'};
const DES = {annual_net_wealth:'Annual net wealth tax',one_off_levy:'One-off levy',billionaire_minimum:'Billionaire minimum',partial_wealth:'Partial (e.g. property)',wealth_tax_unspecified:'Unspecified wealth tax',unrealised_gains:'Unrealised gains',exit_tax:'Exit tax'};
const EVT = {open_letter:'Open letter',motion_signature:'Signed motion',motion:'Motion',vote:'Vote',campaign:'Campaign',op_ed:'Op-ed',editorial:'Editorial',speech:'Speech',statement:'Statement',policy_adoption:'Policy adopted',publication:'Publication',report:'Report',funding:'Funding',coalition_membership:'Coalition member',interview:'Interview',manifesto:'Manifesto',bill_sponsorship:'Bill sponsor',testimony:'Testimony',social_post:'Social post',other:'Other'};
const STATE = {support:'Local supporter found',clear:'Meetings read, nothing found',open:'Not fully read yet'};

// ---------- pan and zoom for any SVG map ----------
function makeMap(svg, box, tip, vb, nameOf, onPick) {
  const [vx, vy, vw, vh] = vb;
  let x = vx, y = vy, w = vw, h = vh, drag = null, moved = false, selKey = null;
  const set = () => svg.setAttribute('viewBox', `${x} ${y} ${w} ${h}`);
  function fit() {
    const r = svg.getBoundingClientRect(), asp = (r.width / r.height) || 1;
    let nw = vw, nh = vh;
    if (nw / nh > asp) nh = nw / asp; else nw = nh * asp;
    w = nw; h = nh; x = vx - (nw - vw) / 2; y = vy - (nh - vh) / 2; set();
  }
  function zoom(f) {
    const nw = Math.min(vw * 1.6, Math.max(vw / 60, w * f)), nh = h * (nw / w);
    x += (w - nw) / 2; y += (h - nh) / 2; w = nw; h = nh; set();
  }
  svg.addEventListener('pointerdown', e => { drag = {x: e.clientX, y: e.clientY}; moved = false; svg.setPointerCapture(e.pointerId); });
  svg.addEventListener('pointermove', e => {
    if (drag) {
      const r = svg.getBoundingClientRect(), dx = e.clientX - drag.x, dy = e.clientY - drag.y;
      if (Math.abs(dx) + Math.abs(dy) > 3) moved = true;
      if (moved) { x -= dx * w / r.width; y -= dy * h / r.height; drag = {x: e.clientX, y: e.clientY}; set(); }
    }
    const t = e.target.closest && e.target.closest('path');
    if (t && !drag) {
      const b = box.getBoundingClientRect();
      tip.hidden = false; tip.textContent = nameOf(t.dataset.k);
      tip.style.left = (e.clientX - b.left) + 'px'; tip.style.top = (e.clientY - b.top) + 'px';
    } else tip.hidden = true;
  });
  svg.addEventListener('pointerup', e => {
    const was = moved; drag = null;
    if (!was) { const t = document.elementFromPoint(e.clientX, e.clientY); if (t && t.dataset && t.dataset.k !== undefined) onPick(t.dataset.k); }
  });
  svg.addEventListener('pointerleave', () => { tip.hidden = true; });
  new ResizeObserver(() => { if (selKey === null && !drag) fit(); }).observe(svg);
  fit();
  return {
    fit, zoom,
    select(k) {
      svg.querySelectorAll('path.sel').forEach(p => p.classList.remove('sel'));
      selKey = k;
      const p = svg.querySelector(`path[data-k="${CSS.escape(k)}"]`);
      if (p) { p.classList.add('sel'); p.parentNode.appendChild(p); }
    }
  };
}

// ---------- tabs and routing ----------
let WORLD = null, CUR = null; // CUR = {slug, data, sub}
const cache = {};
const TABS = ['world', 'country', 'contribute'];
function showTab(t) {
  document.querySelectorAll('#tabs button').forEach(b => b.setAttribute('aria-selected', String(b.dataset.t === t)));
  TABS.forEach(s => $('#' + s).hidden = s !== t);
}
function route(replace) {
  const h = (location.hash || '#world').slice(1), [a, b] = h.split('.');
  if (a === 'contribute') showTab('contribute');
  else if (WORLD && WORLD.countries.some(c => c.slug === a)) openCountry(a, b, replace);
  else showTab('world');
}
function go(h) { if (location.hash === '#' + h) route(); else location.hash = h; }
window.addEventListener('hashchange', () => route());
$('#tabs').addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b) return;
  if (b.dataset.t === 'country') go(CUR ? CUR.slug + (CUR.sub ? '.' + CUR.sub : '') : WORLD.countries[0].slug);
  else go(b.dataset.t);
});

// ---------- world ----------
async function boot() {
  try { WORLD = await (await fetch('data/world.json')).json(); }
  catch (e) { $('#wside').innerHTML = '<p class="empty">Could not load the data. Open this page through a web server, not from a file.</p>'; return; }
  const cs = WORLD.countries;
  $('#stats').innerHTML = [[cs.length, 'countries'], [cs.reduce((n, c) => n + c.supporters, 0), 'supporters'], [cs.reduce((n, c) => n + c.evidence, 0), 'sourced rows']]
    .map(x => `<div class="stat"><b>${x[0]}</b><span>${x[1]}</span></div>`).join('');
  $('#csel').innerHTML = cs.map(c => `<option value="${esc(c.slug)}">${esc(c.name)}</option>`).join('');
  $('#csel').addEventListener('change', () => go($('#csel').value));
  drawWorld();
  route(true);
}
function drawWorld() {
  const byNum = {}; WORLD.countries.forEach(c => { if (c.numeric) byNum[c.numeric] = c; });
  const mx = Math.max(1, ...WORLD.countries.map(c => c.supporters));
  const svg = $('#wsvg'); svg.classList.add('world');
  const paths = WORLD.paths;
  svg.innerHTML = Object.entries(paths).map(([id, p]) => {
    const c = byNum[id];
    const op = c ? (.35 + .65 * Math.log(c.supporters + 1) / Math.log(mx + 1)).toFixed(2) : 1;
    return `<path data-k="${id}" class="${c ? 'has' : 'none'}" style="${c ? `fill-opacity:${op}` : ''}" d="${p.path}"></path>`;
  }).join('');
  let xs = [], ys = [];
  Object.values(paths).forEach(p => { (p.path.match(/-?\d+\.?\d*/g) || []).forEach((n, i) => (i % 2 ? ys : xs).push(+n)); });
  const vb = [Math.min(...xs), Math.min(...ys), Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys)];
  const m = makeMap(svg, $('#wmapbox'), $('#wtip'), vb, k => (byNum[k] ? byNum[k].name : (paths[k] || {}).name) || '', k => {
    m.select(k);
    const c = byNum[k];
    if (c) { worldSide(c); } else noData((paths[k] || {}).name);
  });
  $('#wmapbox').insertAdjacentHTML('beforeend', '<div class="zoom"><button id="wzi" aria-label="Zoom in">+</button><button id="wzo" aria-label="Zoom out">&minus;</button><button id="wzr" aria-label="Reset view" style="font-size:13px">&#8634;</button></div>');
  $('#wzi').onclick = () => m.zoom(.6); $('#wzo').onclick = () => m.zoom(1 / .6); $('#wzr').onclick = m.fit;
  worldHome();
}
function worldHome() {
  $('#wside').innerHTML = `<h2>Countries so far</h2><p class="note">Click a country on the map, or pick one here.</p>` +
    WORLD.countries.map(c => `<div class="ev" data-open="${esc(c.slug)}" style="cursor:pointer"><b>${esc(c.name)}</b>
      <div class="note">${c.supporters} supporters · ${c.evidence} sourced rows · ${esc(c.status)}</div></div>`).join('') +
    `<p style="margin-top:14px"><a href="#contribute">Add your country</a></p>`;
}
function worldSide(c) {
  $('#wside').innerHTML = `<h2>${esc(c.name)}</h2><p><span class="pill">${esc(c.status)}</span> <span class="pill">${c.iso2}</span></p>
   <p style="font-size:14px">${c.supporters} supporters (${c.A} explicit, ${c.B} named, ${c.C} implied) from ${c.evidence} sourced rows. ${c.verified} of ${c.evidence} rows checked by a person.</p>
   ${c.units ? `<p class="note">${c.units_done} of ${c.units} local areas read.</p>` : ''}
   ${c.notes ? `<p class="note">${esc(c.notes)}</p>` : ''}
   <p><a href="#${esc(c.slug)}"><b>Open the ${esc(c.name)} database</b></a></p>
   <a class="report" href="${esc(issueUrl('[' + c.iso2 + '] Report: country data', {country: c.slug}))}" target="_blank" rel="noopener">Report a problem with this country</a>`;
}
function noData(name) {
  $('#wside').innerHTML = `<h2>${esc(name || 'Unknown')}</h2><p class="note">No database for this country yet.</p><p><a href="#contribute">Find out how to start one</a></p>`;
}
$('#wside').addEventListener('click', e => { const r = e.target.closest('[data-open]'); if (r) go(r.dataset.open); });

// ---------- country ----------
async function openCountry(slug, sub, replace) {
  showTab('country');
  $('#csel').value = slug;
  if (!cache[slug]) { $('#cbody').innerHTML = '<p class="empty">Loading…</p>'; cache[slug] = await (await fetch(`data/${slug}.json`)).json(); }
  const data = cache[slug];
  const subs = data.C.length ? ['map', 'people', 'timeline', 'method'] : ['people', 'timeline', 'method'];
  if (!subs.includes(sub)) sub = subs[0];
  CUR = {slug, data, sub};
  document.querySelectorAll('#subtabs button').forEach(b => { b.hidden = !subs.includes(b.dataset.s); b.setAttribute('aria-selected', String(b.dataset.s === sub)); });
  renderCountry();
}
$('#subtabs').addEventListener('click', e => { const b = e.target.closest('button'); if (b && CUR) go(CUR.slug + '.' + b.dataset.s); });

function evCard(e, cc) {
  const u = safeUrl(e[7]);
  return `<div class="ev"><div><span class="g g${e[2]}">${e[2]}</span> <b>${esc(EVT[e[3]] || e[3])}</b> <span class="m">${esc(e[1])}${e[10] === 'y' ? '' : ' · not yet verified'}</span></div>
  ${e[5] ? `<div style="font-size:13px">${esc(e[5])}</div>` : ''}${e[6] ? `<q>&ldquo;${esc(e[6])}&rdquo;</q>` : ''}
  <div class="m">${u ? `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(e[8] || e[9] || 'Source')}</a>` : esc(e[8])}${e[9] ? ' · ' + esc(e[9]) : ''}
  · <a href="${esc(issueUrl('[' + cc + '] Report: ' + e[11], {country: CUR.slug, entry: e[11]}))}" target="_blank" rel="noopener">Report</a></div></div>`;
}

function renderCountry() {
  const {data, sub, slug} = CUR, cc = data.meta.iso2;
  const P = data.P, E = data.E, pid = {}; P.forEach((p, i) => pid[p[0]] = i);
  const evBy = {}; E.forEach(e => { (evBy[e[0]] ??= []).push(e); });
  const card = i => {
    const p = P[i];
    const es = (evBy[p[0]] || []).slice().sort((a, b) => 'ABC'.indexOf(a[2]) - 'ABC'.indexOf(b[2]) || b[1].localeCompare(a[1]));
    return `<h2>${esc(p[1])}</h2><div style="margin-bottom:8px"><span class="g g${p[8]}">${p[8]}</span> <span class="pill">${esc(TYPE[p[3]] || p[3])}</span> <span class="pill">${esc(p[6])}</span>${p[7] ? ` <span class="pill">${esc(p[7])}</span>` : ''}</div>
      <div style="font-size:14px">${esc(p[4])}</div>${p[5] && p[5] !== p[4] ? `<div class="note">${esc(p[5])}</div>` : ''}
      ${p[13] ? `<p class="note">${esc(p[13])}</p>` : ''}<h3 style="margin-top:14px">Evidence (${es.length})</h3>${es.map(e => evCard(e, cc)).join('')}
      <a class="report" href="${esc(issueUrl('[' + cc + '] Report: ' + p[1], {country: slug, entry: p[0]}))}" target="_blank" rel="noopener">Report a problem with this entry</a>`;
  };
  const body = $('#cbody');

  if (sub === 'map') {
    body.innerHTML = `<div class="grid"><div class="mapbox" id="mapbox"><svg class="map local" id="svg" role="img" aria-label="Local map coloured by findings"></svg>
      <div class="zoom"><button id="zi" aria-label="Zoom in">+</button><button id="zo" aria-label="Zoom out">&minus;</button><button id="zr" aria-label="Reset view" style="font-size:13px">&#8634;</button></div>
      <div class="legend"><span><i style="background:var(--support)"></i>Local supporter found</span><span><i style="background:var(--clear)"></i>Meetings read, nothing found</span><span><i style="background:var(--open)"></i>Not fully read yet</span></div>
      <div class="tip" id="tip" hidden></div></div><aside class="panel" id="mapside"></aside></div>
      <p class="note" style="margin-top:10px">Unshaded areas are not evidence of opposition: most are only partly read, and many council sites block automated reading.</p>`;
    const C = data.C, svg = $('#svg');
    svg.innerHTML = C.map((c, i) => `<path data-k="${i}" class="${c[2]}" d="${c[7]}"></path>`).join('');
    const m = makeMap(svg, $('#mapbox'), $('#tip'), data.vb, k => C[k][0], k => { m.select(k); side(+k); });
    $('#zi').onclick = () => m.zoom(.6); $('#zo').onclick = () => m.zoom(1 / .6); $('#zr').onclick = m.fit;
    const home = () => { $('#mapside').innerHTML = `<h2>Click an area</h2><p class="note">Drag to pan, use the buttons to zoom.</p>` +
      (data.O.length ? '<h3 style="margin-top:14px">Not on the map</h3>' + data.O.map(o => `<div class="ev"><b>${esc(o[0])}</b><div class="note">${o[4].length} supporters recorded</div></div>`).join('') : ''); };
    const side = i => {
      const c = C[i];
      $('#mapside').innerHTML = `<h2>${esc(c[0])}</h2><p><span class="pill">${esc(STATE[c[2]])}</span> ${c[1] ? `<span class="pill">${esc(c[1])}</span>` : ''}</p>
        ${c[6].length ? `<h3>Supporters here (${c[6].length})</h3>` + c[6].map(id => { const p = P[pid[id]]; return p ? `<div class="ev" data-p="${pid[id]}" style="cursor:pointer"><span class="g g${p[8]}">${p[8]}</span> <b>${esc(p[1])}</b><div class="note">${esc(p[4])}</div></div>` : ''; }).join('') : '<p class="note">No supporter recorded for this area yet.</p>'}
        ${c[5] ? `<h3 style="margin-top:14px">Sweep notes</h3><p class="note">${esc(c[5])}</p>` : ''}
        <a class="report" href="${esc(issueUrl('[' + cc + '] Report: ' + c[0], {country: slug}))}" target="_blank" rel="noopener">Report a problem with this area</a>`;
    };
    $('#mapside').addEventListener('click', e => { const r = e.target.closest('[data-p]'); if (r) { PEOPLE_SEL = +r.dataset.p; go(slug + '.people'); } });
    home();
  }

  if (sub === 'people') {
    body.innerHTML = `<div class="ctl"><input type="search" id="q" placeholder="Search names, roles, parties" aria-label="Search"><select id="ft" aria-label="Type"></select>
      <select id="fl" aria-label="Level"><option value="">Any level</option><option value="national">National</option><option value="regional">Regional</option><option value="local">Local</option><option value="supranational">Supranational</option></select>
      <select id="fg" aria-label="Grade"><option value="">Any grade</option><option value="A">A explicit</option><option value="B">B named</option><option value="C">C implied</option></select>
      <select id="fk" aria-label="Kind"><option value="">People and organisations</option><option value="person">People</option><option value="organisation">Organisations</option></select>
      <select id="fv" aria-label="Verification"><option value="">Verified or not</option><option value="y">Has a verified row</option></select></div>
      <div class="grid"><div><div class="tw" style="max-height:74vh;overflow:auto"><table id="tbl"><thead><tr><th data-k="1">Name</th><th data-k="3">Type</th><th data-k="8">Grade</th><th data-k="9">Rows</th><th data-k="11">Latest</th></tr></thead><tbody></tbody></table></div>
      <p class="note" id="count" style="margin-top:8px"></p></div><aside class="panel" id="pside"><p class="empty">Select a row to see the evidence behind it.</p></aside></div>`;
    const ft = $('#ft');
    ft.innerHTML = '<option value="">Any type</option>' + [...new Set(P.map(p => p[3]))].sort((a, b) => (TYPE[a] || a).localeCompare(TYPE[b] || b)).map(t => `<option value="${t}">${esc(TYPE[t] || t)}</option>`).join('');
    let sortK = 1, sortD = 1, cur = PEOPLE_SEL;
    const rows = () => {
      const q = $('#q').value.toLowerCase(), t = ft.value, l = $('#fl').value, g = $('#fg').value, k = $('#fk').value, v = $('#fv').value;
      const r = P.map((p, i) => i).filter(i => {
        const p = P[i];
        return (!t || p[3] === t) && (!l || p[6] === l) && (!g || p[8] === g) && (!k || p[2] === k) &&
          (!v || (evBy[p[0]] || []).some(e => e[10] === 'y')) && (!q || (p[1] + ' ' + p[4] + ' ' + p[5] + ' ' + p[7]).toLowerCase().includes(q));
      });
      r.sort((a, b) => { const x = P[a][sortK], y = P[b][sortK]; return (typeof x === 'number' ? x - y : String(x).localeCompare(String(y))) * sortD; });
      return r;
    };
    const draw = () => {
      const r = rows();
      $('#tbl tbody').innerHTML = r.slice(0, 400).map(i => { const p = P[i];
        return `<tr tabindex="0" data-p="${i}" aria-selected="${i === cur}"><td><b>${esc(p[1])}</b><div class="role">${esc(p[4].slice(0, 90))}</div></td><td>${esc(TYPE[p[3]] || p[3])}</td><td><span class="g g${p[8]}">${p[8]}</span></td><td class="n">${p[9]}</td><td class="n">${esc(p[11].slice(0, 7))}</td></tr>`; }).join('');
      $('#count').textContent = `${r.length} of ${P.length} shown` + (r.length > 400 ? ' (first 400; narrow the filters to see the rest)' : '');
    };
    const pick = i => { cur = i; $('#pside').innerHTML = card(i); draw(); };
    ['#q', '#ft', '#fl', '#fg', '#fk', '#fv'].forEach(s => $(s).addEventListener('input', draw));
    $('#tbl thead').addEventListener('click', e => { const th = e.target.closest('th'); if (!th) return; const k = +th.dataset.k; if (sortK === k) sortD *= -1; else { sortK = k; sortD = (k === 11 || k === 9) ? -1 : 1; } draw(); });
    $('#tbl tbody').addEventListener('click', e => { const tr = e.target.closest('tr'); if (tr) pick(+tr.dataset.p); });
    $('#tbl tbody').addEventListener('keydown', e => { if (e.key === 'Enter') { const tr = e.target.closest('tr'); if (tr) pick(+tr.dataset.p); } });
    draw();
    if (cur != null) { $('#pside').innerHTML = card(cur); const row = $(`#tbl tr[data-p="${cur}"]`); if (row) row.scrollIntoView({block: 'nearest'}); }
    PEOPLE_SEL = null;
  }

  if (sub === 'timeline') {
    body.innerHTML = `<div class="panel"><h2>Evidence by year</h2><p class="note">Dated evidence rows by grade. Years with few rows reflect where the harvest started, so earlier support is under-counted.</p><div id="tl"></div></div>
      <div class="charts"><div class="panel"><h3>Supporters by type</h3><div class="bars" id="btype"></div></div><div class="panel"><h3>Designs backed (supporters)</h3><div class="bars" id="bdes"></div></div><div class="panel"><h3>Evidence by kind</h3><div class="bars" id="bev"></div></div></div>`;
    const yrs = {}; let y0 = 9999, y1 = 0;
    E.forEach(e => { const y = +String(e[1]).slice(0, 4); if (y >= 2000 && y <= 2100) { (yrs[y] ??= {A: 0, B: 0, C: 0})[e[2]]++; y0 = Math.min(y0, y); y1 = Math.max(y1, y); } });
    y0 = Math.min(y0, 2010); y1 = Math.max(y1, new Date().getFullYear());
    const ys = []; for (let y = y0; y <= y1; y++) ys.push(y);
    const tot = y => yrs[y] ? yrs[y].A + yrs[y].B + yrs[y].C : 0, max = Math.max(1, ...ys.map(tot));
    const W = 860, H = 300, L = 34, B = 28, T = 24, bw = (W - L) / ys.length, sc = v => (H - B - T) * v / max;
    let s = `<svg class="chart" viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="Evidence rows per year by grade">`;
    [0, .5, 1].forEach(f => { const v = Math.round(max * f), yy = H - B - sc(v); s += `<line x1="${L}" x2="${W}" y1="${yy}" y2="${yy}" stroke="var(--line)"/><text x="${L - 6}" y="${yy + 4}" text-anchor="end">${v}</text>`; });
    ys.forEach((y, i) => { const d = yrs[y] || {A: 0, B: 0, C: 0}; let acc = 0; const x = L + i * bw + 4, w = bw - 8;
      ['A', 'B', 'C'].forEach(g => { const h = sc(d[g]); if (h > 0) s += `<rect x="${x}" y="${H - B - acc - h}" width="${w}" height="${h}" fill="var(--${g.toLowerCase()})"><title>${y} grade ${g}: ${d[g]}</title></rect>`; acc += h; });
      s += `<text x="${x + w / 2}" y="${H - 10}" text-anchor="middle">${String(y).slice(2)}</text>`; });
    s += `</svg><p class="note"><span class="dot" style="background:var(--a)"></span>A explicit <span class="dot" style="background:var(--b);margin-left:12px"></span>B named <span class="dot" style="background:var(--c);margin-left:12px"></span>C implied</p>`;
    $('#tl').innerHTML = s;
    const cnt = (arr, f) => { const o = {}; arr.forEach(x => { const k = f(x); if (k) o[k] = (o[k] || 0) + 1; }); return Object.entries(o).sort((a, b) => b[1] - a[1]); };
    const bars = (el, pairs, lab) => { const m = Math.max(1, ...pairs.map(p => p[1])); $(el).innerHTML = pairs.map(p => `<div class="bar"><span>${esc(lab(p[0]))}</span><div class="t"><i style="width:${p[1] / m * 100}%"></i></div><span class="v">${p[1]}</span></div>`).join(''); };
    bars('#btype', cnt(P, p => p[3]), k => TYPE[k] || k);
    bars('#bdes', cnt(P, p => p[12][0] && (['annual_net_wealth', 'one_off_levy', 'billionaire_minimum', 'partial_wealth'].find(d => p[12].includes(d)) || 'wealth_tax_unspecified')), k => DES[k] || k);
    bars('#bev', cnt(E, e => e[3]).slice(0, 10), k => EVT[k] || k);
  }

  if (sub === 'method') {
    const m = data.meta, unver = m.evidence - m.verified;
    body.innerHTML = `<div class="panel method"><h2>How to read ${esc(m.name)}</h2>
      <p><b>What counts.</b> A person or organisation is listed only if a dated, linked source shows them supporting an actual wealth tax: a recurring tax on net wealth, a one-off levy, or a minimum tax on billionaires. Income, property and capital gains reforms alone do not count. Opponents are not listed.</p>
      <p><span class="g gA">A</span> explicit: a formal act or a stated design, such as a vote, signed motion, party policy or a named rate. <span class="g gB">B</span> named: backs a wealth tax without a design. <span class="g gC">C</span> implied: wording that suggests support without naming a wealth tax.</p>
      <h3 style="margin-top:20px">Gaps and caveats</h3><ul>
      <li>${unver} of ${m.evidence} sourced rows are not yet checked by a person against the original page.</li>
      ${m.units ? `<li>${m.units_done} of ${m.units} local areas have been fully read. A blank area means unread, not opposed.</li>` : ''}
      <li>${m.excluded} people and organisations were looked at and excluded, for example opponents, sceptics and people who have died.</li>
      <li>People are assumed alive unless a death record was found; those people are removed.</li>
      <li>${esc(m.notes || '')}</li></ul>
      <p class="note">Last run ${esc(m.updated)}. Country lead: ${esc(m.lead)}.</p>
      <a class="report" href="${esc(issueUrl('[' + cc + '] Report: ' + m.name, {country: slug}))}" target="_blank" rel="noopener">Report a problem with this country</a></div>`;
  }
}
let PEOPLE_SEL = null;
boot();
