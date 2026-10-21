"""Build design/prototype/index.html: a canvas of all screens + a clickable Run mode.

Usage: python3 design/_gen/proto.py   (after build.py; reads /tmp/frndu_registry.tsv or scans folders)
"""
import json
import os
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'prototype', 'index.html')


def collect():
    order = []
    reg = '/tmp/frndu_registry.tsv'
    if os.path.exists(reg):
        for line in open(reg):
            sid, screen, state, rel, note = (line.rstrip('\n').split('\t') + [''] * 5)[:5]
            order.append((sid, screen, state, rel, note))
    else:
        for p in sorted(glob.glob(os.path.join(ROOT, '*', '*.svg'))):
            rel = os.path.relpath(p, ROOT)
            name = os.path.basename(p)[:-4]
            sid, rest = name.split('_', 1)
            screen, state = rest.rsplit('_', 1)
            order.append((sid, screen, state, rel, ''))
    seen = set()
    frames, screens, sheets, notes = {}, {}, [], {}
    for sid, screen, state, rel, note in order:
        if rel in seen:
            continue
        seen.add(rel)
        svg = open(os.path.join(ROOT, rel)).read()
        if screen == 'Components':
            sheets.append({'name': state, 'svg': svg})
            continue
        name = f'{sid}_{screen}_{state}'
        frames[name] = svg
        screens.setdefault(sid, {'id': sid, 'name': screen.replace('-', ' '), 'states': []})['states'].append(state)
        if note:
            notes[name] = note
    return frames, screens, sheets, notes


