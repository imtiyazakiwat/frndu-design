"""Frndu SVG frame library.

One canonical definition per component (design.md §13). Every screen frame is
composed from these functions so geometry stays identical across frames.
Coordinates follow design/LAYOUT-CONSTANTS.md (PROPOSED).
"""
import os
import re
from xml.sax.saxutils import escape as _esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- tokens
BLUE = '#5B7CFA'
CORAL = '#E94B4B'
CREAM = '#FFF4D6'
NAVY = '#10233F'
SLATE = '#66758A'
WHITE = '#FFFFFF'
BTINT = '#EAF0FF'
CTINT = '#FDE8E8'
CSURF = '#FFF9EA'
TERT = '#8794A5'
DIS_T = '#B8C0CB'
PLACE = '#9AA6B5'
BORDER = '#E2E7EF'
CBORDER = '#EEF1F5'
SKEL = '#E9EDF3'
DIS_BG = '#D8DDE5'
SUCCESS = '#21A366'
WARN = '#E6A21A'
ERROR = '#D9363E'
BLUE_PRESSED = '#5270E1'   # Blue darkened ~10% (design.md: pressed = darken 8-12%)

# name: (size, weight, line-height, letter-spacing, default colour)
STY = {
    'display': (36, 700, 44, -0.8, NAVY),
    'h1': (32, 700, 40, -0.6, NAVY),
    'h2': (26, 700, 34, -0.4, NAVY),
    'h3': (22, 700, 30, -0.2, NAVY),
    'h4': (18, 700, 26, 0, NAVY),
    'bodyL': (17, 400, 26, 0, SLATE),
    'body': (15, 400, 22, 0, SLATE),
    'bodyM': (15, 500, 22, 0, NAVY),
    'label': (14, 600, 20, 0, NAVY),
    'caption': (12, 500, 18, 0, SLATE),
    'button': (16, 700, 22, 0, WHITE),
    'notice': (13, 400, 19, 0, SLATE),
}

# Devanagari fallbacks so Hindi renders (Plus Jakarta Sans has no Devanagari glyphs; final font pairing = question for owner)
FONT = "'Plus Jakarta Sans', Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
DEVA_FONT = "'Noto Sans Devanagari', 'Kohinoor Devanagari', sans-serif"


def _ff(s):
    return f' font-family="{DEVA_FONT}"' if any('\u0900' <= c <= '\u097F' for c in str(s)) else ''


def esc(s):
    return _esc(str(s))


def hit(x, y, w, h, key):
    """Prototype hotspot: transparent rect tagged with data-hit (used by design/prototype)."""
    k = _esc(str(key), {'"': '&quot;'})
    return f'<rect class="hit" data-hit="{k}" x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF" fill-opacity="0"/>'


# ---------------------------------------------------------------- text metrics
def _cw(ch):
    if ch == ' ':
        return 0.28
    if ch in 'il.,:;|!\'’·':
        return 0.27
    if ch in 'fjrt()[]':
        return 0.36
    if ch in 'mwMW':
        return 0.86
    if ch.isdigit():
        return 0.58
    if ch.isupper():
        return 0.68
    if '\u0900' <= ch <= '\u097F':
        return 0.52
    if ord(ch) > 0x2000:
        return 0.9
    return 0.55


def tw(s, size, weight=400):
    f = 1.0 + (0.07 if weight >= 700 else 0.04 if weight >= 600 else 0.02 if weight >= 500 else 0)
    return sum(_cw(c) for c in s) * size * f


_TOK = re.compile(r'(\*\*.+?\*\*|\[\[.+?\]\])')


def _words(s):
    """Split rich text into (word, kind). **x** = emphasis, [[x]] = link."""
    out = []
    for seg in _TOK.split(s):
        if not seg:
            continue
        kind = 'n'
        if seg.startswith('**'):
            kind, seg = 'b', seg[2:-2]
        elif seg.startswith('[['):
            kind, seg = 'l', seg[2:-2]
        parts = seg.split(' ')
        for i, p in enumerate(parts):
            if p == '' and i not in (0, len(parts) - 1):
                continue
            out.append([p, kind, i < len(parts) - 1])  # trailing space flag
    # merge empties
    res = []
    for w, k, sp in out:
        if w == '':
            if res:
                res[-1][2] = True
            continue
        res.append([w, k, sp])
    return res


def wrap(s, maxw, size, weight=400):
    lines = []
    for para in s.split('\n'):
        words = _words(para)
        cur, curw = [], 0
        for w, k, sp in words:
            ww = tw(w, size, weight)
            spw = tw(' ', size, weight) if cur and cur[-1][2] else 0
            if cur and curw + spw + ww > maxw:
                lines.append(cur)
                cur, curw = [[w, k, sp]], ww
            else:
                cur.append([w, k, sp])
                curw += spw + ww
        lines.append(cur)
    return lines


def text(x, top, s, style='body', w=342, anchor='start', color=None, weight=None,
         em_color=NAVY, em_weight=None, link_color=BLUE, size=None, lh=None, opacity=None):
    """Rich text block. Returns (svg, bottom_y). Baselines from line-height box."""
    sz, wt, l_h, ls, col = STY[style]
    sz = size or sz
    l_h = lh or l_h
    wt = weight or wt
    col = color or col
    emw = em_weight or (500 if wt < 500 else 700 if wt >= 700 else 600)
    lines = wrap(s, w, sz, wt)
    out = []
    for i, line in enumerate(lines):
        base = top + i * l_h + (l_h - sz) / 2 + sz * 0.78
        spans = []
        for j, (word, kind, sp) in enumerate(line):
            t = esc(word) + (' ' if sp and j < len(line) - 1 else '')
            if kind == 'b':
                spans.append(f'<tspan fill="{em_color}" font-weight="{emw}">{t}</tspan>')
            elif kind == 'l':
                spans.append(f'<tspan fill="{link_color}" font-weight="600">{t}</tspan>')
            else:
                spans.append(t)
        lsa = f' letter-spacing="{ls}"' if ls else ''
        op = f' opacity="{opacity}"' if opacity is not None else ''
        out.append(f'<text x="{x}" y="{base:.1f}" text-anchor="{anchor}" font-size="{sz}" '
                   f'font-weight="{wt}" fill="{col}"{lsa}{op}{_ff(s)} xml:space="preserve">{"".join(spans)}</text>')
    return '\n'.join(out), top + len(lines) * l_h


def t1(x, base, s, size, weight, color, anchor='start', ls=0):
    """Single-line text at an explicit baseline."""
    lsa = f' letter-spacing="{ls}"' if ls else ''
    return (f'<text x="{x}" y="{base}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}"{lsa}{_ff(s)} xml:space="preserve">{esc(s)}</text>')


def nlines(s, style, w=342):
    sz, wt = STY[style][0], STY[style][1]
    return len(wrap(s, w, sz, wt))


