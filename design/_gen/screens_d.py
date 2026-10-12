"""Host tabs: 24 Dashboard, 25 Call History, 26 Profile & Rates."""
import math

from lib import *
from lib2 import HOST_IMG
from screens_b import perm_dialog

CONTENT_BOTTOM = BAR_TOP - 24  # 24 above the bottom bar


def host_header():
    return ('<!-- T2 header: avatar → 00.1 (host variant) -->\n' + avatar(44, 75, 40, photo=True)
            + t1(72, 81, 'Hi, Priya', 18, 700, NAVY) + hit(20, 51, 48, 48, 'avatar'))


# ============================================================ 24 Host Dashboard
def master_card(y, mode):
    o = ['<!-- Master card -->', card(24, y, 342, 88, 20)]
    title = {'off': "You're Offline", 'on': "You're Online", 'call': 'On a call', 'blocked': "You're Offline"}[mode]
    cap = {'off': 'Go online to receive calls.', 'on': 'You can receive calls now.', 'call': "You're in a call right now.",
           'blocked': 'Go online to receive calls.'}[mode]
    tx = 40
    if mode in ('on', 'call'):
        o.append(f'<circle cx="46" cy="{y + 31}" r="6" fill="{SUCCESS}"/>')
        tx = 60
    o.append(t1(tx, y + 16 + 22, title, 22, 700, NAVY, ls=-0.2))
    o.append(t1(40, y + 16 + 30 + 4 + 14, cap, 12, 500, SLATE))
    o.append('<!-- Master Switch (on = Success green) → go online, or "Before you go online" sheet when blocked -->')
    o.append(switch(286, y + 26, mode in ('on', 'call'), SUCCESS, large=True, disabled=mode in ('call', 'blocked'), key='switch:master'))
    return '\n'.join(o)


def channels_card(y, voice=True, video=True, chat=False):
    o = ['<!-- Channels card -->', card(24, y, 342, 168)]
    for i, (ic, lbl, on) in enumerate([('phone', 'Voice Mode', voice), ('video', 'Video Mode', video), ('message-square', 'Chat Mode', chat)]):
        ry = y + i * 56
        o.append(icon(ic, 40, ry + 16, NAVY))
        o.append(t1(76, ry + 33, lbl, 15, 500, NAVY))
        o.append(switch(298, ry + 12, on, BLUE, key=f'switch:{lbl}'))
        if i < 2:
            o.append(f'<rect x="40" y="{ry + 55.5}" width="310" height="1" fill="{CBORDER}"/>')
    return '\n'.join(o)


def stat_card(x, y, value, label, diamond=False):
    o = [card(x, y, 165, 88)]
    vx = x + 16
    if diamond:
        o.append(gem(vx, y + 20, 22))
        vx += 28
    o.append(t1(vx, y + 16 + 26, value, 26, 700, NAVY, ls=-0.4))
    o.append(t1(x + 16, y + 16 + 34 + 4 + 14, label, 12, 500, SLATE))
    return '\n'.join(o)


def health_card(y):
    o = ['<!-- Connection health card -->', card(24, y, 342, 132)]
    o.append(t1(40, y + 16 + 15, 'Connection health', 14, 600, NAVY))
    items = [('signal', 'Network', 'Good'), ('mic', 'Microphone', 'Ready'), ('camera', 'Camera', 'Ready')]
    for i, (ic, lbl, st) in enumerate(items):
        cx = 40 + i * 106
        o.append(icon(ic, cx, y + 48, BLUE))
        o.append(t1(cx, y + 48 + 24 + 4 + 13, lbl, 12, 500, SLATE))
        o.append(icon('check-circle', cx, y + 100, SUCCESS, 16))
        o.append(t1(cx + 22, y + 113, st, 14, 600, NAVY))
    return '\n'.join(o)


