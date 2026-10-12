"""Shared components for the Girish + Abid screens (app shell, discovery, calls, chat, wallet, safety, settings).

Owners (per briefs): TopBar, BottomNavigation, SideDrawer, Host card, StatusBadge, DiamondPill, RatingStars,
SegmentedTabs, call controls → Girish. ListRow, MenuRow, Accordion, Timeline, Stepper, StatusPill → Abid.
"""
from lib import *
from illus import girl, boy, portrait, logo_mark, sparks, dashes3, soft_blob, hero_clock, hero_shield, SKIN

CONTENT_TOP = 103
TAB_BOTTOM = BAR_TOP - 24          # scroll content limit on tab roots
CTA_ABOVE_BAR = NAV_Y - 16 - 56  # primary button y when the floating bottom bar is visible

HOSTS = [
    dict(name='Priya', img='priya.jpg', hid='H-20481', langs=['Hindi', 'English'], voice=40, video=80, status='Online', bg=CTINT, shirt=CORAL, who='girl', flag='IN', age=24, rating=4.8, reviews=120),
    dict(name='Ananya', img='ananya.jpg', hid='H-10932', langs=['Kannada', 'English', 'Hindi'], voice=30, video=60, status='Online', bg=BTINT, shirt=BLUE, who='girl', flag='IN', age=26, rating=4.6, reviews=86),
    dict(name='Meera', img='priya_full.jpg', hid='H-33017', langs=['Tamil', 'English'], voice=50, video=None, status='Busy', bg=CSURF, shirt=CORAL, who='girl', flag='IN', age=23, rating=4.9, reviews=210),
    dict(name='Sana', img='ananya_alt.jpg', hid='H-41120', langs=['Urdu', 'Hindi'], voice=40, video=90, status='Online', bg=BTINT, shirt=CORAL, who='girl', flag='IN', age=25, rating=4.7, reviews=64),
    dict(name='Riya', img='priya_alt.jpg', hid='H-50211', langs=['Bengali', 'Hindi'], voice=35, video=70, status='Offline', bg=CTINT, shirt=BLUE, who='girl', flag='IN', age=27, rating=4.5, reviews=41),
    dict(name='Kavya', img='ananya.jpg', hid='H-61734', langs=['Telugu', 'English'], voice=45, video=85, status='Online', bg=CSURF, shirt=BLUE, who='girl', flag='IN', age=22, rating=4.8, reviews=150),
]
ME = dict(name='Aarav', uid='4821930', balance='1,250')


# ---------------------------------------------------------------- bars
def topbar1(title=None, right=None, right2=None, nav_back=None, back='back', nav_right=None, nav_right2=None, color=NAVY):
    """T1 Standard: back + centred H4 title + up to two right actions (slot 2 hit right edge x=330)."""
    out = [topbar(back, title=title, right=right, nav_back=nav_back, nav_right=nav_right, color=color)]
    if right2:
        out.append(f'<!-- Right action slot 2 ({right2}) → {nav_right2} -->' + icon(right2, 294, 63, color) + hit(282, 51, 48, 48, f'right2:{right2}'))
    return '\n'.join(out)


def media_btn(x, y, ic, key, label=None):
    """T3 Media button: 48 circle Navy 40% behind a White icon."""
    return (f'<!-- T3 media button {ic} -->'
            f'<circle cx="{x + 24}" cy="{y + 24}" r="24" fill="{NAVY}" opacity="0.4"/>' + icon(ic, x + 12, y + 12, WHITE) + hit(x, y, 48, 48, key))


def tab_header(title, right_svg=''):
    return f'<!-- T2 Tab root -->' + t1(24, 86, title, 26, 700, NAVY, ls=-0.4) + right_svg


# ---------------------------------------------------------------- Girish components
def diamond_pill(xr, y, bal, plus=True, key='pill:balance', h=40, label=None):
    """DiamondPill: Blue Tint, gem 20 + balance Label + plus 20. Right edge at xr."""
    txt = label or bal
    w = 14 + 20 + 8 + tw(txt, 14, 600) + (10 + 28 if plus else 0) + (6 if plus else 14)
    x = xr - w
    out = (f'<!-- DiamondPill (frosted) → 30 -->' + glass(round(x), y, round(w), h, h / 2)
           + gem(round(x + 14), y + (h - 20) / 2, 20)
           + t1(round(x + 42), y + h / 2 + 5, txt, 14, 600, NAVY))
    if plus:
        out += f'<circle cx="{xr - 20}" cy="{y + h / 2}" r="14" fill="{BTINT}"/>' + icon('plus', round(xr - 29), y + h / 2 - 9, BLUE, 18)
    return out + hit(round(x), y - 2, round(w), h + 4, key)