# ---------------------------------------------------------------- icons (Lucide, 24 grid)
I = {
    'compass': ['<circle cx="12" cy="12" r="10"/>', '<path d="m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z"/>'],
    'plus': ['<path d="M5 12h14"/>', '<path d="M12 5v14"/>'],
    'minus': ['<path d="M5 12h14"/>'],
    'sliders-horizontal': ['<path d="M21 4h-7"/>', '<path d="M10 4H3"/>', '<path d="M21 12h-9"/>', '<path d="M8 12H3"/>', '<path d="M21 20h-5"/>', '<path d="M12 20H3"/>', '<path d="M14 2v4"/>', '<path d="M8 10v4"/>', '<path d="M16 18v4"/>'],
    'radar': ['<path d="M19.07 4.93A10 10 0 0 0 6.99 3.34"/>', '<path d="M4 6h.01"/>', '<path d="M2.29 9.62A10 10 0 1 0 21.31 8.35"/>', '<path d="M16.24 7.76A6 6 0 1 0 8.23 16.67"/>', '<path d="M12 18h.01"/>', '<path d="M17.99 11.66A6 6 0 0 1 15.77 16.67"/>', '<circle cx="12" cy="12" r="2"/>', '<path d="m13.41 10.59 5.66-5.66"/>'],
    'more-vertical': ['<circle cx="12" cy="12" r="1"/>', '<circle cx="12" cy="5" r="1"/>', '<circle cx="12" cy="19" r="1"/>'],
    'star': ['<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>'],
    'phone-off': ['<path d="M10.1 13.9a14 14 0 0 0 3.732 2.668 1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2 18 18 0 0 1-12.728-5.272"/>', '<path d="M22 2 2 22"/>', '<path d="M4.76 13.582A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 .244.473"/>'],
    'video-off': ['<path d="M10.66 6H14a2 2 0 0 1 2 2v2.5l5.248-3.062A.5.5 0 0 1 22 7.87v8.196"/>', '<path d="M16 16a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h2"/>', '<path d="m2 2 20 20"/>'],
    'mic-off': ['<path d="M12 19v3"/>', '<path d="M15 9.34V5a3 3 0 0 0-5.68-1.33"/>', '<path d="M16.95 16.95A7 7 0 0 1 5 12v-2"/>', '<path d="M18.89 13.23A7 7 0 0 0 19 12v-2"/>', '<path d="m2 2 20 20"/>', '<path d="M9 9v3a3 3 0 0 0 5.12 2.12"/>'],
    'volume-2': ['<path d="M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z"/>', '<path d="M16 9a5 5 0 0 1 0 6"/>', '<path d="M19.364 18.364a9 9 0 0 0 0-12.728"/>'],
    'bluetooth': ['<path d="m7 7 10 10-5 5V2l5 5L7 17"/>'],
    'headphones': ['<path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/>'],
    'send': ['<path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/>', '<path d="m21.854 2.147-10.94 10.939"/>'],
    'check-check': ['<path d="M18 6 7 17l-5-5"/>', '<path d="m22 10-7.5 7.5L13 16"/>'],
    'bell-off': ['<path d="M10.268 21a2 2 0 0 0 3.464 0"/>', '<path d="M17 17H4a1 1 0 0 1-.74-1.673C4.59 13.956 6 12.499 6 8a6 6 0 0 1 .258-1.742"/>', '<path d="m2 2 20 20"/>', '<path d="M8.668 3.01A6 6 0 0 1 18 8c0 2.687.77 4.653 1.707 6.05"/>'],
    'megaphone': ['<path d="m3 11 18-5v12L3 14v-3z"/>', '<path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>'],
    'receipt': ['<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/>', '<path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/>', '<path d="M12 17.5v-11"/>'],
    'user-x': ['<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>', '<circle cx="9" cy="7" r="4"/>', '<path d="m17 8 5 5"/>', '<path d="m22 8-5 5"/>'],
    'life-buoy': ['<circle cx="12" cy="12" r="10"/>', '<path d="m4.93 4.93 4.24 4.24"/>', '<path d="m14.83 9.17 4.24-4.24"/>', '<path d="m14.83 14.83 4.24 4.24"/>', '<path d="m9.17 14.83-4.24 4.24"/>', '<circle cx="12" cy="12" r="4"/>'],
    'shield-alert': ['<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>', '<path d="M12 8v4"/>', '<path d="M12 16h.01"/>'],
    'image-plus': ['<path d="M16 5h6"/>', '<path d="M19 2v6"/>', '<path d="M21 11.5V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7.5"/>', '<path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>', '<circle cx="9" cy="9" r="2"/>'],
    'user-plus': ['<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>', '<circle cx="9" cy="7" r="4"/>', '<path d="M19 8v6"/>', '<path d="M22 11h-6"/>'],
    'mail': ['<rect x="2" y="4" width="20" height="16" rx="2"/>', '<path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>'],
    'percent': ['<path d="M19 5 5 19"/>', '<circle cx="6.5" cy="6.5" r="2.5"/>', '<circle cx="17.5" cy="17.5" r="2.5"/>'],
    'landmark': ['<path d="M10 18v-7"/>', '<path d="M11.12 2.198a2 2 0 0 1 1.76.006l7.866 3.847c.476.233.31.949-.22.949H3.474c-.53 0-.695-.716-.22-.949z"/>', '<path d="M14 18v-7"/>', '<path d="M18 18v-7"/>', '<path d="M3 22h18"/>', '<path d="M6 18v-7"/>'],
    'smartphone': ['<rect x="5" y="2" width="14" height="20" rx="2"/>', '<path d="M12 18h.01"/>'],
    'eye-off': ['<path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"/>', '<path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"/>', '<path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"/>', '<path d="m2 2 20 20"/>'],
    'type': ['<path d="M12 4v16"/>', '<path d="M4 7V5a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2"/>', '<path d="M9 20h6"/>'],
    'copy': ['<rect x="8" y="8" width="14" height="14" rx="2"/>', '<path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>'],
    'pencil': ['<path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/>', '<path d="m15 5 4 4"/>'],
    'cloud-off': ['<path d="m2 2 20 20"/>', '<path d="M5.782 5.782A7 7 0 0 0 9 19h8.5a4.5 4.5 0 0 0 1.307-.193"/>', '<path d="M21.532 16.5A4.5 4.5 0 0 0 17.5 10h-1.79A7.008 7.008 0 0 0 10 5.07"/>'],
    'wrench': ['<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>'],
    'download': ['<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>', '<path d="m7 10 5 5 5-5"/>', '<path d="M12 15V3"/>'],
    'map-pin': ['<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/>', '<circle cx="12" cy="10" r="3"/>'],
    'fingerprint': ['<path d="M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4"/>', '<path d="M14 13.12c0 2.38 0 6.38-1 8.88"/>', '<path d="M17.29 21.02c.12-.6.43-2.3.5-3.02"/>', '<path d="M2 12a10 10 0 0 1 18-6"/>', '<path d="M2 16h.01"/>', '<path d="M21.8 16c.2-2 .131-5.354 0-6"/>', '<path d="M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2"/>', '<path d="M8.65 22c.21-.66.45-1.32.57-2"/>', '<path d="M9 6.8a6 6 0 0 1 9 5.2v2"/>'],
    'credit-card': ['<rect x="2" y="5" width="20" height="14" rx="2"/>', '<path d="M2 10h20"/>'],
    'circle-dot': ['<circle cx="12" cy="12" r="10"/>', '<circle cx="12" cy="12" r="1"/>'],
    'circle-help': ['<circle cx="12" cy="12" r="10"/>', '<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>', '<path d="M12 17h.01"/>'],
    'external-link': ['<path d="M15 3h6v6"/>', '<path d="M10 14 21 3"/>', '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'],
    'trash-2': ['<path d="M3 6h18"/>', '<path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>', '<path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>', '<path d="M10 11v6"/>', '<path d="M14 11v6"/>'],
    'flag': ['<path d="M4 22V4a1 1 0 0 1 .4-.8A6 6 0 0 1 8 2c3 0 5 2 7.333 2q2 0 3.067-.8A1 1 0 0 1 20 4v10a1 1 0 0 1-.4.8A6 6 0 0 1 16 16c-3 0-5-2-8-2a6 6 0 0 0-4 1.528"/>'],
    'hash': ['<path d="M4 9h16"/>', '<path d="M4 15h16"/>', '<path d="M10 3 8 21"/>', '<path d="M16 3l-2 18"/>'],
    'chevron-left': ['<path d="m15 18-6-6 6-6"/>'],
    'arrow-left': ['<path d="m12 19-7-7 7-7"/>', '<path d="M19 12H5"/>'],
    'crown': ['<path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z"/>', '<path d="M5 21h14"/>'],
    'shield': ['<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>'],
    'globe': ['<circle cx="12" cy="12" r="10"/>', '<path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>', '<path d="M2 12h20"/>'],
    'user-round': ['<circle cx="12" cy="8" r="5"/>', '<path d="M20 21a8 8 0 0 0-16 0"/>'],
    'chevron-right': ['<path d="m9 18 6-6-6-6"/>'],
    'chevron-down': ['<path d="m6 9 6 6 6-6"/>'],
    'chevron-up': ['<path d="m18 15-6-6-6 6"/>'],
    'x': ['<path d="M18 6 6 18"/>', '<path d="m6 6 12 12"/>'],
    'check': ['<path d="M20 6 9 17l-5-5"/>'],
    'languages': ['<path d="m5 8 6 6"/>', '<path d="m4 14 6-6 2-3"/>', '<path d="M2 5h12"/>', '<path d="M7 2h1"/>',
                  '<path d="m22 22-5-10-5 10"/>', '<path d="M14 18h6"/>'],
    'lock': ['<rect x="3" y="11" width="18" height="11" rx="2"/>', '<path d="M7 11V7a5 5 0 0 1 10 0v4"/>'],
    'alert-circle': ['<circle cx="12" cy="12" r="10"/>', '<path d="M12 8v4"/>', '<path d="M12 16h.01"/>'],
    'alert-triangle': ['<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/>',
                       '<path d="M12 9v4"/>', '<path d="M12 17h.01"/>'],
    'info': ['<circle cx="12" cy="12" r="10"/>', '<path d="M12 16v-4"/>', '<path d="M12 8h.01"/>'],
    'check-circle': ['<circle cx="12" cy="12" r="10"/>', '<path d="m9 12 2 2 4-4"/>'],
    'x-circle': ['<circle cx="12" cy="12" r="10"/>', '<path d="m15 9-6 6"/>', '<path d="m9 9 6 6"/>'],
    'calendar': ['<rect x="3" y="4" width="18" height="18" rx="2"/>', '<path d="M16 2v4"/>', '<path d="M8 2v4"/>',
                 '<path d="M3 10h18"/>'],
    'camera': ['<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/>',
               '<circle cx="12" cy="13" r="3"/>'],
    'mic': ['<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>', '<path d="M19 10v2a7 7 0 0 1-14 0v-2"/>',
            '<path d="M12 19v3"/>'],
    'bell': ['<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>', '<path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>'],
    'users': ['<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>', '<circle cx="9" cy="7" r="4"/>',
              '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/>', '<path d="M16 3.13a4 4 0 0 1 0 7.75"/>'],
    'badge-check': ['<path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/>',
                    '<path d="m9 12 2 2 4-4"/>'],
    'video': ['<path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5"/>',
              '<rect x="2" y="6" width="14" height="12" rx="2"/>'],
    'phone': ['<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>'],
    'search': ['<circle cx="11" cy="11" r="8"/>', '<path d="m21 21-4.3-4.3"/>'],
    'clock': ['<circle cx="12" cy="12" r="10"/>', '<path d="M12 6v6l4 2"/>'],
    'wifi-off': ['<path d="M12 20h.01"/>', '<path d="M8.5 16.429a5 5 0 0 1 7 0"/>', '<path d="M5 12.859a10 10 0 0 1 5.17-2.69"/>',
                 '<path d="M19 12.859a10 10 0 0 0-2.007-1.523"/>', '<path d="M2 8.82a15 15 0 0 1 4.177-2.643"/>',
                 '<path d="M22 8.82a15 15 0 0 0-11.288-3.764"/>', '<path d="m2 2 20 20"/>'],
    'wifi': ['<path d="M12 20h.01"/>', '<path d="M2 8.82a15 15 0 0 1 20 0"/>', '<path d="M5 12.859a10 10 0 0 1 14 0"/>',
             '<path d="M8.5 16.429a5 5 0 0 1 7 0"/>'],
    'layout-dashboard': ['<rect x="3" y="3" width="7" height="9" rx="1"/>', '<rect x="14" y="3" width="7" height="5" rx="1"/>',
                         '<rect x="14" y="12" width="7" height="9" rx="1"/>', '<rect x="3" y="16" width="7" height="5" rx="1"/>'],
    'message-circle': ['<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>'],
    'message-square': ['<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'],
    'wallet': ['<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/>',
               '<path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>'],
    'user': ['<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>', '<circle cx="12" cy="7" r="4"/>'],
    'gem': ['<path d="M6 3h12l4 6-10 13L2 9Z"/>', '<path d="M11 3 8 9l4 13 4-13-3-6"/>', '<path d="M2 9h20"/>'],
    'mars': ['<path d="M16 3h5v5"/>', '<path d="m21 3-6.75 6.75"/>', '<circle cx="10" cy="14" r="6"/>'],
    'venus': ['<path d="M12 15v7"/>', '<path d="M9 19h6"/>', '<circle cx="12" cy="9" r="6"/>'],
    'play': ['<path d="M6 3l14 9-14 9V3z"/>'],
    'pause': ['<rect x="14" y="4" width="4" height="16" rx="1"/>', '<rect x="6" y="4" width="4" height="16" rx="1"/>'],
    'trash': ['<path d="M3 6h18"/>', '<path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>', '<path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>'],
    'rotate-ccw': ['<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>', '<path d="M3 3v5h5"/>'],
    'image': ['<rect x="3" y="3" width="18" height="18" rx="2"/>', '<circle cx="9" cy="9" r="2"/>',
              '<path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>'],
    'shield-check': ['<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
                     '<path d="m9 12 2 2 4-4"/>'],
    'book-open': ['<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>', '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'],
    'coins': ['<circle cx="8" cy="8" r="6"/>', '<path d="M18.09 10.37A6 6 0 1 1 10.34 18"/>', '<path d="M7 6h1v4"/>',
              '<path d="m16.71 13.88.7.71-2.82 2.82"/>'],
    'heart': ['<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>'],
    'phone-call': ['<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
                   '<path d="M14.05 2a9 9 0 0 1 8 7.94"/>', '<path d="M14.05 6A5 5 0 0 1 18 10"/>'],
    'signal': ['<path d="M2 20h.01"/>', '<path d="M7 20v-4"/>', '<path d="M12 20v-8"/>', '<path d="M17 20V8"/>', '<path d="M22 4v16"/>'],
    'settings': ['<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>',
                 '<circle cx="12" cy="12" r="3"/>'],
    'arrow-left-right': ['<path d="M8 3 4 7l4 4"/>', '<path d="M4 7h16"/>', '<path d="m16 21 4-4-4-4"/>', '<path d="M20 17H4"/>'],
    'refresh-cw': ['<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>', '<path d="M21 3v5h-5"/>',
                   '<path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>', '<path d="M8 16H3v5"/>'],
    'upload': ['<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>', '<path d="m17 8-5-5-5 5"/>', '<path d="M12 3v12"/>'],
    'sun': ['<circle cx="12" cy="12" r="4"/>', '<path d="M12 2v2"/>', '<path d="M12 20v2"/>', '<path d="m4.93 4.93 1.41 1.41"/>',
            '<path d="m17.66 17.66 1.41 1.41"/>', '<path d="M2 12h2"/>', '<path d="M20 12h2"/>', '<path d="m6.34 17.66-1.41 1.41"/>',
            '<path d="m19.07 4.93-1.41 1.41"/>'],
    'scan-face': ['<path d="M3 7V5a2 2 0 0 1 2-2h2"/>', '<path d="M17 3h2a2 2 0 0 1 2 2v2"/>', '<path d="M21 17v2a2 2 0 0 1-2 2h-2"/>',
                  '<path d="M7 21H5a2 2 0 0 1-2-2v-2"/>', '<path d="M8 14s1.5 2 4 2 4-2 4-2"/>', '<path d="M9 9h.01"/>', '<path d="M15 9h.01"/>'],
    'log-out': ['<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>', '<path d="m16 17 5-5-5-5"/>', '<path d="M21 12H9"/>'],
    'file-text': ['<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>', '<path d="M14 2v4a2 2 0 0 0 2 2h4"/>',
                  '<path d="M10 9H8"/>', '<path d="M16 13H8"/>', '<path d="M16 17H8"/>'],
    'arrow-right': ['<path d="M5 12h14"/>', '<path d="m12 5 7 7-7 7"/>'],
    'smile': ['<circle cx="12" cy="12" r="10"/>', '<path d="M8 14s1.5 2 4 2 4-2 4-2"/>', '<path d="M9 9h.01"/>', '<path d="M15 9h.01"/>'],
    'delete': ['<path d="M10 5a2 2 0 0 0-1.344.519l-6.328 5.74a1 1 0 0 0 0 1.481l6.328 5.741A2 2 0 0 0 10 19h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2z"/>',
               '<path d="m12 9 6 6"/>', '<path d="m18 9-6 6"/>'],
    'crop': ['<path d="M6 2v14a2 2 0 0 0 2 2h14"/>', '<path d="M18 22V8a2 2 0 0 0-2-2H2"/>'],
    'circle': ['<circle cx="12" cy="12" r="10"/>'],
}


