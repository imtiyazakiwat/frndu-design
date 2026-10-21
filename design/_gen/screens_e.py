"""Girish batch 1: 00 App Shell, 00.1 Side Drawer, 13 Home, 13.1 Quick Match, 14 Filter & Search, 15 Radar, 16 Host Profile."""
from lib2 import *
from illus import hero_clock, portrait, dashes3, sparks


def compose(content, header='', actions='', bar='', overlay='', scroll=0, clip=(103, 714), top_blob=True, bottom_blob=False, cid='cc'):
    o = [blobs(top=top_blob, bottom=bottom_blob)]
    o.append(clip_group(cid, clip[0], clip[1], content, scroll) if clip else content)
    o += [actions, header, status_bar(), bar, overlay, home_indicator()]
    return '\n'.join(x for x in o if x)


def spec_note(label, y=127):
    """Small spec caption under the top bar on specimen frames (not app UI)."""
    return f'<!-- Spec note (not app UI) -->' + t1(24, y + 12, label, 12, 600, TERT)


# ============================================================ 00 App Shell
def not_built(scr, lbl):
    """Tab root whose screen is not designed yet: tab header + a plain note (no fake content)."""
    names = {'27': 'Chat List', '30': 'Recharge Store', '40': 'Profile & Settings', '32': 'Host Wallet & Payout'}
    return compose(empty_state(400, 'clock', f'{scr} {names.get(scr, lbl)}', 'This screen is in the next design batch.'),
                   tab_header(lbl), clip=None)


def tab_root(scr, lbl, bar):
    """Real screen content behind the bar where the screen exists (13, 24, 25, 26)."""
    from screens_d import s24_body, s25_body, s26_body
    if scr == '13':
        return home_body(bar=bar)
    if scr in ('24', '25', '26'):
        return {'24': s24_body, '25': s25_body, '26': s26_body}[scr]()
    import screens_g
    import screens_h
    host = 'htab' in bar
    if scr == '27':
        return screens_g.s27(host=host)
    if scr == '30':
        return screens_g.s30()
    if scr == '40':
        return screens_h.s40()
    if scr == '32':
        return screens_h.s32()
    return not_built(scr, lbl) + bar


def gen_00():
    F, ID, N = '00_App-Shell', '00', 'App-Shell'
    for i, (lbl, ic, scr) in enumerate(USER_TABS):
        frame(F, ID, N, f'User-Tab-{lbl}', tab_root(scr, lbl, user_bar(i, 3)), note=f'User bar 4 × 97.5; tab {i + 1} active → {scr}')
    for i, (lbl, ic, scr) in enumerate(HOST_TABS):
        body = tab_root(scr, lbl, host_bar(i, 3))
        frame(F, ID, N, f'Host-Tab-{lbl}', body, note=f'Host bar 5 × 78; tab {i + 1} active → {scr}')
    for n, nm in [(0, 'Badge-0'), (7, 'Badge-1-Digit'), (24, 'Badge-2-Digits'), (140, 'Badge-99-Plus')]:
        frame(F, ID, N, nm, home_body(bar=user_bar(0, n)), note=f'Messages badge = {n}')
    frame(F, ID, N, 'Tab-Pressed', home_body(bar=user_bar(0, 3, pressed=1)), note='Messages tab pressed')
    kb = compose(spec_note('Bottom bar hidden while the keyboard is open') + input_box(452, 'Hello', None, 'focused'),
                 tab_header('Messages'), clip=None, overlay=keyboard('alpha'))
    frame(F, ID, N, 'Keyboard-Bar-Hidden', kb)
    # TopBar variants
    def tb(h, label):
        return compose(spec_note(label), h, clip=None)
    frame(F, ID, N, 'TopBar-T1-No-Title', tb(topbar1(None, nav_back='previous'), 'T1 Standard · back only'))
    frame(F, ID, N, 'TopBar-T1-Title', tb(topbar1('Notifications', nav_back='previous'), 'T1 · back + centred H4 title'))
    frame(F, ID, N, 'TopBar-T1-One-Action', tb(topbar1('Transaction history', right='mail', nav_back='previous'), 'T1 · one right action (x 330–378)'))
    frame(F, ID, N, 'TopBar-T1-Two-Actions', tb(topbar1(None, right='more-vertical', right2='heart', nav_back='previous'), 'T1 · two right actions (slot 2 hit right edge x 330)'))
    frame(F, ID, N, 'TopBar-T2-Tab-Root', tb(tab_header('Messages', icon('search', 342, 63, NAVY) + hit(330, 51, 48, 48, 'right:search')), 'T2 · H2 at x 24'))
    t3 = video_scene('girl') + media_btn(12, 51, 'arrow-left', 'back') + media_btn(330, 51, 'more-vertical', 'right:more') + media_btn(282, 51, 'heart', 'right2:heart')
    frame(F, ID, N, 'TopBar-T3-Media', t3 + status_bar(WHITE) + home_indicator(WHITE))
    t4 = scrim() + sheet(180, text(24, 204, 'Sheet title', 'h3')[0] + icon('x', 342, 200, NAVY) + hit(330, 188, 48, 48, 'close')
                         + spec_note('T4 · sheet title H3 at x 24, close 48 × 48 at x 330', 240))
    frame(F, ID, N, 'TopBar-T4-Sheet', home_body(overlay=t4))
    ruler = [compose('', topbar1('Title', right='more-vertical', right2='heart'), clip=None)]
    R = ERROR
    ruler.append(f'<g opacity="0.85"><rect x="12" y="51" width="48" height="48" fill="none" stroke="{R}" stroke-dasharray="3 3"/>'
                 f'<rect x="330" y="51" width="48" height="48" fill="none" stroke="{R}" stroke-dasharray="3 3"/>'
                 f'<rect x="282" y="51" width="48" height="48" fill="none" stroke="{R}" stroke-dasharray="3 3"/>'
                 f'<rect x="0" y="47" width="390" height="56" fill="none" stroke="{BLUE}" stroke-dasharray="4 4"/>'
                 f'<line x1="24" y1="40" x2="24" y2="120" stroke="{R}"/><line x1="366" y1="40" x2="366" y2="120" stroke="{R}"/></g>'
                 + t1(26, 118, 'x 24 · back icon left edge', 11, 600, R) + t1(364, 132, 'x 366 · right icon edge', 11, 600, R, 'end')
                 + t1(14, 112, 'hit 48×48 from x 12', 11, 600, R) + t1(195, 44, 'bar 56 (y 47–103)', 11, 600, BLUE, 'middle')
                 + t1(330, 112, '378', 11, 600, R) + t1(282, 146, 'slot 2 → 330', 11, 600, R))
    frame(F, ID, N, 'TopBar-Ruler', '\n'.join(ruler), note='Positions for every designer to check against')