def quick_links(y):
    o = ['<!-- Quick links -->']
    for i, (ic, lbl, nav) in enumerate([('phone', 'Call history', '25'), ('wallet', 'Earnings', '32'), ('user', 'Profile & rates', '26')]):
        x = 24 + i * 118
        o.append(f'<!-- Quick link "{lbl}" → {nav} -->' + card(x, y, 106, 88))
        o.append(icon(ic, x + 41, y + 18, BLUE))
        o.append(t1(x + 53, y + 18 + 24 + 8 + 15, lbl, 14 if tw(lbl, 14, 600) < 92 else 12, 600, NAVY, 'middle'))
        o.append(hit(x, y, 106, 88, f'quick:{lbl}'))
    return '\n'.join(o)


def s24_content(mode='off', voice=True, video=True, top_banner=None):
    o = []
    y = 103 + 16
    if top_banner:
        s, y = top_banner(y)
        o.append(s)
        y += 16
    o.append(master_card(y, mode))
    y += 88 + 12
    o.append(channels_card(y, voice, video))
    y += 168 + 8
    o.append(text(24, y, 'Turn on at least Voice or Video to go online.', 'caption', color=ERROR if not (voice or video) else None)[0])
    y += 18 + 24
    o.append(t1(24, y + 15, 'Today', 14, 600, NAVY))
    y += 20 + 12
    o.append(stat_card(24, y, '480', 'Diamonds earned', True) + stat_card(201, y, '12', 'Calls completed'))
    y += 100
    o.append(stat_card(24, y, '1h 20m', 'Talk time') + stat_card(201, y, '1', 'Missed calls'))
    y += 88 + 24
    o.append(health_card(y))
    y += 132 + 24
    o.append(quick_links(y))
    return '\n'.join(o)


def s24_loading():
    o = []
    y = 119
    o.append(card(24, y, 342, 88, 20) + skeleton(40, y + 20, 150, 22) + skeleton(40, y + 54, 190, 14) + skeleton(286, y + 26, 64, 36, 18))
    y += 100
    o.append(card(24, y, 342, 168))
    for i in range(3):
        o.append(skeleton(40, y + 16 + i * 56, 24, 24) + skeleton(76, y + 21 + i * 56, 120, 14) + skeleton(298, y + 12 + i * 56, 52, 32, 16))
    y += 168 + 50
    o.append(skeleton(24, y, 60, 16))
    y += 32
    for r in range(2):
        for c in range(2):
            o.append(card(24 + c * 177, y + r * 100, 165, 88) + skeleton(40 + c * 177, y + r * 100 + 18, 70, 24)
                     + skeleton(40 + c * 177, y + r * 100 + 56, 100, 12))
    return '\n'.join(o)


def s24_body(mode='off', voice=True, video=True, scroll=0, top_banner=None, overlay=None, state=None):
    o = [blobs(bottom=False)]
    if state == 'loading':
        o.append(clip_group('c24', 103, CONTENT_BOTTOM, s24_loading()))
    elif state == 'error':
        o.append(banner(119, "We couldn't load your dashboard. Try again in a moment.", 'error')[0])
        o.append(f'<circle cx="195" cy="300" r="40" fill="{CTINT}"/>' + icon('refresh-cw', 175, 280, CORAL, 40))
        o.append(text(195, 364, "Something didn't load", 'h4', anchor='middle')[0])
        o.append(text(195, 394, 'Check your connection and try again.', 'body', anchor='middle')[0])
        o.append('<!-- Retry → reload 24 -->' + button(436, 'Try again', 'secondary', x=115, w=160))
    else:
        o.append(clip_group('c24', 103, CONTENT_BOTTOM, s24_content(mode, voice, video, top_banner), scroll))
    o.append(host_header())
    o.append(status_bar())
    o.append(host_bar(0))
    if overlay:
        o.append(overlay)
    o.append(home_indicator())
    return '\n'.join(o)