def icon(name, x, y, color=NAVY, size=24, sw=2):
    s = size / 24.0
    stroke = sw / s
    tr = f'translate({x} {y})' + (f' scale({s:.4f})' if s != 1 else '')
    return (f'<g transform="{tr}" fill="none" stroke="{color}" stroke-width="{stroke:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round">{"".join(I[name])}</g>')


def gem(x, y, size=20, color=BLUE):
    """Diamond glyph placeholder (Girish owns the final Diamond component)."""
    return '<!-- Diamond glyph: placeholder for shared Diamond component (owner: Girish) -->' + icon('gem', x, y, color, size)


# ---------------------------------------------------------------- frame chrome
def defs_block(extra=''):
    return (
        '<defs>\n'
        '<style>@import url(\'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;display=swap\');</style>\n'
        '<clipPath id="screen"><rect width="390" height="844"/></clipPath>\n'
        '<filter id="sh-card" x="-30%" y="-40%" width="160%" height="200%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#5B7CFA" flood-opacity="0.08"/></filter>\n'
        '<filter id="sh-lg" x="-20%" y="-30%" width="140%" height="160%"><feDropShadow dx="0" dy="-8" stdDeviation="24" flood-color="#10233F" flood-opacity="0.10"/></filter>\n'
        '<filter id="sh-sm" x="-30%" y="-50%" width="160%" height="220%"><feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#10233F" flood-opacity="0.06"/></filter>\n'
        '<filter id="gl-blue" x="-30%" y="-60%" width="160%" height="260%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#5B7CFA" flood-opacity="0.32"/></filter>\n'
        '<filter id="gl-coral" x="-30%" y="-60%" width="160%" height="260%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#E94B4B" flood-opacity="0.30"/></filter>\n'
        '<filter id="gl-red" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#D9363E" flood-opacity="0.30"/></filter>\n'
        '<filter id="blur-xl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="28"/></filter>\n'
        '<filter id="blur-md" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>\n'
        '<linearGradient id="g-glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.82"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0.56"/></linearGradient>\n'
        '<linearGradient id="g-edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="1"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0.35"/></linearGradient>\n'
        '<linearGradient id="g-blue" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5B7CFA" stop-opacity="0.82"/><stop offset="1" stop-color="#5B7CFA"/></linearGradient>\n'
        '<linearGradient id="g-coral" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E94B4B" stop-opacity="0.84"/><stop offset="1" stop-color="#E94B4B"/></linearGradient>\n'
        '<linearGradient id="g-fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF4D6" stop-opacity="0"/><stop offset="0.55" stop-color="#FFF4D6" stop-opacity="0.85"/><stop offset="1" stop-color="#FFF4D6" stop-opacity="0.95"/></linearGradient>\n'
        '<radialGradient id="g-halo"><stop offset="0" stop-color="#5B7CFA" stop-opacity="0.20"/><stop offset="1" stop-color="#5B7CFA" stop-opacity="0"/></radialGradient>\n'
        f'{extra}</defs>')


