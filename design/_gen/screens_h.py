"""Abid batch: 40, 40.1, 60, 41, 63, 65, 68, 64, 31, 32, 33, 51, 34, 34.1, 35, 42, 56, 57, 59.

Drafted WITHOUT the Abid brief file (not saved in docs/design_tasks/). Sources: PRD §5 inventory, §7.9 wallet & payouts,
§7.11 settings, §7.12 support/system/legal, §8.4–8.8 safety, §10.2 notification preferences (origin/dev).
Q1 scope only: menu rows link only to built (Q1) destinations. Assumptions are logged in README.
"""
from lib2 import *
from illus import soft_blob, sparks, portrait, logo_mark
from screens_e import compose, overflow_sheet
from screens_f import gem_text
from screens_g import hero


# ---------------------------------------------------------------- helpers
def page(title, body, footer='', overlay='', scroll=0, right=None, bar=None, bottom=None, cid='ch', back='back', right2=None):
    hdr = topbar1(title, right=right, right2=right2) if back == 'back' else topbar('close', title=title, right=right)
    return compose(body, hdr, actions=footer, bar=bar, overlay=overlay, scroll=scroll,
                   clip=(103, bottom or (TAB_BOTTOM + 24 if bar else 820)), cid=cid)


def cta(items, cover=CREAM):
    return action_area(items, cover=cover)


def group(y, title, rows, x=24, w=342):
    """Section label + white card of MenuRows. rows: (label, icon, nav[, trailing[, color[, key]]])."""
    o = []
    if title:
        o.append(section_label(y, title))
        y += 28
    h = len(rows) * 56
    o.append(card(x, y, w, h, shadow=False))
    for i, r in enumerate(rows):
        lbl, ic, nav = r[:3]
        trailing = r[3] if len(r) > 3 else None
        col = r[4] if len(r) > 4 else NAVY
        key = r[5] if len(r) > 5 else None
        chev = r[6] if len(r) > 6 else col == NAVY
        o.append(menu_row(y + i * 56, lbl, ic, nav, x=x, w=w, last=i == len(rows) - 1, trailing=trailing, color=col, chevron=chev, key=key))
    return '\n'.join(o), y + h


def switch_rows(y, title, rows, x=24, w=342):
    """Card of label/sub + Switch rows. rows: (label, sub, on, disabled)."""
    o = [section_label(y, title)] if title else []
    y += 28 if title else 0
    hs = [72 if r[1] else 56 for r in rows]
    o.append(card(x, y, w, sum(hs), shadow=False))
    yy = y
    for i, (lbl, sub, on, dis) in enumerate(rows):
        h = hs[i]
        o.append(t1(x + 16, yy + (28 if sub else 33), lbl, 15, 500, DIS_T if dis else NAVY))
        if sub:
            o.append(t1(x + 16, yy + 50, sub, 12, 500, SLATE))
        o.append(switch(x + w - 16 - 52, yy + (h - 32) / 2, on, BLUE, disabled=dis, key=f'switch:{lbl}'))
        if dis:
            o.append(icon('lock', x + w - 16 - 52 - 28, yy + (h - 18) / 2, TERT, 18))
        if i < len(rows) - 1:
            o.append(f'<rect x="{x + 16}" y="{yy + h - 1}" width="{w - 32}" height="1" fill="{CBORDER}"/>')
        yy += h
    return '\n'.join(o), yy


def info_card(y, ic, title, body, bg=BTINT, col=BLUE, x=24, w=342):
    n = nlines(body, 'notice', w - 88)
    h = max(72, 16 + 22 + n * 19 + 16)
    s, _ = text(x + 72, y + 40, body, 'notice', w=w - 88)
    return (card(x, y, w, h, shadow=False) + f'<circle cx="{x + 36}" cy="{y + 36}" r="20" fill="{bg}"/>' + icon(ic, x + 24, y + 24, col)
            + t1(x + 72, y + 32, title, 15, 600, NAVY) + s), y + h


def center_state(ic, title, body, items, col=BLUE, bg=BTINT, extra=None, cy=250):
    o = [blobs(), hero(cy, ic, col, bg)]
    s, y = text(195, cy + 88, title, 'h2', anchor='middle', w=320)
    o.append(s)
    if body:
        s, y = text(195, y + 8, body, 'body', anchor='middle', w=320)
        o.append(s)
    if extra:
        o.append(extra(y + 24))
    a, _ = action_area(items)
    o.append(a + status_bar() + home_indicator())
    return '\n'.join(o)


def otp_sheet(title, sub, digits='', state='empty', err=None, btn='Confirm', kind='primary', nav=''):
    top = 844 - 420
    b = [text(24, top + 24, title, 'h3')[0] + icon('x', 342, top + 22, NAVY) + hit(330, top + 10, 48, 48, 'close'),
         text(24, top + 62, sub, 'body', w=342)[0]]
    b.append(otp_boxes(top + 120, digits, 'error' if err else 'empty', focus=len(digits) if len(digits) < 6 else None))
    if err:
        b.append(err_msg(24, top + 188, err)[0])
    else:
        b.append(t1(24, top + 202, 'Resend code in 0:42', 13, 500, SLATE))
    b.append(button(844 - 34 - 56, btn, kind if len(digits) == 6 or kind.endswith('loading') else 'disabled', nav=nav))
    return scrim() + sheet(top, '\n'.join(b))


# ============================================================ 40 Profile & Settings (user tab 4)
def me_card(y, host=False):
    o = [card(24, y, 342, 96)]
    o.append(avatar(72, y + 48, 56, letter=None if host else 'A', photo=host))
    o.append(t1(112, y + 42, 'Priya' if host else ME['name'], 18, 700, NAVY))
    o.append(t1(112, y + 64, f'ID: {ME["uid"]}', 12, 500, SLATE) + icon('copy', round(118 + tw(f'ID: {ME["uid"]}', 12, 500)), y + 51, SLATE, 16) + hit(176, y + 38, 44, 44, 'copy'))
    o.append(t1(350, y + 53, 'Edit', 14, 600, BLUE, 'end') + hit(300, y + 26, 66, 44, 'link:Edit'))
    return '\n'.join(o), y + 96


SET_ACCOUNT = [('Edit profile', 'user', '40.1'), ('Notification preferences', 'bell', '60'), ('Language', 'languages', '01.1', 'English'),
               ('Theme', 'sun', 'theme sheet', 'System')]
SET_ACTIVITY = [('Purchase history', 'receipt', '31'), ('Blocked users', 'user-x', '41')]
SET_HELP = [('Help & Support', 'life-buoy', '65'), ('Safety Center', 'shield-check', '59')]
SET_ABOUT = [('About Frndu', 'info', '63'), ('Terms of Service', 'file-text', '68'), ('Privacy Policy', 'lock', '68')]


def s40_content(host=False, y0=115):
    o = []
    s, y = me_card(y0, host)
    o.append(s)
    y += 24
    acct = SET_ACCOUNT if not host else [('Edit profile', 'user', '40.1'), ('Notification preferences', 'bell', '60'), ('Language', 'languages', '01.1', 'English')]
    for title, rows in [('Account', acct), ('Activity', SET_ACTIVITY if not host else [('Blocked users', 'user-x', '41')]),
                        ('Help', SET_HELP), ('About', SET_ABOUT)]:
        s, y = group(y, title, rows)
        o.append(s)
        y += 24
    s, y = group(y, None, [('Log Out', 'log-out', 'confirm dialog → 01', None, NAVY, None, False),
                           ('Delete account', 'trash-2', '42', None, ERROR)])
    o.append(s)
    o.append(t1(195, y + 32, 'Frndu v1.0.0', 12, 500, TERT, 'middle'))
    return '\n'.join(o), y + 48


def s40(scroll=0, overlay='', host=False, state=None):
    if state == 'offline':
        b, y2 = offline_banner(115)
        c = b + s40_content(host, y2 + 12)[0]
    else:
        c, _ = s40_content(host)
    if host:
        return page('Account settings', c, overlay=overlay, scroll=scroll, cid='c40')
    return compose(c, tab_header('Profile'), bar=user_bar(3, 3), overlay=overlay, scroll=scroll, clip=(103, TAB_BOTTOM + 24), cid='c40')


def theme_sheet(sel='System'):
    rows = ['System', 'Light', 'Dark']
    top = 844 - (24 + 38 + 3 * 56 + 24 + 34)
    b = [text(24, top + 24, 'Theme', 'h3')[0]]
    for i, r in enumerate(rows):
        y = top + 62 + i * 56
        b.append(radio(42, y + 28, r == sel) + t1(66, y + 33, r, 15, 500, NAVY) + hit(0, y, 390, 56, f'theme:{r}'))
    return scrim() + sheet(top, '\n'.join(b))