def before_online_sheet():
    rows = [('Permissions', 'Camera, microphone, notifications', False, 'permission dialog from 12'),
            ('Languages', 'Hindi, English, Kannada', True, '09A as sheet'),
            ('Terms accepted', 'Accept the latest Host Terms', False, '11A')]
    h = 24 + 30 + 8 + 22 + 16 + len(rows) * 64 + 24 + 34
    top = 844 - h
    b = [text(24, top + 24, 'Before you go online', 'h3')[0], text(24, top + 62, 'Fix these to start receiving calls.', 'body')[0]]
    y = top + 24 + 30 + 8 + 22 + 16
    for lbl, sub, ok, nav in rows:
        b.append(f'<!-- Checklist row "{lbl}" -->')
        b.append(icon('check-circle' if ok else 'alert-circle', 24, y + 20, SUCCESS if ok else WARN))
        b.append(t1(60, y + 28, lbl, 14, 600, NAVY))
        b.append(t1(60, y + 46, sub, 12, 500, SLATE))
        if ok:
            b.append(t1(366, y + 37, 'Done', 14, 600, SUCCESS, 'end'))
        else:
            b.append(f'<!-- "Fix" → {nav} -->' + f'<rect x="318" y="{y + 10}" width="48" height="44" fill="#FFFFFF" fill-opacity="0"/>'
                     + t1(366, y + 37, 'Fix', 14, 600, BLUE, 'end') + hit(318, y + 10, 48, 44, f'fix:{lbl}'))
        if lbl != rows[-1][0]:
            b.append(f'<rect x="60" y="{y + 63}" width="306" height="1" fill="{CBORDER}"/>')
        y += 64
    return scrim() + sheet(top, '\n'.join(b))


def gen_24():
    F, ID, N = '24_Host-Dashboard', '24', 'Host-Dashboard'
    frame(F, ID, N, 'Offline-Master-Off', s24_body('off'), note='No bell at Launch. Reviews/Levels/Followers/Analytics/Leaderboard/Schedule not shown')
    frame(F, ID, N, 'Online-Master-On', s24_body('on'))
    frame(F, ID, N, 'Online-Scrolled', s24_body('on', scroll=230), note='Stats, connection health, quick links')
    frame(F, ID, N, 'On-A-Call', s24_body('call'))
    frame(F, ID, N, 'Voice-Video-Off', s24_body('blocked', voice=False, video=False), note='Master switch disabled + helper line')
    frame(F, ID, N, 'Before-Online-Sheet', s24_body('off', overlay=before_online_sheet()))
    frame(F, ID, N, 'Before-Online-Permission-Dialog', s24_body('off', overlay=perm_dialog('Microphone')))
    frame(F, ID, N, 'Auto-Offline-Notice', s24_body('off', top_banner=lambda y: banner(y, 'You were set to Offline after 3 missed calls.', 'warning')),
          note='Shown on next open')
    frame(F, ID, N, 'Loading', s24_body(state='loading'))
    frame(F, ID, N, 'Error', s24_body(state='error'))
    frame(F, ID, N, 'Connection-Offline', s24_body('off', top_banner=offline_banner))


# ============================================================ 25 Host Call History
CALLS = {
    'Today': [('Rohan_K', '10:42 AM', 'video', '12m 30s', 'ans', '+360'), ('Vikram', '9:15 AM', 'phone', '6m 05s', 'ans', '+240'),
              ('Arjun.S', '8:02 AM', 'phone', '', 'missed', None)],
    'Yesterday': [('Sameer', '11:48 PM', 'video', '22m 10s', 'ans', '+1,320'), ('Kabir_07', '9:30 PM', 'phone', '', 'rejected', None),
                  ('Dev', '7:12 PM', 'phone', '3m 40s', 'ans', '+160'), ('Nikhil R', '6:05 PM', 'video', '8m 00s', 'ans', '+480')],
}


def call_row(y, name, ts, kind, dur, status, earned):
    o = [f'<!-- Call row {name} → call detail sheet -->', card(24, y, 342, 80)]
    o.append(avatar(64, y + 40, 48, img=HOST_IMG.get(name)) if name in HOST_IMG else avatar(64, y + 40, 48, letter=name[0]))
    o.append(t1(100, y + 16 + 16, name, 15, 500, NAVY))
    o.append(icon(kind, 100, y + 44, SLATE, 16))
    sub = f'{ts} · {dur}' if dur else ts
    o.append(t1(122, y + 57, sub, 12, 500, SLATE))
    if earned:
        w = tw(earned, 14, 600)
        o.append(t1(350, y + 45, earned, 14, 600, NAVY, 'end') + gem(350 - w - 22, y + 31, 18))
    else:
        o.append(t1(350, y + 45, 'Missed' if status == 'missed' else 'Rejected', 14, 600, TERT, 'end'))
    o.append(hit(24, y, 342, 80, f'call:{name}'))
    return '\n'.join(o)