def status_badge(x, y, st, dark=False, small=False):
    """StatusBadge: Online (Success), Busy (Coral, D-COLOUR open), Offline (Tertiary)."""
    col = {'Online': SUCCESS, 'Busy': CORAL, 'Offline': TERT}[st]
    w = tw(st, 12, 600) + 28
    bg = WHITE
    return (f'<!-- StatusBadge {st} -->'
            f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{bg}" fill-opacity="0.9" filter="url(#sh-sm)"/>'
            f'<circle cx="{x + 12:.0f}" cy="{y + 12}" r="4" fill="{col}"/>' + t1(round(x + 20), y + 16, st, 12, 600, NAVY)), w


def stars(x, y, val, size=16, gap=4, key=None):
    """RatingStars: filled Warning, empty outline Tertiary."""
    out = ['<!-- RatingStars -->']
    for i in range(5):
        sx = x + i * (size + gap)
        on = i + 1 <= round(val)
        s = size / 24
        out.append(f'<g transform="translate({sx} {y}) scale({s:.3f})"><path d="{I["star"][0][9:-3]}" fill="{WARN if on else "none"}" '
                   f'stroke="{WARN if on else TERT}" stroke-width="{2 / s:.2f}" stroke-linejoin="round"/></g>')
        if key:
            out.append(hit(sx - (48 - size) / 2, y - (48 - size) / 2, 48, 48, f'{key}:{i + 1}'))
    return ''.join(out)


def seg_tabs(y, labels, active, x=24, w=342, h=48, badges=None, key='seg'):
    """SegmentedTabs: White track r12, active = Blue Tint segment with Blue label."""
    badges = badges or {}
    n = len(labels)
    sw = (w - 8) / n
    out = [f'<!-- SegmentedTabs (frosted track) -->', glass(x, y, w, h, h / 2, shadow=False, op=0.5)]
    for i, l in enumerate(labels):
        sx = x + 4 + i * sw
        if i == active:
            out.append(f'<rect x="{sx:.1f}" y="{y + 4}" width="{sw:.1f}" height="{h - 8}" rx="{(h - 8) / 2}" fill="{WHITE}" filter="url(#sh-sm)"/>')
        lw = tw(l, 14, 600)
        b = badges.get(l)
        cx = sx + sw / 2 - (10 if b else 0)
        out.append(t1(f'{cx:.1f}', y + h / 2 + 5, l, 14, 600, BLUE if i == active else SLATE, 'middle'))
        if b:
            out.append(f'<circle cx="{cx + lw / 2 + 14:.1f}" cy="{y + h / 2}" r="9" fill="{CORAL}"/>' + t1(f'{cx + lw / 2 + 14:.1f}', y + h / 2 + 4, str(b), 11, 700, WHITE, 'middle'))
        out.append(hit(round(sx), y, round(sw), h, f'{key}:{l}'))
    return '\n'.join(out)


_photo_n = [0]


def host_photo(x, y, w, h, host, r_top=16, r_all=None, missing=False, scale=None):
    """Host cover photo (illustrated placeholder). Missing photo = Blue Tint + user icon."""
    _photo_n[0] += 1
    cid = f'hp{_photo_n[0]}'
    rr = r_all if r_all is not None else r_top
    if r_all is not None:
        clip = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rr}"/>'
    else:
        clip = f'<path d="M{x} {y + rr} a{rr} {rr} 0 0 1 {rr} -{rr} H{x + w - rr} a{rr} {rr} 0 0 1 {rr} {rr} V{y + h} H{x} Z"/>'
    out = [f'<clipPath id="{cid}">{clip}</clipPath><g clip-path="url(#{cid})">']
    if missing:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BTINT}"/>' + icon('user', x + w / 2 - 20, y + h / 2 - 20, BLUE, 40))
    else:
        sc = scale or (w / 120)
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{host["bg"]}"/>'
                   f'<circle cx="{x + w * 0.85}" cy="{y + h * 0.12}" r="{w * 0.38}" fill="{WHITE}" opacity="0.45"/>')
        if host.get('img'):
            out.append(photo_img(x, y, w, h, host['img'], 'xMidYMin'))
        else:
            fig = girl if host['who'] == 'girl' else boy
            out.append(fig(x + w / 2, y + h * 0.42, sc, host['shirt']))
    out.append('</g>')
    return ''.join(out)