def status_bar(color=NAVY, low_power=False):
    batt = WARN if low_power else color
    return (f'<!-- Status bar (safe area 0-47) -->\n'
            f'<text x="40" y="32" font-size="15" font-weight="600" fill="{color}">9:41</text>\n'
            f'<g fill="{color}"><rect x="290" y="24" width="3" height="6" rx="1"/><rect x="295" y="21" width="3" height="9" rx="1"/>'
            f'<rect x="300" y="18" width="3" height="12" rx="1"/><rect x="305" y="15" width="3" height="15" rx="1"/>'
            f'<path d="M314 20 a10 10 0 0 1 14 0 l-2 2 a7 7 0 0 0 -10 0 Z M318 24 a4.5 4.5 0 0 1 6 0 l-3 3 Z"/>'
            f'<rect x="334" y="17" width="22" height="12" rx="3" fill="none" stroke="{color}" stroke-width="1.2"/>'
            f'<rect x="336" y="19" width="16" height="8" rx="1.5" fill="{batt}"/>'
            f'<rect x="357.5" y="21" width="1.6" height="4" rx="0.8"/></g>')


def home_indicator(color=NAVY):
    return f'<rect x="128" y="826" width="134" height="5" rx="2.5" fill="{color}"/>'


def blobs(top=True, bottom=True):
    """Frndu background: soft blurred colour clouds (Blue top-right, Coral bottom-left) with a fine highlight arc.
    Built from design.md tokens at low opacity, blurred, so they dissolve into Cream.
    Theme rule (11 Oct): every Cream screen shows both clouds, so the flags are ignored."""
    top = bottom = True
    out = ['<!-- Background clouds (decorative): blurred Blue top-right, Coral bottom-left -->']
    if top:
        out.append('<g filter="url(#blur-xl)"><path d="M210 -40 C200 40 240 96 286 120 C330 142 336 210 380 250 L460 260 L460 -40 Z" fill="#5B7CFA" opacity="0.30"/>'
                   '<ellipse cx="372" cy="70" rx="90" ry="110" fill="#5B7CFA" opacity="0.18"/></g>'
                   '<path d="M300 -10 C292 70 330 150 400 196" fill="none" stroke="#FFFFFF" stroke-opacity="0.75" stroke-width="1.5"/>')
    if bottom:
        out.append('<g filter="url(#blur-xl)"><path d="M-60 560 C20 560 80 620 110 690 C130 740 170 800 200 900 L-60 900 Z" fill="#E94B4B" opacity="0.20"/>'
                   '<ellipse cx="0" cy="760" rx="110" ry="120" fill="#E94B4B" opacity="0.10"/></g>'
                   '<path d="M-10 640 C60 660 100 720 112 800" fill="none" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="1.5"/>')
    return '\n'.join(out)


def logo(cx, cy, size, cut=CREAM, sparks_on=False):
    """Frndu mark (two smiling speech bubbles). Drawn in illus.logo_mark; `size` = mark width."""
    from illus import logo_mark
    return logo_mark(cx, cy, size, sparks_on=sparks_on)


def progress(step, total=6):
    """Step indicator centred in the top bar (PROPOSED new component from the reference)."""
    w, g = 20, 6
    x0 = 195 - (total * w + (total - 1) * g) / 2
    out = [f'<!-- Step progress {step}/{total} -->']
    for i in range(total):
        out.append(f'<rect x="{x0 + i * (w + g):.0f}" y="73" width="{w}" height="5" rx="2.5" fill="{BLUE if i + 1 == step else DIS_BG}"/>')
    return ''.join(out)


def radio(cx, cy, on):
    return (f'<circle cx="{cx}" cy="{cy}" r="11" fill="{WHITE}" fill-opacity="0.85" stroke="{BLUE if on else DIS_T}" stroke-width="2"/>'
            + (f'<circle cx="{cx}" cy="{cy}" r="6" fill="{BLUE}"/>' if on else ''))


def option_card(y, title, desc, icon_svg, state='unselected', key=None, h=72, pill=None, tint=False):
    """List option card with icon circle + radio (reference style). state: selected / unselected / disabled."""
    sel = state == 'selected'
    out = [f'<!-- Option card "{title}" ({state}) -->',
           (f'<rect x="24.75" y="{y + 0.75}" width="340.5" height="{h - 1.5}" rx="20" fill="{BTINT}" fill-opacity="0.9" stroke="{BLUE}" stroke-width="1.5" filter="url(#sh-card)"/>'
            if sel else glass(24, y, 342, h, 20, shadow=state != 'disabled', op=0.4 if state == 'disabled' else None)),
           f'<g transform="translate(0 {(h - 56) / 2})">{icon_svg(40, y).replace(f'fill="{BTINT}"', f'fill="{WHITE}"', 1) if sel else icon_svg(40, y)}</g>']
    tx = 112
    tcol = DIS_T if state == 'disabled' else NAVY
    n = len(wrap(desc, 200, 13, 400)) if desc else 0
    block = 24 + (n * 19 if desc else 0)
    ty = y + (h - block) / 2
    out.append(t1(tx, ty + 18, title, 16, 700, tcol))
    if pill:
        pw = tw(pill, 11, 600) + 16
        px = tx + tw(title, 16, 700) + 8
        out.append(f'<rect x="{px:.0f}" y="{ty + 3:.0f}" width="{pw:.0f}" height="20" rx="10" fill="{WHITE if sel else BTINT}" stroke="{BTINT}"/>'
                   + t1(f'{px + pw / 2:.0f}', ty + 17, pill, 11, 600, BLUE, 'middle'))
    if desc:
        out.append(text(tx, ty + 26, desc, 'notice', w=200, color=SLATE if state != 'disabled' else DIS_T)[0])
    if state != 'disabled':
        out.append(radio(342, y + h / 2, sel))
        out.append(hit(24, y, 342, h, key or f'card:{title}'))
    return '\n'.join(out)


def icon_circle(name, bg=BTINT, color=BLUE, d=56):
    """Factory for option_card icons: tint circle + Lucide icon."""
    def f(x, y):
        return f'<circle cx="{x + d / 2}" cy="{y + d / 2}" r="{d / 2}" fill="{bg}"/>' + icon(name, x + d / 2 - 12, y + d / 2 - 12, color)
    return f


def face_circle(who, bg, d=56):
    def f(x, y):
        from illus import portrait
        return portrait(x + d / 2, y + d / 2, d / 2, who, bg)
    return f