def filter_chips(y, sel='All'):
    items = [(l, 'selected' if l == sel else 'unselected') for l in ['All', 'Answered', 'Missed', 'Rejected']]
    s, _ = chips_wrap(24, y, items, maxw=400)
    return '<!-- Filter chips (horizontal scroll) → filter list -->' + s


def s25_list(flt='All', loading_more=False):
    o = []
    y = 103 + 12 + 40 + 16
    for day, rows in CALLS.items():
        rows = [r for r in rows if flt == 'All' or (flt == 'Missed' and r[4] == 'missed') or (flt == 'Answered' and r[4] == 'ans')
                or (flt == 'Rejected' and r[4] == 'rejected')]
        if not rows:
            continue
        o.append('<!-- Sticky date header -->' + t1(24, y + 15, day, 14, 600, SLATE))
        y += 20 + 8
        for r in rows:
            o.append(call_row(y, *r))
            y += 92
        y += 4
    if loading_more:
        o.append(spinner(195, y + 20, BLUE, 10) + t1(195, y + 52, 'Loading more calls…', 12, 500, SLATE, 'middle'))
    return '\n'.join(o)


def s25_body(flt='All', state='list', scroll=0, overlay=None, top_banner=None):
    o = [blobs(bottom=False)]
    o.append(topbar(None, tab_title='Call history', right='calendar', nav_right='date-range sheet'))
    chips_y = 115
    if top_banner:
        b, bb = top_banner
        o.append(b)
        chips_y = bb + 12
    o.append(filter_chips(chips_y, flt))
    off = chips_y - 115
    if state == 'list':
        o.append(clip_group('c25', chips_y + 52, CONTENT_BOTTOM, f'<g transform="translate(0 {off})">{s25_list(flt, scroll > 0)}</g>', scroll))
    elif state == 'loading':
        sk = [skeleton(24, 171, 60, 16)]
        y = 199
        for _ in range(6):
            sk.append(card(24, y, 342, 80) + f'<circle cx="64" cy="{y + 40}" r="24" fill="{SKEL}"/>' + skeleton(100, y + 20, 120, 14)
                      + skeleton(100, y + 46, 90, 12) + skeleton(300, y + 32, 50, 16))
            y += 92
        o.append(clip_group('c25', 167, CONTENT_BOTTOM, '\n'.join(sk)))
    elif state in ('empty', 'empty-filtered'):
        y = 260
        o.append(f'<circle cx="195" cy="{y + 40}" r="44" fill="{BTINT}"/>' + icon('phone', 171, y + 16, BLUE, 48))
        if state == 'empty':
            o.append(text(195, y + 108, 'No calls yet.', 'h4', anchor='middle')[0])
            o.append(text(195, y + 138, 'Go online to start receiving calls.', 'body', anchor='middle')[0])
            o.append(link_row(y + 172, 'Go to dashboard', '24'))
        else:
            o.append(text(195, y + 108, 'No calls match these filters.', 'h4', anchor='middle')[0])
            o.append(link_row(y + 146, 'Reset filters', 'All chip, clear dates'))
    elif state == 'error':
        y = 240
        o.append(f'<circle cx="195" cy="{y + 40}" r="44" fill="{CTINT}"/>' + icon('refresh-cw', 175, y + 20, CORAL, 40))
        o.append(text(195, y + 108, "We couldn't load your calls", 'h4', anchor='middle')[0])
        o.append(text(195, y + 138, 'Check your connection and try again.', 'body', anchor='middle')[0])
        o.append('<!-- Retry → reload -->' + button(y + 180, 'Try again', 'secondary', x=115, w=160))
    o.append(status_bar())
    o.append(host_bar(2))
    if overlay:
        o.append(overlay)
    o.append(home_indicator())
    return '\n'.join(o)


