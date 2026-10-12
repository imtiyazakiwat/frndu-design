"""Screens 01, 01.1, 02, 03, 03A."""
from lib import *

LEGAL_01 = 'By continuing you agree to our [[Terms of Service]] and [[Privacy Policy]]'
LEGAL_02 = 'By continuing you agree to our [[Terms]] and [[Privacy Policy]]'


# ============================================================ 01 Splash & Welcome
def gen_01():
    F, ID, N = '01_Splash-Welcome', '01', 'Splash-Welcome'
    frame(F, ID, N, 'Loading', s01_body('loading'), note='Checking saved session, max 2 s')
    frame(F, ID, N, 'Ready', s01_body('ready'))
    frame(F, ID, N, 'Low-Power', s01_body('ready', low_power=True), note='Static background frame; battery shows low-power')


# ============================================================ 01.1 Language Sheet
def lang_row(y, native, eng, selected, pressed=False, loading=False):
    out = [f'<!-- Language option "{native}" → apply + close sheet, return to caller -->']
    fill = BTINT if selected else (SKEL if pressed else WHITE)
    out.append(f'<rect x="24" y="{y}" width="342" height="64" rx="12" fill="{fill}"/>')
    if eng:
        out.append(t1(40, y + 28, native, 15, 500, NAVY))
        out.append(t1(40, y + 47, eng, 12, 500, SLATE))
    else:
        out.append(t1(40, y + 37, native, 15, 500, NAVY))
    if loading:
        out.append(spinner(338, y + 32, BLUE))
    elif selected:
        out.append(icon('check', 326, y + 20, BLUE))
    out.append(hit(24, y, 342, 64, f'lang:{native}'))
    return '\n'.join(out)


def s011_body(sel='en', pressed=None, loading=False):
    top = 580
    body = [text(24, top + 24, 'Choose your language', 'h3')[0],
            lang_row(top + 70, 'हिन्दी', 'Hindi', sel == 'hi', pressed == 'hi', loading and sel == 'hi'),
            lang_row(top + 142, 'English', None, sel == 'en', pressed == 'en', loading and sel == 'en')]
    return '\n'.join([s01_body('ready'), scrim(), sheet(top, '\n'.join(body)), home_indicator()])


def gen_011():
    F, ID, N = '01.1_Language-Sheet', '01.1', 'Language-Sheet'
    frame(F, ID, N, 'English-Selected', s011_body('en'), note='Same sheet opened from 01, 40 and 00.1')
    frame(F, ID, N, 'Hindi-Selected', s011_body('hi'))
    frame(F, ID, N, 'Pressed', s011_body('en', pressed='hi'))
    frame(F, ID, N, 'Switching-Loading', s011_body('hi', loading=True), note='200 ms while language applies')


# ============================================================ 02 Phone Input
def country_sheet():
    top = 220
    b = []
    s, y = text(24, top + 24, 'Choose your country', 'h3')
    b.append(s)
    y += 16
    b.append(input_box(y, None, 'Search countries', 'empty', left_icon='search'))
    y += 56 + 8
    rows = [('IN', 'India', '+91', True), ('AE', 'United Arab Emirates', '+971', False), ('US', 'United States', '+1', False),
            ('GB', 'United Kingdom', '+44', False), ('SA', 'Saudi Arabia', '+966', False), ('SG', 'Singapore', '+65', False),
            ('AU', 'Australia', '+61', False), ('CA', 'Canada', '+1', False), ('NP', 'Nepal', '+977', False)]
    for code, name, dial, sel in rows:
        if y + 56 > 810:
            break
        b.append(f'<!-- Country row {name} → select + close sheet -->')
        if sel:
            b.append(f'<rect x="12" y="{y}" width="366" height="56" rx="12" fill="{BTINT}"/>')
        b.append(flag_in(24, y + 20) if code == 'IN' else flag_placeholder(24, y + 20, code))
        b.append(t1(60, y + 34, name, 15, 500, NAVY))
        dx = 366 - (32 if sel else 0)
        b.append(t1(dx, y + 34, dial, 15, 400, SLATE, 'end'))
        if sel:
            b.append(icon('check', 342, y + 16, BLUE))
        b.append(hit(12, y, 366, 56, f'country:{name}'))
        y += 56
    return scrim() + sheet(top, '\n'.join(b))