# ============================================================ 00.1 Side Drawer
USER_MENU = [[('Profile & Settings', 'user', '40'), ('Recharge Diamonds', 'gem', '30'), ('Transaction History', 'receipt', '31')],
             [('Blocked Users', 'user-x', '41'), ('Notifications', 'bell', '60'), ('Language', 'languages', '01.1')],
             [('Safety Center', 'shield-check', '59'), ('Help Center', 'life-buoy', '65'), ('About Frndu', 'info', '63')]]
HOST_MENU = [[('Switch to User view', 'arrow-left-right', '13')],
             [('Profile & Settings', 'user', '40'), ('Earnings', 'wallet', '32'), ('Call History', 'phone', '25')],
             [('Notifications', 'bell', '60'), ('Language', 'languages', '01.1')],
             [('Safety Center', 'shield-check', '59'), ('Help Center', 'life-buoy', '65'), ('About Frndu', 'info', '63')]]
DW = 292


def drawer(host=False, offset=0, pressed=None, nickname=None, switch_host=False, labels=None, scroll=0, scrim_op=0.4):
    nick = nickname or ('Priya' if host else ME['name'])
    x0 = -offset
    o = [f'<rect x="0" y="0" width="390" height="844" fill="{NAVY}" opacity="{scrim_op}"/>' + hit(DW - offset, 0, 390, 844, 'scrim'),
         f'<!-- SideDrawer (owner: Girish) width {DW} = 75% -->',
         f'<g transform="translate({x0} 0)"><clipPath id="dwc"><rect width="{DW}" height="844"/></clipPath>'
         f'<rect x="0" y="0" width="{DW}" height="844" fill="{CREAM}" filter="url(#sh-lg)"/>' + hit(0, 0, DW, 844, 'sheet'),
         f'<g clip-path="url(#dwc)"><g filter="url(#blur-xl)"><ellipse cx="240" cy="40" rx="140" ry="130" fill="{BLUE}" {cloud("cl-b3")}/>'
         f'<ellipse cx="20" cy="820" rx="120" ry="110" fill="{CORAL}" {cloud("cl-c3")}/></g></g>',
         glass(12, 56, DW - 24, 236, 24)]
    o.append(avatar(60, 107, 72, photo=host, letter=None if host else nick[0]) + hit(24, 71, 72, 72, 'avatar'))
    nm = nick if tw(nick, 22, 700) < 240 else nick[:16] + '…'
    o.append(t1(24, 177, nm, 22, 700, NAVY, ls=-0.2))
    o.append(t1(24, 200, 'ID: 4821930', 12, 500, SLATE) + icon('copy', 100, 187, SLATE, 16) + hit(88, 176, 44, 44, 'copy'))
    if host:
        o.append(diamond_pill(24 + 196, 219, '12,400', plus=False, key='pill:earnings', label='Available 12,400'))
    else:
        o.append(diamond_pill(24 + 120, 219, ME['balance']))
    o.append(t1(24, 287, 'Edit profile', 14, 600, BLUE) + hit(24, 266, 120, 44, 'link:Edit profile'))
    o.append(f'<rect x="0" y="303" width="{DW}" height="1" fill="{BORDER}"/>')
    groups = HOST_MENU if host else ([[('Switch to Host mode', 'arrow-left-right', '24')]] + USER_MENU if switch_host else USER_MENU)
    rows = []
    y = 312
    for gi, g in enumerate(groups):
        for lbl, ic, nav in g:
            lab = (labels or {}).get(lbl, lbl)
            h = 64 if nlines(lab, 'bodyM', DW - 24 - 36 - 40) > 1 else 56
            rows.append(menu_row(y, lbl, ic, nav, x=0, w=DW, pad=24, last=True, pressed=pressed == lbl, h=h, chevron=False))
            if lab != lbl:
                rows[-1] = rows[-1].replace(f'>{esc(lbl)}</text>', '></text>')
                rows[-1] += text(60, y + (h - 2 * 22) / 2, lab, 'bodyM', w=DW - 60 - 24)[0]
            y += h
        if gi < len(groups) - 1:
            rows.append(f'<rect x="24" y="{y + 8}" width="{DW - 48}" height="1" fill="{BORDER}"/>')
            y += 17
    o.append(clip_group('dwm', 304, 690, '\n'.join(rows), scroll))
    o.append(f'<rect x="0" y="690" width="{DW}" height="1" fill="{CBORDER}"/>')
    o.append(menu_row(704, 'Log Out', 'log-out', 'confirm dialog, then 01', x=0, w=DW, pad=24, last=True, chevron=False))
    o.append(t1(24, 786, 'Frndu v1.0.0', 12, 500, SLATE))
    o.append('</g>')
    return '\n'.join(o)