def date_range_sheet():
    h = 24 + 30 + 16 + 40 + 24 + 2 * (20 + 8 + 56) + 16 + 24 + 56 + 12 + 56 + 34
    top = 844 - h
    b = [text(24, top + 24, 'Choose dates', 'h3')[0]]
    y = top + 70
    b.append('<!-- Quick options -->' + chips_wrap(24, y, [('7 days', 'selected'), ('30 days', 'unselected')])[0])
    y += 40 + 24
    for lbl, val in [('From', '02 / 10 / 2026'), ('To', '09 / 10 / 2026')]:
        b.append(t1(24, y + 15, lbl, 14, 600, NAVY))
        b.append(f'<!-- Date field "{lbl}" → date picker -->' + input_box(y + 28, val, None, 'filled', right_icon='calendar'))
        y += 84 + 16
    y += 24
    b.append(button(y, 'Apply', 'primary', nav='filter list, close sheet'))
    b.append(button(y + 68, 'Reset', 'ghost', nav='clear dates'))
    return scrim() + sheet(top, '\n'.join(b))


def call_detail_sheet():
    rows = [('Date', '9 Oct 2026, 10:42 AM'), ('Duration', '12m 30s'), ('Call type', 'Video'), ('Gross', '360', True),
            ('Commission (30%)', '−108', True), ('Net', '252', True)]
    h = 24 + 56 + 24 + len(rows) * 44 + 24 + 34
    top = 844 - h
    b = [avatar(52, top + 52, 56, letter='R'), t1(96, top + 24 + 23, 'Rohan_K', 18, 700, NAVY), t1(96, top + 24 + 44, 'Video call', 12, 500, SLATE)]
    y = top + 24 + 56 + 24
    for r in rows:
        lbl, val = r[0], r[1]
        net = lbl == 'Net'
        b.append(t1(24, y + 27, lbl, 14 if net else 15, 600 if net else 400, NAVY if net else SLATE))
        b.append(t1(366, y + 27, val, 16 if net else 15, 700 if net else 500, NAVY, 'end'))
        if len(r) > 2:
            b.append(gem(366 - tw(val, 16 if net else 15, 700 if net else 500) - 22, y + 13, 18))
        if lbl == 'Commission (30%)':
            b.append(f'<rect x="24" y="{y + 43}" width="342" height="1" fill="{BORDER}"/>')
        y += 44
    b.append('<!-- No gifts row at Launch -->')
    return scrim() + sheet(top, '\n'.join(b))


def gen_25():
    F, ID, N = '25_Host-Call-History', '25', 'Host-Call-History'
    frame(F, ID, N, 'Default', s25_body(), note='Grouped by date, sticky headers, pull-to-refresh')
    frame(F, ID, N, 'Filter-Missed', s25_body('Missed'))
    frame(F, ID, N, 'Loading-More', s25_body(scroll=360), note='Spinner row at end while next page loads')
    frame(F, ID, N, 'Date-Range-Sheet', s25_body(overlay=date_range_sheet()))
    frame(F, ID, N, 'Call-Detail-Sheet', s25_body(overlay=call_detail_sheet()), note='Commission default 30% per PRD')
    frame(F, ID, N, 'Loading', s25_body(state='loading'))
    frame(F, ID, N, 'Empty', s25_body(state='empty'))
    frame(F, ID, N, 'Empty-Filtered', s25_body('Rejected', state='empty-filtered'))
    frame(F, ID, N, 'Error', s25_body(state='error'))
    frame(F, ID, N, 'Offline-Cached', s25_body(top_banner=banner(115, "You're offline. Showing your last saved calls.", 'offline')))


# ============================================================ 26 Host Profile & Rates
def status_pill(x, y, label='Under review'):
    pw = tw(label, 12, 600) + 40
    return ('<!-- StatusPill (shared, owner: Abid) -->'
            f'<rect x="{x:.0f}" y="{y}" width="{pw:.0f}" height="28" rx="14" fill="{WHITE}" stroke="{WARN}" stroke-width="1.5"/>'
            + icon('clock', round(x + 10), y + 6, WARN, 16) + t1(round(x + 32), y + 18, label, 12, 600, NAVY)), pw