def topbar(kind='back', title=None, right=None, nav_back=None, nav_right=None, color=NAVY, tab_title=None, step=None):
    """TopBar (owner: Girish; placeholder per LAYOUT-CONSTANTS §3). y 47-103."""
    out = ['<!-- TopBar (shared component, owner: Girish) y 47-103 -->']
    if kind in ('back', 'close'):
        nm = 'arrow-left' if kind == 'back' else 'x'
        out.append(f'<!-- {"Back" if kind == "back" else "Close"} button → {nav_back or "previous"} -->')
        out.append(glass(14, 53, 44, 44, 22, shadow=True) if color == NAVY else f'<circle cx="36" cy="75" r="22" fill="{WHITE}" opacity="0.18"/>')
        out.append(icon(nm, 24, 63, color))
        out.append(hit(12, 51, 48, 48, kind))
    if step:
        out.append(progress(step))
    if title:
        out.append(t1(195, 81, title, 18, 700, color, 'middle'))
    if tab_title:
        out.append(t1(24, 86, tab_title, 26, 700, color, ls=-0.4))
    if right:
        out.append(f'<!-- Right action ({right}) → {nav_right} -->')
        out.append(glass(332, 53, 44, 44, 22, shadow=True) if color == NAVY else f'<circle cx="354" cy="75" r="22" fill="{WHITE}" opacity="0.18"/>')
        out.append(icon(right, 342, 63, color))
        out.append(hit(330, 51, 48, 48, f'right:{right}'))
    return '\n'.join(out)


# ---------------------------------------------------------------- controls
def spinner(cx, cy, color=WHITE, r=9):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-opacity="0.35" stroke-width="2.4"/>'
            f'<path d="M{cx} {cy - r} a{r} {r} 0 0 1 {r} {r}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>')


def button(y, label, kind='primary', x=24, w=342, nav=None, h=56, icon_right=None, icon_left=None):
    """Button (Primary / Coral / Secondary / Ghost / Destructive) H56 r16, label 16/700."""
    cx = x + w / 2
    fill, txt, stroke = BLUE, WHITE, None
    loading = kind.endswith('loading')
    base = kind.replace('-loading', '')
    if base == 'primary':
        fill, txt = BLUE, WHITE
    elif base == 'pressed':
        fill, txt = BLUE_PRESSED, WHITE
    elif base == 'coral':
        fill, txt = CORAL, WHITE
    elif base == 'disabled':
        fill, txt = DIS_BG, WHITE
    elif base == 'destructive':
        fill, txt = ERROR, WHITE
    elif base == 'secondary':
        fill, txt, stroke = WHITE, BLUE, BORDER
    elif base == 'secondary-disabled':
        fill, txt, stroke = WHITE, DIS_T, BORDER
    elif base == 'ghost':
        fill, txt = None, BLUE
    elif base == 'ghost-disabled':
        fill, txt = None, DIS_T
    elif base == 'ghost-white':
        fill, txt = None, WHITE
    out = [f'<!-- Button {base}{" loading" if loading else ""}: "{label}"' + (f' → {nav}' if nav else '') + ' -->']
    r = h / 2  # pill (radius 999)
    if base in ('secondary', 'secondary-disabled'):
        out.append(glass(x, y, w, h, r, shadow=True))
    elif fill:
        grad = {BLUE: 'url(#g-blue)', CORAL: 'url(#g-coral)'}.get(fill, fill)
        glow = {BLUE: ' filter="url(#gl-blue)"', CORAL: ' filter="url(#gl-coral)"', ERROR: ' filter="url(#gl-red)"',
                BLUE_PRESSED: ''}.get(fill, '')
        if base == 'disabled':
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{DIS_BG}"/>')
        else:
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{grad}"{glow}/>'
                       f'<rect x="{x + 1}" y="{y + 1}" width="{w - 2}" height="{h / 2}" rx="{r - 1}" fill="{WHITE}" opacity="0.10"/>')
    else:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#FFFFFF" fill-opacity="0"/>')
    if loading:
        out.append(spinner(cx, y + h / 2, txt if fill in (None, WHITE) else WHITE))
    else:
        if icon_right:
            lw = tw(label, 16, 700)
            lx = cx - (lw + 28) / 2
            out.append(t1(f'{lx:.1f}', y + 34, label, 16, 700, txt))
            out.append(icon(icon_right, round(lx + lw + 8, 1), y + 18, txt, 20))
        elif icon_left:
            lw = tw(label, 16, 700)
            lx = cx - (lw + 28) / 2
            out.append(icon(icon_left, round(lx, 1), y + 18, txt, 20))
            out.append(t1(f'{lx + 28:.1f}', y + 34, label, 16, 700, txt))
        else:
            out.append(t1(cx, y + 34, label, 16, 700, txt, 'middle'))
    if not loading and 'disabled' not in base:
        out.append(hit(x, y, w, h, f'btn:{label}'))
    return '\n'.join(out)


def link_row(y, label, nav=None, x=195, color=BLUE):
    """Text link with a 44 high touch row."""
    return (f'<!-- Link "{label}"' + (f' → {nav}' if nav else '') + ' -->\n'
            f'<rect x="24" y="{y}" width="342" height="44" fill="#FFFFFF" fill-opacity="0"/>'
            + t1(x, y + 27, label, 14, 600, color, 'middle') + hit(24, y, 342, 44, f'link:{label}'))


def action_area(items, bottom=794, cover=None):
    """Bottom action area. items top→bottom: ('btn',label,kind,nav) | ('link',label,nav) |
    ('legal', richtext) | ('note', richtext, style, color) | ('progress', label, pct).
    Returns (svg, top_y)."""
    out = []
    y = bottom
    placed = []
    for it in reversed(items):
        k = it[0]
        if k == 'btn':
            y -= 56
            placed.append(button(y, it[1], it[2], nav=it[3] if len(it) > 3 else None))
            y -= 12
        elif k == 'link':
            y -= 44
            placed.append(link_row(y, it[1], it[2] if len(it) > 2 else None))
            y -= 12
        elif k in ('legal', 'note'):
            style = it[2] if len(it) > 2 else 'notice'
            col = it[3] if len(it) > 3 else None
            n = nlines(it[1], style)
            lh = STY[style][2]
            y -= n * lh
            svg, _ = text(195, y, it[1], style, anchor='middle', color=col)
            placed.append(svg)
            y -= 12
        elif k == 'progress':
            # label + bar (upload progress)
            y -= 8
            pct = it[2]
            placed.append(f'<rect x="24" y="{y}" width="342" height="8" rx="4" fill="{BORDER}"/>'
                          f'<rect x="24" y="{y}" width="{342 * pct / 100:.0f}" height="8" rx="4" fill="{BLUE}"/>')
            y -= 8
            y -= 20
            placed.append(t1(195, y + 15, it[1], 14, 600, NAVY, 'middle'))
            y -= 12
    top = y + 12
    if cover:
        out.append(f'<rect x="0" y="{top - 24}" width="390" height="{844 - top + 24}" fill="{cover}"/>')
    out.append('<!-- Bottom action area -->')
    out.extend(reversed(placed))
    return '\n'.join(out), top


def err_msg(x, y, s, w=342, color=ERROR, icon_name='alert-circle', style='notice', weight=500):
    """Inline message: icon 20 + Notice text (never colour alone)."""
    svg, bottom = text(x + 28, y, s, style, w=w - 28, color=color, weight=weight)
    return icon(icon_name, x, y - 1 + 0.5, color, 20) + svg, bottom


def banner(y, s, variant='info', x=24, w=342, icon_name=None, action=None):
    """PersistentBanner. Returns (svg, bottom)."""
    bg, ic, icn = {
        'info': (BTINT, BLUE, 'info'),
        'offline': (BTINT, BLUE, 'wifi-off'),
        'warning': (CTINT, WARN, 'alert-triangle'),
        'error': (CTINT, ERROR, 'alert-circle'),
        'success': (BTINT, SUCCESS, 'check-circle'),
        'clock': (BTINT, BLUE, 'clock'),
        'lock': (CTINT, NAVY, 'lock'),
        'reason': (CTINT, NAVY, 'info'),
    }[variant]
    icn = icon_name or icn
    aw = tw(action, 14, 600) + 12 if action else 0
    tw_ = w - 16 - 20 - 12 - 16 - aw
    n = nlines(s, 'notice', tw_)
    h = max(44, n * 19 + 24)
    out = [f'<!-- PersistentBanner ({variant}) -->',
           glass(x, y, w, h, 16, shadow=False), f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" opacity="0.7"/>',
           icon(icn, x + 16, y + (h - 20) / 2, ic, 20)]
    svg, _ = text(x + 48, y + (h - n * 19) / 2, s, 'notice', w=tw_, color=NAVY)
    out.append(svg)
    if action:
        out.append(f'<!-- Banner action "{action}" -->' + t1(x + w - 16, y + h / 2 + 5, action, 14, 600, BLUE, 'end'))
    return '\n'.join(out), y + h