def gen_40():
    F, ID, N = '40_Profile-Settings', '40', 'Profile-Settings'
    frame(F, ID, N, 'Default', s40(), note='Q1 menu shows only built destinations (PRD phase notes). Earn with Us (36), Favorites (43), My Reports (58) arrive later')
    frame(F, ID, N, 'Scrolled', s40(scroll=520))
    frame(F, ID, N, 'ID-Copied', s40(overlay=toast(TAB_BOTTOM - 56, 'ID copied')))
    frame(F, ID, N, 'Theme-Sheet', s40(overlay=theme_sheet()), note='Dark mode is an open decision (PRD §16 D5)')
    frame(F, ID, N, 'Log-Out-Dialog', s40(scroll=520, overlay=dialog('Log out of Frndu?', 'You can log back in with your phone number.',
                                                                       [('Log Out', 'primary', '01'), ('Cancel', 'ghost', 'close')], 'log-out')))
    frame(F, ID, N, 'Logging-Out', s40(scroll=520, overlay=dialog('Log out of Frndu?', 'You can log back in with your phone number.',
                                                                    [('Log Out', 'primary-loading', '01'), ('Cancel', 'ghost', 'close')], 'log-out')))
    frame(F, ID, N, 'Host-Account', s40(host=True), note='Opened from 26 "Account settings"; pushed with back')
    frame(F, ID, N, 'Offline', s40(state='offline'))


# ============================================================ 40.1 Edit Profile
def s401(nick='Aarav', state='view', overlay='', err=None):
    o = []
    y = 127
    o.append(avatar(195, y + 48, 96, letter='A') + f'<circle cx="230" cy="{y + 84}" r="16" fill="{BLUE}" stroke="{WHITE}" stroke-width="2"/>'
             + icon('camera', 222, y + 76, WHITE, 16) + hit(147, y, 96, 96, 'avatar'))
    y += 96 + 12
    o.append(link_row(y, 'Change photo', 'photo sheet'))
    y += 44 + 16
    o.append(t1(24, y + 15, 'Nickname', 14, 600, NAVY) + t1(366, y + 15, f'{len(nick)}/20', 12, 500, SLATE, 'end'))
    o.append(input_box(y + 24, nick, 'Your nickname', 'error' if err else ('focused' if state == 'editing' else 'empty')))
    y += 24 + 56
    if err:
        s, y = err_msg(24, y + 8, err)
        o.append(s)
    y += 20
    for lbl, val in [('Date of birth', '12 / 03 / 2000'), ('Gender', 'Male')]:
        o.append(t1(24, y + 15, lbl, 14, 600, NAVY))
        o.append(input_box(y + 24, val, None, 'disabled', right_icon='lock') + hit(24, y + 24, 342, 56, f'locked:{lbl}'))
        y += 24 + 56 + 16
    o.append(text(24, y, "Date of birth and gender can't be changed.", 'notice')[0])
    y += 19 + 24
    o.append(t1(24, y + 15, 'Languages you speak', 14, 600, NAVY))
    s, y = chips_wrap(24, y + 28, [(l, 'selected' if l in ('Hindi', 'English') else 'unselected') for l in ['Hindi', 'English', 'Kannada', 'Tamil', 'Telugu']])
    o.append(s)
    kind = {'view': 'disabled', 'editing': 'primary', 'saving': 'primary-loading', 'error': 'disabled'}.get(state, 'disabled')
    a, top = cta([('btn', 'Save', kind, 'save → toast → 40')])
    return page('Edit profile', '\n'.join(o), a, overlay, bottom=top - 16, cid='c401')


def gen_401():
    F, ID, N = '40.1_Edit-Profile', '40.1', 'Edit-Profile'
    frame(F, ID, N, 'Default', s401(), note='Save stays disabled until something changes. DOB and gender are locked (PRD §7.11)')
    frame(F, ID, N, 'Editing', s401('Aarav_K', 'editing'))
    frame(F, ID, N, 'Nickname-Error', s401('Aa', 'error', err='Use 3 to 20 letters, numbers or underscores.'))
    frame(F, ID, N, 'Locked-Field-Toast', s401(overlay=toast(666, "Date of birth can't be changed", 'lock')))
    frame(F, ID, N, 'Photo-Sheet', s401(overlay=overflow_sheet([('Take photo', 'camera', NAVY, 'camera'), ('Choose from gallery', 'image', NAVY, 'gallery'),
                                                                 ('Remove photo', 'trash-2', ERROR, 'remove')])))
    frame(F, ID, N, 'Saving', s401('Aarav_K', 'saving'))
    frame(F, ID, N, 'Saved-Toast', s401(overlay=toast(666, 'Profile updated')))


# ============================================================ 60 Notification Preferences
def s60(os_off=False, host=False, overlay='', presence_on=True):
    o = []
    y = 115
    if os_off:
        b, y2 = banner(y, 'Notifications are off for Frndu on this phone.', 'warning', icon_name='bell-off', action='Open Settings')
        o.append(b + hit(24, y, 342, y2 - y, 'btn:Open Settings'))
        y = y2 + 16
    if host:
        rows = [('Incoming calls', "Can't be turned off while you're online", True, True), ('Chat messages', None, True, False),
                ('Chat requests', None, True, False), ('Payouts & KYC', 'Always on for your security', True, True)]
        s, y = switch_rows(y, 'Host alerts', rows)
        o.append(s)
        y += 24
    else:
        s, y = switch_rows(y, 'Favourite hosts', [('Presence alerts', 'When a favourite host comes online', presence_on, False)])
        o.append(s)
        if presence_on:
            y += 12
            o.append(seg_tabs(y, ['All alerts', 'Max 1 per day'], 0, key='freq'))
            y += 48
        y += 24
    rows = [('Chat messages', None, True, False), ('Offers & promotions', None, False, False), ('Payments & wallet', None, True, False),
            ('Account & safety', 'Always on for your security', True, True)]
    if host:
        rows = [r for r in rows if r[0] not in ('Chat messages', 'Payments & wallet')]
    s, y = switch_rows(y, 'Other', rows)
    o.append(s)
    y += 24
    o.append(section_label(y, 'Quiet hours'))
    y += 28
    o.append(card(24, y, 342, 72, shadow=False) + t1(40, y + 30, 'Quiet hours', 15, 500, NAVY) + t1(40, y + 52, '22:00 – 08:00 · presence and promotions', 12, 500, SLATE)
             + icon('chevron-right', 330, y + 26, TERT, 20) + hit(24, y, 342, 72, 'row:Quiet hours'))
    return page('Notifications', '\n'.join(o), overlay=overlay, cid='c60')


def quiet_sheet():
    top = 844 - 360
    b = [text(24, top + 24, 'Quiet hours', 'h3')[0], text(24, top + 62, 'No presence or promotion alerts during these hours.', 'body')[0]]
    for i, (lbl, val) in enumerate([('From', '22:00'), ('To', '08:00')]):
        x = 24 + i * 177
        b.append(t1(x, top + 118, lbl, 14, 600, NAVY) + input_box(top + 128, val, None, 'empty', x=x, w=165, right_icon='clock'))
    b.append(button(844 - 34 - 56, 'Save', 'primary', nav='60'))
    return scrim() + sheet(top, '\n'.join(b))


def gen_60():
    F, ID, N = '60_Notification-Preferences', '60', 'Notification-Preferences'
    frame(F, ID, N, 'Default', s60(), note='Saved instantly on toggle (server-side). Account & safety locked on (PRD §10.2)')
    frame(F, ID, N, 'Presence-Off', s60(presence_on=False))
    frame(F, ID, N, 'OS-Notifications-Off', s60(os_off=True))
    frame(F, ID, N, 'Quiet-Hours-Sheet', s60(overlay=quiet_sheet()))
    frame(F, ID, N, 'Host', s60(host=True), note='Incoming calls cannot be disabled while Online')
    frame(F, ID, N, 'Save-Failed-Toast', s60(overlay=toast(738, "Couldn't save. Try again.", 'alert-circle')))


# ============================================================ 41 Blocked Users
BLOCKED = [('Rohan_K', 'Blocked 2 Oct 2026'), ('Vikram', 'Blocked 18 Sep 2026'), ('Kabir_07', 'Blocked 1 Sep 2026')]


def s41(state='list', overlay='', rows=None):
    o = []
    y = 115
    if state == 'loading':
        o.append(skeleton_rows(y, 4))
    elif state == 'empty':
        o.append(empty_state(360, 'user-x', "You haven't blocked anyone.", 'People you block show up here.'))
    elif state == 'error':
        o.append(empty_state(340, 'cloud-off', "We couldn't load this list.", 'Try again in a moment.') + button(500, 'Try again', 'secondary', x=97, w=196, nav='reload'))
    else:
        for nm, sub in (rows or BLOCKED):
            def right(xr, yy, h, nm=nm):
                w = tw('Unblock', 13, 600) + 28
                return (f'<rect x="{xr - w:.0f}" y="{yy + (h - 32) / 2}" width="{w:.0f}" height="32" rx="16" fill="{WHITE}" stroke="{BORDER}"/>'
                        + t1(f'{xr - w / 2:.0f}', yy + h / 2 + 5, 'Unblock', 13, 600, BLUE, 'middle') + hit(round(xr - w - 4), yy + (h - 44) / 2, round(w + 8), 44, f'unblock:{nm}'))
            o.append(list_row(y, nm, sub, lead=lead_avatar(nm[0]), right=right))
            y += 72
        o.append(text(24, y + 16, "Blocked people can't call or message you, and you won't see them in the app.", 'notice')[0])
    return page('Blocked users', '\n'.join(o), overlay=overlay, cid='c41')