def gen_001():
    F, ID, N = '00.1_Side-Drawer', '00.1', 'Side-Drawer'
    base = home_body()
    hbase = None
    frame(F, ID, N, 'Opening', base + drawer(offset=146, scrim_op=0.2), note='Panel slides in 250–350 ms, scrim fades in')
    frame(F, ID, N, 'Open-User', base + drawer(), note='Opened from 13 avatar or left-edge swipe')
    frame(F, ID, N, 'Open-Scrolled', base + drawer(scroll=150), note='Menu scrolls; Log Out stays pinned')
    frame(F, ID, N, 'Row-Pressed', base + drawer(pressed='Recharge Diamonds'))
    frame(F, ID, N, 'ID-Copied', base + drawer() + toast(674, 'ID copied'))
    frame(F, ID, N, 'Long-Nickname', base + drawer(nickname='Aarav_the_storyteller_22'))
    frame(F, ID, N, 'Approved-Host-User-Drawer', base + drawer(switch_host=True), note='Approved host browsing as user')
    frame(F, ID, N, 'Hindi-Labels', base + drawer(labels={'Profile & Settings': 'प्रोफ़ाइल और सेटिंग्स', 'Recharge Diamonds': 'डायमंड रिचार्ज करें',
                                                          'Transaction History': 'लेन-देन का इतिहास', 'Blocked Users': 'ब्लॉक किए गए उपयोगकर्ता',
                                                          'Safety Center': 'सुरक्षा केंद्र'}), note='Labels wrap to 2 lines max; row grows to 64')
    from screens_d import s24_body
    frame(F, ID, N, 'Open-Host', s24_body('off') + drawer(host=True), note='Opened from 24 avatar')
    frame(F, ID, N, 'Closing', base + drawer(offset=220, scrim_op=0.1))


# ============================================================ 13 Home Feed
CATS = ['Popular', 'New', 'Video Hosts', 'Audio Hosts', 'Nearby']


def home_banner(y):
    cid = 'hb'
    blob = (f'M262 {y + 22} C292 {y + 2} 344 {y + 14} 352 {y + 52} C362 {y + 96} 336 {y + 132} 296 {y + 130} '
            f'C258 {y + 128} 236 {y + 100} 238 {y + 70} C240 {y + 46} 246 {y + 32} 262 {y + 22} Z')
    return (f'<!-- Banner carousel (server images) → 16 or 30 -->'
            + glass(24, y, 342, 140, 24) + f'<rect x="24" y="{y}" width="342" height="140" rx="24" fill="{BTINT}" opacity="0.65"/>'
            + f'<path d="{blob}" fill="{BLUE}" opacity="0.18" transform="translate(4 4)" filter="url(#blur-md)"/>'
            + f'<path d="{blob}" fill="{WHITE}" opacity="0.7" transform="translate(0 0) scale(1)" filter="url(#blur-md)"/>'
            + f'<clipPath id="{cid}"><path d="{blob}"/></clipPath><g clip-path="url(#{cid})"><rect x="230" y="{y}" width="140" height="140" fill="{CTINT}"/>'
            + photo_img(232, y, 136, 136, 'priya.jpg', 'xMidYMin') + '</g>'
            + sparks(244, y + 16, BLUE, flip=True, s=0.7)
            + t1(44, y + 44, 'Meet Priya tonight', 18, 700, NAVY) + text(44, y + 54, 'Video calls from 80 per min. Say hello.', 'notice', w=180)[0]
            + glass(44, y + 94, 92, 32, 16) + t1(60, y + 115, 'Say hi', 13, 600, NAVY) + icon('arrow-right', 106, y + 102, BLUE, 16)
            + hit(24, y, 342, 140, 'banner')
            + ''.join(f'<circle cx="{195 - 16 + i * 16}" cy="{y + 156}" r="4" fill="{BLUE if i == 0 else BORDER}"/>' for i in range(3)))