def offline_banner(y):
    return banner(y, "You're offline. Check your connection and try again.", 'offline')


def glass(x, y, w, h, r=20, shadow=True, op=None, edge=True):
    """Frosted surface: White gradient (82% → 56%) + bright 1.2 px edge + soft Blue-tinted shadow."""
    f = ' filter="url(#sh-card)"' if shadow else ''
    fill = f'fill="{WHITE}" fill-opacity="{op}"' if op is not None else 'fill="url(#g-glass)"'
    st = ' stroke="url(#g-edge)" stroke-width="1.2"' if edge else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" {fill}{st}{f}/>'


def card(x, y, w, h, r=20, fill=WHITE, stroke=CBORDER, shadow=True, sw=1):
    """Card. White cards are frosted glass so they melt into the background; other fills stay solid."""
    if fill == WHITE:
        return glass(x, y, w, h, max(r, 20), shadow)
    f = ' filter="url(#sh-card)"' if shadow else ''
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st}{f}/>'


def check_badge(x, y):
    """Selected badge 24: Blue circle, white check."""
    return f'<circle cx="{x + 12}" cy="{y + 12}" r="12" fill="{BLUE}"/>' + icon('check', x + 5, y + 5, WHITE, 14, 2)


def icon_box(x, y, name, size=48, bg=BTINT, color=BLUE, isz=24, r=12):
    off = (size - isz) / 2
    return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r}" fill="{bg}"/>' + icon(name, x + off, y + off, color, isz)


def chip(x, y, label, state='unselected', h=40):
    w = tw(label, 14, 600) + 32
    fill, txt, op = {'selected': (BLUE, WHITE, None), 'unselected': (WHITE, NAVY, None),
                     'disabled': (WHITE, DIS_T, None), 'pressed': (BLUE_PRESSED, WHITE, None),
                     'readonly': (BTINT, NAVY, None)}[state]
    if state in ('unselected', 'disabled'):
        bg = glass(x, y, round(w), h, h / 2, shadow=False)
    elif state == 'selected':
        bg = f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="url(#g-blue)" filter="url(#gl-blue)"/>'
    else:
        bg = f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{fill}"/>'
    return (bg
            + t1(f'{x + w / 2:.1f}', y + h / 2 + 5, label, 14, 600, txt, 'middle')
            + (hit(x, y, round(w), h, f'chip:{label}') if state != 'disabled' else '')), round(w)


def chips_wrap(x, y, items, maxw=342, gap=8, rowgap=8, h=40):
    """items: list of (label, state). Returns (svg, bottom)."""
    out = []
    cx, cy = x, y
    for label, st in items:
        w = tw(label, 14, 600) + 32
        if cx > x and cx + w > x + maxw:
            cx = x
            cy += h + rowgap
        svg, ww = chip(round(cx), cy, label, st, h)
        out.append(svg)
        cx += ww + gap
    return '\n'.join(out), cy + h