CSS = r"""
:root { --ink:#10233F; --slate:#66758A; --line:#D8DDE5; --bg:#EEF0F4; --blue:#5B7CFA; }
* { box-sizing: border-box; }
html, body { margin:0; height:100%; font-family: 'Plus Jakarta Sans', Inter, system-ui, -apple-system, sans-serif; color:var(--ink); background:var(--bg); overflow:hidden; }
header { position:fixed; inset:0 0 auto 0; height:56px; display:flex; align-items:center; gap:12px; padding:0 16px; background:#fff; border-bottom:1px solid var(--line); z-index:20; }
header h1 { font-size:16px; margin:0 12px 0 0; font-weight:700; white-space:nowrap; }
header .sp { flex:1; }
button { font:inherit; cursor:pointer; border:1px solid var(--line); background:#fff; color:var(--ink); border-radius:10px; padding:8px 12px; font-size:13px; font-weight:600; }
button:hover { border-color:#B8C0CB; }
button.primary { background:var(--blue); color:#fff; border-color:var(--blue); }
button.primary:hover { filter:brightness(0.95); }
button:focus-visible { outline:2px solid var(--blue); outline-offset:2px; }
.seg { display:flex; border:1px solid var(--line); border-radius:10px; overflow:hidden; }
.seg button { border:0; border-radius:0; }
.seg button[aria-pressed=true] { background:#EAF0FF; color:var(--blue); }
.hint { font-size:12px; color:var(--slate); white-space:nowrap; }
#viewport { position:fixed; inset:56px 0 0 0; overflow:hidden; cursor:grab; background:
  radial-gradient(circle, #D8DDE5 1px, transparent 1px) 0 0/24px 24px, var(--bg); }
#viewport.dragging { cursor:grabbing; }
#world { position:absolute; left:0; top:0; transform-origin:0 0; }
.rowtitle { position:absolute; white-space:nowrap; font-size:32px; font-weight:700; color:var(--ink); letter-spacing:-0.4px; }
.scr { position:absolute; z-index:1; }
#edges .el { }
.scr .lbl { display:flex; align-items:center; gap:8px; margin-bottom:10px; font-weight:700; font-size:18px; }
.scr .lbl .id { background:var(--ink); color:#fff; border-radius:8px; padding:2px 8px; font-size:14px; }
.scr .lbl .play { margin-left:auto; padding:4px 10px; font-size:12px; }
.scr .main { display:block; width:260px; height:563px; border-radius:24px; box-shadow:0 8px 30px rgba(16,35,63,.12); background:#fff; cursor:pointer; overflow:hidden; }
.scr .main img, .thumb img { width:100%; height:100%; display:block; pointer-events:none; }
.states { display:flex; flex-wrap:wrap; gap:10px; margin-top:14px; width:420px; }
.thumb { width:76px; cursor:pointer; }
.thumb .im { width:76px; height:164px; border-radius:10px; overflow:hidden; box-shadow:0 2px 8px rgba(16,35,63,.10); background:#fff; outline:2px solid transparent; }
.thumb:hover .im { outline-color:var(--blue); }
.thumb span { display:block; font-size:10px; line-height:13px; color:var(--slate); margin-top:4px; word-break:break-word; }
#edges { position:absolute; z-index:0; left:0; top:0; overflow:visible; pointer-events:none; }
#edges path { fill:none; stroke:#5B7CFA; stroke-width:2.5; opacity:.7; }
#edges .el rect { fill:#fff; stroke:#5B7CFA; stroke-width:1.5; }
#edges .el text { font-size:13px; font-weight:600; fill:#5B7CFA; }
.sheetimg { position:absolute; border-radius:16px; box-shadow:0 8px 30px rgba(16,35,63,.12); background:#fff; }
/* Run mode */
#run { position:fixed; inset:56px 0 0 0; display:none; background:#E4E7EC; }
#run.on { display:flex; }
#side { width:300px; background:#fff; border-right:1px solid var(--line); overflow:auto; padding:16px; }
#side h2 { font-size:13px; text-transform:uppercase; letter-spacing:.06em; color:var(--slate); margin:16px 0 8px; }
#side select { width:100%; font:inherit; padding:8px; border-radius:10px; border:1px solid var(--line); }
#side .st { display:block; width:100%; text-align:left; margin:0 0 6px; font-weight:500; }
#side .st[aria-current=true] { background:#EAF0FF; border-color:var(--blue); color:var(--blue); }
#side .note { font-size:12px; color:var(--slate); background:#F6F7F9; border-radius:10px; padding:10px; margin-top:8px; }
#stage { flex:1; display:flex; align-items:center; justify-content:center; position:relative; }
#phone { position:relative; width:414px; height:868px; border-radius:56px; background:#10233F; padding:12px; box-shadow:0 30px 80px rgba(16,35,63,.35); transform-origin:center center; }
#screen { width:390px; height:844px; border-radius:44px; overflow:hidden; background:#FFF4D6; position:relative; }
#screen svg { display:block; animation:fade .16s ease-out; }
@keyframes fade { from { opacity:.35; } to { opacity:1; } }
#screen svg * { pointer-events:none; }
#screen svg [data-hit] { pointer-events:all; cursor:pointer; }
#screen svg [data-hit="scrim"], #screen svg [data-hit="sheet"], #screen svg [data-hit="dialog"] { cursor:default; }
#screen.flash svg [data-hit]:not([data-hit="scrim"]):not([data-hit="sheet"]):not([data-hit="dialog"]),
#screen.show svg [data-hit]:not([data-hit="scrim"]):not([data-hit="sheet"]):not([data-hit="dialog"]) { fill:#5B7CFA !important; fill-opacity:.22 !important; stroke:#5B7CFA; stroke-width:1.5; }
#crumb { position:absolute; top:16px; left:50%; transform:translateX(-50%); background:#fff; border:1px solid var(--line); border-radius:999px; padding:6px 14px; font-size:12px; font-weight:600; white-space:nowrap; }
#auto { position:absolute; bottom:16px; left:50%; transform:translateX(-50%); font-size:12px; color:var(--slate); white-space:nowrap; }
.step { position:absolute; top:50%; transform:translateY(-50%); width:52px; height:52px; border-radius:26px; font-size:26px; line-height:1; padding:0;
  display:flex; align-items:center; justify-content:center; box-shadow:0 4px 14px rgba(16,35,63,.12); z-index:5; }
#prev { left:24px; } #next { right:24px; }
#stepper { display:flex; align-items:center; gap:8px; margin-top:4px; }
#stepper .count { font-size:12px; color:var(--slate); font-weight:600; min-width:64px; text-align:center; }
#play[aria-pressed=true] { background:#EAF0FF; border-color:var(--blue); color:var(--blue); }
/* Background opacity control (client update 21 Oct): preview the Blue / Coral cloud strength on every frame */
#cloudBtn .val { color:var(--slate); font-weight:500; margin-left:6px; font-variant-numeric:tabular-nums; }
#cloudBtn[aria-expanded=true], #cloudBtn.custom { background:#EAF0FF; border-color:var(--blue); color:var(--blue); }
#cloudPanel { position:fixed; top:64px; right:16px; width:304px; z-index:40; background:#fff; border:1px solid var(--line); border-radius:16px;
  box-shadow:0 12px 40px rgba(16,35,63,.18); padding:16px; }
#cloudPanel[hidden] { display:none; }
#cloudPanel .head { display:flex; align-items:center; justify-content:space-between; }
#cloudPanel h2 { font-size:15px; margin:0; }
#cloudPanel .x { border:0; padding:4px 10px; font-size:20px; line-height:1; }
#cloudPanel .row { display:flex; align-items:center; justify-content:space-between; font-size:13px; font-weight:600; margin:14px 0 6px; }
#cloudPanel .row span { display:flex; align-items:center; gap:8px; }
#cloudPanel .sw { width:12px; height:12px; border-radius:6px; display:inline-block; }
#cloudPanel output { color:var(--slate); font-variant-numeric:tabular-nums; }
#cloudPanel input[type=range] { width:100%; margin:0; }
#clB { accent-color:#5B7CFA; } #clC { accent-color:#E94B4B; }
#cloudPanel .acts { display:flex; gap:8px; margin-top:16px; }
#cloudPanel .acts button { flex:1; }
#cloudPanel .note { font-size:12px; line-height:17px; color:var(--slate); margin:12px 0 0; }
@media (max-width: 1240px) { header .hint.long { display:none; } }
"""