def flag_badge(x, y):
    return flag_in(x, y + 2)


HOST_CARD_W, HOST_CARD_H = 165, 240


def host_card(x, y, host, missing=False, crossfade=False):
    """Host card 165 x 240 (Home ref): frosted card, photo 153 x 150 inset 6 with radius 20 and a soft white halo,
    Online pill + flag on the photo, name H4-ish, languages, rating | rate row and a round chevron."""
    W, H = HOST_CARD_W, HOST_CARD_H
    out = [f'<!-- Host card "{host["name"]}" → 16 (frosted, Home ref) -->', glass(x, y, W, H, 24),
           f'<rect x="{x + 6}" y="{y + 6}" width="153" height="150" rx="20" fill="{WHITE}" opacity="0.6" filter="url(#blur-md)"/>',
           host_photo(x + 6, y + 6, 153, 150, host, r_all=20, missing=missing)]
    sb, _ = status_badge(x + 14, y + 14, host['status'], dark=True)
    out.append(sb)
    out.append(flag_in(x + W - 14 - 24, y + 18))
    nm = host['name'] if tw(host['name'], 16, 700) < 141 else host['name'][:13] + '…'
    out.append(t1(x + 12, y + 156 + 24, nm, 16, 700, NAVY))
    langs = host['langs']
    lt = ' · '.join(langs[:2]) + (f' +{len(langs) - 2}' if len(langs) > 2 else '')
    out.append(t1(x + 12, y + 156 + 42, lt, 12, 500, SLATE))
    ry = y + 156 + 54
    out.append(icon('star', x + 12, ry, WARN, 16).replace('fill="none"', f'fill="{WARN}"', 1)
               + t1(x + 32, ry + 13, f'{host["rating"]}', 12, 600, NAVY)
               + f'<rect x="{x + 58}" y="{ry + 2}" width="1" height="12" fill="{BORDER}"/>')
    mode, rate = ('video', host['video']) if host['video'] else ('phone', host['voice'])
    out.append(icon(mode, x + 66, ry, SLATE, 16) + icon('gem', x + 86, ry, BLUE, 14) + t1(x + 103, ry + 13, str(rate), 12, 600, NAVY))
    out.append(f'<circle cx="{x + W - 26}" cy="{ry + 8}" r="16" fill="{BTINT}"/>' + icon('chevron-right', x + W - 35, ry - 1, BLUE, 18))
    out.append(hit(x, y, W, H, f'host:{host["name"]}'))
    return '\n'.join(out)


def round_btn(cx, cy, d, ic, bg, fg, key, label=None, lc=WHITE, op=1.0, isz=24):
    glow = {ERROR: ' filter="url(#gl-red)"', BLUE: ' filter="url(#gl-blue)"', SUCCESS: ' filter="url(#sh-card)"', CORAL: ' filter="url(#gl-coral)"'}.get(bg, '')
    out = (f'<circle cx="{cx}" cy="{cy}" r="{d / 2}" fill="{bg}" opacity="{op}"{glow}/>' + icon(ic, cx - isz / 2, cy - isz / 2, fg, isz)
           + hit(cx - max(d, 48) / 2, cy - max(d, 48) / 2, max(d, 48), max(d, 48), key))
    if label:
        out += t1(cx, cy + d / 2 + 18, label, 12, 500, lc, 'middle')
    return out


def pill(x, y, label, bg, fg, ic=None, h=32, op=1.0, anchor='start'):
    w = tw(label, 14, 600) + 24 + (24 if ic else 0)
    if anchor == 'middle':
        x = x - w / 2
    elif anchor == 'end':
        x = x - w
    out = f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{bg}" opacity="{op}"/>'
    tx = x + 12
    if ic:
        out += icon(ic, round(tx), y + (h - 18) / 2, fg, 18)
        tx += 24
    return out + t1(round(tx), y + h / 2 + 5, label, 14, 600, fg), w