def skeleton(x, y, w, h, r=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{SKEL}"/>'


# ---------------------------------------------------------------- photos (hosted on the Vercel deploy, /img/)
PHOTO_BASE = 'https://frndu-prototype.vercel.app/img/'


def photo_img(x, y, w, h, file, pos='xMidYMid'):
    """Real placeholder photo (cropped from design/_refs, source in design/_assets/photos). Covers the box (slice)."""
    return (f'<image href="{PHOTO_BASE}{file}" x="{x}" y="{y}" width="{w}" height="{h}" '
            f'preserveAspectRatio="{pos} slice"/>')


def avatar(cx, cy, d, letter=None, photo=False, ring=None, img=None):
    """Avatar 40/48/56/72. Fallback = Blue Tint circle + initial. photo=True (or img=file) shows a real photo."""
    r = d / 2
    out = []
    if photo or img:
        cid = f'av{int(cx)}{int(cy)}{d}'
        out.append(f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>')
        out.append(f'<g clip-path="url(#{cid})"><rect x="{cx - r}" y="{cy - r}" width="{d}" height="{d}" fill="{CTINT}"/>'
                   + photo_img(cx - r, cy - r, d, d, img or 'priya.jpg', 'xMidYMin') + '</g>'
                   f'<circle cx="{cx}" cy="{cy}" r="{r - 0.75}" fill="none" stroke="{WHITE}" stroke-width="1.5"/>')
    else:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BTINT}"/><circle cx="{cx}" cy="{cy}" r="{r - 0.6}" fill="url(#g-glass)" stroke="{WHITE}" stroke-width="1.2" filter="url(#sh-sm)"/>')
        if letter:
            fs = {40: 16, 48: 18, 56: 22, 72: 26}.get(d, 18)
            out.append(t1(cx, round(cy + fs * 0.36, 1), letter, fs, 700, BLUE, 'middle'))
        else:
            out.append(icon('user', cx - d * 0.25, cy - d * 0.25, BLUE, d * 0.5))
    if ring:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ring}" stroke-width="2"/>')
    return '\n'.join(out)


def switch(x, y, on, color=BLUE, large=False, disabled=False, key='switch'):
    w, h = (64, 36) if large else (52, 32)
    k = h - 6
    fill = color if on else DIS_BG
    kx = x + w - 3 - k if on else x + 3
    op = ' opacity="0.45"' if disabled else ''
    return (f'<!-- Switch {"on" if on else "off"}{" disabled" if disabled else ""} -->'
            f'<g{op}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{fill}"/>'
            f'<circle cx="{kx + k / 2}" cy="{y + h / 2}" r="{k / 2}" fill="{WHITE}" filter="url(#sh-sm)"/></g>'
            + ('' if disabled else hit(x - 4, y + h / 2 - 22, w + 8, 44, key)))


def checkbox(x, y, checked=False, disabled=False, highlight=False):
    out = ['<!-- Checkbox 24 in 48x48 touch area -->',
           f'<rect x="{x - 12}" y="{y - 12}" width="48" height="48" rx="12" fill="{BTINT if highlight else "#FFFFFF"}" fill-opacity="{1 if highlight else 0}"/>']
    if checked:
        out.append(f'<rect x="{x}" y="{y}" width="24" height="24" rx="8" fill="{BLUE}"/>' + icon('check', x + 4, y + 4, WHITE, 16, 2))
    else:
        out.append(f'<rect x="{x + 0.75}" y="{y + 0.75}" width="22.5" height="22.5" rx="8" fill="{SKEL if disabled else WHITE}" stroke="{DIS_BG if disabled else PLACE}" stroke-width="1.5"/>')
        if disabled:
            out.append(icon('lock', x + 6, y + 6, TERT, 12, 2))
    if not disabled:
        out.append(hit(x - 12, y - 12, 48, 48, 'checkbox'))
    return '\n'.join(out)


def slider(x, y, w, pct, locked=False):
    """Slider: track #E2E7EF 4px, fill Blue, thumb 24 white with 2px Blue border. y = thumb centre."""
    fx = x + w * pct
    fill = DIS_BG if locked else BLUE
    return (f'<!-- Slider{" locked" if locked else ""} -->'
            f'<rect x="{x}" y="{y - 2}" width="{w}" height="4" rx="2" fill="{BORDER}"/>'
            f'<rect x="{x}" y="{y - 2}" width="{fx - x:.0f}" height="4" rx="2" fill="{fill}"/>'
            f'<circle cx="{fx:.0f}" cy="{y}" r="11" fill="{WHITE}" stroke="{fill}" stroke-width="2" filter="url(#sh-sm)"/>')


def input_box(y, value=None, placeholder=None, state='empty', x=24, w=342, h=56, left_pad=16,
              right_icon=None, left_icon=None, caret=None, prefix=None, multiline=False, text_color=NAVY):
    """Input H56 r16 White, border 1px #E2E7EF; focused 2px Blue; error border Error."""
    stroke, sw, fill = BORDER, 1, WHITE
    if state == 'focused':
        stroke, sw = BLUE, 2
    elif state == 'error':
        stroke, sw = ERROR, 2
    elif state == 'disabled':
        fill = CBORDER
    off = sw / 2
    r = 20 if multiline else min(h / 2, 28)
    out = [f'<!-- Input ({state}) -->']
    if state == 'disabled':
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{WHITE}" fill-opacity="0.35" stroke="{WHITE}" stroke-opacity="0.6"/>')
    else:
        out.append(glass(x, y, w, h, r, shadow=state == 'empty'))
        if state in ('focused', 'error'):
            out.append(f'<rect x="{x + off}" y="{y + off}" width="{w - sw}" height="{h - sw}" rx="{r}" fill="none" stroke="{stroke}" stroke-width="{sw}"/>')
    tx = x + left_pad
    if prefix:
        out.append(prefix)
    if left_icon:
        out.append(icon(left_icon, x + 16, y + (h - 20) / 2 if not multiline else y + 16, SLATE, 20))
        tx = x + 48
    base = y + h / 2 + 6 if not multiline else y + 30
    tcol = DIS_T if state == 'disabled' else text_color
    if value:
        if multiline:
            svg, _ = text(tx, y + 14, value, 'bodyM', w=w - (tx - x) - 16, color=tcol, size=16, lh=24)
            out.append(svg)
        else:
            out.append(t1(tx, base, value, 16, 500, tcol))
    elif placeholder:
        if multiline:
            svg, _ = text(tx, y + 14, placeholder, 'body', w=w - (tx - x) - 16, color=PLACE, size=16, lh=24)
            out.append(svg)
        else:
            out.append(t1(tx, base, placeholder, 16, 400, PLACE))
    if state == 'focused' and caret is not False:
        cx = tx + (tw(value, 16, 500) + 2 if value and not multiline else 0)
        cy = y + h / 2 - 11 if not multiline else y + 16
        out.append(f'<rect x="{cx:.1f}" y="{cy}" width="2" height="22" rx="1" fill="{BLUE}"/>')
    if right_icon:
        out.append(icon(right_icon, x + w - 16 - 20, y + (h - 20) / 2, SLATE, 20))
    if state != 'disabled':
        out.append(hit(x, y, w, h, f'input:{placeholder or value or ""}'))
    return '\n'.join(out)


def flag_in(x, y):
    """India flag image asset (content imagery, not UI colour)."""
    return (f'<!-- Country flag image asset (IN) -->'
            f'<g><clipPath id="fl{x}{y}"><rect x="{x}" y="{y}" width="24" height="16" rx="3"/></clipPath>'
            f'<g clip-path="url(#fl{x}{y})"><rect x="{x}" y="{y}" width="24" height="5.34" fill="#FF9933"/>'
            f'<rect x="{x}" y="{y + 5.33}" width="24" height="5.34" fill="#FFFFFF"/>'
            f'<rect x="{x}" y="{y + 10.66}" width="24" height="5.34" fill="#138808"/>'
            f'<circle cx="{x + 12}" cy="{y + 8}" r="2" fill="none" stroke="#000080" stroke-width="0.8"/></g>'
            f'<rect x="{x + 0.25}" y="{y + 0.25}" width="23.5" height="15.5" rx="3" fill="none" stroke="{BORDER}" stroke-width="0.5"/></g>')


def flag_placeholder(x, y, code):
    return (f'<!-- Country flag image asset ({code}) -->'
            f'<rect x="{x}" y="{y}" width="24" height="16" rx="3" fill="{SKEL}"/>'
            + t1(x + 12, y + 11.5, code, 8, 700, SLATE, 'middle'))


def phone_input(y, value=None, state='empty'):
    prefix = (flag_in(36, y + 20) + t1(68, y + 34, '+91', 15, 500, NAVY)
              + icon('chevron-down', 96, y + 18, SLATE, 20)
              + f'<rect x="128" y="{y + 14}" width="1" height="28" fill="{BORDER}"/>'
              + '<!-- Country segment → country picker sheet (state of 02) -->')
    return input_box(y, value, '98765 43210', state, left_pad=116, prefix=prefix) + hit(24, y, 108, 56, 'country')


def otp_boxes(y, digits='', state='empty', focus=None):
    """6 OTP boxes 50x56 r14 gap 8, total 340, centred (x 25..365)."""
    out = ['<!-- OTP field: 6 boxes 50x56 r14 gap 8 -->']
    for i in range(6):
        x = 25 + i * 58
        d = digits[i] if i < len(digits) else ''
        st, sw, fill = BORDER, 1, WHITE
        if state == 'error':
            st, sw = ERROR, 2
        elif state == 'disabled':
            fill = CBORDER
        elif focus == i:
            st, sw = BLUE, 2
        off = sw / 2
        out.append(glass(x, y, 50, 56, 14, shadow=False) if fill == WHITE else f'<rect x="{x}" y="{y}" width="50" height="56" rx="14" fill="{fill}"/>')
        if st != BORDER:
            out.append(f'<rect x="{x + off}" y="{y + off}" width="{50 - sw}" height="{56 - sw}" rx="14" fill="none" stroke="{st}" stroke-width="{sw}"/>')
        if d:
            out.append(t1(x + 25, y + 36, d, 22, 700, DIS_T if state == 'disabled' else NAVY, 'middle'))
        elif focus == i and state not in ('error', 'disabled'):
            out.append(f'<rect x="{x + 24}" y="{y + 17}" width="2" height="22" rx="1" fill="{BLUE}"/>')
    if state != 'disabled':
        out.append(hit(25, y, 340, 56, 'otp'))
    return '\n'.join(out)


def keyboard(kind='numeric'):
    """System keyboard (not designed; neutral tokens). Top y=553."""
    top = 553
    out = ['<!-- System keyboard (OS-provided, drawn for layout only) -->',
           f'<rect x="0" y="{top}" width="390" height="{844 - top}" fill="{SKEL}"/>', hit(0, top, 390, 844 - top, 'keyboard')]
    if kind == 'numeric':
        keys = [('1', ''), ('2', 'ABC'), ('3', 'DEF'), ('4', 'GHI'), ('5', 'JKL'), ('6', 'MNO'),
                ('7', 'PQRS'), ('8', 'TUV'), ('9', 'WXYZ'), ('', ''), ('0', ''), ('del', '')]
        kw, kh, g = 120, 48, 7
        for i, (k, sub) in enumerate(keys):
            r, c = divmod(i, 3)
            x = 6 + c * (kw + g)
            y = top + 8 + r * (kh + g)
            if k == '':
                continue
            if k == 'del':
                out.append(icon('delete', x + kw / 2 - 12, y + 12, NAVY))
                continue
            out.append(f'<rect x="{x}" y="{y}" width="{kw}" height="{kh}" rx="8" fill="{WHITE}"/>')
            out.append(t1(x + kw / 2, y + (28 if sub else 32), k, 24, 400, NAVY, 'middle'))
            if sub:
                out.append(t1(x + kw / 2, y + 42, sub, 9, 600, NAVY, 'middle', ls=1.5))
    else:
        rows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
        kw, kh = 33, 44
        for ri, row in enumerate(rows):
            n = len(row)
            total = n * kw + (n - 1) * 6
            x0 = (390 - total) / 2
            y = top + 10 + ri * 54
            for ci, ch in enumerate(row):
                x = x0 + ci * (kw + 6)
                out.append(f'<rect x="{x:.1f}" y="{y}" width="{kw}" height="{kh}" rx="8" fill="{WHITE}"/>')
                out.append(t1(f'{x + kw / 2:.1f}', y + 29, ch, 20, 400, NAVY, 'middle'))
        y = top + 10 + 3 * 54
        out.append(f'<rect x="6" y="{y}" width="88" height="44" rx="8" fill="{DIS_BG}"/>' + t1(50, y + 28, '123', 16, 400, NAVY, 'middle'))
        out.append(f'<rect x="100" y="{y}" width="190" height="44" rx="8" fill="{WHITE}"/>' + t1(195, y + 28, 'space', 16, 400, NAVY, 'middle'))
        out.append(f'<rect x="296" y="{y}" width="88" height="44" rx="8" fill="{BLUE}"/>' + t1(340, y + 28, 'done', 16, 600, WHITE, 'middle'))
    return '\n'.join(out)


KB_TOP = 553


def scrim(op=0.4):
    return f'<!-- Scrim -->\n<rect x="0" y="0" width="390" height="844" fill="{NAVY}" opacity="{op * 0.8:.2f}"/>' + hit(0, 0, 390, 844, 'scrim')


def sheet(top, body, handle=True):
    """BottomSheet: white, top radius 24, grab handle 8 below top."""
    out = ['<!-- BottomSheet (frosted) -->',
           f'<path d="M0 {top + 24} a24 24 0 0 1 24 -24 H366 a24 24 0 0 1 24 24 V844 H0 Z" fill="{CREAM}" filter="url(#sh-lg)"/>',
           f'<path d="M0 {top + 24} a24 24 0 0 1 24 -24 H366 a24 24 0 0 1 24 24 V844 H0 Z" fill="{WHITE}" fill-opacity="0.72" stroke="{WHITE}" stroke-width="1.2"/>']
    out.append(hit(0, top, 390, 844 - top, 'sheet'))
    if handle:
        out.append(f'<rect x="175" y="{top + 8}" width="40" height="4" rx="2" fill="{DIS_BG}"/>')
    out.append(body)
    return '\n'.join(out)


def dialog(title, body, buttons, icon_name=None, icon_color=BLUE, icon_bg=BTINT):
    """Dialog: x=24 w=342 r24 padding 24, stacked buttons 294 wide."""
    h = 24
    if icon_name:
        h += 48 + 16
    nt = nlines(title, 'h3', 294)
    nb = nlines(body, 'body', 294)
    h += nt * 30 + 8 + nb * 22 + 24 + len(buttons) * 56 + (len(buttons) - 1) * 12 + 24
    y = round((844 - h) / 2)
    out = [scrim(), '<!-- Dialog (frosted) -->', f'<rect x="24" y="{y}" width="342" height="{h}" rx="24" fill="{CREAM}" filter="url(#sh-lg)"/>',
           f'<rect x="24" y="{y}" width="342" height="{h}" rx="24" fill="{WHITE}" fill-opacity="0.75" stroke="{WHITE}" stroke-width="1.2"/>', hit(24, y, 342, h, 'dialog')]
    cy = y + 24
    if icon_name:
        out.append(icon_box(48, cy, icon_name, 48, icon_bg, icon_color))
        cy += 64
    s, cy = text(48, cy, title, 'h3', w=294)
    out.append(s)
    s, cy = text(48, cy + 8, body, 'body', w=294)
    out.append(s)
    cy += 24
    for lbl, kind, nav in buttons:
        out.append(button(cy, lbl, kind, x=48, w=294, nav=nav))
        cy += 68
    return '\n'.join(out)


def toast(y, s, icon_name='check-circle'):
    return (f'<!-- Toast -->\n<rect x="24" y="{y}" width="342" height="48" rx="24" fill="{NAVY}" fill-opacity="0.92" filter="url(#sh-card)"/>'
            + icon(icon_name, 40, y + 14, WHITE, 20) + t1(68, y + 29, s, 15, 500, WHITE))


HOST_TABS = [('Dashboard', 'layout-dashboard', '24'), ('Messages', 'message-circle', '27'),
             ('Calls', 'phone', '25'), ('Earnings', 'wallet', '32'), ('Profile', 'user', '26')]
USER_TABS = [('Explore', 'compass', '13'), ('Messages', 'message-circle', '27'), ('Wallet', 'wallet', '30'), ('Profile', 'user', '40')]
BAR_TOP = 746   # 64 tab row + 34 inset


def nav_badge(cx, y, n):
    if not n:
        return ''
    lbl = '99+' if n > 99 else str(n)
    w = max(16, tw(lbl, 12, 600) + 10)
    return (f'<rect x="{cx + 6:.0f}" y="{y}" width="{w:.0f}" height="16" rx="8" fill="{CORAL}" stroke="{WHITE}" stroke-width="1.5"/>'
            + t1(f'{cx + 6 + w / 2:.0f}', y + 12, lbl, 12, 600, WHITE, 'middle'))


NAV_X, NAV_Y, NAV_W, NAV_H = 16, 750, 358, 68   # floating frosted pill


def _bar(tabs, active, key, badge=0, pressed=None):
    n = len(tabs)
    cw = NAV_W / n
    out = [f'<!-- BottomNavigation ({"host" if n == 5 else "user"}, owner: Girish): floating frosted pill {NAV_X},{NAV_Y} {NAV_W}x{NAV_H} -->',
           f'<rect x="0" y="{NAV_Y - 56}" width="390" height="{844 - NAV_Y + 56}" fill="url(#g-fade)"/>',
           f'<rect x="{NAV_X}" y="{NAV_Y}" width="{NAV_W}" height="{NAV_H}" rx="{NAV_H / 2}" fill="{CREAM}" opacity="0.6"/>',
           glass(NAV_X, NAV_Y, NAV_W, NAV_H, NAV_H / 2, shadow=True, op=0.8)]
    for i, (lbl, ic, scr) in enumerate(tabs):
        cx = NAV_X + cw * i + cw / 2
        on = i == active
        col = BLUE if on else TERT
        out.append(f'<!-- Tab {i + 1} "{lbl}" → {scr} -->')
        if on or pressed == i:
            pw = min(cw - 8, 72)
            out.append(f'<rect x="{cx - pw / 2:.1f}" y="{NAV_Y + 6}" width="{pw:.1f}" height="{NAV_H - 12}" rx="22" fill="{BTINT}" opacity="{1 if on else 0.6}"/>')
        out.append(icon(ic, round(cx - 12, 1), NAV_Y + 12, col))
        out.append(t1(round(cx, 1), NAV_Y + 53, lbl, 12 if n == 4 else 11, 600, col, 'middle'))
        if lbl == 'Messages':
            out.append(nav_badge(cx, NAV_Y + 7, badge))
        out.append(hit(round(cx - cw / 2, 1), NAV_Y, round(cw, 1), NAV_H, f'{key}:{lbl}'))
    return '\n'.join(out)


def host_bar(active, badge=0, pressed=None):
    """Host BottomNavigation: 5 tabs of 78."""
    return _bar(HOST_TABS, active, 'htab', badge, pressed)


def user_bar(active, badge=0, pressed=None):
    """User BottomNavigation: 4 tabs of 97.5."""
    return _bar(USER_TABS, active, 'tab', badge, pressed)


def illus_block(x, y, w, h, inner, r=20, fill=CSURF):
    return f'<!-- Illustration area (placeholder art) -->\n<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>\n{inner}'


def menu_row(y, label, icon_name, nav, x=24, w=342, last=False, pad=16, trailing=None, color=NAVY, pressed=False, h=56,
             chevron=True, key=None):
    """MenuRow (owner: Abid): height 56, icon 24 + Body Medium label, optional trailing text, chevron."""
    out = [f'<!-- MenuRow "{label}" → {nav} -->']
    if pressed:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BTINT}"/>')
    out.append(icon(icon_name, x + pad, y + (h - 24) / 2, color if color != NAVY else NAVY))
    out.append(t1(x + pad + 36, y + h / 2 + 5, label, 15, 500, color))
    rx = x + w - pad
    if chevron:
        out.append(icon('chevron-right', rx - 20, y + (h - 20) / 2, TERT, 20))
        rx -= 28
    if trailing:
        out.append(t1(rx, y + h / 2 + 5, trailing, 14, 500, SLATE, 'end'))
    if not last:
        out.append(f'<rect x="{x + pad + 36}" y="{y + h - 1}" width="{w - pad * 2 - 36}" height="1" fill="{CBORDER}"/>')
    out.append(hit(x, y, w, h, key or f'row:{label}'))
    return '\n'.join(out)


# ---------------------------------------------------------------- frame writer
REGISTRY = []


def frame(folder, sid, screen, state, body, bg=CREAM, extra_defs='', note=''):
    name = f'{sid}_{screen}_{state}'
    path = os.path.join(ROOT, folder, name + '.svg')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844" viewBox="0 0 390 844" font-family="{FONT}">\n'
           f'<title>Frndu – {sid} {screen.replace("-", " ")} – {state.replace("-", " ")} (390 x 844)</title>\n'
           + defs_block(extra_defs) + '\n<g clip-path="url(#screen)">\n'
           f'<rect width="390" height="844" fill="{bg}"/>\n{body}\n</g>\n</svg>\n')
    with open(path, 'w') as f:
        f.write(svg)
    REGISTRY.append((sid, screen, state, os.path.relpath(path, ROOT), note))
    return path


def clip_group(cid, y0, y1, body, scroll=0):
    """Scrollable content region clipped to y0..y1, shifted up by `scroll`."""
    return (f'<clipPath id="{cid}"><rect x="0" y="{y0}" width="390" height="{y1 - y0}"/></clipPath>\n'
            f'<g clip-path="url(#{cid})"><g transform="translate(0 {-scroll})">\n{body}\n</g></g>')
