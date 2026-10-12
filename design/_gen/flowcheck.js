// Flow checker for design/prototype/index.html.
// Usage: node design/_gen/flowcheck.js design/prototype/index.html [v]
// Checks: every FLOW frame exists, every target exists (frame, BACK, BACK_SCREEN, null, X:<EXTERNAL>),
// every key is a data-hit on that frame or another state of the same screen, EDGES/LAYOUT/DEFAULT_STATE are valid.
// With "v", also lists hotspots that resolve to nothing (informational; many sit under a scrim).
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const js = html.slice(html.lastIndexOf('<script>') + 8, html.lastIndexOf('</script>'));
const body = js.split('const $ = ')[0];
const { EXTERNAL, GLOBAL, FLOW, EDGES, LAYOUT, DEFAULT_STATE, START, FRAMES, SCREENS } =
  new Function(body + '; return { S, EXTERNAL, GLOBAL, FLOW, EDGES, LAYOUT, DEFAULT_STATE, START, FRAMES, SCREENS };')();
const unesc = (s) => s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");
const hits = {};
for (const [n, svg] of Object.entries(FRAMES)) hits[n] = new Set([...svg.matchAll(/data-hit="([^"]+)"/g)].map((m) => unesc(m[1])));
const scrOf = (n) => n.split('_')[0];
const screenHits = {};
for (const [n, hs] of Object.entries(hits)) { const k = scrOf(n); screenHits[k] = screenHits[k] || new Set(); hs.forEach((h) => screenHits[k].add(h)); }
const missing = (fr, test) => ![...hits[fr]].some(test) && ![...screenHits[scrOf(fr)]].some(test);
const errs = [];
const okTarget = (t) => t === null || t === 'BACK' || t === 'BACK_SCREEN' ||
  (typeof t === 'string' && (FRAMES[t] || (t.startsWith('X:') && EXTERNAL[t.slice(2)])));
for (const [fr, map] of Object.entries(FLOW)) {
  if (!FRAMES[fr]) { errs.push(`FLOW frame missing: ${fr}`); continue; }
  for (const [k, v] of Object.entries(map)) {
    if (k === 'auto') { if (!okTarget(v[1])) errs.push(`${fr} auto → bad target ${v[1]}`); continue; }
    if (k === 'down' || k === 'up') { if (!okTarget(v)) errs.push(`${fr} ${k} → bad target ${v}`); continue; }
    if (!okTarget(v)) errs.push(`${fr} [${k}] → bad target ${v}`);
    if (k.endsWith(':*')) { const p = k.slice(0, -1); if (missing(fr, (h) => h.startsWith(p))) errs.push(`${fr} wildcard key unused: ${k}`); }
    else if (missing(fr, (h) => h === k)) errs.push(`${fr} key not in screen: ${k}`);
  }
}
for (const [k, v] of Object.entries(GLOBAL)) if (!okTarget(v)) errs.push(`GLOBAL ${k} → bad target ${v}`);
for (const [a, b] of EDGES) for (const id of [a, b]) if (!SCREENS[id]) errs.push(`EDGE screen missing: ${id}`);
for (const r of LAYOUT) for (const id of r.screens) if (!SCREENS[id]) errs.push(`LAYOUT screen missing: ${id}`);
for (const [id, st] of Object.entries(DEFAULT_STATE)) if (!SCREENS[id] || !SCREENS[id].states.includes(st)) errs.push(`DEFAULT_STATE bad: ${id} ${st}`);
const inLayout = new Set(LAYOUT.flatMap((r) => r.screens));
for (const id of Object.keys(SCREENS)) if (!inLayout.has(id)) errs.push(`screen not in LAYOUT: ${id}`);
if (!FRAMES[START]) errs.push('START missing');
const resolve = (fr, k) => { const fl = FLOW[fr] || {}; if (k in fl) return fl[k]; const p = k.split(':')[0] + ':*'; if (p in fl) return fl[p]; return GLOBAL[k]; };
const dead = [];
for (const [fr, hs] of Object.entries(hits)) for (const k of hs) if (resolve(fr, k) === undefined && !['sheet', 'dialog'].includes(k)) dead.push(`${fr} ${k}`);
console.log(`frames ${Object.keys(FRAMES).length}, screens ${Object.keys(SCREENS).length}, flow frames ${Object.keys(FLOW).length}`);
console.log(errs.length ? 'ERRORS:\n' + errs.join('\n') : 'no errors');
console.log(`unwired hotspots: ${dead.length}`);
if (process.argv[3]) console.log(dead.join('\n'));