def gen_02():
    F, ID, N = '02_Phone-Input', '02', 'Phone-Input'
    num = '98765 43210'
    frame(F, ID, N, 'Empty', s02_body())
    frame(F, ID, N, 'Focused', s02_body(None, 'focused'))
    frame(F, ID, N, 'Filled-Valid', s02_body(num, 'filled', btn='primary'))
    frame(F, ID, N, 'Invalid-Number', s02_body('98765 4321', 'error', "That number doesn't look right. Check it and try again.", btn='disabled'))
    frame(F, ID, N, 'Rate-Limited', s02_body(num, 'filled', 'Too many tries. Try again in 04:59', btn='disabled'), note='Live MM:SS countdown')
    frame(F, ID, N, 'Send-Failed', s02_body(num, 'filled', "We couldn't send the code right now. Try again in a moment.", btn='primary'))
    frame(F, ID, N, 'Blocked-Number', s02_body(num, 'filled', "This number can't be used. Please contact support.", btn='disabled'),
          note='PLACEHOLDER copy. OPEN decision D8 / tasks.md T-11; do not finalise')
    frame(F, ID, N, 'Sending', s02_body(num, 'filled', btn='primary-loading'))
    frame(F, ID, N, 'Offline', s02_body(num, 'filled', btn='disabled', banner_kind='offline'))
    frame(F, ID, N, 'Country-Picker', s02_body(num, 'filled', btn='primary', overlay=country_sheet()), note='Auto-detected country preselected')
    frame(F, ID, N, 'Keyboard-Open', s02_body('98765', 'focused', btn='disabled', kb=True), note='Button 16 above keyboard')


# ============================================================ 03 SMS OTP
def gen_03():
    F, ID, N = '03_SMS-OTP', '03', 'SMS-OTP'
    frame(F, ID, N, 'Empty', s03_body(), note='Resend counting down (60 s)')
    frame(F, ID, N, 'Partly-Filled', s03_body('482', focus=3))
    frame(F, ID, N, 'Complete', s03_body('482913', focus=None, btn='primary'), note='Autofilled/pasted boxes look identical')
    frame(F, ID, N, 'Verifying', s03_body('482913', focus=None, btn='primary-loading'))
    frame(F, ID, N, 'Wrong-Code', s03_body('482193', 'error', None, "That code isn't right. Try again.", btn='disabled'))
    frame(F, ID, N, 'Lockout', s03_body('', 'disabled', None, 'Too many tries. Try again in 09:59', resend='none', btn='disabled'), note='After 5 wrong tries; live countdown')
    frame(F, ID, N, 'Resend-Available', s03_body(resend='available'))
    frame(F, ID, N, 'Resend-Sending', s03_body(resend='sending'))
    frame(F, ID, N, 'Code-Sent-Toast', s03_body(overlay=toast(666, 'Code sent again')))
    frame(F, ID, N, 'Code-Expired', s03_body('482913', 'error', None, 'This code has expired. Request a new one.', resend='available', btn='disabled'))
    frame(F, ID, N, 'Offline', s03_body('482', focus=3, banner_kind='offline'))
    frame(F, ID, N, 'Keyboard-Open', s03_body('48', focus=2, kb=True))


# ============================================================ 03A Account Restore
def s03a_content(days='12 days left', host=False):
    o = []
    y = 47 + 24
    o.append(restore_illus(y))
    y += 160 + 24
    s, y = text(24, y, 'Your account is scheduled for deletion', 'h1')
    o.append(s)
    y += 8
    s, y = text(24, y, days, 'h2')
    o.append(s)
    s, y = text(24, y, 'Your account will be permanently deleted on 21 Oct 2026.', 'body')
    o.append(s)
    y += 24
    rows = [('Diamond balance', 'gem', '1,250'), ('Host status', None, 'Approved host' if host else 'Not a host'),
            ('Pending withdrawals', None, '₹ 1,400' if host else 'None')]
    ch = 16 + 3 * 22 + 2 * 12 + 16
    o.append('<!-- Summary Card -->' + card(24, y, 342, ch))
    ry = y + 16
    for lab, ic, val in rows:
        o.append(t1(40, ry + 16, lab, 14, 600, SLATE))
        o.append(t1(350, ry + 16, val, 15, 500, NAVY, 'end'))
        if ic:
            o.append(gem(350 - tw(val, 15, 500) - 24, ry + 2, 18))
        ry += 34
    y += ch + 16
    s, y = banner(y, 'Diamonds and earnings are lost when your account is deleted.', 'warning')
    o.append(s)
    return '\n'.join(o), y