JS = r"""
const $ = (s) => document.querySelector(s);
const blobs = {};
// Photos live on the Vercel deploy (/img). SVGs inside <img> can't load external files, so thumbnails get data URLs.
const PHOTO_RE = /https:\/\/frndu-prototype\.vercel\.app\/img\/([\w-]+\.jpg)/g;
const PHOTOS = {};
const withPhotos = (svg) => svg.replace(PHOTO_RE, (m, f) => PHOTOS[f] || m);

// Background clouds: the frames carry the default opacities (cl-* classes). The Background control previews other values:
// Run mode (inline SVG) follows the CSS variables live; canvas images are SVG files, so they get a literal <style> injected.
const CLOUD_KEY = 'frndu-clouds';
const pct = (v) => Math.round(v * 100);
let clouds = (() => {
  try { const v = JSON.parse(localStorage.getItem(CLOUD_KEY)); if (v && v.b >= 0 && v.b <= 1 && v.c >= 0 && v.c <= 1) return v; } catch (e) { /* no saved values */ }
  return { b: CLOUDS.def.b, c: CLOUDS.def.c };
})();
const cloudsDefault = () => pct(clouds.b) === pct(CLOUDS.def.b) && pct(clouds.c) === pct(CLOUDS.def.c);
const cloudCss = () => Object.entries(CLOUDS.shapes).map(([cls, [k, share]]) => `.${cls}{opacity:${(clouds[k] * share).toFixed(3)}}`).join('');
const withClouds = (svg) => (cloudsDefault() ? svg : svg.replace('<defs>', `<defs><style>${cloudCss()}</style>`));

const url = (name) => blobs[name] || (blobs[name] = URL.createObjectURL(new Blob([withClouds(withPhotos(FRAMES[name] || extSvg(name)))], { type: 'image/svg+xml' })));
function refreshImages() {   // rebuild every canvas image (after photos load or the cloud opacity changes)
  for (const k in blobs) { URL.revokeObjectURL(blobs[k]); delete blobs[k]; }
  document.querySelectorAll('img[data-src]').forEach((im) => { if (im.src) im.src = url(im.dataset.src); });
}
setTimeout(function preloadPhotos() {  // deferred: FRAMES is declared further down
  const files = [...new Set(Object.values(FRAMES).join('').match(PHOTO_RE) || [])];
  Promise.all(files.map((u) => fetch(u).then((r) => r.blob()).then((b) => new Promise((res) => {
    const fr = new FileReader(); fr.onload = () => { PHOTOS[u.split('/').pop()] = fr.result; res(); }; fr.readAsDataURL(b);
  })).catch(() => {}))).then(refreshImages);
}, 0);

let cloudTimer = null;
function applyClouds(refresh) {
  const r = document.documentElement.style;
  r.setProperty('--cl-b', clouds.b); r.setProperty('--cl-c', clouds.c);
  $('#clB').value = pct(clouds.b); $('#clC').value = pct(clouds.c);
  $('#clBv').textContent = `${pct(clouds.b)}%`; $('#clCv').textContent = `${pct(clouds.c)}%`;
  $('#cloudVal').textContent = `${pct(clouds.b)} · ${pct(clouds.c)}`;
  $('#cloudBtn').classList.toggle('custom', !cloudsDefault());
  try { if (cloudsDefault()) localStorage.removeItem(CLOUD_KEY); else localStorage.setItem(CLOUD_KEY, JSON.stringify(clouds)); } catch (e) { /* private mode */ }
  if (refresh) { clearTimeout(cloudTimer); cloudTimer = setTimeout(refreshImages, 300); }
}
function toggleCloudPanel(open) {
  const p = $('#cloudPanel');
  const on = open === undefined ? p.hidden : open;
  p.hidden = !on;
  $('#cloudBtn').setAttribute('aria-expanded', String(on));
  if (on) $('#clB').focus(); else if (p.contains(document.activeElement)) $('#cloudBtn').focus();
}
function initCloudPanel() {
  $('#cloudNote').textContent = `Preview only. The frames ship at Blue ${pct(CLOUDS.def.b)}% · Coral ${pct(CLOUDS.def.c)}%. `
    + `Before = the 11 Oct look (${pct(CLOUDS.before.b)}% · ${pct(CLOUDS.before.c)}%). Your values stay in this browser.`;
  $('#cloudBtn').onclick = () => toggleCloudPanel();
  $('#cloudClose').onclick = () => toggleCloudPanel(false);
  $('#clB').addEventListener('input', (e) => { clouds = { b: e.target.value / 100, c: clouds.c }; applyClouds(true); });
  $('#clC').addEventListener('input', (e) => { clouds = { b: clouds.b, c: e.target.value / 100 }; applyClouds(true); });
  $('#clBefore').onclick = () => { clouds = { b: CLOUDS.before.b, c: CLOUDS.before.c }; applyClouds(true); };
  $('#clReset').onclick = () => { clouds = { b: CLOUDS.def.b, c: CLOUDS.def.c }; applyClouds(true); };
  $('#cloudPanel').addEventListener('keydown', (e) => { if (e.key === 'Escape') { e.stopPropagation(); toggleCloudPanel(false); } });
  applyClouds(false);
}
const screenOf = (name) => name.split('_')[0];
const stateOf = (name) => name.slice(name.lastIndexOf('_') + 1);

// ---------- placeholder screens owned by others ----------
function extSvg(key) {
  const id = key.slice(2), [title, owner] = EXTERNAL[id] || [id, '?'];
  const label = /^\d/.test(id) ? `${id} · ${title}` : title;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844" viewBox="0 0 390 844" font-family="'Plus Jakarta Sans', Inter, system-ui, sans-serif">
  <rect width="390" height="844" fill="#FFF4D6"/>
  <text x="40" y="32" font-size="15" font-weight="600" fill="#10233F">9:41</text>
  <g transform="translate(24 63)" fill="none" stroke="#10233F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></g>
  <rect data-hit="back" x="12" y="51" width="48" height="48" fill="#fff" fill-opacity="0"/>
  <rect x="24" y="300" width="342" height="200" rx="20" fill="#FFF9EA" stroke="#EEF1F5"/>
  <text x="195" y="372" text-anchor="middle" font-size="22" font-weight="700" fill="#10233F">${label}</text>
  <text x="195" y="404" text-anchor="middle" font-size="14" fill="#66758A">Not in this batch · owner: ${owner}</text>
  <text x="195" y="440" text-anchor="middle" font-size="13" fill="#8794A5">Tap back to return</text>
  <rect x="24" y="738" width="342" height="56" rx="16" fill="#5B7CFA"/>
  <text x="195" y="772" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">Go back</text>
  <rect data-hit="back" x="24" y="738" width="342" height="56" fill="#fff" fill-opacity="0"/>
  <rect x="128" y="826" width="134" height="5" rx="2.5" fill="#10233F"/></svg>`;
}

// ---------- canvas ----------
const COLW = 460, MAIN_W = 260, MAIN_H = 563, ROW_GAP = 160, X0 = 80;
let view = { x: 40, y: 40, k: 0.42 };
const anchors = {};

function buildCanvas() {
  const world = $('#world');
  let y = 40, maxX = 0;
  const parts = [];
  LAYOUT.forEach((row) => {
    parts.push(`<div class="rowtitle" style="left:${X0}px;top:${y}px">${row.title}</div>`);
    y += 70;
    let rowH = 0;
    row.screens.forEach((sid, i) => {
      const sc = SCREENS[sid]; if (!sc) return;
      const x = X0 + i * COLW;
      const def = `${sid}_${sc.name.replace(/ /g, '-')}_${DEFAULT_STATE[sid] || sc.states[0]}`;
      anchors[sid] = { x, y: y + 44, w: MAIN_W, h: MAIN_H };
      const thumbs = sc.states.map((st) => {
        const n = `${sid}_${sc.name.replace(/ /g, '-')}_${st}`;
        return `<div class="thumb" data-go="${n}" title="${n}"><div class="im"><img loading="lazy" alt="" data-src="${n}"></div><span>${st.replace(/-/g, ' ')}</span></div>`;
      }).join('');
      parts.push(`<div class="scr" style="left:${x}px;top:${y}px">
        <div class="lbl"><span class="id">${sid}</span>${sc.name}<button class="play" data-go="${def}" aria-label="Run from ${sid}">▶ Run</button></div>
        <div class="main" data-go="${def}" title="${def}"><img alt="${sid} ${sc.name}" data-src="${def}"></div>
        <div class="states">${thumbs}</div></div>`);
      const rows = Math.ceil(sc.states.length / 5);
      rowH = Math.max(rowH, 44 + MAIN_H + 14 + rows * 195);
      maxX = Math.max(maxX, x + COLW);
    });
    y += rowH + ROW_GAP;
  });
  // component sheets
  parts.push(`<div class="rowtitle" style="left:${X0}px;top:${y}px">Shared components</div>`);
  y += 70;
  let sx = X0;
  SHEETS.forEach((s, i) => {
    const b = URL.createObjectURL(new Blob([s.svg], { type: 'image/svg+xml' }));
    const w = 700;
    parts.push(`<img class="sheetimg" style="left:${sx}px;top:${y}px;width:${w}px" src="${b}" alt="${s.name}">`);
    sx += w + 60;
  });
  world.innerHTML = `<svg id="edges" width="${Math.max(maxX, sx)}" height="${y + 1200}"></svg>` + parts.join('');
  world.querySelectorAll('img[data-src]').forEach((im) => { im.src = url(im.dataset.src); });
  drawEdges();
  applyView();
}

function drawEdges() {
  const out = [];
  EDGES.forEach(([a, b, label]) => {
    const A = anchors[a], B = anchors[b]; if (!A || !B) return;
    let x1, y1, x2, y2, d;
    const sameRow = Math.abs(A.y - B.y) < 10;
    if (sameRow && B.x > A.x) {
      x1 = A.x + A.w; y1 = A.y + A.h * 0.35; x2 = B.x; y2 = B.y + B.h * 0.35;
      if (B.x - A.x > COLW + 10) { // skip over neighbours: arc above
        const top = A.y - 30;
        x1 = A.x + A.w / 2; y1 = A.y; x2 = B.x + B.w / 2; y2 = B.y;
        d = `M${x1} ${y1} C${x1} ${top - 60} ${x2} ${top - 60} ${x2} ${y2}`;
      } else d = `M${x1} ${y1} C${x1 + 90} ${y1} ${x2 - 90} ${y2} ${x2} ${y2}`;
    } else if (sameRow) { // backwards in same row: arc below
      x1 = A.x + A.w / 2; y1 = A.y + A.h; x2 = B.x + B.w / 2; y2 = B.y + B.h;
      const low = y1 + 120;
      d = `M${x1} ${y1} C${x1} ${low} ${x2} ${low} ${x2} ${y2}`;
    } else if (B.y > A.y) { // next row
      x1 = A.x + A.w / 2; y1 = A.y + A.h; x2 = B.x + B.w / 2; y2 = B.y - 44;
      d = `M${x1} ${y1} C${x1} ${y1 + 500} ${x2} ${y2 - 400} ${x2} ${y2}`;
    } else { // up a row
      x1 = A.x; y1 = A.y + A.h * 0.5; x2 = B.x + B.w; y2 = B.y + B.h * 0.6;
      d = `M${x1} ${y1} C${x1 - 260} ${y1} ${x2 + 260} ${y2} ${x2} ${y2}`;
    }
    const mx = (x1 + x2) / 2, my = sameRow && B.x > A.x && B.x - A.x <= COLW + 10 ? (y1 + y2) / 2 : (sameRow ? (B.x > A.x ? A.y - 75 : A.y + A.h + 90) : (y1 + y2) / 2);
    const tw = label.length * 7.5 + 20;
    out.push(`<path d="${d}" marker-end="url(#arr)"/>`,
      `<g class="el"><rect x="${mx - tw / 2}" y="${my - 13}" width="${tw}" height="26" rx="13"/><text x="${mx}" y="${my + 5}" text-anchor="middle">${label}</text></g>`);
  });
  $('#edges').innerHTML = `<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#5B7CFA"/></marker></defs>` + out.join('');
}

function applyView() { $('#world').style.transform = `translate(${view.x}px,${view.y}px) scale(${view.k})`; $('#zoomv').textContent = Math.round(view.k * 100) + '%'; }
function zoomAt(k, cx, cy) {
  k = Math.min(2, Math.max(0.08, k));
  view.x = cx - (cx - view.x) * (k / view.k); view.y = cy - (cy - view.y) * (k / view.k); view.k = k; applyView();
}
function fit() {
  const w = $('#world').scrollWidth || 2900, vp = $('#viewport').getBoundingClientRect();
  view.k = Math.min(0.6, (vp.width - 80) / 2900); view.x = 40; view.y = 30; applyView();
}

function initCanvasEvents() {
  const vp = $('#viewport');
  let drag = null, moved = false;
  vp.addEventListener('pointerdown', (e) => { if (e.button !== 0) return; drag = { x: e.clientX, y: e.clientY, vx: view.x, vy: view.y }; moved = false; vp.classList.add('dragging'); });
  window.addEventListener('pointermove', (e) => {
    if (!drag) return; const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    if (Math.abs(dx) + Math.abs(dy) > 4) moved = true;
    view.x = drag.vx + dx; view.y = drag.vy + dy; applyView();
  });
  window.addEventListener('pointerup', (e) => {
    if (drag && !moved) { const t = e.target.closest('[data-go]'); if (t) startRun(t.dataset.go); }
    drag = null; vp.classList.remove('dragging');
  });
  vp.addEventListener('wheel', (e) => {
    e.preventDefault();
    const r = vp.getBoundingClientRect();
    if (e.ctrlKey || e.metaKey) zoomAt(view.k * Math.exp(-e.deltaY * 0.01), e.clientX - r.left, e.clientY - r.top);
    else { view.x -= e.deltaX; view.y -= e.deltaY; applyView(); }
  }, { passive: false });
}

// ---------- run mode ----------
let cur = null, hist = [], timer = null, showHot = false, stepping = false, playing = null;
let ORDER = [];   // every frame, in canvas order: screen by screen, state by state
const frameName = (sid, st) => `${sid}_${SCREENS[sid].name.replace(/ /g, '-')}_${st}`;

// Step through every state of the current screen; past the last state it rolls on to the next screen.
function step(dir) {
  if (!cur || cur.startsWith('X:')) { cur = ORDER[0]; }
  let i = ORDER.indexOf(cur);
  if (i < 0) i = 0; else i = (i + dir + ORDER.length) % ORDER.length;
  stepping = true; cur = ORDER[i]; render();
}
function togglePlay() {
  if (playing) { clearInterval(playing); playing = null; }
  else { step(1); playing = setInterval(() => step(1), 1800); }
  $('#play').setAttribute('aria-pressed', !!playing);
  $('#play').textContent = playing ? '❚❚ Pause' : '▶ Play all';
}

function resolve(frame, key) {
  const fl = FLOW[frame] || {};
  if (key in fl) return fl[key];
  const pre = key.split(':')[0] + ':*';
  if (pre in fl) return fl[pre];
  if (key in GLOBAL) return GLOBAL[key];
  return undefined;
}

function go(target, push = true) {
  if (target === null || target === undefined) return false;
  if (target === 'BACK') { if (hist.length) { cur = hist.pop(); render(); } return true; }
  if (target === 'BACK_SCREEN') { // leave the current screen: skip history entries that are states of it
    const sid = screenOf(cur);
    while (hist.length && screenOf(hist[hist.length - 1]) === sid) hist.pop();
    if (hist.length) { cur = hist.pop(); stepping = false; render(); }
    return true;
  }
  if (push && cur) hist.push(cur);
  stepping = false; cur = target; render(); return true;
}

function render() {
  clearTimeout(timer);
  const scr = $('#screen');
  scr.innerHTML = FRAMES[cur] || extSvg(cur);
  scr.classList.toggle('show', showHot);
  const sid = cur.startsWith('X:') ? null : screenOf(cur);
  $('#crumb').textContent = cur.startsWith('X:') ? `${cur.slice(2)} · ${(EXTERNAL[cur.slice(2)] || [''])[0]} (placeholder)` : `${sid} · ${SCREENS[sid].name} — ${stateOf(cur).replace(/-/g, ' ')}`;
  const fl = FLOW[cur] || {};
  const paused = stepping || playing;
  $('#auto').textContent = fl.auto ? (paused ? 'Auto-advance paused while stepping · click the phone to resume the flow'
    : `Auto-advances in ${(fl.auto[0] / 1000).toFixed(1)} s`) : (fl.down || fl.up ? 'Scroll on the phone to see more' : '');
  if (fl.auto && !paused) timer = setTimeout(() => go(fl.auto[1]), fl.auto[0]);
  // side panel
  if (sid) {
    $('#scrsel').value = sid;
    const sc = SCREENS[sid];
    $('#states').innerHTML = sc.states.map((st) => {
      const n = `${sid}_${sc.name.replace(/ /g, '-')}_${st}`;
      return `<button class="st" data-frame="${n}" aria-current="${n === cur}">${st.replace(/-/g, ' ')}</button>`;
    }).join('');
    const si = sc.states.indexOf(stateOf(cur));
    $('#count').textContent = `${si + 1} / ${sc.states.length}`;
    $('#note').textContent = NOTES[cur] || '';
    $('#note').style.display = NOTES[cur] ? 'block' : 'none';
  }
  location.hash = encodeURIComponent(cur);
}

function startRun(frame) {
  hist = []; cur = frame; $('#run').classList.add('on'); $('#viewport').style.display = 'none';
  $('#modeCanvas').setAttribute('aria-pressed', 'false'); $('#modeRun').setAttribute('aria-pressed', 'true');
  fitPhone(); render();
}
function stopRun() {
  clearTimeout(timer); if (playing) togglePlay(); $('#run').classList.remove('on'); $('#viewport').style.display = 'block';
  $('#modeCanvas').setAttribute('aria-pressed', 'true'); $('#modeRun').setAttribute('aria-pressed', 'false');
  history.replaceState(null, '', location.pathname);
}
function fitPhone() {
  const st = $('#stage').getBoundingClientRect();
  const k = Math.min(1, (st.height - 90) / 868, (st.width - 40) / 414);
  $('#phone').style.transform = `scale(${k})`;
}

function initRunEvents() {
  $('#screen').addEventListener('click', (e) => {
    const h = e.target.closest('[data-hit]');
    const key = h && h.getAttribute('data-hit');
    const t = key ? resolve(cur, key) : undefined;
    if (!go(t)) { const s = $('#screen'); s.classList.add('flash'); setTimeout(() => s.classList.remove('flash'), 450); }
  });
  let lastWheel = 0;
  $('#screen').addEventListener('wheel', (e) => {
    e.preventDefault();
    const now = Date.now(); if (now - lastWheel < 500 || Math.abs(e.deltaY) < 15) return;
    const fl = FLOW[cur] || {}; const t = e.deltaY > 0 ? fl.down : fl.up;
    if (t) { lastWheel = now; go(t); }
  }, { passive: false });
  $('#states').addEventListener('click', (e) => { const b = e.target.closest('[data-frame]'); if (b) go(b.dataset.frame); });
  $('#scrsel').addEventListener('change', (e) => {
    const sid = e.target.value, sc = SCREENS[sid];
    go(`${sid}_${sc.name.replace(/ /g, '-')}_${DEFAULT_STATE[sid] || sc.states[0]}`);
  });
  $('#back').onclick = () => go('BACK');
  $('#prev').onclick = () => step(-1); $('#next').onclick = () => step(1);
  $('#sprev').onclick = () => step(-1); $('#snext').onclick = () => step(1);
  $('#play').onclick = togglePlay;
  $('#restart').onclick = () => { hist = []; stepping = false; cur = START; render(); };
  $('#hot').onclick = () => { showHot = !showHot; $('#hot').setAttribute('aria-pressed', showHot); $('#screen').classList.toggle('show', showHot); };
  window.addEventListener('resize', () => { if ($('#run').classList.contains('on')) fitPhone(); });
  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'SELECT' || e.target.tagName === 'INPUT' || e.target.closest('#cloudPanel')) return;
    if (!$('#run').classList.contains('on')) return;
    if (e.key === 'Escape') { if (playing) togglePlay(); stopRun(); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
    else if (e.key === 'Backspace' || e.key.toLowerCase() === 'b') { e.preventDefault(); go('BACK'); }
    else if (e.key === ' ') { e.preventDefault(); togglePlay(); }
    else if (e.key.toLowerCase() === 'h') $('#hot').click();
    else if (e.key.toLowerCase() === 'r') $('#restart').click();
    else if (e.key === 'ArrowDown') { const t = (FLOW[cur] || {}).down; if (t) go(t); }
    else if (e.key === 'ArrowUp') { const t = (FLOW[cur] || {}).up; if (t) go(t); }
  });
}

// ---------- boot ----------
window.addEventListener('DOMContentLoaded', () => {
  initCloudPanel();
  $('#scrsel').innerHTML = LAYOUT.flatMap((r) => r.screens).filter((s) => SCREENS[s]).map((s) => `<option value="${s}">${s} · ${SCREENS[s].name}</option>`).join('');
  ORDER = LAYOUT.flatMap((r) => r.screens).filter((s) => SCREENS[s]).flatMap((s) => SCREENS[s].states.map((st) => frameName(s, st)));
  buildCanvas(); fit(); initCanvasEvents(); initRunEvents();
  $('#runBtn').onclick = () => startRun(START);
  $('#modeRun').onclick = () => startRun(cur || START);
  $('#modeCanvas').onclick = stopRun;
  $('#zin').onclick = () => { const r = $('#viewport').getBoundingClientRect(); zoomAt(view.k * 1.25, r.width / 2, r.height / 2); };
  $('#zout').onclick = () => { const r = $('#viewport').getBoundingClientRect(); zoomAt(view.k / 1.25, r.width / 2, r.height / 2); };
  $('#zfit').onclick = fit;
  const h = decodeURIComponent(location.hash.slice(1));
  if (h && (FRAMES[h] || h.startsWith('X:'))) startRun(h);
});
"""

HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Frndu prototype · all screens</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>__CSS__</style></head>
<body>
<header>
  <h1>Frndu · Prototype</h1>
  <div class="seg" role="group" aria-label="Mode"><button id="modeCanvas" aria-pressed="true">Canvas</button><button id="modeRun" aria-pressed="false">Prototype</button></div>
  <button id="runBtn" class="primary">▶ Run</button>
  <span class="sp"></span>
  <span class="hint long">Drag or scroll to pan · ⌘/Ctrl + scroll or pinch to zoom · click any frame to run from it</span>
  <button id="cloudBtn" aria-expanded="false" aria-controls="cloudPanel">◐ Background<span class="val" id="cloudVal"></span></button>
  <button id="zout" aria-label="Zoom out">−</button><span id="zoomv" class="hint" style="min-width:40px;text-align:center">40%</span><button id="zin" aria-label="Zoom in">+</button><button id="zfit">Fit</button>
</header>
<div id="cloudPanel" role="dialog" aria-labelledby="cloudTitle" hidden>
  <div class="head"><h2 id="cloudTitle">Background opacity</h2><button class="x" id="cloudClose" aria-label="Close background opacity">×</button></div>
  <label class="row" for="clB"><span><i class="sw" style="background:#5B7CFA"></i>Blue · top right</span><output id="clBv" for="clB"></output></label>
  <input id="clB" type="range" min="0" max="100" step="1">
  <label class="row" for="clC"><span><i class="sw" style="background:#E94B4B"></i>Coral · bottom left</span><output id="clCv" for="clC"></output></label>
  <input id="clC" type="range" min="0" max="100" step="1">
  <div class="acts"><button id="clBefore">Before</button><button id="clReset" class="primary">Reset</button></div>
  <p class="note" id="cloudNote"></p>