# ---------------------------------------------------------------- Abid components
PILL_KINDS = {
    'Pending': (BTINT, BLUE, None), 'Processing': (BTINT, BLUE, None), 'Submitted': (BTINT, BLUE, None),
    'In review': (CSURF, NAVY, WARN), 'Not started': (CBORDER, SLATE, None),
    'Completed': (WHITE, SUCCESS, SUCCESS), 'Verified': (WHITE, SUCCESS, SUCCESS), 'Success': (WHITE, SUCCESS, SUCCESS),
    'Failed': (CTINT, ERROR, None), 'Rejected': (CTINT, ERROR, None), 'Refunded': (CBORDER, SLATE, None),
    'Action needed': (WHITE, NAVY, WARN), 'Warning': (WHITE, NAVY, WARN), 'Suspended': (WHITE, NAVY, WARN),
    'Permanently banned': (WHITE, ERROR, ERROR), 'Final warning': (WHITE, ERROR, ERROR),
}


def status_pill(x, y, label, kind=None, anchor='start', h=24):
    """StatusPill (owner: Abid)."""
    bg, fg, border = PILL_KINDS.get(kind or label, (BTINT, BLUE, None))
    w = tw(label, 12, 600) + 20
    if anchor == 'end':
        x = x - w
    st = f' stroke="{border}" stroke-width="1.5"' if border else ''
    return (f'<!-- StatusPill {label} -->'
            f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{bg}"{st}/>'
            + t1(f'{x + w / 2:.0f}', y + h / 2 + 4, label, 12, 600, fg, 'middle')), w


def list_row(y, title, sub=None, lead=None, right=None, key=None, h=72, sub2=None, divider=True, title_col=NAVY):
    """ListRow (owner: Abid): leading 48, title Body Medium, sub Caption, trailing content."""
    out = [f'<!-- ListRow "{title}" (frosted tile) -->']
    if divider:
        out.append(glass(12, y + 4, 366, h - 8, 20, shadow=False))
    tx = 24
    if lead:
        out.append(lead(24, y + (h - 48) / 2))
        tx = 84
    lines = 1 + (1 if sub else 0) + (1 if sub2 else 0)
    ty = y + (h - (22 + (lines - 1) * 18)) / 2
    out.append(t1(tx, round(ty + 16), title, 15, 500, title_col))
    if sub:
        out.append(t1(tx, round(ty + 22 + 13), sub, 12, 500, SLATE))
    if sub2:
        out.append(t1(tx, round(ty + 40 + 13), sub2, 12, 500, TERT))
    if right:
        out.append(right(366, y, h))
    if key:
        out.append(hit(24, y, 342, h, key))
    return '\n'.join(out)


def lead_icon(name, bg=BTINT, col=BLUE, d=48):
    return lambda x, y: f'<circle cx="{x + d / 2}" cy="{y + d / 2}" r="{d / 2}" fill="{bg}"/>' + icon(name, x + d / 2 - 12, y + d / 2 - 12, col)


HOST_IMG = {h['name']: h['img'] for h in HOSTS}
HOST_IMG.update({'Rohan_K': 'rohan.jpg', 'Rohan': 'rohan.jpg'})


def lead_avatar(letter=None, photo=False, d=48, verified=False):
    def f(x, y):
        s = avatar(x + d / 2, y + d / 2, d, letter=letter, photo=photo)
        if verified:
            s += f'<circle cx="{x + d - 4}" cy="{y + d - 4}" r="9" fill="{WHITE}"/>' + icon('badge-check', x + d - 12, y + d - 12, BLUE, 16)
        return s
    return f