def home_content(cat='Popular', nearby=True, filters=False, hosts=None, missing=None, longname=False, loadmore=False, guest=False, offline=False, refresh=False):
    o = []
    y = 115
    if guest or offline:
        b, bb = (banner(y, 'Host verification in progress', 'clock') if guest else banner(y, "You're offline. Showing saved hosts.", 'offline'))
        o.append(b)
        y = bb + 12
    if refresh:
        o.append(spinner(195, y + 8, BLUE, 10))
        y += 32
    o.append(f'<!-- Search row (read-only) → 14 -->' + input_box(y, None, 'Search by name or Host ID', 'empty', left_icon='search')
             .replace('data-hit="input:Search by name or Host ID"', 'data-hit="search"'))
    o.append(f'<circle cx="338" cy="{y + 28}" r="20" fill="{WHITE}" filter="url(#sh-sm)"/>' + icon('sliders-horizontal', 328, y + 18, NAVY, 20)
             + hit(314, y + 4, 48, 48, 'filters'))
    if filters:
        o.append(f'<circle cx="353" cy="{y + 12}" r="8" fill="{CORAL}" stroke="{WHITE}" stroke-width="1.5"/>' + t1(353, y + 16, '2', 10, 700, WHITE, 'middle'))
    y += 56 + 16
    o.append(home_banner(y))
    y += 140 + 12 + 8 + 12
    cats = CATS if nearby else CATS[:-1]
    s, _ = chips_wrap(24, y, [(c, 'selected' if c == cat else 'unselected') for c in cats], maxw=600)
    o.append('<!-- Category tabs (horizontal scroll) -->' + s)
    y += 40 + 16
    hs = hosts if hosts is not None else HOSTS
    def hx(i, h):
        hh = dict(h)
        if longname and i == 0:
            hh['name'] = 'Priyanka Venkataraman'
            hh['langs'] = ['Hindi', 'English', 'Tamil', 'Telugu']
        return hh
    # Featured carousel (Home ref): 165 cards, 8 gap, the third card peeks at the right edge
    car = [host_card(24 + i * 173, y, hx(i, h), missing=(missing == i)) for i, h in enumerate(hs[:3])]
    if car:
        o.append(f'<!-- Host carousel (horizontal scroll, next card peeks) -->' + '\n'.join(car))
    y += HOST_CARD_H + 72   # 'All hosts' starts below the fold (under Quick Match)
    # Rest of the feed: two-column grid of the same card (scrolls under Quick Match)
    if len(hs) > 3:
        o.append(t1(24, y + 18, 'All hosts', 18, 700, NAVY))
        y += 26 + 12
        for j, h in enumerate(hs[3:] + hs[:3]):
            x = 24 + (j % 2) * 177
            o.append(host_card(x, y + (j // 2) * (HOST_CARD_H + 12), hx(j + 3, h)))
        y += ((len(hs) + 1) // 2) * (HOST_CARD_H + 12)
    if loadmore:
        o.append(spinner(195, y + 12, BLUE, 10))
    return '\n'.join(o)


def quick_match_btn(y=None):
    y = y if y is not None else NAV_Y - 16 - 56
    w = 24 + 24 + 12 + tw('Quick Match', 16, 700) + 12 + 20 + 24
    x = 195 - w / 2
    return (f'<!-- Quick Match (primary, floating, centred) → 13.1 -->'
            f'<rect x="0" y="{y - 40}" width="390" height="{NAV_Y - y + 40}" fill="url(#g-fade)"/>'
            f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="56" rx="28" fill="url(#g-coral)" filter="url(#gl-coral)"/>'
            f'<rect x="{x + 1:.0f}" y="{y + 1}" width="{w - 2:.0f}" height="28" rx="27" fill="{WHITE}" opacity="0.10"/>'
            + icon('radar', round(x + 24), y + 16, WHITE) + t1(round(x + 60), y + 34, 'Quick Match', 16, 700, WHITE)
            + icon('arrow-right', round(x + w - 44), y + 18, WHITE, 20)
            + dashes3(round(x - 30), y + 34, CORAL, 0.75, True) + dashes3(round(x + w + 30), y + 34, CORAL, 0.75)
            + hit(round(x), y, round(w), 56, 'btn:Quick Match'))


def home_header(balance=ME['balance']):
    return ('<!-- T2 custom header: avatar → 00.1, DiamondPill → 30 (no bell at Launch) -->'
            + avatar(44, 75, 40, letter='A') + hit(20, 51, 48, 48, 'avatar') + diamond_pill(366, 55, balance))


def home_body(scroll=0, balance=ME['balance'], content=None, overlay='', qm=True, bar=None, **kw):
    c = content if content is not None else home_content(**kw)
    return compose(c, home_header(balance), quick_match_btn() if qm else '', bar or user_bar(0, 3), overlay, scroll, (103, TAB_BOTTOM), cid='c13', bottom_blob=True)


def home_loading():
    o = [skeleton(24, 115, 342, 56, 16), skeleton(24, 187, 342, 140, 20)]
    o += [skeleton(24 + i * 92, 363, 80, 40, 20) for i in range(4)]
    for i in range(3):
        x = 24 + i * 173
        y = 415
        o.append(glass(x, y, 165, 240, 24) + skeleton(x + 6, y + 6, 153, 150, 20) + skeleton(x + 12, y + 168, 90, 14) + skeleton(x + 12, y + 190, 70, 10) + skeleton(x + 12, y + 212, 110, 12))
    return '\n'.join(o)


def gen_13():
    F, ID, N = '13_Home-Feed', '13', 'Home-Feed'
    frame(F, ID, N, 'Loading', home_body(content=home_loading(), qm=False))
    frame(F, ID, N, 'Default', home_body(), note='Banners auto-scroll every 4 s; Busy/Online changes cross-fade 200 ms')
    frame(F, ID, N, 'Scrolled', home_body(scroll=300), note='88 px bottom padding keeps the last card above Quick Match')
    frame(F, ID, N, 'Filters-Active', home_body(filters=True, cat='Video Hosts', hosts=[h for h in HOSTS if h['video']]))
    frame(F, ID, N, 'Load-More', home_body(scroll=700, loadmore=True))
    frame(F, ID, N, 'Pull-To-Refresh', home_body(refresh=True))
    empty = home_content(hosts=[]) + empty_state(560, 'users', 'No hosts available right now.', 'Try Quick Match.')
    frame(F, ID, N, 'Empty', home_body(content=empty))
    frame(F, ID, N, 'Offline-Cached', home_body(offline=True))
    frame(F, ID, N, 'Guest-Verification-Pending', home_body(guest=True), note='Banner component from 10')
    frame(F, ID, N, 'Balance-Zero', home_body(balance='0'))
    frame(F, ID, N, 'Balance-Five-Digit', home_body(balance='12,480'))
    frame(F, ID, N, 'Long-Name-Missing-Photo', home_body(longname=True, missing=1))
    frame(F, ID, N, 'Without-Nearby', home_body(nearby=False), note='If Nearby is cut (tasks.md T-31)')
    frame(F, ID, N, 'Busy-Status-Change', home_body(hosts=[dict(HOSTS[0], status='Busy')] + HOSTS[1:]), note='Online → Busy: 200 ms cross-fade, no flicker')


# ============================================================ 13.1 Quick Match Picker
def qm_sheet(sel='video', low=False, few=False, loading=False, offline=False):
    top = 844 - (24 + 30 + 16 + 128 + 16 + 38 + 16 + 44 + 24 + 56 + 34) - (60 if offline else 0)
    b = [text(24, top + 24, 'How do you want to talk?', 'h3')[0]]
    y = top + 70
    if offline:
        b.append(offline_banner(y)[0])
        y += 60
    for i, (m, ic, price) in enumerate([('voice', 'phone', 'from 30'), ('video', 'video', 'from 60')]):
        x = 24 + i * 177
        on = sel == m
        b.append(f'<!-- Mode card {m} -->')
        if on:
            b.append(f'<rect x="{x + 1}" y="{y + 1}" width="163" height="126" rx="16" fill="{BTINT}" stroke="{BLUE}" stroke-width="2"/>' + check_badge(x + 125, y + 16))
        else:
            b.append(card(x, y, 165, 128))
        b.append(icon_box(x + 16, y + 16, ic, 48, WHITE if on else BTINT, BLUE))
        b.append(t1(x + 16, y + 16 + 48 + 12 + 19, m.capitalize(), 18, 700, NAVY))
        if loading:
            b.append(skeleton(x + 16, y + 102, 90, 12))
        else:
            b.append(t1(x + 16, y + 112, f'{price} ◆/min', 12, 500, SLATE).replace('◆', '💎') if False else
                     t1(x + 16, y + 112, f'{price} ', 12, 500, SLATE) + icon('gem', x + 16 + tw(price + ' ', 12, 500), y + 101, BLUE, 14)
                     + t1(round(x + 32 + tw(price + ' ', 12, 500)), y + 112, '/min', 12, 500, SLATE))
        if few and m == 'voice':
            b.append(t1(x + 76, y + 36, 'Few hosts', 12, 600, WARN) + t1(x + 76, y + 52, 'online', 12, 600, WARN))
        b.append(hit(x, y, 165, 128, f'mode:{m}'))
    y += 128 + 16
    if low:
        s, y = err_msg(24, y, 'You need at least 1 minute of balance.', color=WARN, icon_name='alert-triangle')
    else:
        b.append(gem(24, y, 20))
        s, y = text(52, y, 'Your balance covers about 12 min.', 'notice', w=314)
    b.append(s)
    y = max(y, top + 70 + 144 + 38 + (60 if offline else 0)) + 16
    b.append(t1(24, y + 27, 'Match my languages first', 15, 500, NAVY) + switch(314, y + 6, True, BLUE, key='switch:languages'))
    y += 44 + 24
    if low:
        b.append(button(y, 'Recharge to continue', 'primary', nav='30'))
    else:
        b.append(button(y, 'Start Matching', 'disabled' if (loading or offline) else 'primary', nav='15'))
    return scrim() + sheet(top, '\n'.join(b))


def gen_131():
    F, ID, N = '13.1_Quick-Match-Picker', '13.1', 'Quick-Match-Picker'
    base = home_body()
    frame(F, ID, N, 'Video-Selected', base + qm_sheet('video'), note='Last used mode is preselected')
    frame(F, ID, N, 'Voice-Selected', base + qm_sheet('voice'))
    frame(F, ID, N, 'Balance-Too-Low', base + qm_sheet('video', low=True))
    frame(F, ID, N, 'Few-Hosts-Online', base + qm_sheet('voice', few=True))
    frame(F, ID, N, 'Loading-Prices', base + qm_sheet('video', loading=True))
    frame(F, ID, N, 'Offline', base + qm_sheet('video', offline=True))


# ============================================================ 14 Filter & Search
LANGS14 = ['Hindi', 'English', 'Kannada', 'Tamil', 'Telugu', 'Marathi', 'Bengali']


RECENT14 = ['Priya', 'H-10932', 'Ananya']
AGES14 = ['18–24', '25–34', '35–44', '45+']   # Q2 age-group filter (client update 21 Oct)


def recent_chip(x, y, label):
    """Recent search: frosted pill with a clock icon; tap runs the search again."""
    w = round(tw(label, 14, 600) + 50)
    return (f'<!-- Recent search "{label}" → search again -->' + glass(x, y, w, 36, 18, shadow=False)
            + icon('clock', x + 12, y + 10, SLATE, 16) + t1(x + 36, y + 23, label, 14, 600, NAVY) + hit(x, y, w, 36, f'recent:{label}')), w


def filters_body(y, mode, langs, ages):
    """Filter view of 14, from y down. Returns (svg, bottom). Client update 21 Oct: no price-per-minute or host-rating filter."""
    o = [t1(24, y + 15, 'Recent searches', 14, 600, NAVY) + t1(366, y + 15, 'Clear all', 14, 600, BLUE, 'end')]
    x = 24
    for r in RECENT14:
        s, w = recent_chip(x, y + 28, r)
        o.append(s)
        x += w + 8
    y += 28 + 36 + 24
    o.append(t1(24, y + 15, 'Call mode', 14, 600, NAVY))
    o.append(seg_tabs(y + 28, ['All', 'Video Only', 'Voice Only'], ['All', 'Video Only', 'Voice Only'].index(mode), key='mode'))
    y += 28 + 48 + 24
    o.append(t1(24, y + 15, 'Language', 14, 600, NAVY) + t1(366, y + 15, 'Show all', 14, 600, BLUE, 'end') + hit(290, y - 12, 76, 44, 'link:Show all'))
    s, y = chips_wrap(24, y + 28, [(l, 'selected' if l in langs else 'unselected') for l in LANGS14])
    o.append(s)
    if ages is not None:
        y += 24
        o.append('<!-- Q2 (Jan–Mar 2027): Age group filter, multi-select; not in the Launch build -->'
                 + t1(24, y + 15, 'Age group', 14, 600, NAVY) + status_pill(24 + tw('Age group', 14, 600) + 8, y + 1, 'Q2')[0])
        s, y = chips_wrap(24, y + 28, [(a, 'selected' if a in ages else 'unselected') for a in AGES14])
        o.append(s.replace('data-hit="chip:', 'data-hit="age:'))
    return '\n'.join(o), y


def filter_sheet(mode='All', langs=(), query=None, state='filters', reset=True, ages=None):
    """14 Search & filters. "Vertical scaling" (client update 21 Oct): the sheet is as tall as its content, so it shrinks
    now that price and rating are gone, grows with extra sections (Q2 age group) and opens to 90% for search results."""
    def body(top):
        b = [text(24, top + 24, 'Search & filters', 'h3')[0], icon('x', 342, top + 22, NAVY) + hit(330, top + 10, 48, 48, 'close')]
        y = top + 70
        b.append(input_box(y, query, 'Search by name or Host ID', 'focused' if query else 'empty', left_icon='search'))
        y += 56 + 24
        if state == 'filters':
            s, y = filters_body(y, mode, langs, ages)
            b.append(s)
            y += 24
            b.append(button(y, 'Apply Filters', 'primary', nav='13 (filtered feed)'))
            y += 56 + 12
            b.append(button(y, 'Reset Filters', 'ghost' if reset else 'ghost-disabled', nav='reset'))
            y += 56
        elif state == 'searching':
            b.append(skeleton_rows(y, 5))
        elif state == 'results':
            for i, h in enumerate(HOSTS[:4]):
                b.append(list_row(y + i * 72, h['name'], h['hid'], lead=lambda x, yy, h=h: f'<g>{host_photo(x, yy, 48, 48, h, r_all=24, scale=0.4)}</g>',
                                  right=lambda xr, yy, hh, h=h: status_badge(xr - tw(h['status'], 12, 600) - 28, yy + 24, h['status'])[0], key=f'host:{h["name"]}'))
        elif state == 'noresults':
            b.append(empty_state(y + 140, 'search', 'No hosts found.', 'Try another name or Host ID.'))
        elif state in ('offline', 'error'):
            s, y = (offline_banner(y) if state == 'offline' else banner(y, "We couldn't load filters. Try again in a moment.", 'error'))
            b.append(s)
            y += 24
            b.append(button(y, 'Try again', 'secondary', nav='retry'))
            y += 56
        return '\n'.join(b), y
    if state in ('searching', 'results', 'noresults'):
        top = 84   # results get the tall sheet
    else:
        _, bottom = body(0)
        top = 844 - 50 - bottom   # content height + 50 below the last button (home indicator area)
    b, _ = body(top)
    return scrim() + sheet(top, b)


def gen_14():
    F, ID, N = '14_Filter-Search', '14', 'Filter-Search'
    base = home_body()
    frame(F, ID, N, 'Default', base + filter_sheet(reset=False),
          note='Client update 21 Oct: price-per-minute and host-rating filters removed. Sheet height follows its content (vertical scaling); results open at 90%')
    frame(F, ID, N, 'Filters-Changed', base + filter_sheet('Video Only', ('Hindi', 'Kannada')))
    frame(F, ID, N, 'Nothing-Selected', base + filter_sheet(reset=False), note='Reset disabled')
    frame(F, ID, N, 'Searching', base + filter_sheet(query='Pri', state='searching'))
    frame(F, ID, N, 'Results', base + filter_sheet(query='Pri', state='results'), note='Results never include hosts without the selected mode')
    frame(F, ID, N, 'No-Results', base + filter_sheet(query='Zxq', state='noresults'))
    frame(F, ID, N, 'Offline', base + filter_sheet(state='offline'))
    frame(F, ID, N, 'Error', base + filter_sheet(state='error'))
    frame(F, ID, N, 'Q2-Age-Group', base + filter_sheet('All', ('Hindi',), ages=('25–34',)),
          note='Q2 (Jan–Mar 2027), not in the Launch build: filter hosts by age group, using the ages collected in 06. The sheet grows by one section')


# ============================================================ 15 Matching Radar
def radar_body(mode='Video', state='searching'):
    o = [blobs()]
    if state == 'offline':
        o.append(offline_banner(63)[0])
    if state == 'nohosts':
        o.append(hero_clock(150))
        s, y = text(195, 350, 'No hosts available right now', 'h2', anchor='middle', w=300)
        o.append(s + text(195, y + 8, 'Try again in a moment.', 'body', anchor='middle')[0])
        a, _ = action_area([('btn', 'Try again', 'primary', 'restart matching'), ('btn', 'Back to home', 'ghost', '13')])
        o.append(a)
    else:
        p, _ = pill(195, 111 if state == 'offline' else 63, f'{mode} match', BTINT, BLUE, 'video' if mode == 'Video' else 'phone', anchor='middle')
        p = p.replace(f'fill="{BTINT}" opacity="1.0"', 'fill="url(#g-glass)" stroke="#FFFFFF" filter="url(#sh-sm)"')
        o.append(p)
        cx, cy = 195, 340
        o.append(call_halo(cx, cy, 52, 'boy', BTINT, dots=state not in ('reduced', 'cancelled'), dim=state == 'cancelled'))
        o.append(f'<circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="{CORAL}" stroke-opacity="0.18" stroke-width="1.5"/>')
        if state not in ('reduced', 'cancelled'):
            import math
            for ang, rr, bg in [(-40, 110, CTINT), (150, 110, CSURF), (60, 150, BTINT), (230, 150, CTINT)]:
                a = math.radians(ang)
                px, py = cx + rr * math.cos(a), cy + rr * math.sin(a)
                o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="24" fill="{WHITE}" filter="url(#sh-card)"/>' + portrait(px, py, 21, 'girl', bg))
        title = {'searching': 'Matching with available host…', 'still': 'Still looking…', 'reduced': 'Matching with available host…',
                 'cancelled': 'Cancelling…', 'offline': 'Waiting for connection…'}[state]
        body = {'still': 'Hang on, we are checking more hosts.'}.get(state, 'This usually takes a few seconds.')
        s, y = text(195, cy + 150 + 32, title, 'h3', anchor='middle')
        o.append(s + text(195, y + 8, body, 'body', anchor='middle')[0])
        a, _ = action_area([('btn', 'Cancel Match', 'secondary' if state != 'cancelled' else 'secondary-disabled', '13')])
        o.append(a)
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def gen_15():
    F, ID, N = '15_Matching-Radar', '15', 'Matching-Radar'
    frame(F, ID, N, 'Searching', radar_body(), note='Orbiting avatars are decorative, not real hosts. No top bar')
    frame(F, ID, N, 'Searching-Voice', radar_body('Voice'))
    frame(F, ID, N, 'Still-Looking', radar_body(state='still'), note='After 10 s')
    frame(F, ID, N, 'No-Hosts-Available', radar_body(state='nohosts'), note='After 30 s')
    frame(F, ID, N, 'Cancelled', radar_body(state='cancelled'))
    frame(F, ID, N, 'Reduced-Motion', radar_body(state='reduced'), note='Rings static, no orbit')
    frame(F, ID, N, 'Offline', radar_body(state='offline'))


# ============================================================ 16 Host Public Profile
BIO = ('Hi, I am Priya. I love long talks about books, music and food. I am a good listener, so tell me about your day. '
       'I speak Hindi and English and I am usually online in the evening.')


def hp_content(h, reviews=True, longbio=False, mode_off=None, missing=False):
    o = [host_photo(0, 0, 390, 440, h, r_top=0, missing=missing, scale=2.4)]
    o.append(''.join(f'<circle cx="{195 - 16 + i * 16}" cy="400" r="4" fill="{WHITE if i == 0 else WHITE}" opacity="{1 if i == 0 else 0.5}"/>' for i in range(3)))
    p, _ = pill(24, 360, 'Play intro', NAVY, WHITE, 'play', op=0.4)
    o.append('<!-- Play intro (inline) -->' + p + hit(24, 356, 130, 40, 'btn:Play intro'))
    o.append(f'<path d="M0 440 a24 24 0 0 1 24 -24 H366 a24 24 0 0 1 24 24 V2000 H0 Z" fill="{CREAM}"/>'
             f'<g filter="url(#blur-xl)"><ellipse cx="380" cy="520" rx="90" ry="110" fill="{BLUE}" {cloud("cl-b4")}/>'
             f'<ellipse cx="0" cy="1100" rx="110" ry="140" fill="{CORAL}" {cloud("cl-c4")}/></g>')
    y = 440
    o.append(t1(24, y + 26, h['name'], 26, 700, NAVY, ls=-0.4) + icon('badge-check', 30 + tw(h['name'], 26, 700), y + 6, BLUE))
    sb, w = status_badge(0, 0, h['status'])
    o.append(status_badge(366 - w, y + 6, h['status'])[0])
    o.append(t1(24, y + 52, f'Host ID: {h["hid"]}', 12, 500, SLATE))
    y += 64 + 16
    o.append(icon('user', 24, y, SLATE, 18) + t1(48, y + 14, f'{h["age"]}', 12, 500, SLATE) + flag_in(80, y + 1) + t1(110, y + 14, 'India', 12, 500, SLATE)
             + icon('languages', 168, y, SLATE, 18) + t1(192, y + 14, f'{len(h["langs"])} languages', 12, 500, SLATE))
    y += 18 + 16
    o.append(card(24, y, 342, 72, 20))
    cols = [('star', f'{h["rating"]}', f'({h["reviews"]} reviews)'), ('clock', '320 h', 'talk time')]
    for i, (ic, v, c) in enumerate(cols):
        cx = 24 + 85 + i * 171
        if i:
            o.append(f'<rect x="{24 + i * 171}" y="{y + 16}" width="1" height="40" fill="{BORDER}"/>')
        o.append((stars(cx - 34, y + 14, 5, 12, 2)[:0] if False else '') + (icon('star', cx - 30, y + 16, WARN, 18) if ic == 'star' else icon(ic, cx - 30, y + 16, SLATE, 18))
                 + t1(cx - 8, y + 32, v, 18, 700, NAVY) + t1(cx, y + 56, c, 12, 500, SLATE, 'middle'))
    y += 72 + 24
    bio = BIO if longbio else BIO[:150]
    lines = wrap(bio, 342, 15)
    show = lines[:3]
    txt = ' '.join(w for ln in show for w, _, _ in ln)
    s, y = text(24, y, txt + ('…' if len(lines) > 3 else ''), 'body')
    o.append(s)
    if len(lines) > 3 or longbio:
        o.append(t1(24, y + 18, 'Read more', 14, 600, BLUE) + hit(24, y - 4, 100, 44, 'link:Read more'))
        y += 28
    y += 16
    s, y = chips_wrap(24, y, [(l, 'readonly') for l in h['langs']])
    o.append(s)
    y += 24
    for i, (m, ic, rate) in enumerate([('Voice', 'phone', h['voice']), ('Video', 'video', h['video'])]):
        x = 24 + i * 177
        off = (mode_off == m.lower()) or not rate
        o.append(card(x, y, 165, 88, 16, fill=WHITE))
        o.append(icon(ic, x + 16, y + 16, DIS_T if off else BLUE) + t1(x + 48, y + 33, m, 15, 600, DIS_T if off else NAVY))
        if off:
            o.append(t1(x + 16, y + 66, 'Not available right now', 12, 500, DIS_T))
        else:
            o.append(gem(x + 16, y + 52, 18) + t1(x + 40, y + 67, f'{rate}/min', 16, 700, NAVY))
    y += 88 + 24
    o.append(t1(24, y + 19, 'Reviews', 18, 700, NAVY))
    y += 26 + 12
    if not reviews:
        o.append(empty_state(y + 70, 'star', 'No reviews yet', 'Be the first to talk to Priya.'))
        return '\n'.join(o), y + 200
    o.append(t1(24, y + 40, f'{h["rating"]}', 32, 700, NAVY, ls=-0.6) + stars(24, y + 52, 5, 16, 4) + t1(24, y + 92, f'{h["reviews"]} reviews', 12, 500, SLATE))
    for i, (n, c) in enumerate([(5, 88), (4, 22), (3, 6), (2, 2), (1, 2)]):
        by = y + 4 + i * 18
        o.append(t1(140, by + 11, str(n), 12, 600, SLATE) + f'<rect x="156" y="{by + 3}" width="170" height="8" rx="4" fill="{SKEL}"/>'
                 f'<rect x="156" y="{by + 3}" width="{170 * c / 100:.0f}" height="8" rx="4" fill="{BLUE}"/>' + t1(366, by + 11, str(round(h['reviews'] * c / 100)), 12, 500, SLATE, 'end'))
    y += 104 + 16
    for nm, st, txt, d in [('Rohan', 5, 'So easy to talk to. Made my evening better.', '2 days ago'),
                           ('Vikram', 4, 'Friendly and polite. Good Hindi and English. Would call again for sure.', '1 week ago')]:
        o.append(avatar(44, y + 20, 40, letter=nm[0]) + t1(76, y + 16, nm, 15, 500, NAVY) + stars(76, y + 24, st, 14, 3) + t1(366, y + 16, d, 12, 500, SLATE, 'end'))
        s, yy = text(76, y + 46, txt, 'body', w=290)
        o.append(s)
        y = yy + 16
    o.append(link_row(y, 'Show more', 'next page'))
    return '\n'.join(o), y + 44


def hp_bar(state='ok', mode_off=None, chat_off=False):
    offline = state in ('Busy', 'Offline')
    o = [f'<!-- Sticky call bar (frosted) -->', f'<rect x="0" y="722" width="390" height="122" fill="{CREAM}" opacity="0.7"/>',
         f'<rect x="0" y="722" width="390" height="122" fill="{WHITE}" fill-opacity="0.55"/><rect x="0" y="722" width="390" height="1" fill="{WHITE}"/>']
    if offline:
        o.append(t1(195, 712, 'Host is offline right now' if state == 'Offline' else 'Priya is on another call', 12, 500, SLATE, 'middle'))
        o.insert(1, f'<rect x="0" y="694" width="390" height="28" fill="{CREAM}" opacity="0.9"/>')
    o.append(glass(24, 738, 56, 56, 28) + icon('message-circle', 40, 754, DIS_T if chat_off else BLUE)
             + hit(24, 738, 56, 56, 'btn:Message'))
    o.append(button(738, 'Voice', 'disabled' if offline or mode_off == 'voice' else 'primary', x=92, w=131, nav='17 (or 30 if balance short)', icon_left='phone'))
    o.append(button(738, 'Video', 'disabled' if offline or mode_off == 'video' else 'primary', x=235, w=131, nav='17 (or 30 if balance short)', icon_left='video'))
    return '\n'.join(o)


def hp_body(h=None, scroll=0, heart=False, state='ok', mode_off=None, chat_off=False, overlay='', reviews=True, longbio=False, missing=False, loading=False):
    h = h or HOSTS[0]
    if state in ('Busy', 'Offline'):
        h = dict(h, status=state)
    o = []
    if loading:
        o.append(f'<rect width="390" height="440" fill="{SKEL}"/><path d="M0 440 a24 24 0 0 1 24 -24 H366 a24 24 0 0 1 24 24 V844 H0 Z" fill="{WHITE}"/>'
                 + skeleton(24, 456, 160, 24) + skeleton(24, 492, 100, 12) + skeleton(24, 528, 342, 72, 16) + skeleton(24, 624, 342, 14) + skeleton(24, 646, 300, 14))
    else:
        c, _ = hp_content(h, reviews, longbio, mode_off, missing)
        o.append(clip_group('c16', 0, 722, c, scroll))
    o.append(hp_bar(state, mode_off, chat_off))
    o.append(media_btn(12, 51, 'arrow-left', 'back') + media_btn(330, 51, 'more-vertical', 'right:more') + media_btn(282, 51, 'heart', 'right2:heart'))
    if heart:
        o.append(f'<g transform="translate(294 63)"><path d="{I["heart"][0][9:-3]}" fill="{CORAL}" stroke="{CORAL}" stroke-width="2"/></g>')
    o.append(status_bar(WHITE))
    o.append(overlay)
    o.append(home_indicator())
    return f'<rect width="390" height="844" fill="{CREAM}"/>' + '\n'.join(o)


def overflow_sheet(rows, title=None):
    h = 24 + (38 if title else 0) + len(rows) * 56 + 24 + 34
    top = 844 - h
    b = []
    y = top + 24
    if title:
        b.append(text(24, y, title, 'h3')[0])
        y += 38
    for lbl, ic, col, nav in rows:
        b.append(f'<!-- Sheet row "{lbl}" → {nav} -->' + icon(ic, 24, y + 16, col) + t1(60, y + 33, lbl, 15, 500, col) + hit(0, y, 390, 56, f'row:{lbl}'))
        y += 56
    return scrim() + sheet(top, '\n'.join(b))


def gen_16():
    F, ID, N = '16_Host-Profile', '16', 'Host-Profile'
    frame(F, ID, N, 'Loading', hp_body(loading=True))
    frame(F, ID, N, 'Default', hp_body(), note='3 CTAs (Message + Voice + Video): PRD §16.3 one-primary question')
    frame(F, ID, N, 'Scrolled-Pricing', hp_body(scroll=360))
    frame(F, ID, N, 'Scrolled-Reviews', hp_body(scroll=640))
    frame(F, ID, N, 'Long-Bio', hp_body(longbio=True, scroll=200))
    frame(F, ID, N, 'No-Reviews', hp_body(reviews=False, scroll=560))
    frame(F, ID, N, 'Missing-Photos', hp_body(missing=True))
    frame(F, ID, N, 'Favorite-On', hp_body(heart=True))
    frame(F, ID, N, 'Host-Busy', hp_body(state='Busy'))
    frame(F, ID, N, 'Host-Offline', hp_body(state='Offline'))
    frame(F, ID, N, 'Video-Mode-Off', hp_body(mode_off='video', scroll=360))
    frame(F, ID, N, 'Chat-Off-Toast', hp_body(chat_off=True, overlay=toast(666, "This host isn't accepting messages", 'info')))
    frame(F, ID, N, 'Low-Balance-Toast', hp_body(overlay=toast(666, 'Recharge to call', 'gem')), note='Then pushes 30')
    frame(F, ID, N, 'Overflow-Sheet', hp_body(overlay=overflow_sheet([('Report', 'flag', NAVY, '39'), ('Block', 'user-x', ERROR, '39')])))
    frame(F, ID, N, 'Offline', hp_body(overlay=offline_banner(111)[0]))
    frame(F, ID, N, 'Error', hp_body(loading=True, overlay=banner(456, "We couldn't load this profile. Try again in a moment.", 'error')[0]
                                     + button(738, 'Try again', 'secondary', nav='reload')))


def gen_all():
    gen_00(); gen_001(); gen_13(); gen_131(); gen_14(); gen_15(); gen_16()