def cover(y, state):
    o = [f'<!-- Cover photo uploader ({state}) → photo picker + crop (from 06) -->']
    if state == 'empty':
        o.append(f'<rect x="24" y="{y}" width="342" height="192" rx="16" fill="{BTINT}"/>' + icon('camera', 183, y + 70, BLUE))
        o.append(t1(195, y + 120, 'Add cover photo', 14, 600, BLUE, 'middle'))
        o.append(hit(24, y, 342, 192, 'cover'))
        return '\n'.join(o)
    o.append(f'<clipPath id="cov"><rect x="24" y="{y}" width="342" height="192" rx="16"/></clipPath>'
             f'<g clip-path="url(#cov)"><rect x="24" y="{y}" width="342" height="192" fill="{CTINT}"/>'
             f'<circle cx="300" cy="{y + 30}" r="70" fill="{BTINT}"/><circle cx="195" cy="{y + 82}" r="44" fill="{CORAL}" opacity="0.45"/>'
             f'<ellipse cx="195" cy="{y + 210}" rx="96" ry="72" fill="{CORAL}" opacity="0.45"/>'
             + photo_img(24, y, 342, 192, 'priya_full.jpg', 'xMidYMid'))
    if state == 'uploading':
        o.append(f'<rect x="24" y="{y}" width="342" height="192" fill="{NAVY}" opacity="0.4"/>')
    if state == 'rejected':
        o.append(f'<rect x="24" y="{y}" width="342" height="192" fill="{NAVY}" opacity="0.55"/>')
    o.append('</g>')
    if state == 'uploading':
        o.append(f'<rect x="64" y="{y + 92}" width="262" height="8" rx="4" fill="{WHITE}" opacity="0.4"/>'
                 f'<rect x="64" y="{y + 92}" width="160" height="8" rx="4" fill="{WHITE}"/>' + t1(195, y + 124, 'Uploading… 60%', 14, 600, WHITE, 'middle'))
    elif state == 'review':
        o.append(status_pill(36, y + 12)[0])
    elif state == 'rejected':
        o.append(icon('alert-circle', 183, y + 60, WHITE) + t1(195, y + 112, "This photo can't be used.", 14, 600, WHITE, 'middle')
                 + t1(195, y + 132, 'Try another one.', 13, 400, WHITE, 'middle'))
    o.append(hit(24, y, 342, 192, 'cover'))
    if state in ('photo', 'review', 'rejected'):
        lbl = 'Change'
        cw = tw(lbl, 12, 600) + 44
        o.append('<!-- "Change" chip → photo picker -->'
                 f'<rect x="{354 - cw:.0f}" y="{y + 148}" width="{cw:.0f}" height="32" rx="16" fill="{WHITE}"/>'
                 + icon('camera', round(354 - cw + 12), y + 156, NAVY, 16) + t1(round(354 - cw + 34), y + 169, lbl, 12, 600, NAVY))
    return '\n'.join(o)


def waveform(x, y, w, played=0.0, live=False, color=BLUE):
    o = []
    n = int(w / 6)
    for i in range(n):
        h = 6 + 18 * abs(math.sin(i * 0.9) * math.cos(i * 0.37))
        c = color if (i / n) <= played or live else DIS_BG
        if live and i > n * 0.6:
            c = DIS_BG
            h = 4
        o.append(f'<rect x="{x + i * 6}" y="{y - h / 2:.1f}" width="3" height="{h:.1f}" rx="1.5" fill="{c}"/>')
    return ''.join(o)