def kv_card(y, rows, x=24, w=342, title=None, pad=16, rowh=32):
    """Card of label/value rows."""
    h = pad * 2 + len(rows) * rowh + (30 if title else 0)
    out = [card(x, y, w, h)]
    ry = y + pad
    if title:
        out.append(t1(x + pad, ry + 18, title, 18, 700, NAVY))
        ry += 30
    for r in rows:
        lab, val = r[0], r[1]
        bold = len(r) > 2 and r[2] == 'bold'
        dia = len(r) > 2 and r[2] == 'gem'
        col = r[3] if len(r) > 3 else NAVY
        out.append(t1(x + pad, ry + 21, lab, 14 if bold else 15, 600 if bold else 400, NAVY if bold else SLATE))
        out.append(t1(x + w - pad, ry + 21, val, 16 if bold else 15, 700 if bold else 500, col, 'end'))
        if dia:
            out.append(gem(round(x + w - pad - tw(val, 15, 500) - 26), ry + 7, 18))
        ry += rowh
    return '\n'.join(out), y + h


def section_label(y, s, x=24):
    return t1(x, y + 15, s, 14, 600, SLATE)


def empty_state(cy, ic, title, body=None, link=None, nav=None, bg=BTINT, col=BLUE, primary=None):
    out = [soft_blob(195, cy, 70, 50, bg), f'<circle cx="195" cy="{cy}" r="40" fill="{WHITE}"/>', icon(ic, 175, cy - 20, col, 40),
           sparks(238, cy - 52, CORAL)]
    y = cy + 72
    s, y = text(195, y, title, 'h4', anchor='middle', w=300)
    out.append(s)
    if body:
        s, y = text(195, y + 6, body, 'body', anchor='middle', w=300)
        out.append(s)
    if link:
        out.append(link_row(y + 4, link, nav))
    return '\n'.join(out)


def skeleton_rows(y, n, h=72, avatar_d=48):
    out = []
    for i in range(n):
        ry = y + i * h
        out.append(f'<circle cx="{24 + avatar_d / 2}" cy="{ry + h / 2}" r="{avatar_d / 2}" fill="{SKEL}"/>'
                   + skeleton(84, ry + h / 2 - 14, 150, 12) + skeleton(84, ry + h / 2 + 4, 100, 10) + skeleton(306, ry + h / 2 - 8, 60, 14))
    return '\n'.join(out)


def accordion(y, q, a=None, open_=False, helpful=None):
    """Accordion (owner: Abid): question row 56, answer + 'Was this helpful?'"""
    out = [f'<!-- Accordion "{q}" -->']
    n = nlines(q, 'bodyM', 290)
    qh = max(56, n * 22 + 24)
    out.append(text(24, y + (qh - n * 22) / 2, q, 'bodyM', w=290)[0])
    out.append(icon('chevron-up' if open_ else 'chevron-down', 346, y + qh / 2 - 10, SLATE, 20))
    out.append(hit(24, y, 342, qh, f'faq:{q[:24]}'))
    yy = y + qh
    if open_ and a:
        s, yy = text(24, yy, a, 'body', w=342)
        out.append(s)
        yy += 12
        out.append(t1(24, yy + 22, 'Was this helpful?', 13, 400, SLATE))
        c1, w1 = chip(160, yy + 4, 'Yes', 'selected' if helpful == 'yes' else 'unselected', h=32)
        c2, _ = chip(160 + w1 + 8, yy + 4, 'No', 'selected' if helpful == 'no' else 'unselected', h=32)
        out.append(c1 + c2)
        yy += 48
    out.append(f'<rect x="24" y="{yy}" width="342" height="1" fill="{CBORDER}"/>')
    return '\n'.join(out), yy + 1


def timeline(y, events, x=40):
    """Timeline (owner: Abid): dots + connecting line + label + timestamp."""
    out = ['<!-- Timeline -->']
    for i, (label, ts, state) in enumerate(events):
        cy = y + i * 52 + 10
        col = {'done': SUCCESS, 'now': BLUE, 'todo': DIS_BG, 'fail': ERROR}[state]
        if i < len(events) - 1:
            out.append(f'<rect x="{x - 1}" y="{cy + 8}" width="2" height="36" fill="{BORDER}"/>')
        out.append(f'<circle cx="{x}" cy="{cy}" r="8" fill="{col}"/>')
        if state == 'done':
            out.append(icon('check', x - 5, cy - 5, WHITE, 10, 2))
        out.append(t1(x + 20, cy + 5, label, 15, 500, NAVY if state != 'todo' else TERT))
        if ts:
            out.append(t1(x + 20, cy + 23, ts, 12, 500, SLATE))
    return '\n'.join(out), y + len(events) * 52