def s03a_body(days='12 days left', primary='primary', msg=None, banner_top=None, scroll=0, host=False):
    o = [blobs(bottom=False)]
    content, bottom = s03a_content(days, host)
    if msg:
        s, _ = err_msg(24, bottom + 12, msg)
        content += '\n' + s
    items = [('btn', 'Restore My Account', primary, '13 (24 for a host)'), ('btn', 'Continue with Deletion', 'ghost', '01 (logged out)'),
             ('link', 'Contact Support', 'support link (66 not built at Launch)')]
    a, top = action_area(items, cover=None)
    y0 = 47
    if banner_top:
        o.append(banner_top[0])
        y0 = banner_top[1] + 8
    o.append(clip_group('c3a', y0, top - 24, content, scroll))
    o.append(a)
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def gen_03a():
    F, ID, N = '03A_Account-Restore', '03A', 'Account-Restore'
    frame(F, ID, N, 'Default', s03a_body(), note='No top bar, no back. Content scrolls under pinned actions')
    frame(F, ID, N, 'Default-Scrolled', s03a_body(scroll=110))
    frame(F, ID, N, 'Host-Account', s03a_body(host=True, scroll=110))
    frame(F, ID, N, 'Last-Day', s03a_body('Last day'))
    frame(F, ID, N, 'Restoring', s03a_body(primary='primary-loading', scroll=110))
    frame(F, ID, N, 'Restore-Limit-Reached', s03a_body(primary='disabled', msg="You've reached the restore limit. Contact support.", scroll=150),
          note='Max 3 restores in 12 months')
    b = banner(63, "We couldn't connect right now. Try again in a moment.", 'error')
    frame(F, ID, N, 'Error', s03a_body(banner_top=b, scroll=170))
    b = offline_banner(63)
    frame(F, ID, N, 'Offline', s03a_body(primary='disabled', banner_top=b, scroll=170))


# ============================================================ RESTYLE (reference look) — overrides above
from illus import (logo_mark, hero_phone_call, hero_phone_otp, hero_calendar)

LEGAL_REF = 'By continuing, you agree to our [[Terms]] and [[Privacy Policy]]'


def legal_below(top, s=LEGAL_REF):
    """Legal line under the CTA (reference). Links Blue + underline → 68."""
    svg, _ = text(195, top, s, 'caption', anchor='middle', weight=400, size=12, lh=18)
    return '<!-- Legal: Terms / Privacy → 68 -->' + svg.replace(f'<tspan fill="{BLUE}" font-weight="600">', f'<tspan fill="{BLUE}" font-weight="500" text-decoration="underline">')


def cta(label, kind='primary', nav=None, legal=False, bottom=794, arrow=True):
    """Primary CTA in the reference position; optional legal line underneath."""
    y = bottom - 56 - (34 if legal else 0)
    ic = 'arrow-right' if arrow and kind in ('primary', 'coral', 'pressed') else None
    out = button(y, label, kind, nav=nav, icon_right=ic)
    if legal:
        out += legal_below(y + 56 + 14)
    return out, y


def lang_pill(label='English'):
    w = tw(label, 14, 600) + 24 + 8 + 16 + 8 + 16 + 4
    x = 366 - w
    return ('<!-- Language pill → 01.1 Language Sheet -->'
            f'<rect x="{x:.0f}" y="55" width="{w:.0f}" height="40" rx="20" fill="{WHITE}" stroke="{BORDER}"/>'
            + icon('globe', round(x + 14), 63, NAVY) + t1(round(x + 46), 80, label, 14, 600, NAVY)
            + icon('chevron-down', round(x + w - 30), 67, SLATE, 16) + hit(round(x), 51, round(w), 48, 'right:languages'))


def s01_body(state='ready', low_power=False):
    out = [blobs()]
    if state == 'loading':
        out.append(logo_mark(195, 380, 168, sparks_on=True))
        out.append(text(195, 452, 'Frndu', 'display', anchor='middle')[0])
    else:
        out.append('<!-- Lottie background: static frame (low-power mode freezes here) -->'
                   f'<circle cx="58" cy="200" r="10" fill="{BTINT}"/><circle cx="340" cy="300" r="7" fill="{CTINT}"/>'
                   f'<circle cx="330" cy="640" r="12" fill="{BTINT}"/>')
        out.append(logo_mark(195, 282, 168, sparks_on=True))
        out.append(text(195, 352, 'Frndu', 'display', anchor='middle')[0])
        s, y = text(195, 420, 'Talk to someone who gets you.', 'display', anchor='middle', w=330)
        out.append(s)
        out.append(text(195, y + 16, 'Real conversations with real people, anytime you need a friend.', 'bodyL', anchor='middle', w=300)[0])
        c, _ = cta('Get Started', nav='02', legal=True)
        out.append(c)
        out.append(lang_pill())
    out.append(status_bar(low_power=low_power))
    out.append(home_indicator())
    out.append('<!-- Automatic routing (no tap): user session → 13; host session → 24; banned/suspended → 56; deleting → 03A; new legal version → 68; offline/maintenance/force update/error → 64 -->')
    return '\n'.join(out)