</div>
<div id="viewport"><div id="world"></div></div>
<div id="run">
  <aside id="side">
    <h2>Screen</h2><select id="scrsel" aria-label="Jump to screen"></select>
    <h2>States</h2>
    <div id="stepper"><button id="sprev" aria-label="Previous state">‹</button><span id="count" class="count"></span><button id="snext" aria-label="Next state">›</button>
      <button id="play" aria-pressed="false">▶ Play all</button></div>
    <div id="states" style="margin-top:10px"></div>
    <div id="note" class="note"></div>
    <h2>Controls</h2>
    <div style="display:flex;gap:8px;flex-wrap:wrap"><button id="back">Back (⌫ / B)</button><button id="restart">↺ Restart</button><button id="hot" aria-pressed="false">Hotspots (H)</button></div>
    <p class="hint" style="white-space:normal;margin-top:12px">Click buttons, cards, chips, inputs and tabs on the phone. Clicking empty space flashes the hotspots. Scroll on the phone for long screens. ‹ › or ← → step through every state (then on to the next screen). Space plays all frames. Esc returns to the canvas.</p>
  </aside>
  <section id="stage"><div id="crumb"></div><button id="prev" class="step" aria-label="Previous state">‹</button><button id="next" class="step" aria-label="Next state">›</button><div id="phone"><div id="screen"></div></div><div id="auto"></div></section>