def stepper(y, steps, x=24, w=342):
    """Stepper (owner: Abid): numbered 28 circles joined by a 2 px line, label under each.
    steps: [(label, state)] with state done | now | todo | fail."""
    n = len(steps)
    gap = (w - 28) / (n - 1)
    out = ['<!-- Stepper -->']
    for i in range(n - 1):
        x1 = x + 14 + i * gap + 18
        done = steps[i][1] == 'done'
        out.append(f'<rect x="{x1:.0f}" y="{y + 13}" width="{gap - 36:.0f}" height="2" rx="1" fill="{SUCCESS if done else BORDER}"/>')
    for i, (label, st) in enumerate(steps):
        cx = x + 14 + i * gap
        fill, fg, stroke = {'done': (SUCCESS, WHITE, None), 'now': (BLUE, WHITE, None), 'todo': (WHITE, TERT, BORDER),
                            'fail': (ERROR, WHITE, None)}[st]
        s = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ''
        out.append(f'<circle cx="{cx:.0f}" cy="{y + 14}" r="14" fill="{fill}"{s}/>')
        if st == 'done':
            out.append(icon('check', round(cx - 8), y + 6, WHITE, 16, 2))
        elif st == 'fail':
            out.append(icon('x', round(cx - 8), y + 6, WHITE, 16, 2))
        else:
            out.append(t1(f'{cx:.0f}', y + 19, str(i + 1), 13, 700, fg, 'middle'))
        anchor = 'start' if i == 0 else 'end' if i == n - 1 else 'middle'
        lx = x if i == 0 else x + w if i == n - 1 else cx
        out.append(t1(f'{lx:.0f}', y + 48, label, 12, 600, NAVY if st != 'todo' else TERT, anchor))
    return '\n'.join(out), y + 56


def blur_defs(id_='blr', sd=18):
    return f'<filter id="{id_}" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="{sd}"/></filter>'


def video_scene(who='girl', blur=False, shirt=CORAL, bg=CTINT, dim=0.0, img=None, shade=True):
    """Full-screen remote video: real photo filling the screen, soft dark gradient top and bottom for legibility."""
    fig = ''
    img = img or ('priya_full.jpg' if who == 'girl' else 'rohan.jpg')
    f = ' filter="url(#blr)"' if blur else ''
    out = (blur_defs() if blur else '') + (f'<g{f}><rect x="-40" y="-40" width="470" height="924" fill="{bg}"/>'
                                           f'<circle cx="330" cy="120" r="160" fill="{WHITE}" opacity="0.4"/>'
                                           f'<rect x="-40" y="600" width="470" height="300" fill="{CSURF}" opacity="0.6"/>{fig}'
                                           + f'<rect x="-40" y="560" width="470" height="324" fill="{NAVY}"/>'
                                           + photo_img(-80, 0, 550, 600, img, 'xMidYMin') + '</g>')
    if shade:
        out += ('<linearGradient id="vs-top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#10233F" stop-opacity="0.55"/><stop offset="1" stop-color="#10233F" stop-opacity="0"/></linearGradient>'
                '<linearGradient id="vs-bot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#10233F" stop-opacity="0"/><stop offset="0.75" stop-color="#10233F" stop-opacity="0.9"/><stop offset="1" stop-color="#10233F"/></linearGradient>'
                '<rect width="390" height="180" fill="url(#vs-top)"/><rect y="380" width="390" height="222" fill="url(#vs-bot)"/>'
                f'<rect y="600" width="390" height="244" fill="{NAVY}"/>')
    if dim:
        out += f'<rect width="390" height="844" fill="{NAVY}" opacity="{dim}"/>'
    return out


def dark_status():
    return status_bar(WHITE)


def money(n):
    return f'{n:,}'