# ------------------------------------------------------------ 02 Phone Input
def s02_content(value=None, state='empty', msg=None, msg_kind='error', y0=103):
    o = [hero_phone_call(y0 + 16)]
    y = y0 + 16 + 164 + 20
    s, y = text(195, y, 'How should we reach you?', 'h1', anchor='middle', w=300)
    o.append(s)
    s, y = text(195, y + 8, "We'll text you a code to confirm it's you.", 'bodyL', anchor='middle', w=342)
    o.append(s)
    y += 24
    o.append(phone_input(y, value, state))
    y += 56 + 8
    o.append('<!-- Error slot (reserved 2 lines) -->')
    if msg:
        s, _ = err_msg(24, y, msg, color=ERROR if msg_kind == 'error' else SLATE)
        o.append(s)
    y += 38 + 4
    lw = tw('We only use your number to sign you in.', 13, 400) + 28
    o.append(icon('lock', round(195 - lw / 2), y, SLATE, 20) + t1(round(195 - lw / 2 + 28), y + 15, 'We only use your number to sign you in.', 13, 400, SLATE))
    return '\n'.join(o)


def s02_body(value=None, state='empty', msg=None, btn='disabled', banner_kind=None, overlay=None, kb=False):
    o = [blobs()]
    y0 = 103
    if banner_kind == 'offline':
        b, bb = offline_banner(107)
        o.append(b)
        y0 = bb - 12
    if kb:
        o.append(clip_group('c02', 103, KB_TOP - 16 - 56 - 16, s02_content(value, state, msg), scroll=290))
        c, _ = cta('Send Verification Code', btn, '03', bottom=KB_TOP - 16)
    else:
        o.append(s02_content(value, state, msg, y0=y0))
        c, _ = cta('Send Verification Code', btn, '03 (after server accepts)', legal=True)
    o.append(c)
    o.append(topbar('back', nav_back='01', step=1))
    o.append(status_bar())
    if kb:
        o.append(keyboard('numeric'))
    if overlay:
        o.append(overlay)
    o.append(home_indicator())
    return '\n'.join(o)


# ------------------------------------------------------------ 03 SMS OTP
def s03_content(digits='', ostate='empty', focus=0, msg=None, resend='count', y0=103):
    o = [hero_phone_otp(y0 + 12)]
    y = y0 + 12 + 164 + 16
    s, y = text(195, y, 'Enter the OTP', 'h1', anchor='middle')
    o.append(s)
    s, y = text(195, y + 8, 'Code sent to **+91 98765 43210**', 'body', anchor='middle')
    o.append(s)
    o.append(link_row(y - 6, 'Change number', '02'))
    y += 38 + 16
    o.append(otp_boxes(y, digits, ostate, focus))
    y += 56 + 12
    if msg:
        mw = tw(msg, 13, 500) + 28
        s, _ = err_msg(round(195 - mw / 2), y, msg, w=342)
        o.append(s)
    y += 19 + 20
    if resend == 'count':
        o.append(t1(195, y + 14, 'Resend code in 00:42', 13, 400, SLATE, 'middle'))
    elif resend == 'available':
        o.append(link_row(y - 12, 'Resend code', 'resend (stays on 03)'))
    elif resend == 'sending':
        o.append(spinner(140, y + 9, BLUE, 7) + t1(156, y + 14, 'Sending a new code…', 13, 400, SLATE))
    return '\n'.join(o)


def s03_body(digits='', ostate='empty', focus=0, msg=None, resend='count', btn='disabled', banner_kind=None, overlay=None, kb=False):
    o = [blobs()]
    y0 = 103
    if banner_kind == 'offline':
        b, bb = offline_banner(107)
        o.append(b)
        y0 = bb - 12
    if kb:
        o.append(clip_group('c03', 103, KB_TOP - 16 - 56 - 12, s03_content(digits, ostate, focus, msg, resend), scroll=190))
        c, _ = cta('Verify', btn, '04 new / 13 or 24 returning', bottom=KB_TOP - 16)
    else:
        o.append(s03_content(digits, ostate, focus, msg, resend, y0))
        c, _ = cta('Verify', btn, 'new user → 04; returning → 13 / 24; banned → 56; deleting → 03A; under-18 → 06.1')
    o.append(c)
    o.append(topbar('back', nav_back='02', step=2))
    o.append(status_bar())
    if kb:
        o.append(keyboard('numeric'))
    if overlay:
        o.append(overlay)
    o.append(home_indicator())
    return '\n'.join(o)


# ------------------------------------------------------------ 03A Account Restore (hero swap)
def restore_illus(y):
    return hero_calendar(y)

def gen_all():
    gen_01(); gen_011(); gen_02(); gen_03(); gen_03a()