def gen_41():
    F, ID, N = '41_Blocked-Users', '41', 'Blocked-Users'
    frame(F, ID, N, 'Default', s41())
    frame(F, ID, N, 'Unblock-Dialog', s41(overlay=dialog('Unblock Rohan_K?', 'They will be able to see your profile, call and message you again.',
                                                          [('Unblock', 'primary', 'Unblocked-Toast'), ('Cancel', 'ghost', 'close')], 'user-x')))
    frame(F, ID, N, 'Unblocked-Toast', s41(rows=BLOCKED[1:], overlay=toast(738, 'Rohan_K unblocked')))
    frame(F, ID, N, 'Empty', s41('empty'))
    frame(F, ID, N, 'Loading', s41('loading'))
    frame(F, ID, N, 'Error', s41('error'))


# ============================================================ 63 About & App Info
def s63(state='ok', overlay='', scroll=0):
    o = [logo_mark(195, 175, 96, sparks_on=False), t1(195, 250, 'Frndu', 22, 700, NAVY, 'middle'),
         t1(195, 274, 'Version 1.0.0 (build 112)', 13, 500, SLATE, 'middle')]
    y = 296
    if state == 'checking':
        o.append(f'<rect x="120" y="{y}" width="150" height="36" rx="18" fill="{BTINT}"/>' + spinner(195, y + 18, BLUE, 8))
    elif state == 'update':
        p, _ = pill(195, y, 'Update available · 1.1.0', CTINT, CORAL, 'download', h=36, anchor='middle')
        o.append(p + hit(110, y - 4, 170, 44, 'btn:Update'))
    elif state == 'latest':
        p, _ = pill(195, y, "You're on the latest version", BTINT, SUCCESS, 'check-circle', h=36, anchor='middle')
        o.append(p)
    else:
        o.append(f'<rect x="120" y="{y}" width="150" height="36" rx="18" fill="{WHITE}" stroke="{BORDER}"/>' + t1(195, y + 23, 'Check for update', 13, 600, BLUE, 'middle')
                 + hit(120, y - 4, 150, 44, 'btn:Check for update'))
    y += 36 + 24
    s, y = group(y, 'Legal', [('Terms of Service', 'file-text', '68'), ('Privacy Policy', 'lock', '68'),
                              ('Community Guidelines', 'users', '68'), ('Refund Policy', 'receipt', '68'), ('Open-source licences', 'book-open', 'licences')])
    o.append(s)
    y += 24
    s, y = group(y, 'More', [('Rate Frndu', 'star', 'store'), ('Copy diagnostic ID', 'copy', 'clipboard', None, NAVY, 'row:Copy diagnostic ID')])
    o.append(s)
    y += 24
    o.append(section_label(y, 'Company'))
    s, y = kv_card(y + 28, [('Company', 'Frndu Technologies Pvt Ltd'), ('Grievance Officer', 'grievance@frndu.app'), ('Support', 'support@frndu.app')], rowh=30)
    o.append(s)
    return page('About Frndu', '\n'.join(o), overlay=overlay, scroll=scroll, cid='c63')


def gen_63():
    F, ID, N = '63_About', '63', 'About'
    frame(F, ID, N, 'Default', s63(), note='Company name and emails are placeholders. Grievance Officer contact required by Indian IT rules')
    frame(F, ID, N, 'Scrolled', s63(scroll=330))
    frame(F, ID, N, 'Checking-Update', s63('checking'))
    frame(F, ID, N, 'Update-Available', s63('update'), note='Opens the store; force updates use 64')
    frame(F, ID, N, 'Up-To-Date', s63('latest'))
    frame(F, ID, N, 'Diagnostic-ID-Copied', s63(overlay=toast(738, 'Diagnostic ID copied')))


# ============================================================ 65 Help Center
CATS65 = [('Account & Login', 'user'), ('Calls & Billing', 'phone'), ('Wallet & Payments', 'wallet'),
          ('Host Verification & Payouts', 'badge-check'), ('Safety & Reporting', 'shield-check'), ('Chat', 'message-circle')]
FAQ = [('How am I charged for a call?', 'The first minute is charged when the call connects. After that, each new minute is charged at the start of the minute. '
        'If the call never connects, the first minute is refunded automatically.'),
       ('What happens if my balance runs out?', 'You get a warning when you have about 2 minutes left. If your balance reaches zero, you have 15 seconds to add diamonds before the call ends.'),
       ('Why did my call drop?', 'Calls end if the connection is lost for more than 10 seconds. You are only charged for minutes that started.'),
       ('Can I get a refund?', 'See the Refund Policy. Payments that fail are returned automatically in 5 to 7 business days.')]


def help_footer():
    a, top = cta([('btn', 'Contact Support', 'secondary', '66 (Q3) / support link')])
    return a, top