# ---------------------------------------------------------------- call visuals (new theme)
def call_halo(cx, cy, r=64, who='girl', bg=CTINT, online=False, dots=True, dim=False, rings=True, img=None):
    """Avatar in soft glowing rings with orbit dots (calling / matching screens)."""
    import math
    o = [f'<!-- Call halo -->', f'<circle cx="{cx}" cy="{cy}" r="{r * 2.3:.0f}" fill="url(#g-halo)"/>']
    if rings:
        for rr, op, sw in [(r + 18, 0.30, 10), (r + 44, 0.16, 1.5), (r + 78, 0.12, 1.2)]:
            if sw > 2:
                o.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{BLUE}" stroke-opacity="{op * 0.6:.2f}" stroke-width="{sw}"/>')
            else:
                o.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{BLUE}" stroke-opacity="{op:.2f}" stroke-width="{sw}"/>')
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 8}" fill="none" stroke="{BLUE}" stroke-opacity="0.45" stroke-width="2"/>')
    if dots:
        for ang, rr, d in [(-130, r + 78, 6), (-30, r + 78, 5), (20, r + 82, 3), (150, r + 78, 7), (110, r + 70, 2.5), (60, r + 78, 3.5)]:
            a = math.radians(ang)
            o.append(f'<circle cx="{cx + rr * math.cos(a):.1f}" cy="{cy + rr * math.sin(a):.1f}" r="{d}" fill="{BLUE}" opacity="0.55"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="{WHITE}" filter="url(#sh-card)"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/>')
    img = img or ('priya_full.jpg' if who == 'girl' else 'rohan.jpg')
    _photo_n[0] += 1
    o.append(f'<clipPath id="ch{_photo_n[0]}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
             f'<g clip-path="url(#ch{_photo_n[0]})">' + photo_img(cx - r, cy - r, 2 * r, 2 * r, img, 'xMidYMid') + '</g>')
    if dim:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CREAM}" opacity="0.45"/>')
    if online:
        a = math.radians(45)
        ox, oy = cx + r * math.cos(a), cy + r * math.sin(a)
        o.append(f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="10" fill="{SUCCESS}" stroke="{WHITE}" stroke-width="3"/>')
    return '\n'.join(o)


def waveform(cx, cy, live=True, w=300, color=BLUE):
    """Symmetric voice waveform that fades into dots at both ends."""
    import math
    o = ['<!-- Waveform -->']
    n = 29
    gap = w / (n - 1)
    for i in range(n):
        x = cx - w / 2 + i * gap
        t = abs(i - (n - 1) / 2) / ((n - 1) / 2)
        if t > 0.72:
            o.append(f'<circle cx="{x:.1f}" cy="{cy}" r="2" fill="{color}" opacity="{0.55 - (t - 0.72):.2f}"/>')
            continue
        h = (8 + 54 * (1 - t) ** 1.6 * abs(math.sin(i * 1.7 + 0.4))) if live else 6
        h = max(h, 6)
        o.append(f'<rect x="{x - 1.75:.1f}" y="{cy - h / 2:.1f}" width="3.5" height="{h:.1f}" rx="1.75" fill="{color}" opacity="{0.95 - t * 0.5:.2f}"/>')
    return ''.join(o)


def call_btn(cx, cy, ic, key, label=None, kind='glass', d=64, lc=SLATE):
    """Round call control. kind: glass (frosted, Navy icon) | on (Blue, White icon) | end (red, glow) | accept (Blue, glow)."""
    if kind == 'glass':
        o = glass(cx - d / 2, cy - d / 2, d, d, d / 2) + icon(ic, cx - 12, cy - 12, NAVY)
    elif kind == 'on':
        o = f'<circle cx="{cx}" cy="{cy}" r="{d / 2}" fill="url(#g-blue)" filter="url(#gl-blue)"/>' + icon(ic, cx - 12, cy - 12, WHITE)
    elif kind == 'accept':
        o = f'<circle cx="{cx}" cy="{cy}" r="{d / 2}" fill="url(#g-blue)" filter="url(#gl-blue)"/>' + icon(ic, cx - 14, cy - 14, WHITE, 28)
    else:
        o = f'<circle cx="{cx}" cy="{cy}" r="{d / 2}" fill="{ERROR}" filter="url(#gl-red)"/>' + icon(ic, cx - 14, cy - 14, WHITE, 28)
    o += hit(cx - max(d, 48) / 2, cy - max(d, 48) / 2, max(d, 48), max(d, 48), key)
    if label:
        o += t1(cx, cy + d / 2 + 22, label, 14, 500, lc, 'middle')
    return o