def audio_card(y, state):
    o = [f'<!-- Intro audio recorder ({state}) -->', card(24, y, 342, 120)]
    o.append(t1(40, y + 16 + 15, 'Intro audio', 14, 600, NAVY))
    if state == 'review':
        pw = tw('Under review', 12, 600) + 40
        o.append(status_pill(350 - pw, y + 12)[0])
    by = y + 48
    if state in ('recorded', 'review', 'uploading'):
        o.append(f'<!-- Play intro -->'f'<circle cx="68" cy="{by + 28}" r="28" fill="{BTINT}"/>' + icon('play', 58, by + 16, BLUE))
    else:
        o.append(f'<!-- Record button (Coral) → start/stop recording -->'
                 f'<circle cx="68" cy="{by + 28}" r="28" fill="{CORAL}"/>'
                 + (f'<rect x="58" y="{by + 18}" width="20" height="20" rx="4" fill="{WHITE}"/>' if state == 'recording' else icon('mic', 56, by + 16, WHITE)))
    o.append(hit(40, by, 56, 56, 'record'))
    if state == 'empty':
        o.append(t1(112, by + 24, 'Record a short hello', 15, 500, NAVY) + t1(112, by + 44, 'Tap to start recording', 12, 500, SLATE))
    elif state == 'recording':
        o.append(waveform(112, by + 22, 170, live=True, color=CORAL) + t1(112, by + 50, 'Recording… 00:07', 12, 500, CORAL))
    elif state == 'uploading':
        o.append(f'<rect x="112" y="{by + 20}" width="238" height="6" rx="3" fill="{BORDER}"/><rect x="112" y="{by + 20}" width="140" height="6" rx="3" fill="{BLUE}"/>'
                 + t1(112, by + 46, 'Uploading… 60%', 12, 500, SLATE))
    else:
        o.append(waveform(112, by + 22, 170, played=0.35) + t1(112, by + 50, '00:04 / 00:12', 12, 500, SLATE))
        o.append('<!-- Re-record → recording; Delete → empty -->'
                 + icon('rotate-ccw', 290, by + 38, SLATE, 20) + icon('trash', 326, by + 38, SLATE, 20))
    return '\n'.join(o)


GREET = 'Hi! I love talking about music, movies and life. Say hello anytime.'


def s26_content(cov='photo', aud='recorded', greet=GREET, gstate='filled', limit=False, rate_locked=False):
    o = []
    y = 119
    o.append(cover(y, cov))
    y += 192 + 24
    o.append(audio_card(y, aud))
    y += 120 + 24
    o.append(t1(24, y + 15, 'Greeting', 14, 600, NAVY))
    y += 28
    gl = len(wrap(greet, 310, 16, 500)) if greet else 1
    gh = max(96, gl * 24 + 28)
    o.append(input_box(y, greet, 'Say hello to your callers', gstate, h=gh, multiline=True))
    y += gh + 8
    cnt = '120/120' if limit else f'{len(greet or "")}/120'
    o.append(t1(366, y + 14, cnt, 13, 400, ERROR if limit else SLATE, 'end'))
    if limit:
        o.append(t1(24, y + 14, "That's the limit", 13, 500, ERROR))
    y += 19 + 24
    o.append(t1(24, y + 15, 'Languages', 14, 600, NAVY))
    o.append('<!-- "Edit" → 09A as sheet -->' + t1(366, y + 15, 'Edit', 14, 600, BLUE, 'end') + hit(318, y - 12, 48, 44, 'link:Edit'))
    y += 20 + 12
    s, y = chips_wrap(24, y, [('Hindi', 'readonly'), ('English', 'readonly'), ('Kannada', 'readonly')])
    o.append(s)
    y += 24
    h = 16 + 78 + 20 + 78 + 12 + 38 + 16
    o.append('<!-- Rates card -->' + card(24, y, 342, h))
    ry = y + 16
    for lbl, val, pct, lo, hi in [('Voice', '40/min', (40 - 30) / 50, '30', '80'), ('Video', '90/min', (90 - 60) / 90, '60', '150')]:
        o.append(t1(40, ry + 15, lbl, 14, 600, NAVY))
        pw = tw(val, 14, 600) + 48
        o.append(f'<rect x="{350 - pw:.0f}" y="{ry - 4}" width="{pw:.0f}" height="28" rx="14" fill="{BTINT}"/>'
                 + gem(round(350 - pw + 10), ry + 2, 16) + t1(round(350 - pw + 32), ry + 15, val, 14, 600, NAVY))
        o.append(slider(52, ry + 44, 286, pct, rate_locked))
        o.append(t1(40, ry + 74, lo, 12, 500, SLATE) + t1(350, ry + 74, hi, 12, 500, SLATE, 'end'))
        ry += 98
    ry -= 8
    if rate_locked:
        s, _ = err_msg(40, ry, 'You can change your rate again in 42 min.', w=310, color=SLATE, icon_name='lock', weight=400)
    else:
        s, _ = text(40, ry, 'New rates apply to new calls. You can change them once an hour.', 'notice', w=310)
    o.append(s)
    y += h + 24
    o.append(card(24, y, 342, 112))
    o.append(menu_row(y, 'Account settings', 'settings', '40'))
    o.append(menu_row(y + 56, 'Switch to User view', 'arrow-left-right', '13', last=True))
    return '\n'.join(o)