</div>
<script>
__FLOW__
const FRAMES = __FRAMES__;
const SCREENS = __SCREENS__;
const SHEETS = __SHEETS__;
const NOTES = __NOTES__;
const CLOUDS = __CLOUDS__;
__JS__
</script>
</body></html>
"""


def js_json(o):
    return json.dumps(o, ensure_ascii=False).replace('</', '<\\/')


def cloud_bits():
    """Background-cloud defaults + one CSS rule per cloud shape, so Run mode follows --cl-b / --cl-c live."""
    from lib import CLOUD_DEFAULT, CLOUD_BEFORE, CLOUD_SHAPES
    data = {'def': CLOUD_DEFAULT, 'before': CLOUD_BEFORE, 'shapes': {k: list(v) for k, v in CLOUD_SHAPES.items()}}
    css = (f':root {{ --cl-b:{CLOUD_DEFAULT["b"]}; --cl-c:{CLOUD_DEFAULT["c"]}; }}\n'
           + '\n'.join(f'#screen .{cls} {{ opacity:calc(var(--cl-{k}) * {share}); }}' for cls, (k, share) in CLOUD_SHAPES.items()) + '\n')
    return data, css


def main():
    frames, screens, sheets, notes = collect()
    flow = open(os.path.join(HERE, 'flow.js')).read()
    clouds, cloud_css = cloud_bits()
    html = (HTML.replace('__CSS__', CSS + cloud_css).replace('__FLOW__', flow).replace('__FRAMES__', js_json(frames))
            .replace('__SCREENS__', js_json(screens)).replace('__SHEETS__', js_json(sheets))
            .replace('__NOTES__', js_json(notes)).replace('__CLOUDS__', js_json(clouds)).replace('__JS__', JS))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        f.write(html)
    print(f'{OUT}: {len(frames)} frames, {len(screens)} screens, {len(sheets)} sheets, {os.path.getsize(OUT) // 1024} KB')


if __name__ == '__main__':
    main()
