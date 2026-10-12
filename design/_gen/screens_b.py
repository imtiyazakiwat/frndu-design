"""Screens 04, 05, 06, 06.1, 12."""
from lib import *


def top_msg(kind, y=None):
    """Error/offline banner under the top bar (or under the status bar when there is no top bar)."""
    y = y or 63
    if kind == 'offline':
        return offline_banner(y)
    return banner(y, "We couldn't connect right now. Try again in a moment.", 'error')


# ============================================================ 04 Gender
def gender_card(x, y, label, ic, state):
    """Selectable card 165x168 r20 padding 16."""
    out = [f'<!-- Selectable card "{label}" ({state}) -->']
    if state == 'selected':
        out.append(f'<rect x="{x + 1}" y="{y + 1}" width="163" height="166" rx="20" fill="{BTINT}" stroke="{BLUE}" stroke-width="2"/>')
        out.append(check_badge(x + 165 - 16 - 24, y + 16))
        col = BLUE
    elif state == 'disabled':
        out.append(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="164" height="167" rx="20" fill="{CBORDER}" stroke="{CBORDER}"/>')
        col = DIS_T
    else:
        out.append(card(x, y, 165, 168, 20))
        col = NAVY
    out.append(icon_box(x + 16, y + 16, ic, 56, WHITE if state == 'selected' else (WHITE if state == 'disabled' else CSURF), col, 32, 16))
    out.append(t1(x + 16, y + 16 + 56 + 16 + 19, label, 18, 700, DIS_T if state == 'disabled' else NAVY))
    if state != 'disabled':
        out.append(hit(x, y, 165, 168, f'card:{label}'))
    return '\n'.join(out)


def gen_04():
    F, ID, N = '04_Gender', '04', 'Gender'
    frame(F, ID, N, 'Nothing-Selected', s04_body(), note='No top bar at first entry')
    frame(F, ID, N, 'Male-Selected', s04_body('m'))
    frame(F, ID, N, 'Female-Selected', s04_body('f'))
    frame(F, ID, N, 'Confirm-Male-Dialog', s04_body('m', overlay=dialog('Confirm Male?', 'This is permanent.',
          [('Confirm', 'primary', '06'), ('Go back', 'ghost', 'close dialog')])), note='Scrim tap does not dismiss')
    frame(F, ID, N, 'Confirm-Female-Dialog', s04_body('f', overlay=dialog('Confirm Female?', 'This is permanent.',
          [('Confirm', 'primary', '05'), ('Go back', 'ghost', 'close dialog')])), note='Scrim tap does not dismiss')
    frame(F, ID, N, 'Saving', s04_body('f', btn='primary-loading'))
    frame(F, ID, N, 'Locked-Re-entry', s04_body('f', locked=True), note='Reached with Back from 05; gender not reset')
    frame(F, ID, N, 'Error', s04_body('m', msg='error'))
    frame(F, ID, N, 'Offline', s04_body('m', btn='disabled', msg='offline'))


# ============================================================ 05 Role Select
def role_card(y, title, desc, ic, state):
    out = [f'<!-- Role card "{title}" ({state}) -->']
    if state == 'selected':
        out.append(f'<rect x="25" y="{y + 1}" width="340" height="118" rx="20" fill="{BTINT}" stroke="{BLUE}" stroke-width="2"/>')
        out.append(check_badge(366 - 16 - 24, y + 16))
    else:
        out.append(card(24, y, 342, 120, 20))
    out.append(icon_box(40, y + 16, ic, 48, WHITE if state == 'selected' else BTINT, BLUE))
    s, ty = text(104, y + 16, title, 'h4', w=210)
    out.append(s)
    s, _ = text(104, ty + 4, desc, 'body', w=222)
    out.append(s)
    out.append(hit(24, y, 342, 120, f'card:{title}'))
    return '\n'.join(out)


def gen_05():
    F, ID, N = '05_Role-Select', '05', 'Role-Select'
    frame(F, ID, N, 'Nothing-Selected', s05_body(), note='Female users only. "You can change this later." needs owner confirmation')
    frame(F, ID, N, 'User-Selected', s05_body('u'))
    frame(F, ID, N, 'Host-Selected', s05_body('h'))
    frame(F, ID, N, 'Loading', s05_body('h', btn='primary-loading'))
    frame(F, ID, N, 'Error', s05_body('h', msg='error'))


# ============================================================ 06 Basic Profile
LANGS6 = ['Hindi', 'English', 'Kannada', 'Tamil', 'Telugu', 'Marathi', 'Bengali', 'Malayalam', 'Gujarati', 'Punjabi', 'Urdu', 'Odia']


def s06_form(av='empty', nick=None, nick_state='empty', nick_msg=None, dob=None, dob_state='empty',
             langs=(), limit=False, ref='collapsed', ref_val=None, ref_state='empty'):
    o = []
    y = 103 + 8
    s, y = text(24, y, 'Set up your profile', 'h2')
    o.append(s)
    s, y = text(24, y + 8, 'This is how people will see you.', 'body')
    o.append(s)
    y += 24
    cy = y + 36
    o.append('<!-- Avatar block → photo sheet (Take photo / Choose from gallery / Remove) → 1:1 crop -->')
    if av in ('done', 'uploading'):
        o.append(avatar(195, cy, 72, img='rohan.jpg'))
    elif av == 'letter':
        o.append(avatar(195, cy, 72, letter=(nick or 'A')[0].upper()))
    else:
        o.append(avatar(195, cy, 72))
    if av == 'uploading':
        o.append(f'<circle cx="195" cy="{cy}" r="36" fill="{NAVY}" opacity="0.35"/>'
                 f'<circle cx="195" cy="{cy}" r="34" fill="none" stroke="{WHITE}" stroke-opacity="0.4" stroke-width="4"/>'
                 f'<path d="M195 {cy - 34} A34 34 0 0 1 229 {cy}" fill="none" stroke="{WHITE}" stroke-width="4" stroke-linecap="round"/>')
    o.append(f'<circle cx="221" cy="{cy + 26}" r="14" fill="{CREAM}"/><circle cx="221" cy="{cy + 26}" r="12" fill="{BLUE}"/>'
             + icon('camera', 214, cy + 19, WHITE, 14) + hit(159, cy - 36, 72, 72, 'avatar'))
    y += 72 + 8
    o.append(link_row(y - 12, 'Change photo' if av == 'done' else 'Add photo', 'photo sheet'))
    y += 20
    if av == 'rejected':
        s, y2 = err_msg(24 + 18, y + 8, "This photo can't be used. Try another one.", w=306)
        o.append(s)
        y = y2
    y += 24
    # Nickname
    o.append(t1(24, y + 15, 'Nickname', 14, 600, NAVY))
    cnt = f'{len(nick) if nick else 0}/20'
    o.append(t1(366, y + 15, cnt, 13, 400, ERROR if nick and len(nick) >= 20 else SLATE, 'end'))
    y += 20 + 8
    o.append(input_box(y, nick, 'Your nickname', nick_state))
    y += 56 + 8
    if nick_msg:
        s, y = err_msg(24, y, nick_msg)
    else:
        s, y = text(24, y, 'Letters, numbers, spaces and underscore.', 'notice')
    o.append(s)
    y += 24
    # DOB
    o.append(t1(24, y + 15, 'Date of birth', 14, 600, NAVY))
    y += 28
    o.append('<!-- Date of birth field → date picker sheet -->')
    o.append(input_box(y, dob, 'DD / MM / YYYY', dob_state, right_icon='calendar'))
    y += 64
    s, y = text(24, y, "You must be 18 or older. You can't change this later.", 'notice')
    o.append(s)
    y += 24
    # Languages
    o.append(t1(24, y + 15, 'Languages you speak', 14, 600, NAVY))
    o.append(t1(366, y + 15, f'{len(langs)} of 5', 13, 400, SLATE, 'end'))
    y += 24
    s, y = text(24, y, 'You can pick up to 5' if limit else 'Choose 1 to 5', 'notice')
    o.append(s)
    y += 12
    items = [(l, 'selected' if l in langs else ('disabled' if limit else 'unselected')) for l in LANGS6]
    s, y = chips_wrap(24, y, items)
    o.append('<!-- Multi-select chips -->' + s)
    y += 24
    o.append('<!-- Referral toggle → expand/collapse -->')
    o.append(f'<rect x="24" y="{y}" width="342" height="44" fill="#FFFFFF" fill-opacity="0"/>'
             + t1(24, y + 27, 'Have a referral code?', 14, 600, BLUE)
             + icon('chevron-up' if ref != 'collapsed' else 'chevron-down', 24 + tw('Have a referral code?', 14, 600) + 6, y + 12, BLUE, 20)
             + hit(24, y, 200, 44, 'link:Have a referral code?'))
    y += 44
    if ref != 'collapsed':
        y += 8
        o.append(input_box(y, ref_val, 'Enter code', ref_state))
        y += 64
        if ref == 'error':
            s, y = err_msg(24, y, "That code doesn't look right. You can still continue.")
            o.append(s)
        else:
            y += 19
    y += 24
    return '\n'.join(o), y


def photo_sheet():
    top = 844 - (24 + 30 + 16 + 3 * 56 + 24 + 34)
    b = [text(24, top + 24, 'Profile photo', 'h3')[0]]
    y = top + 70
    for ic, lbl, nav, col in [('camera', 'Take photo', 'camera → 1:1 crop', NAVY), ('image', 'Choose from gallery', 'gallery → 1:1 crop', NAVY),
                              ('trash', 'Remove photo', 'fallback avatar', ERROR)]:
        b.append(f'<!-- Photo picker row "{lbl}" → {nav} -->')
        b.append(icon_box(24, y + 4, ic, 48, BTINT if col == NAVY else CTINT, BLUE if col == NAVY else ERROR))
        b.append(t1(88, y + 34, lbl, 15, 500, col))
        b.append(hit(12, y, 366, 56, f'photo:{lbl}'))
        y += 56
    return scrim() + sheet(top, '\n'.join(b))


def date_sheet(day='12', month='Mar', year='1998'):
    top = 844 - (24 + 30 + 16 + 220 + 24 + 56 + 24 + 34)
    b = [text(24, top + 24, 'Date of birth', 'h3')[0]]
    y = top + 70
    b.append('<!-- Date picker (wheel) -->')
    b.append(f'<rect x="24" y="{y + 88}" width="342" height="44" rx="12" fill="{BTINT}"/>')
    cols = [(80, ['10', '11', day, '13', '14']), (195, ['Jan', 'Feb', month, 'Apr', 'May']),
            (310, [str(int(year) - 2), str(int(year) - 1), year, str(int(year) + 1), str(int(year) + 2)])]
    for cx, vals in cols:
        for i, v in enumerate(vals):
            yy = y + 22 + i * 44
            sel = i == 2
            b.append(t1(cx, yy + 6 + 12, v, 17 if sel else 15, 600 if sel else 400, NAVY if sel else (TERT if i in (1, 3) else DIS_T), 'middle'))
    y += 220 + 24
    b.append(button(y, 'Done', 'primary', nav='close sheet, fill field'))
    return scrim() + sheet(top, '\n'.join(b))


def crop_screen():
    o = [f'<rect width="390" height="844" fill="{NAVY}"/>']
    o.append(topbar('close', nav_back='06 (discard)', color=WHITE))
    o.append(status_bar(WHITE))
    y = 160
    o.append('<!-- Photo being cropped (placeholder image) -->')
    o.append(f'<clipPath id="cropimg"><rect x="0" y="{y - 60}" width="390" height="462"/></clipPath>'
             f'<g clip-path="url(#cropimg)"><rect x="0" y="{y - 60}" width="390" height="462" fill="{CTINT}"/>'
             f'<circle cx="195" cy="{y + 150}" r="80" fill="{CORAL}" opacity="0.45"/>'
             f'<ellipse cx="195" cy="{y + 360}" rx="150" ry="110" fill="{CORAL}" opacity="0.45"/></g>')
    o.append(f'<!-- Dim outside the crop window -->'
             f'<path d="M0 {y - 60} H390 V{y + 402} H0 Z M24 {y} V{y + 342} H366 V{y} Z" fill="{NAVY}" opacity="0.55" fill-rule="evenodd"/>')
    o.append(f'<rect x="24" y="{y}" width="342" height="342" fill="none" stroke="{WHITE}" stroke-width="2"/>')
    o.append(f'<circle cx="195" cy="{y + 171}" r="171" fill="none" stroke="{WHITE}" stroke-opacity="0.7" stroke-width="1.5" stroke-dasharray="6 6"/>')
    for gx in (138, 252):
        o.append(f'<rect x="{gx}" y="{y}" width="1" height="342" fill="{WHITE}" opacity="0.3"/>')
    for gy in (y + 114, y + 228):
        o.append(f'<rect x="24" y="{gy}" width="342" height="1" fill="{WHITE}" opacity="0.3"/>')
    o.append(t1(195, y + 342 + 32, 'Pinch and drag to adjust', 13, 400, WHITE, 'middle'))
    a, _ = action_area([('btn', 'Use photo', 'primary', '06 (avatar uploading)'), ('btn', 'Choose another', 'ghost-white', 'gallery')])
    o.append(a)
    o.append(home_indicator(WHITE))
    return '\n'.join(o)


def gen_06():
    F, ID, N = '06_Basic-Profile', '06', 'Basic-Profile'
    full = dict(av='done', nick='Aarav_22', nick_state='filled', dob='12 / 03 / 1998', dob_state='filled', langs=('Hindi', 'English'))
    frame(F, ID, N, 'Empty', s06_body(), note='Form scrolls; Complete Setup pinned. Photo optional? (question)')
    frame(F, ID, N, 'Partly-Filled', s06_body(av='letter', nick='Aarav_22', nick_state='filled'))
    frame(F, ID, N, 'Ready', s06_body(scroll=300, btn='primary', **full))
    frame(F, ID, N, 'Ready-Top', s06_body(btn='primary', **full))
    frame(F, ID, N, 'Photo-Sheet', s06_body(av='letter', nick='Aarav_22', nick_state='filled', overlay=photo_sheet()))
    frame(F, ID, N, 'Crop', crop_screen(), note='Full-screen state of 06, reused by 40.1 and 26')
    frame(F, ID, N, 'Avatar-Uploading', s06_body(av='uploading', nick='Aarav_22', nick_state='filled'))
    frame(F, ID, N, 'Avatar-Rejected', s06_body(av='rejected', nick='Aarav_22', nick_state='filled'), note='Default avatar + moderation message')
    frame(F, ID, N, 'Nickname-Error', s06_body(av='letter', nick='Aarav 98765', nick_state='error',
          nick_msg='Please keep phone numbers and bad words out of your nickname.'))
    frame(F, ID, N, 'Nickname-At-Limit', s06_body(av='letter', nick='Aarav_the_storyteller'[:20], nick_state='focused'))
    frame(F, ID, N, 'Date-Picker', s06_body(av='done', nick='Aarav_22', nick_state='filled', overlay=date_sheet()))
    frame(F, ID, N, 'Date-Under-18', s06_body(scroll=300, btn='primary', av='done', nick='Aarav_22', nick_state='filled', dob='12 / 03 / 2010',
          dob_state='filled', langs=('Hindi',)), note='Complete Setup → 06.1')
    frame(F, ID, N, 'Languages-Limit', s06_body(scroll=300, btn='primary', av='done', nick='Aarav_22', nick_state='filled', dob='12 / 03 / 1998',
          dob_state='filled', langs=('Hindi', 'English', 'Kannada', 'Tamil', 'Marathi'), limit=True))
    frame(F, ID, N, 'Referral-Expanded', s06_body(scroll=380, btn='primary', ref='expanded', ref_state='focused', **full))
    frame(F, ID, N, 'Referral-Error', s06_body(scroll=380, btn='primary', ref='error', ref_val='FRN12', ref_state='error', **full),
          note='Non-blocking; Launch accepts code without validation')
    frame(F, ID, N, 'Keyboard-Nickname', s06_body(scroll=200, kb='alpha', av='letter', nick='Aarav', nick_state='focused'))
    frame(F, ID, N, 'Keyboard-Referral', s06_body(scroll=640, kb='alpha', btn='primary', ref='expanded', ref_val='FRN', ref_state='focused', **full))
    frame(F, ID, N, 'Saving', s06_body(scroll=300, btn='primary-loading', **full))
    frame(F, ID, N, 'Error', s06_body(scroll=300, btn='primary', msg='error', **full))
    frame(F, ID, N, 'Offline', s06_body(scroll=300, btn='disabled', msg='offline', **full))


# ============================================================ 06.1 Under-18 Blocked
def s061_body(h1, body, b1, b2, b3):
    o = [blobs(bottom=False)]
    y = 47 + 40
    o.append(shield_illus(y))
    y += 160 + 24
    s, y = text(195, y, h1, 'h1', anchor='middle')
    o.append(s)
    s, y = text(195, y + 12, body, 'body', anchor='middle')
    o.append(s)
    a, _ = action_area([('btn', b1, 'secondary', '68'), ('btn', b2, 'secondary', 'support link (age verification)'), ('btn', b3, 'ghost', '01')])
    o.append(a)
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def gen_061():
    F, ID, N = '06.1_Under-18-Blocked', '06.1', 'Under-18-Blocked'
    frame(F, ID, N, 'Default', s061_body('You must be 18 or older to use this app',
          "Frndu is for adults only. If you think this is a mistake, contact support and we'll look into it.",
          'Read our policy', 'Contact Support', 'Log Out'), note='NEW screen; no back, not dismissible; no primary button')
    frame(F, ID, N, 'Hindi', s061_body('इस ऐप का उपयोग करने के लिए आपकी उम्र 18 वर्ष या उससे अधिक होनी चाहिए',
          'Frndu केवल वयस्कों के लिए है। अगर आपको लगता है कि यह गलती है, तो सपोर्ट से संपर्क करें, हम इसे देखेंगे।',
          'हमारी नीति पढ़ें', 'सपोर्ट से संपर्क करें', 'लॉग आउट'), note='Hindi translation is draft; needs review')
    frame(F, ID, N, 'Long-Text', s061_body('You must be 18 or older to use this app',
          "Frndu is for adults only. If you think this is a mistake, contact support and we'll look into it. "
          'We may ask you to confirm your age before you can continue.',
          'Read our policy', 'Contact Support', 'Log Out'), note='Stress test for long copy')


# ============================================================ 12 Permissions Primer
PERMS = [('camera', 'Camera', 'So you and your host can see each other on video calls.'),
         ('mic', 'Microphone', 'So you can talk on voice and video calls.'),
         ('bell', 'Notifications', "So you don't miss incoming calls and messages.")]


PERM_DIALOGS = {
    'Camera': ('camera', 'Camera access is off', 'Turn it on in Settings to use video.'),
    'Microphone': ('mic', 'Microphone access is off', 'Turn it on in Settings to talk on calls.'),
    'Notifications': ('bell', 'Notifications are off', "Turn them on in Settings so you don't miss calls."),
}


def perm_dialog(kind):
    ic, t, b = PERM_DIALOGS[kind]
    return dialog(t, b, [('Open Settings', 'primary', 'OS settings'), ('Not now', 'ghost', 'close dialog')], icon_name=ic)


def gen_12():
    F, ID, N = '12_Permissions-Primer', '12', 'Permissions-Primer'
    frame(F, ID, N, 'Default', s12_body(), note='T4 full-height sheet, no back. System prompts not designed')
    for k in PERM_DIALOGS:
        frame(F, ID, N, f'Dialog-{k}-Off', s12_body(perm_dialog(k)), note='Reused before first call and on 08')


# ============================================================ RESTYLE (reference look) — overrides above
from illus import hero_gender, hero_girl_clean, hero_shield, hero_permissions
from screens_a import cta


def s04_body(sel=None, btn=None, locked=False, overlay=None, msg=None):
    o = [blobs()]
    y = 103
    if msg:
        b, bb = top_msg(msg, 107)
        o.append(b)
        y = bb - 8
    o.append(hero_gender(y + 12))
    y += 12 + 150 + 16
    s, y = text(195, y, 'Choose your gender', 'h1', anchor='middle')
    o.append(s)
    s, y = text(195, y + 8, "This can't be changed later, so choose carefully.", 'body', anchor='middle', w=300)
    o.append(s)
    y += 24

    def st(g):
        if sel == g:
            return 'selected'
        return 'disabled' if locked else 'unselected'
    o.append(option_card(y, 'Female', "I'm a woman", face_circle('girl', CTINT), st('f'), key='card:Female'))
    o.append(option_card(y + 80, 'Male', "I'm a man", face_circle('boy', BTINT), st('m'), key='card:Male'))
    y += 160 + 12
    msg_txt = 'Your gender is locked.' if locked else 'Gender cannot be altered once confirmed. Choose carefully.'
    o.append(banner(y, msg_txt, 'lock')[0])
    nav = ('05' if sel == 'f' else '06') if locked else f'Confirm dialog, then {"05" if sel == "f" else "06"}'
    c, _ = cta('Continue', btn or ('primary' if sel else 'disabled'), nav)
    o.append(c)
    o.append(topbar(None, step=3))
    o.append(status_bar())
    if overlay:
        o.append(overlay)
    o.append(home_indicator())
    return '\n'.join(o)


def s05_body(sel=None, btn=None, msg=None):
    o = [blobs()]
    y = 103
    if msg:
        b, bb = top_msg(msg, 107)
        o.append(b)
        y = bb - 8
    o.append(hero_girl_clean(y + 8))
    y += 8 + 164 + 12
    s, y = text(195, y, 'How would you like to use Frndu?', 'h1', anchor='middle', w=310)
    o.append(s)
    s, y = text(195, y + 8, 'You can change this later.', 'body', anchor='middle')
    o.append(s)
    y += 20
    o.append(option_card(y, 'Explore as User', 'Talk to hosts and enjoy conversations.', icon_circle('users', BTINT, BLUE),
                         'selected' if sel == 'u' else 'unselected', key='card:Explore as User', h=84))
    o.append(option_card(y + 96, 'Become a Host & Earn', 'Get verified and earn from your conversations.', icon_circle('crown', CTINT, CORAL),
                         'selected' if sel == 'h' else 'unselected', key='card:Become a Host & Earn', h=84))
    nav = {'u': '06', 'h': '07'}.get(sel, '06 (User) / 07 (Host)')
    c, _ = cta('Continue', btn or ('primary' if sel else 'disabled'), nav)
    o.append(c)
    o.append(topbar('back', nav_back='04 (locked state)', step=4))
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def shield_illus(y):
    return hero_shield(y)


def s12_body(overlay=None):
    o = [blobs(), scrim(0.25)]
    top = 59
    b = []
    y = top + 24
    b.append(hero_permissions(y))
    y += 132
    s, y = text(195, y, "Let's get you set up", 'h2', anchor='middle')
    b.append(s)
    s, y = text(195, y + 8, "We'll ask for three permissions so calls and updates work.", 'body', anchor='middle', w=300)
    b.append(s)
    y += 20
    for ic, ttl, desc in PERMS:
        bg, col = {'camera': (CTINT, CORAL), 'mic': (BTINT, BLUE), 'bell': (CSURF, WARN)}[ic]
        b.append(f'<rect x="24.75" y="{y + 0.75}" width="340.5" height="70.5" rx="16" fill="{WHITE}" stroke="{CBORDER}" stroke-width="1.5"/>')
        b.append(f'<circle cx="64" cy="{y + 36}" r="24" fill="{bg}"/>' + icon(ic, 52, y + 24, col))
        b.append(t1(104, y + 30, ttl, 15, 700, NAVY))
        b.append(text(104, y + 36, desc, 'notice', w=244)[0])
        y += 80
    c, _ = cta('Grant Permissions', 'primary', 'system prompts one by one, then 13', bottom=794 - 56 - 12)
    b.append(c)
    b.append(button(738, 'Not now', 'ghost', nav='13'))
    o.append(status_bar())
    o.append(sheet(top, '\n'.join(b)))
    if overlay:
        o.append(overlay)
    o.append(home_indicator())
    return '\n'.join(o)


def s06_body(scroll=0, btn='disabled', overlay=None, kb=None, msg=None, **kw):
    o = [blobs(bottom=False)]
    form, h = s06_form(**kw)
    y0 = 103
    if msg:
        b, bb = top_msg(msg, 107)
        o.append(b)
        y0 = bb + 4
    label = 'Complete Setup'
    if kb:
        c, top = cta(label, btn, '12 (under 18 → 06.1)', bottom=KB_TOP - 16)
        o.append(clip_group('c06', y0, top - 24, form, scroll))
        o.append(f'<rect x="0" y="{top - 24}" width="390" height="{KB_TOP - top + 24}" fill="{CREAM}"/>')
    else:
        c, top = cta(label, btn, '12 (under 18 → 06.1)')
        o.append(clip_group('c06', y0, top - 24, form, scroll))
    o.append(c)
    o.append(topbar('back', nav_back='04 or 05', step=5))
    o.append(status_bar())
    if kb:
        o.append(keyboard(kb))
    if overlay:
        o.append(overlay)
    o.append(home_indicator())
    return '\n'.join(o)

def gen_all():
    gen_04(); gen_05(); gen_06(); gen_061(); gen_12()