def s65(state='home', open_i=None, helpful=None, query=None, overlay=''):
    o = []
    y = 115
    if state == 'offline':
        b, y2 = banner(y, "You're offline. Showing saved articles.", 'offline')
        o.append(b)
        y = y2 + 12
    o.append(input_box(y, query, 'Search help articles', 'focused' if query else 'empty', left_icon='search'))
    y += 56 + 24
    if state in ('home', 'offline'):
        o.append(section_label(y, 'Browse by topic'))
        y += 28
        for i, (c, ic) in enumerate(CATS65):
            x = 24 + (i % 2) * 177
            cy = y + (i // 2) * 100
            o.append(card(x, cy, 165, 88, shadow=False) + icon_box(x + 16, cy + 16, ic, 32, BTINT, BLUE, 18, 10))
            s, _ = text(x + 16, cy + 54, c, 'label', w=140, size=13, lh=17)
            o.append(s + hit(x, cy, 165, 88, f'cat:{c}'))
        y += 300 + 12
        o.append(section_label(y, 'Top questions'))
        y += 28
        for q, a in FAQ[:3]:
            s, y = accordion(y, q)
            o.append(s)
    elif state == 'category':
        o.append(t1(24, y + 19, 'Calls & Billing', 18, 700, NAVY))
        y += 38
        for i, (q, a) in enumerate(FAQ):
            s, y = accordion(y, q, a, open_=i == open_i, helpful=helpful)
            o.append(s)
        if helpful == 'yes':
            o.append(toast(666, 'Thanks for your feedback'))
    elif state == 'results':
        o.append(t1(24, y + 15, '2 results for "refund"', 14, 600, SLATE))
        y += 32
        for q, a in [FAQ[3], FAQ[0]]:
            s, y = accordion(y, q)
            o.append(s)
    elif state == 'noresults':
        o.append(empty_state(y + 140, 'search', 'No articles found.', 'Try other words, or contact support.'))
    a, top = help_footer()
    title = 'Help & Support'
    return page(title, '\n'.join(o), a, overlay, bottom=top - 16, cid='c65', right=None)


def gen_65():
    F, ID, N = '65_Help-Center', '65', 'Help-Center'
    frame(F, ID, N, 'Default', s65(), note='CMS articles (Hindi/English). Contact Support form (66) and My Tickets (67) are Q3: button opens the support link for now')
    frame(F, ID, N, 'Category', s65('category'))
    frame(F, ID, N, 'Article-Open', s65('category', open_i=0))
    frame(F, ID, N, 'Helpful-Thanks', s65('category', open_i=0, helpful='yes'))
    frame(F, ID, N, 'Search-Results', s65('results', query='refund'))
    frame(F, ID, N, 'No-Results', s65('noresults', query='xyz'))
    frame(F, ID, N, 'Offline-Cached', s65('offline'))


# ============================================================ 68 Legal Viewer
TERMS = [('1. Who can use Frndu', 'You must be 18 or older to use Frndu. We verify hosts with a video check before they can take calls.'),
         ('2. Your account', 'Keep your phone number up to date. You are responsible for activity on your account.'),
         ('3. Diamonds and payments', 'Diamonds are a virtual currency used for calls and chat. Diamonds have no cash value for users and are non-refundable except as stated in the Refund Policy.'),
         ('4. Community rules', 'Be respectful. No nudity, harassment, fraud, or sharing of personal contact details. We may end calls, issue strikes, or suspend accounts that break these rules.'),
         ('5. Hosts', 'Hosts earn diamonds from calls after the platform commission. Payouts need completed KYC.')]
TERMS_HI = [('1. फ्रेंडू कौन इस्तेमाल कर सकता है', 'फ्रेंडू इस्तेमाल करने के लिए आपकी उम्र 18 साल या उससे ज़्यादा होनी चाहिए।'),
            ('2. आपका अकाउंट', 'अपना फ़ोन नंबर अपडेट रखें। अपने अकाउंट की हर गतिविधि के लिए आप ज़िम्मेदार हैं।')]


def legal_body(y, sections, size=15, lh=22):
    o = []
    for h, p in sections:
        s, y = text(24, y, h, 'h4', size=size + 2, lh=lh + 4)
        o.append(s)
        s, y = text(24, y + 4, p, 'body', size=size, lh=lh)
        o.append(s)
        y += 20
    return '\n'.join(o), y


def legal_header(y, title='Terms of Service', hindi=False, big=False):
    o = [t1(24, y + 26, title if not hindi else 'सेवा की शर्तें', 26, 700, NAVY, ls=-0.4),
         t1(24, y + 52, 'Version 3.2 · Effective 1 Oct 2026', 12, 500, SLATE)]
    o.append(seg_tabs(y + 68, ['English', 'हिन्दी'], 1 if hindi else 0, x=24, w=160, h=40, key='lang'))
    o.append(f'<rect x="286" y="{y + 68}" width="80" height="40" rx="12" fill="{WHITE}" stroke="{CBORDER}"/>'
             + t1(306, y + 93, 'A', 13, 700, NAVY if not big else TERT, 'middle') + t1(342, y + 94, 'A', 18, 700, BLUE if big else NAVY, 'middle')
             + hit(286, y + 64, 40, 48, 'textsize:small') + hit(326, y + 64, 40, 48, 'textsize:large'))
    return '\n'.join(o), y + 124


def scroll_progress(p):
    return f'<rect x="0" y="103" width="390" height="3" fill="{BORDER}"/><rect x="0" y="103" width="{390 * p:.0f}" height="3" fill="{BLUE}"/>'


def s68(scroll=0, hindi=False, big=False, blocking=False, checked=False, state='ok', title='Terms of Service', overlay=''):
    o = []
    y = 115
    if blocking:
        b, y2 = banner(y, "We've updated our Terms. Please read and accept to keep using Frndu.", 'info', icon_name='file-text')
        o.append(b)
        y = y2 + 12
    if state == 'offline':
        b, y2 = banner(y, "You're offline. Showing the saved copy.", 'offline')
        o.append(b)
        y = y2 + 12
    s, y = legal_header(y, title, hindi, big)
    o.append(s)
    if state == 'loading':
        o.append(''.join(skeleton(24, y + i * 26, 342 if i % 4 != 3 else 220, 14) for i in range(14)))
    else:
        s, y = legal_body(y, TERMS_HI if hindi else TERMS, 17 if big else 15, 26 if big else 22)
        o.append(s)
    pg = min(1, (scroll + 600) / 1300)
    if blocking:
        a, top = cta([('btn', 'Accept & Continue', 'primary' if checked else 'disabled', 'logs acceptance → app')], cover=WHITE)
        cb = (f'<rect x="0" y="{top - 88}" width="390" height="72" fill="{WHITE}"/>' + checkbox(28, top - 64, checked)
              + text(64, top - 66, 'I have read and agree to the updated Terms of Service.', 'body', w=290, color=NAVY)[0])
        return compose('\n'.join(o), topbar(None, title=None) + t1(195, 81, 'Updated Terms', 18, 700, NAVY, 'middle') + scroll_progress(pg),
                       actions=a + cb, overlay=overlay, scroll=scroll, clip=(106, top - 88), cid='c68')
    a, top = cta([('link', 'Open in browser', 'browser')])
    return compose('\n'.join(o), topbar1(None) + t1(195, 81, title if len(title) < 22 else 'Legal', 18, 700, NAVY, 'middle') + scroll_progress(pg),
                   actions=a, overlay=overlay, scroll=scroll, clip=(106, top - 8), cid='c68')


def gen_68():
    F, ID, N = '68_Legal-Viewer', '68', 'Legal-Viewer'
    frame(F, ID, N, 'Default', s68(), note='One viewer for Terms, Privacy, Community Guidelines, Host Terms, Refund Policy. Copy is placeholder legal text')
    frame(F, ID, N, 'Scrolled', s68(scroll=420))
    frame(F, ID, N, 'Large-Text', s68(big=True))
    frame(F, ID, N, 'Hindi', s68(hindi=True))
    frame(F, ID, N, 'Privacy-Policy', s68(title='Privacy Policy'))
    frame(F, ID, N, 'Loading', s68(state='loading'))
    frame(F, ID, N, 'Offline-Cached', s68(state='offline'))
    frame(F, ID, N, 'Blocking-Unchecked', s68(blocking=True), note='Version bump: cannot be bypassed by relaunch; acceptance is logged')
    frame(F, ID, N, 'Blocking-Checked', s68(blocking=True, checked=True, scroll=300))


# ============================================================ 64 Global System States
def gen_64():
    F, ID, N = '64_System-States', '64', 'System-States'
    frame(F, ID, N, 'No-Internet', center_state('wifi-off', 'No internet connection', 'Check your Wi-Fi or mobile data and try again.',
                                                [('btn', 'Retry', 'primary', 'retry'), ('btn', 'Open Settings', 'ghost', 'OS settings')]),
          note='Unsent input is kept (PRD §7.12)')
    frame(F, ID, N, 'Retrying', center_state('wifi-off', 'No internet connection', 'Check your Wi-Fi or mobile data and try again.',
                                             [('btn', 'Retry', 'primary-loading', 'retry'), ('btn', 'Open Settings', 'ghost', 'OS settings')]))
    frame(F, ID, N, 'Server-Error', center_state('alert-triangle', 'Something went wrong', 'Please try again in a moment.',
                                                 [('btn', 'Retry', 'primary', 'retry')], WARN, CSURF,
                                                 extra=lambda y: (f'<rect x="97" y="{y}" width="196" height="36" rx="18" fill="{WHITE}" stroke="{BORDER}"/>'
                                                                  + t1(183, y + 23, 'Error code: E-5021', 13, 600, SLATE, 'middle') + icon('copy', 254, y + 9, SLATE, 18)
                                                                  + hit(97, y - 4, 196, 44, 'copy'))))
    frame(F, ID, N, 'Maintenance', center_state('wrench', "We're making Frndu better", 'Back by 2:30 PM. We will retry automatically.',
                                                [('note', 'Retrying every 30 seconds', 'notice')], BLUE, BTINT), note='Message and ETA from remote config')
    frame(F, ID, N, 'Force-Update', center_state('download', 'Update required', 'This version of Frndu is no longer supported. Update to keep using the app.',
                                                 [('btn', 'Update Now', 'primary', 'store')]), note='Blocking (min_supported_version)')
    soft = (scrim() + sheet(844 - 300, text(24, 844 - 276, 'A new version is ready', 'h3')[0]
                            + text(24, 844 - 238, 'Update for the latest fixes and features.', 'body')[0]
                            + button(844 - 34 - 56 - 68, 'Update', 'primary', nav='store') + button(844 - 34 - 56, 'Not now', 'ghost', nav='close')))
    from screens_e import home_body
    frame(F, ID, N, 'Soft-Update-Sheet', home_body(overlay=soft), note='Dismissible; shown again after 3 days')
    frame(F, ID, N, 'Region-Unavailable', center_state('globe', "Frndu isn't available in your country", 'We hope to be there soon.',
                                                       [('btn', 'Contact Support', 'ghost', 'support link')]), note='Optional state')
    frame(F, ID, N, 'Offline-Banner', home_body(offline=True), note='Transient loss: non-blocking top banner on any screen')


# ============================================================ 31 Transaction History
TX = [('Recharge', 'gem', '+550', '9 Oct, 9:00 AM', 'RCPT-88415', SUCCESS, 'Success'), ('Call with Priya', 'video', '−480', '8 Oct, 9:41 PM', '12:40 min', NAVY, None),
      ('Chat with Ananya', 'message-circle', '−9', '8 Oct, 6:02 PM', '3 messages', NAVY, None), ('Recharge', 'gem', '+100', '5 Oct, 1:15 PM', 'RCPT-88102', BLUE, 'Pending'),
      ('Call with Meera', 'phone', '−200', '4 Oct, 10:20 PM', '5:02 min', NAVY, None), ('Recharge', 'gem', '+1,200', '1 Oct, 8:00 PM', 'RCPT-87730', ERROR, 'Failed')]


def tx_rows(y, rows, purchases=False):
    o = []
    for title, ic, amt, ts, sub, col, st in rows:
        plus = amt.startswith('+')

        def right(xr, yy, h, amt=amt, plus=plus, st=st):
            s = t1(xr, yy + 32, amt, 15, 700, SUCCESS if plus and st in (None, 'Success') else NAVY if not plus else SLATE, 'end')
            if st and st != 'Success':
                s += status_pill(xr, yy + 42, st, anchor='end', h=20)[0]
            else:
                s += t1(xr, yy + 52, 'diamonds', 12, 500, TERT, 'end')
            return s
        o.append(list_row(y, title, ts, sub2=sub, lead=lead_icon(ic, BTINT if plus else CSURF, BLUE if plus else SLATE), right=right, h=80, key=f'tx:{title}:{amt}'))
        y += 80
    return '\n'.join(o), y


def s31(tab='All', state='list', overlay='', scroll=0, filt=None):
    o = []
    y = 115
    o.append(seg_tabs(y, ['All', 'Purchases'], 0 if tab == 'All' else 1, key='seg'))
    y += 48 + 12
    chips = [('All types', 'selected' if not filt else 'unselected'), ('Recharges', 'selected' if filt == 'Recharges' else 'unselected'),
             ('Calls', 'unselected'), ('Chat', 'unselected')] if tab == 'All' else [('All', 'selected'), ('Success', 'unselected'), ('Pending', 'unselected'), ('Failed', 'unselected')]
    s, y = chips_wrap(24, y, chips, h=36)
    o.append(s)
    y += 8
    rows = TX if tab == 'All' else [r for r in TX if r[0] == 'Recharge']
    if filt == 'Recharges':
        rows = [r for r in TX if r[0] == 'Recharge']
    if state == 'loading':
        o.append(skeleton_rows(y, 6, 80))
    elif state == 'empty':
        o.append(empty_state(y + 160, 'receipt', 'No transactions yet.', 'Recharges, calls and chats show up here.'))
    elif state == 'error':
        o.append(empty_state(y + 150, 'cloud-off', "We couldn't load your history.", 'Try again in a moment.') + button(y + 290, 'Try again', 'secondary', x=97, w=196, nav='reload'))
    else:
        o.append(section_label(y, 'October 2026'))
        s, y = tx_rows(y + 28, rows)
        o.append(s)
        if state == 'more':
            o.append(spinner(195, y + 24, BLUE, 10))
    return page('Transaction history', '\n'.join(o), overlay=overlay, scroll=scroll, right='mail', cid='c31')


def receipt_sheet(kind='purchase'):
    if kind == 'purchase':
        rows = [('Bundle', '550 + 50 bonus', 'gem'), ('Amount paid', '₹499'), ('Payment method', 'Google Play'), ('Status', 'Success', None, SUCCESS),
                ('Order ID', 'ORD-88415'), ('Invoice', 'INV-2026-1009-15')]
        title, btns = 'Receipt', [button(844 - 34 - 56 - 56, 'Download PDF', 'secondary', nav='pdf'), link_row(844 - 34 - 44, 'Payment issue?', '66 prefilled (Q3) / support link')]
    elif kind == 'pending':
        rows = [('Bundle', '100', 'gem'), ('Amount paid', '₹299'), ('Payment method', 'UPI'), ('Status', 'Pending', None, BLUE), ('Order ID', 'ORD-88102')]
        title, btns = 'Payment pending', [button(844 - 34 - 56, 'Check status', 'primary', nav='48 Pending-Checking')]
    else:
        rows = [('Host', 'Priya'), ('Type', 'Video call'), ('Duration', '12:40'), ('Rate', '80 / min', 'gem'), ('Charged', '480', 'gem')]
        title, btns = 'Call details', [text(195, 844 - 34 - 40, 'Report a charge arrives later (49, Q3).', 'notice', anchor='middle')[0]]
    h = 24 + 38 + 32 + len(rows) * 32 + 32 + 140
    top = 844 - h
    s, _ = kv_card(top + 70, rows, rowh=32)
    b = [text(24, top + 24, title, 'h3')[0] + icon('x', 342, top + 22, NAVY) + hit(330, top + 10, 48, 48, 'close'), s] + btns
    return scrim() + sheet(top, '\n'.join(b))


def gen_31():
    F, ID, N = '31_Transaction-History', '31', 'Transaction-History'
    frame(F, ID, N, 'All', s31(), note='Mail icon = export receipts to email. Paginated')
    frame(F, ID, N, 'Filtered-Recharges', s31(filt='Recharges'))
    frame(F, ID, N, 'Purchases', s31('Purchases'), note='Purchases tab is optional at Q1 (PRD phase notes)')
    frame(F, ID, N, 'Receipt-Sheet', s31('Purchases', overlay=receipt_sheet()))
    frame(F, ID, N, 'Pending-Sheet', s31('Purchases', overlay=receipt_sheet('pending')))
    frame(F, ID, N, 'Call-Detail-Sheet', s31(overlay=receipt_sheet('call')))
    frame(F, ID, N, 'Export-Toast', s31(overlay=toast(738, 'Receipts sent to your email', 'mail')))
    frame(F, ID, N, 'Load-More', s31(state='more', scroll=140))
    frame(F, ID, N, 'Loading', s31(state='loading'))
    frame(F, ID, N, 'Empty', s31(state='empty'))
    frame(F, ID, N, 'Error', s31(state='error'))


# ============================================================ 32 Host Earnings Wallet (host tab 4)
def kyc_chip(x, y, st):
    kind = {'Verified': 'Verified', 'Pending': 'In review', 'Action needed': 'Action needed'}[st]
    s, w = status_pill(x, y, f'KYC {st.lower()}' if st != 'Action needed' else 'KYC action needed', kind, h=28)
    return s + hit(round(x), y - 8, round(w), 44, 'chip:KYC'), w


def s32(kyc='Verified', avail='12,400', state='ok', method=True, overlay=''):
    o = []
    y = 115
    if state == 'offline':
        b, y2 = offline_banner(y)
        o.append(b)
        y = y2 + 12
    if state == 'loading':
        o.append(skeleton(24, y, 342, 176, 20) + skeleton(24, y + 200, 342, 96, 16) + skeleton(24, y + 320, 342, 120, 16))
        return compose('\n'.join(o), tab_header('Earnings'), bar=host_bar(3, 3), clip=(103, TAB_BOTTOM + 24), cid='c32')
    o.append(f'<rect x="24" y="{y}" width="342" height="176" rx="20" fill="{BLUE}"/><circle cx="340" cy="{y + 10}" r="80" fill="{WHITE}" opacity="0.1"/>')
    o.append(t1(44, y + 34, 'Available to withdraw', 14, 600, WHITE) + gem(44, y + 50, 28, WHITE) + t1(80, y + 75, avail, 30, 700, WHITE, ls=-0.6))
    fiat = {'12,400': '≈ $86.80', '3,200': '≈ $22.40', '0': '≈ $0.00'}.get(avail, '')
    o.append(t1(44, y + 100, f'{fiat} estimated', 13, 500, WHITE))
    s, _ = kyc_chip(44, y + 126, kyc)
    o.append(s.replace(f'fill="{WHITE}"', f'fill="{WHITE}"', 1))
    y += 176 + 16
    s, y = kv_card(y, [('Lifetime earned', '86,950', 'gem'), ('Commission', '30%'), ('Pending payouts', '5,000', 'gem')])
    o.append(s + f'<!-- commission info -->' + icon('info', round(46 + tw('Commission', 15, 400)), y - 3 * 32 - 16 + 32 + 7, SLATE, 18) + hit(round(34 + tw('Commission', 15, 400)), y - 80, 44, 44, 'info:commission'))
    y += 16
    s, y = group(y, None, [('Withdrawal history', 'receipt', '35'), ('Payout method', 'landmark', '33', 'UPI ••• 1234' if method else 'Add'),
                           ('KYC status', 'badge-check', '51', kyc)])
    o.append(s)
    y += 16
    below = avail in ('3,200', '0')
    if not method:
        kind, lbl, note = 'primary', 'Add payout method', None
    elif kyc != 'Verified':
        kind, lbl, note = 'disabled', 'Request Cash Out', 'Complete KYC to withdraw.'
    elif below:
        kind, lbl, note = 'disabled', 'Request Cash Out', 'Minimum withdrawal is 5,000 diamonds.'
    else:
        kind, lbl, note = 'primary', 'Request Cash Out', None
    if state == 'offline':
        kind = 'disabled'
    a = button(CTA_ABOVE_BAR, lbl, kind, nav='34' if lbl.startswith('Request') else '33')
    if note:
        a = text(195, CTA_ABOVE_BAR - 30, note, 'notice', anchor='middle')[0] + a
    return compose('\n'.join(o), tab_header('Earnings'), actions=f'<rect x="0" y="{CTA_ABOVE_BAR - 40}" width="390" height="{BAR_TOP - CTA_ABOVE_BAR + 40}" fill="{CREAM}"/>' + a,
                   bar=host_bar(3, 3), overlay=overlay, clip=(103, CTA_ABOVE_BAR - 44), cid='c32')


def commission_sheet():
    top = 844 - 330
    b = [text(24, top + 24, 'How earnings work', 'h3')[0],
         text(24, top + 62, 'You keep 70% of what callers spend. Frndu keeps 30% to run the app, payments and safety.', 'body', w=342)[0]]
    s, _ = kv_card(top + 138, [('Caller spends', '1,000', 'gem'), ('Commission (30%)', '−300', 'gem'), ('You earn', '700', 'bold', SUCCESS)], rowh=30)
    b.append(s)
    return scrim() + sheet(top, '\n'.join(b))


def gen_32():
    F, ID, N = '32_Host-Wallet', '32', 'Host-Wallet'
    frame(F, ID, N, 'Default', s32(), note='Fiat estimate 10,000 diamonds = $70.00 (server config, OPEN #6). Earnings Analytics (50) and Levels (53) are Q3')
    frame(F, ID, N, 'Below-Minimum', s32(avail='3,200'), note='Minimum withdrawal 5,000 diamonds (configurable)')
    frame(F, ID, N, 'KYC-Pending', s32('Pending'))
    frame(F, ID, N, 'KYC-Action-Needed', s32('Action needed'))
    frame(F, ID, N, 'No-Payout-Method', s32('Action needed', method=False), note='First time: set up payout method (33)')
    frame(F, ID, N, 'Commission-Sheet', s32(overlay=commission_sheet()))
    frame(F, ID, N, 'Loading', s32(state='loading'))
    frame(F, ID, N, 'Offline', s32(state='offline'))


# ============================================================ 33 Withdrawal Method Setup
METHODS = [('UPI', 'smartphone', 'Instant to any UPI ID'), ('Bank transfer', 'landmark', 'IFSC + account number'),
           ('PayPal', 'globe', 'For hosts outside India'), ('Local wallet', 'wallet', 'Paytm, PhonePe and others')]


def s33(state='select', sel=None, err=None):
    o = []
    y = 115
    if state == 'cooldown':
        b, y2 = banner(y, 'You changed your payout details on 8 Oct. You can withdraw again from 15 Oct.', 'clock')
        o.append(b)
        y = y2 + 16
    if state in ('select', 'cooldown'):
        s, y = text(24, y, 'Where should we send your money?', 'h3')
        o.append(s)
        y += 16
        for lbl, ic, sub in METHODS:
            on = lbl == sel
            o.append(option_card(y, lbl, sub, icon_circle(ic, BTINT, BLUE, 48), 'selected' if on else 'unselected', key=f'card:{lbl}'))
            y += 72 + 12
        a, _ = cta([('btn', 'Continue', 'primary' if sel else 'disabled', 'form')])
        return page('Payout method', '\n'.join(o), a, cid='c33')
    # form
    bank = state.startswith('bank')
    filled = state in ('bank-filled', 'upi-filled', 'submitting', 'pan-error')
    s, y = text(24, y, 'Bank transfer details' if bank else 'UPI details', 'h3')
    o.append(s)
    y += 16
    fields = ([('Account holder name', 'Priya Sharma'), ('Account number', '•••• •••• 4521'), ('IFSC code', 'HDFC0001234')] if bank
              else [('Account holder name', 'Priya Sharma'), ('UPI ID', 'priya@okhdfc')])
    fields.append(('PAN', 'ABCDE1234F' if state != 'pan-error' else 'ABCD1234'))
    for lbl, val in fields:
        o.append(t1(24, y + 15, lbl, 14, 600, NAVY))
        st = 'error' if (lbl == 'PAN' and err) else 'empty'
        o.append(input_box(y + 24, val if filled else None, lbl if lbl != 'UPI ID' else 'name@bank', st))
        y += 24 + 56
        if lbl == 'PAN' and err:
            s, y = err_msg(24, y + 8, err)
            o.append(s)
        y += 16
    o.append(err_msg(24, y, 'Your details are encrypted. We check the name matches your PAN.', color=SLATE, icon_name='lock')[0])
    kind = 'primary' if filled and not err else 'disabled'
    if state == 'submitting':
        kind = 'primary-loading'
    a, top = cta([('btn', 'Submit', kind, '51 KYC status')])
    return page('Payout method', '\n'.join(o), a, bottom=top - 16, cid='c33')


def gen_33():
    F, ID, N = '33_Withdrawal-Setup', '33', 'Withdrawal-Setup'
    frame(F, ID, N, 'Select-Method', s33(), note='Methods per PRD §7.9: Bank, UPI, PayPal, Local wallet')
    frame(F, ID, N, 'Method-Selected', s33(sel='UPI'))
    frame(F, ID, N, 'UPI-Empty', s33('upi'))
    frame(F, ID, N, 'UPI-Filled', s33('upi-filled'))
    frame(F, ID, N, 'Bank-Filled', s33('bank-filled'))
    frame(F, ID, N, 'PAN-Error', s33('pan-error', err='Enter a valid 10-character PAN, like ABCDE1234F.'))
    frame(F, ID, N, 'Submitting', s33('submitting'))
    frame(F, ID, N, 'Edit-Cooldown', s33('cooldown', sel='UPI'), note='Changing details resets bank verification; 7-day cooldown before withdrawal')


# ============================================================ 51 KYC Status
def s51(state='review'):
    steps = {'notstarted': [('Identity', 'todo'), ('Bank / UPI', 'todo'), ('Review', 'todo')],
             'review': [('Identity', 'done'), ('Bank / UPI', 'done'), ('Review', 'now')],
             'verified': [('Identity', 'done'), ('Bank / UPI', 'done'), ('Review', 'done')],
             'rej-name': [('Identity', 'done'), ('Bank / UPI', 'fail'), ('Review', 'todo')],
             'rej-pan': [('Identity', 'fail'), ('Bank / UPI', 'todo'), ('Review', 'todo')],
             'manual': [('Identity', 'done'), ('Bank / UPI', 'fail'), ('Review', 'now')]}[state]
    o = []
    y = 123
    s, y = stepper(y, steps)
    o.append(s)
    y += 24
    head = {'notstarted': ('Verify to get paid', 'We need your PAN and payout details before your first withdrawal.', 'Not started'),
            'review': ('We are checking your details', 'This usually takes under 24 hours. We will notify you.', 'In review'),
            'verified': ('You are verified', 'You can now withdraw your earnings.', 'Verified'),
            'rej-name': ("The names don't match", 'The name on your bank account must match the name on your PAN.', 'Rejected'),
            'rej-pan': ("We couldn't verify your PAN", 'The PAN is invalid or inactive. Check it and try again.', 'Rejected'),
            'manual': ('Our team will review this', "Automatic checks failed 3 times. A person will review your details within 48 hours.", 'In review')}[state]
    o.append(card(24, y, 342, 0 + 128))
    s, yy = text(40, y + 16, head[0], 'h4', w=230)
    o.append(s + status_pill(350, y + 18, head[2], anchor='end')[0])
    o.append(text(40, yy + 4, head[1], 'body', w=310)[0])
    y += 128 + 24
    o.append(section_label(y, 'Your details'))
    y += 28
    s, y = kv_card(y, [('PAN', 'XXXXX1234X'), ('Name', 'Priya Sharma'), ('Payout', 'UPI ••• 1234')])
    o.append(s)
    y += 24
    if state != 'notstarted':
        o.append(section_label(y, 'Timeline'))
        y += 28
        ev = [('Details submitted', '8 Oct, 4:10 PM', 'done'), ('PAN verified', '8 Oct, 4:12 PM', 'done' if state != 'rej-pan' else 'fail')]
        if state != 'rej-pan':
            ev.append(('Bank check', '8 Oct, 4:20 PM', 'fail' if state in ('rej-name', 'manual') else 'done'))
        if state == 'verified':
            ev.append(('Approved', '9 Oct, 10:02 AM', 'done'))
        elif state in ('review', 'manual'):
            ev.append(('In review', 'Now', 'now'))
        s, y = timeline(y, ev)
        o.append(s)
    items = {'notstarted': [('btn', 'Complete KYC', 'primary', '33')], 'review': [('link', 'Contact support', 'support link')],
             'verified': [('btn', 'Request Cash Out', 'primary', '34')], 'rej-name': [('btn', 'Re-upload details', 'primary', '33'), ('link', 'Contact support', 'support link')],
             'rej-pan': [('btn', 'Re-upload details', 'primary', '33'), ('link', 'Contact support', 'support link')],
             'manual': [('link', 'Contact support', 'support link')]}[state]
    a, top = cta(items)
    return page('KYC status', '\n'.join(o), a, bottom=top - 16, cid='c51')


def gen_51():
    F, ID, N = '51_KYC-Status', '51', 'KYC-Status'
    frame(F, ID, N, 'Not-Started', s51('notstarted'), note='Identity (PAN / Tax ID) → Bank / UPI → Review. Data masked')
    frame(F, ID, N, 'In-Review', s51('review'))
    frame(F, ID, N, 'Verified', s51('verified'))
    frame(F, ID, N, 'Rejected-Name-Mismatch', s51('rej-name'))
    frame(F, ID, N, 'Rejected-Invalid-PAN', s51('rej-pan'))
    frame(F, ID, N, 'Manual-Review', s51('manual'), note='Max 3 automatic retries, then manual review')


# ============================================================ 34 Withdrawal Confirm  (+ 34.1 re-auth)
def s34(amount='10,000', state='ok', err=None, overlay=''):
    o = []
    y = 115
    if state == 'blocked':
        return center_state('lock', 'Complete KYC to withdraw', 'Withdrawals open once your identity and payout details are verified.',
                            [('btn', 'Go to KYC status', 'primary', '51'), ('link', 'Back to wallet', '32')], NAVY, CTINT)
    o.append(t1(24, y + 15, 'Amount to withdraw', 14, 600, NAVY) + t1(366, y + 15, 'Available 12,400', 13, 500, SLATE, 'end'))
    y += 28
    st = 'error' if err else 'focused' if state == 'typing' else 'empty'
    o.append(input_box(y, amount or None, '0', st, left_icon=None, left_pad=52, prefix=gem(40, y + 16, 24)))
    o.append(f'<rect x="290" y="{y + 12}" width="60" height="32" rx="16" fill="{BTINT}"/>' + t1(320, y + 33, 'Max', 13, 600, BLUE, 'middle') + hit(286, y + 6, 68, 44, 'btn:Max'))
    y += 56
    if err:
        s, y = err_msg(24, y + 8, err)
        o.append(s)
    y += 24
    if amount and not err:
        s, y = kv_card(y, [('Payout (estimate)', '$70.00'), ('Platform fee', '−$1.00'), ('You receive', '$69.00', 'bold', SUCCESS), ('Sent to', 'UPI ••• 1234')])
        o.append(s)
        y += 16
    o.append(err_msg(24, y, 'Payouts usually arrive in 3 to 5 business days.', color=SLATE, icon_name='clock')[0])
    kind = 'primary' if amount and not err else 'disabled'
    if state == 'submitting':
        kind = 'primary-loading'
    a, top = cta([('btn', 'Confirm Withdrawal', kind, '34.1 re-auth')])
    kb = keyboard('numeric') if state == 'typing' else ''
    if kb:
        a = ''
    return page('Cash out', '\n'.join(o), a, overlay + kb, bottom=top - 16, cid='c34')


def gen_34():
    F, ID, N = '34_Withdrawal-Confirm', '34', 'Withdrawal-Confirm'
    frame(F, ID, N, 'Default', s34(), note='Fee and fiat estimate are placeholders. Unreachable unless KYC Verified, even by deep link')
    frame(F, ID, N, 'Typing', s34('10,000', 'typing'))
    frame(F, ID, N, 'Empty', s34(None))
    frame(F, ID, N, 'Below-Minimum', s34('2,000', err='Minimum withdrawal is 5,000 diamonds.'))
    frame(F, ID, N, 'Above-Available', s34('15,000', err="You only have 12,400 diamonds available."))
    frame(F, ID, N, 'KYC-Blocked', s34(state='blocked'))


def gen_341():
    F, ID, N = '34.1_Withdrawal-Reauth', '34.1', 'Withdrawal-Reauth'
    base = s34()
    sub = 'Enter the 6-digit code we sent to +91 98765 43210.'
    frame(F, ID, N, 'OTP-Empty', base + otp_sheet('Confirm it’s you', sub), note='OTP or biometric re-auth before payout (PRD §7.9)')
    frame(F, ID, N, 'OTP-Filled', base + otp_sheet('Confirm it’s you', sub, '482913'))
    frame(F, ID, N, 'OTP-Wrong', base + otp_sheet('Confirm it’s you', sub, '482911', err='That code is wrong. 2 tries left.'))
    frame(F, ID, N, 'Biometric', base + scrim() + sheet(844 - 300, text(195, 844 - 270, 'Confirm with fingerprint', 'h3', anchor='middle')[0]
                                                         + icon('fingerprint', 163, 844 - 214, BLUE, 64)
                                                         + button(844 - 34 - 56, 'Use code instead', 'ghost', nav='OTP-Empty')))
    frame(F, ID, N, 'Confirming', base + otp_sheet('Confirm it’s you', sub, '482913', kind='primary-loading'))
    frame(F, ID, N, 'Requested', center_state('check-circle', 'Withdrawal requested', 'We will send $69.00 to UPI ••• 1234. It usually arrives in 3 to 5 business days.',
                                              [('btn', 'View withdrawal', 'primary', '35'), ('link', 'Back to wallet', '32')], SUCCESS, BTINT),
          note='Status: Pending → Processing → Completed (or Failed with diamonds refunded)')


# ============================================================ 35 Withdrawal History
WD = [('10,000', '9 Oct 2026', 'Pending', 'WD-30215'), ('8,000', '1 Oct 2026', 'Processing', 'WD-30102'),
      ('12,500', '15 Sep 2026', 'Completed', 'WD-29870'), ('6,000', '2 Sep 2026', 'Failed', 'WD-29711')]


def s35(state='list', overlay=''):
    o = []
    y = 115
    if state == 'loading':
        o.append(skeleton_rows(y, 5))
    elif state == 'empty':
        o.append(empty_state(360, 'receipt', 'No withdrawals yet.', 'Cash outs you request show up here.'))
    else:
        for amt, d, st, ref in WD:
            o.append(list_row(y, f'{amt} diamonds', d, sub2=ref, lead=lead_icon('landmark'), h=80,
                              right=lambda xr, yy, h, st=st: status_pill(xr, yy + (h - 24) / 2, st, anchor='end')[0], key=f'wd:{ref}'))
            y += 80
    return page('Withdrawals', '\n'.join(o), overlay=overlay, cid='c35')


def wd_sheet(kind='Completed'):
    rows = [('Amount', '12,500' if kind == 'Completed' else '6,000', 'gem'), ('You received' if kind == 'Completed' else 'Payout', '$86.50' if kind == 'Completed' else '$41.00'),
            ('Sent to', 'UPI ••• 1234'), ('Reference ID', 'WD-29870' if kind == 'Completed' else 'WD-29711')]
    top = 844 - (24 + 38 + 24 + 4 * 32 + 32 + 24 + (100 if kind == 'Failed' else 60) + 34)
    s, y = kv_card(top + 70, rows)
    b = [text(24, top + 24, 'Withdrawal details', 'h3')[0] + status_pill(366, top + 28, kind, anchor='end')[0], s]
    if kind == 'Failed':
        b.append(banner(y + 16, 'The bank rejected this payout. Your 6,000 diamonds are back in your wallet.', 'error')[0])
    else:
        b.append(link_row(y + 12, 'Download receipt', 'pdf'))
    return scrim() + sheet(top, '\n'.join(b))


def gen_35():
    F, ID, N = '35_Withdrawal-History', '35', 'Withdrawal-History'
    frame(F, ID, N, 'Default', s35(), note='Documents tab (statements, TDS) arrives in Q3')
    frame(F, ID, N, 'Detail-Completed', s35(overlay=wd_sheet('Completed')))
    frame(F, ID, N, 'Detail-Failed', s35(overlay=wd_sheet('Failed')), note='Failed payouts refund diamonds')
    frame(F, ID, N, 'Empty', s35('empty'))
    frame(F, ID, N, 'Loading', s35('loading'))


# ============================================================ 42 Account Deletion
def s42(checked=False, payout=False, overlay=''):
    o = []
    y = 115
    s, y = text(24, y, 'Delete your account', 'h2')
    o.append(s)
    s, y = text(24, y + 8, 'Your account is hidden right away. You have 14 days to change your mind by logging in again.', 'body')
    o.append(s)
    y += 24
    if payout:
        b, y = banner(y, 'You have a pending withdrawal of 10,000 diamonds. Wait for it to finish before deleting.', 'warning')
        o.append(b)
        y += 16
    for ic, t, b_ in [('gem', 'Diamonds are lost', 'Your balance of 1,250 diamonds will be forfeited. This cannot be refunded.'),
                      ('message-circle', 'Chats and history', 'Your chats, favourites and call history are deleted after 14 days.'),
                      ('file-text', 'Some records are kept', 'Payment and legal records are kept as the law requires, without your personal details.')][:2 if payout else 3]:
        s, y = info_card(y, ic, t, b_, CTINT if ic == 'gem' else BTINT, CORAL if ic == 'gem' else BLUE)
        o.append(s)
        y += 12
    y += 8
    o.append(checkbox(28, y + 2, checked) + text(64, y, 'I understand my diamonds will be lost and this cannot be undone after 14 days.', 'body', w=290, color=NAVY)[0])
    kind = 'destructive' if checked and not payout else 'disabled'
    a, top = cta([('btn', 'Permanently Delete Account', kind, 'OTP re-auth'), ('btn', 'Keep my account', 'ghost', 'back')])
    return page('Delete account', '\n'.join(o), a, overlay, bottom=top - 16, cid='c42')


def gen_42():
    F, ID, N = '42_Account-Deletion', '42', 'Account-Deletion'
    frame(F, ID, N, 'Default', s42(), note='14-day grace; login during grace offers 03A restore')
    frame(F, ID, N, 'Checked', s42(True))
    frame(F, ID, N, 'Pending-Payout', s42(True, payout=True), note='Pending payouts must be withdrawn first [recommended in PRD]')
    sub = 'Enter the 6-digit code we sent to +91 98765 43210.'
    frame(F, ID, N, 'OTP-Reauth', s42(True, overlay=otp_sheet('Confirm deletion', sub, '482913', btn='Delete account', kind='destructive')))
    frame(F, ID, N, 'Deleting', s42(True, overlay=otp_sheet('Confirm deletion', sub, '482913', btn='Delete account', kind='destructive-loading')))
    frame(F, ID, N, 'Deleted', center_state('check-circle', 'Your account is scheduled for deletion', 'It will be deleted on 24 Oct 2026. Log in before then to restore it.',
                                            [('btn', 'OK', 'primary', '01')], SLATE, CBORDER))


# ============================================================ 56 Suspended / Banned
def s56(kind='temp'):
    o = [blobs(), hero(196, 'shield-alert', WARN if kind != 'ban' else ERROR, CSURF if kind != 'ban' else CTINT)]
    title = {'temp': 'Account suspended until 17 Oct 2026', 'ban': 'Account permanently banned', 'host': 'Account suspended until 17 Oct 2026'}[kind]
    s, y = text(195, 284, title, 'h2', anchor='middle', w=320)
    o.append(s)
    if kind != 'ban':
        p, _ = pill(195, y + 8, '6 days 14 hours left', CSURF, NAVY, 'clock', h=32, anchor='middle')
        o.append(p)
        y += 48
    y += 16
    rows = [('Reason', 'Inappropriate content'), ('Reference ID', 'MOD-55120'), ('Date', '10 Oct 2026')]
    s, y = kv_card(y, rows, rowh=30)
    o.append(s)
    y += 12
    what = {'temp': 'You can’t make or take calls or send messages until then. Your diamonds stay in your wallet.',
            'host': 'You can’t go online until then. Your pending earnings are on hold while we review.',
            'ban': 'You can no longer use Frndu. Contact support if you think this is a mistake.'}[kind]
    s, y = text(24, y + 4, what, 'body', w=342)
    o.append(s)
    a, _ = action_area([('btn', 'Contact Support', 'primary', 'support link'), ('link', 'Community Guidelines', '68'), ('link', 'Log Out', '01')])
    o.append(a + status_bar() + home_indicator())
    return '\n'.join(o)


def gen_56():
    F, ID, N = '56_Account-Restricted', '56', 'Account-Restricted'
    frame(F, ID, N, 'Suspended-Temporary', s56('temp'), note='No other screen reachable. Appeal form + tracker arrive in Q3')
    frame(F, ID, N, 'Suspended-Host', s56('host'), note='Host earnings held during review')
    frame(F, ID, N, 'Banned-Permanent', s56('ban'), note='Wallet on permanent ban is OPEN #25')


# ============================================================ 57 Strike / Warning Notice
def s57(level='warning', thumb=False, ack=False):
    tag, kind, cons = {'warning': ('Warning', 'Warning', 'This is a warning. No action has been taken on your account.'),
                       's1': ('Strike 1 of 3', 'Warning', 'Your profile is shown less in search for 3 days.'),
                       's2': ('Strike 2 of 3', 'Warning', 'Your profile is shown less for 7 days.'),
                       's3': ('Final warning', 'Final warning', 'One more strike suspends your account.')}[level]
    if thumb:
        # blurred thumbnail of the flagged content replaces the hero icon
        o = [blobs(), blur_defs('blr57', 6), soft_blob(195, 186, 84, 64, CSURF),
             f'<clipPath id="th"><rect x="139" y="124" width="112" height="112" rx="20"/></clipPath>'
             f'<g clip-path="url(#th)"><g filter="url(#blr57)">{portrait(195, 180, 56, "girl", CTINT)}</g></g>'
             f'<rect x="139" y="124" width="112" height="112" rx="20" fill="{NAVY}" opacity="0.25"/>' + icon('eye-off', 179, 164, WHITE, 32)]
    else:
        o = [blobs(), hero(180, 'shield-alert', ERROR if level == 's3' else WARN, CTINT if level == 's3' else CSURF)]
    w = tw(tag, 12, 600) + 20
    o.append(status_pill(195 - w / 2, 260, tag, kind, h=28)[0])
    s, y = text(195, 304, 'We found a problem with a recent call', 'h3', anchor='middle', w=320)
    o.append(s)
    y += 16
    s, y = kv_card(y, [('Violation', 'Inappropriate content'), ('Call on', '9 Oct 2026, 9:41 PM'), ('Expires', '7 Jan 2027')], rowh=30)
    o.append(s)
    s, y = text(195, y + 16, cons, 'body', anchor='middle', w=320)
    o.append(s)
    a, _ = action_area([('btn', 'I Understand', 'primary-loading' if ack else 'primary', 'logged → 13 / 24'),
                        ('link', 'Community guidelines', '68'), ('link', 'Disagree? Appeal', '66 (Q3) / support link')])
    o.append(a + status_bar() + home_indicator())
    return '\n'.join(o)


def gen_57():
    F, ID, N = '57_Strike-Notice', '57', 'Strike-Notice'
    frame(F, ID, N, 'Warning', s57(), note='Shown after the call or on next app open; must be acknowledged. Consequence copy is a placeholder')
    frame(F, ID, N, 'Strike-1', s57('s1'))
    frame(F, ID, N, 'Strike-2-Thumbnail', s57('s2', thumb=True), note='Blurred thumbnail of flagged content, if any')
    frame(F, ID, N, 'Final-Warning', s57('s3'))
    frame(F, ID, N, 'Acknowledging', s57('s1', ack=True))


# ============================================================ 59 Safety Center
TIPS = [('lock', 'Keep personal details private', 'Never share your phone number, address, OTPs or bank details.'),
        ('coins', 'Never send money', 'Frndu staff and hosts will never ask you for money or gift cards.'),
        ('smartphone', 'Stay on Frndu', "Don't move to other apps. We can only protect you here."),
        ('alert-triangle', 'Spot scams', 'Be careful with links, urgent requests or offers that sound too good.')]


def s59(scroll=0, overlay=''):
    o = [f'<rect x="24" y="115" width="342" height="128" rx="20" fill="{BTINT}"/>', soft_blob(320, 179, 54, 44, WHITE), icon('shield-check', 296, 155, BLUE, 48)]
    s, y = text(44, 135, 'Your safety comes first', 'h4', w=220)
    o.append(s + text(44, y + 4, 'Tips, tools and help if something goes wrong.', 'notice', w=220)[0])
    y = 243 + 24
    o.append(section_label(y, 'Safety tips'))
    y += 28
    for ic, t, b in TIPS:
        s, y = info_card(y, ic, t, b)
        o.append(s)
        y += 12
    y += 12
    o.append(section_label(y, 'How we protect you'))
    y += 28
    for ic, t, b in [('badge-check', 'Verified hosts', 'Every host passes a video check before taking calls.'),
                     ('eye-off', 'Contact details hidden', 'Phone numbers and emails in chat are hidden automatically.'),
                     ('shield', 'Calls are moderated', 'We blur and end calls that break our rules.')]:
        s, y = info_card(y, ic, t, b, CSURF, NAVY)
        o.append(s)
        y += 12
    y += 12
    s, y = group(y, 'Report and block', [('How to report someone', 'flag', '39 guide'), ('Blocked users', 'user-x', '41'), ('Community Guidelines', 'users', '68')])
    o.append(s)
    y += 24
    o.append(section_label(y, 'Emergency help (India)'))
    y += 28
    s, y = kv_card(y, [('Emergency', '112'), ('Cyber crime helpline', '1930')], rowh=32)
    o.append(s)
    s, y = text(24, y + 12, 'Frndu is for adults 18+ only. Numbers to be confirmed by Legal before launch.', 'notice')
    o.append(s)
    a, top = cta([('btn', 'Report an emergency', 'destructive', '66 Safety (P0) — Q3; support link for now')])
    return page('Safety Center', '\n'.join(o), a, overlay, scroll=scroll, bottom=top - 16, cid='c59')


def gen_59():
    F, ID, N = '59_Safety-Center', '59', 'Safety-Center'
    frame(F, ID, N, 'Default', s59(), note='Reachable within 2 taps from calls (19 shield) and Settings. CMS content, Hindi/English')
    frame(F, ID, N, 'Scrolled-Protections', s59(scroll=560))
    frame(F, ID, N, 'Scrolled-Emergency', s59(scroll=1040), note='Helplines by account country; does not replace local authorities')
    frame(F, ID, N, 'Emergency-Dialog', s59(overlay=dialog('Are you in danger right now?', 'Call 112 first. Then tell us what happened and our safety team will act right away.',
                                                           [('Call 112', 'destructive', 'tel:112'), ('Report to Frndu', 'secondary', 'support'), ('Cancel', 'ghost', 'close')],
                                                           'alert-triangle', ERROR, CTINT)))


def gen_all():
    gen_40(); gen_401(); gen_60(); gen_41(); gen_63(); gen_65(); gen_68(); gen_64()
    gen_31(); gen_32(); gen_33(); gen_51(); gen_34(); gen_341(); gen_35(); gen_42(); gen_56(); gen_57(); gen_59()