def s26_body(scroll=0, save=None, overlay=None, top_banner=None, **kw):
    o = [blobs(bottom=False)]
    bottom = BAR_TOP - 16 - 56 - 24 if save else CONTENT_BOTTOM
    y0 = 103
    if top_banner:
        b, bb = top_banner
        o.append(b)
        y0 = bb + 4
    o.append(clip_group('c26', y0, bottom, s26_content(**kw), scroll))
    if save:
        o.append(button(BAR_TOP - 16 - 56, 'Save', save, nav='stay on 26 + toast "Saved"'))
    o.append(topbar(None, tab_title='My profile'))
    o.append(status_bar())
    o.append(host_bar(4))
    if overlay:
        o.append(overlay)
    o.append(home_indicator())
    return '\n'.join(o)


def gen_26():
    F, ID, N = '26_Host-Profile-Rates', '26', 'Host-Profile-Rates'
    edited = GREET + ' Let’s chat!'
    frame(F, ID, N, 'View', s26_body(), note='No changes: no Save button')
    frame(F, ID, N, 'View-Scrolled', s26_body(scroll=540))
    frame(F, ID, N, 'Edited', s26_body(save='primary', greet=edited, gstate='focused'), note='Save appears above the bar')
    frame(F, ID, N, 'Saving', s26_body(save='primary-loading', greet=edited))
    frame(F, ID, N, 'Saved-Toast', s26_body(overlay=toast(BAR_TOP - 16 - 48, 'Saved')))
    frame(F, ID, N, 'Cover-Empty', s26_body(cov='empty', aud='empty', greet=None, gstate='empty'))
    frame(F, ID, N, 'Cover-Uploading', s26_body(cov='uploading'))
    frame(F, ID, N, 'Cover-Under-Review', s26_body(cov='review'))
    frame(F, ID, N, 'Cover-Rejected', s26_body(cov='rejected'))
    frame(F, ID, N, 'Audio-Empty', s26_body(aud='empty'))
    frame(F, ID, N, 'Audio-Recording', s26_body(aud='recording'), note='Max length not in PRD (question)')
    frame(F, ID, N, 'Audio-Recorded', s26_body(aud='recorded', save='primary'))
    frame(F, ID, N, 'Audio-Uploading', s26_body(aud='uploading'))
    frame(F, ID, N, 'Audio-Under-Review', s26_body(aud='review'))
    long = 'Hi! I love talking about music, movies, food and life. Tell me about your day, I am a good listener. Say hi!'
    frame(F, ID, N, 'Greeting-At-Limit', s26_body(save='primary', greet=long, gstate='focused', limit=True),
          note='Limit not in PRD; 120 assumed (question)')
    frame(F, ID, N, 'Rate-Locked', s26_body(scroll=540, rate_locked=True))
    frame(F, ID, N, 'Offline', s26_body(top_banner=offline_banner(107)))
    frame(F, ID, N, 'Error', s26_body(save='primary', greet=edited,
          top_banner=banner(107, "We couldn't save your changes. Try again in a moment.", 'error')))
    frame(F, ID, N, 'Unsaved-Changes-Dialog', s26_body(save='primary', greet=edited,
          overlay=dialog('Save your changes?', "You've edited your profile. Save before you leave?",
                         [('Save', 'primary', 'save, then go to tapped tab'), ('Discard', 'ghost', 'go to tapped tab')])))


def gen_all():
    gen_24(); gen_25(); gen_26()
