"""Screens 07, 08, 09A, 10, 11, 11A."""
from lib import *
from screens_b import perm_dialog, top_msg


# ============================================================ 07 Verification Method
def gen_07():
    F, ID, N = '07_Verification-Method', '07', 'Verification-Method'
    frame(F, ID, N, 'Unselected', s07_body(False), note='Owner to choose: preselected or not (both drawn)')
    frame(F, ID, N, 'Selected', s07_body(True))
    frame(F, ID, N, 'Preselected-Variant', s07_body(True), note='Alternative: card selected on entry')
    frame(F, ID, N, 'Loading', s07_body(loading=True))
    frame(F, ID, N, 'Offline', s07_body(True, msg='offline'))


# ============================================================ 08 Video Verification
CX, CY, R = 195, 335, 140


def prompt_bar(y, prompt, step):
    o = ['<!-- Prompt bar: current gesture prompt (random order per attempt) -->', card(24, y, 342, 66, 16),
         t1(195, y + 12 + 19, prompt, 18, 700, NAVY, 'middle')]
    for i in range(4):
        o.append(f'<circle cx="{195 - 24 + i * 16}" cy="{y + 12 + 26 + 8 + 4}" r="4" fill="{BLUE if i == step else BORDER}"/>')
    return '\n'.join(o)


def precheck_chips(y, fails=()):
    items = [('face', 'Face centred', 'scan-face'), ('light', 'Good light', 'sun'), ('mic', 'Mic on', 'mic')]
    widths = [tw(l, 12, 500) + 20 + 6 + 24 for _, l, _ in items]
    gap = 8
    x = (390 - (sum(widths) + gap * 2)) / 2
    o = ['<!-- Pre-check chips -->']
    for (k, lbl, ic), w in zip(items, widths):
        bad = k in fails
        o.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="32" rx="16" fill="{CTINT if bad else WHITE}" stroke="{CBORDER}"/>')
        o.append(icon('alert-triangle' if bad else 'check-circle', round(x + 10), y + 6, WARN if bad else SUCCESS, 20))
        o.append(t1(round(x + 36), y + 21, lbl, 12, 500, NAVY))
        x += w + gap
    return '\n'.join(o)


def s08_body(state='ready'):
    o = [blobs(top=False, bottom=False)]
    back = state in ('ready', 'precheck-light', 'precheck-face', 'review', 'face-lost', 'daily-limit', 'offline', 'permission', 'upload-failed')
    y = 103 + 8
    o.append(text(195, y, 'Follow the prompts', 'h3', anchor='middle')[0])
    o.append(text(195, y + 38, 'Keep your face in the circle.', 'body', anchor='middle')[0])
    ring = {'recording': 0.4, 'review': 1, 'uploading': 1, 'upload-failed': 1}.get(state, 0)
    o.append(viewfinder(face=state not in ('face-lost',), ring=ring, review=state == 'review',
                        offset=60 if state == 'precheck-face' else 0, dim=state == 'precheck-light'))
    timer = {'recording': '00:09', 'review': '00:15', 'uploading': '00:15', 'upload-failed': '00:15'}.get(state, '00:15')
    o.append('<!-- Countdown (component) -->')
    if state == 'recording':
        o.append(f'<circle cx="{195 - 30}" cy="{CY + 146 + 12 + 10}" r="5" fill="{CORAL}"/>')
    o.append(t1(195, CY + 146 + 12 + 15, timer, 14, 600, NAVY, 'middle'))
    py = CY + 146 + 12 + 20 + 24  # 537
    fails = ()
    if state == 'precheck-light':
        o.append(banner(py, 'We need better light.', 'warning')[0])
        fails = ('light',)
    elif state == 'precheck-face':
        o.append(banner(py, 'Centre your face in the circle.', 'warning')[0])
        fails = ('face',)
    elif state == 'face-lost':
        o.append(banner(py, "We lost your face. Let's start again.", 'warning')[0])
        fails = ('face',)
    elif state == 'daily-limit':
        o.append(banner(py, "You've used all your tries for today. Come back tomorrow.", 'info', icon_name='clock')[0])
    elif state == 'offline':
        o.append(offline_banner(py)[0])
    elif state == 'upload-failed':
        o.append(banner(py, 'Upload paused. Check your connection.', 'error')[0])
    elif state in ('recording',):
        o.append(prompt_bar(py, 'Turn your head right', 1))
    elif state in ('review', 'uploading'):
        o.append(prompt_bar(py, 'All done. Check your video.', 3) if state == 'review' else prompt_bar(py, 'Sending your video…', 3))
    else:
        o.append(prompt_bar(py, 'Look straight', 0))
    if state not in ('review', 'uploading', 'upload-failed', 'daily-limit', 'offline'):
        o.append(precheck_chips(py + 66 + 16, fails))
    items = {
        'ready': [('btn', 'Start', 'primary', 'recording (stays on 08)')],
        'precheck-light': [('btn', 'Start', 'disabled')],
        'precheck-face': [('btn', 'Start', 'disabled')],
        'face-lost': [('btn', 'Start', 'primary', 'restart recording')],
        'recording': [('btn', 'Cancel', 'ghost', 'stop, back to ready')],
        'review': [('btn', 'Submit', 'primary', '09A'), ('btn', 'Retake', 'ghost', 'ready')],
        'uploading': [('progress', 'Uploading… 60%', 60)],
        'upload-failed': [('btn', 'Try again', 'primary', 'resume upload')],
        'daily-limit': [('btn', 'Start', 'disabled')],
        'offline': [('btn', 'Start', 'disabled')],
        'permission': [('btn', 'Start', 'disabled')],
    }[state]
    a, _ = action_area(items)
    o.append(a)
    o.append(topbar('back' if back else None, nav_back='07'))
    o.append(status_bar())
    if state == 'permission':
        o.append(perm_dialog('Camera'))
    o.append(home_indicator())
    return '\n'.join(o)


def gen_08():
    F, ID, N = '08_Video-Verification', '08', 'Video-Verification'
    for st, name, note in [('ready', 'Ready', 'Permissions granted, pre-checks pass'), ('precheck-light', 'Precheck-Low-Light', ''),
                           ('precheck-face', 'Precheck-Face-Off-Centre', ''), ('recording', 'Recording', 'Ring animates over 15 s; back hidden'),
                           ('review', 'Review', 'Recorded clip plays inside the circle'), ('face-lost', 'Face-Lost', 'Face lost > 2 s, ring resets'),
                           ('uploading', 'Uploading', 'Back hidden while uploading'), ('upload-failed', 'Upload-Failed', 'Try again resumes'),
                           ('permission', 'Permission-Denied', 'Dialog from 12'), ('daily-limit', 'Daily-Limit', '5 attempts per day'),
                           ('offline', 'Offline', '')]:
        frame(F, ID, N, name, s08_body(st), note=note)


# ============================================================ 09A Host Languages
LANGS9 = ['Hindi', 'English', 'Kannada', 'Tamil', 'Telugu', 'Marathi', 'Bengali', 'Malayalam', 'Gujarati', 'Punjabi',
          'Urdu', 'Odia', 'Assamese', 'Konkani', 'Bhojpuri', 'Rajasthani']


def s09a_content(y, sel=('Hindi', 'English', 'Kannada'), query=None, state='list', limit=False):
    o = []
    s, y = text(24, y, 'Which languages can you speak?', 'h2')
    o.append(s)
    s, y = text(24, y + 8, 'Pick up to 8. Callers use this to find you.', 'body')
    o.append(s)
    y += 24
    o.append(input_box(y, query, 'Search languages', 'focused' if query else 'empty', left_icon='search'))
    y += 56 + 16
    cnt = f'{len(sel)} of 8 selected' + (" · That's the maximum" if limit else '')
    o.append(t1(24, y + 14, cnt, 13, 400, SLATE))
    y += 19 + 12
    if state == 'loading':
        x = 24
        for i, w in enumerate([72, 88, 96, 64, 84, 100, 76, 92, 70, 86]):
            if x + w > 366:
                x = 24
                y += 52
            o.append(skeleton(x, y, w, 40, 20))
            x += w + 8
    elif state == 'failed':
        s, yy = err_msg(24, y, "We couldn't load languages. Check your connection and try again.")
        o.append(s)
        o.append(f'<!-- Retry → reload list -->' + button(yy + 16, 'Try again', 'secondary', x=24, w=160))
    elif state == 'noresult':
        o.append(f'<circle cx="195" cy="{y + 48}" r="32" fill="{BTINT}"/>' + icon('search', 179, y + 32, BLUE, 32))
        o.append(text(195, y + 96, "We couldn't find that language", 'bodyM', anchor='middle')[0])
        o.append(text(195, y + 120, 'Check the spelling or try another name.', 'body', anchor='middle')[0])
    else:
        langs = [l for l in LANGS9 if not query or l.lower().startswith(query.lower())]
        items = [(l, 'selected' if l in sel else ('disabled' if limit else 'unselected')) for l in langs]
        s, y = chips_wrap(24, y, items, rowgap=12)
        o.append('<!-- Multi-select chips (same component as 06) -->' + s)
    return '\n'.join(o)


def s09a_sheet_body():
    o = [f'<rect width="390" height="844" fill="{CREAM}"/>', scrim()]
    top = 59
    b = [s09a_content(top + 24)]
    a, _ = action_area([('btn', 'Save', 'primary', 'save + close sheet, return to 24 / 26')])
    b.append(a)
    o.append(status_bar(WHITE))
    o.append(sheet(top, '\n'.join(b)))
    o.append(home_indicator())
    return '\n'.join(o)


def gen_09a():
    F, ID, N = '09A_Host-Languages', '09A', 'Host-Languages'
    frame(F, ID, N, 'Prefilled', s09a_body(), note='Profile languages preselected')
    frame(F, ID, N, 'None-Selected', s09a_body(sel=()))
    eight = ('Hindi', 'English', 'Kannada', 'Tamil', 'Telugu', 'Marathi', 'Bengali', 'Urdu')
    frame(F, ID, N, 'Limit-Reached', s09a_body(sel=eight, limit=True, btn='primary'))
    frame(F, ID, N, 'Searching', s09a_body(query='Ta'))
    frame(F, ID, N, 'No-Result', s09a_body(query='Xyz', state='noresult'))
    frame(F, ID, N, 'Loading', s09a_body(sel=(), state='loading'))
    frame(F, ID, N, 'Load-Failed', s09a_body(sel=(), state='failed'))
    frame(F, ID, N, 'Offline', s09a_body(msg='offline', btn='disabled'))
    frame(F, ID, N, 'As-Sheet', s09a_sheet_body(), note='Opened from 24 pre-online check and 26 edit languages')


# ============================================================ 10 Verification Pending
def s10_body(longer=False, msg=None):
    o = [blobs(bottom=False)]
    y = 47 + 40
    if msg:
        b, bb = top_msg(msg)
        o.append(b)
        y = bb + 24
    o.append(clock_illus(y))
    y += 160 + 24
    s, y = text(195, y, 'Application Under Review', 'h1', anchor='middle')
    o.append(s)
    copy = "This is taking a little longer than usual. We're on it." if longer else 'Usually 1 to 2 hours for video.'
    s, y = text(195, y + 8, copy, 'bodyL', anchor='middle')
    o.append(s)
    y += 24
    n = nlines("We'll let you know as soon as there's a decision.", 'body', 270)
    h = max(56, 32 + n * 22)
    o.append(card(24, y, 342, h) + icon('bell', 40, y + (h - 24) / 2, BLUE))
    o.append(text(76, y + (h - n * 22) / 2, "We'll let you know as soon as there's a decision.", 'body', w=270)[0])
    a, _ = action_area([('btn', 'Explore App as Guest User', 'secondary', '13 (decision push/live update → 11)')])
    o.append(a)
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def s10_banner_component():
    o = ['<!-- Persistent banner frame for Girish to place on 13 and other guest screens while pending -->',
         topbar(None, tab_title='Home'), status_bar()]
    o.append(banner(119, 'Host verification in progress', 'clock')[0])
    o.append(f'<rect x="24" y="179" width="342" height="120" rx="16" fill="{SKEL}" opacity="0.6"/>'
             f'<rect x="24" y="315" width="342" height="120" rx="16" fill="{SKEL}" opacity="0.6"/>')
    o.append(t1(195, 248, 'Screen 13 content (owner: Girish)', 13, 400, TERT, 'middle'))
    o.append(home_indicator())
    return '\n'.join(o)


def gen_10():
    F, ID, N = '10_Verification-Pending', '10', 'Verification-Pending'
    frame(F, ID, N, 'Waiting', s10_body(), note='No back. Decision arrives by push/live update → cross-fade to 11')
    frame(F, ID, N, 'Taking-Longer', s10_body(longer=True))
    frame(F, ID, N, 'Offline', s10_body(msg='offline'))
    frame(F, ID, N, 'Persistent-Banner-Component', s10_banner_component(), note='Banner placed under top bar on 13')


# ============================================================ 11 Verification Result
REASONS = [
    ('Poor-Lighting', 'The light was too low. Try again in a brighter place.'),
    ('Script-Mismatch', "We couldn't match what you said to the script. Try again."),
    ('Liveness-Failed', "We couldn't confirm the gestures. Follow the prompts and try again."),
    ('Face-Not-Visible', "We couldn't see your face clearly. Keep it centred in the circle."),
    ('Suspected-Minor', "We couldn't confirm that you meet our age requirement."),
    ('Duplicate-Account', 'This looks like an account that already exists.'),
]


def confetti():
    pieces = [(60, 140, BLUE, 0), (110, 96, CORAL, 30), (300, 120, BLUE, -20), (336, 200, CORAL, 45), (40, 260, CORAL, 15),
              (350, 300, BLUE, 60), (150, 170, BTINT, 0), (250, 84, CTINT, 0), (80, 360, BLUE, -40), (320, 410, CORAL, 20),
              (196, 120, CORAL, 70), (270, 220, BTINT, 0)]
    o = ['<!-- Confetti (plays once, 2 s; static under reduced motion) -->']
    for x, y, c, rot in pieces:
        if c in (BTINT, CTINT):
            o.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{c}"/>')
        else:
            o.append(f'<rect x="{x}" y="{y}" width="10" height="16" rx="3" fill="{c}" opacity="0.8" transform="rotate({rot} {x + 5} {y + 8})"/>')
    return '\n'.join(o)


def s11_rejected(reason=None, permanent=False, h1="We couldn't verify you this time", btn='Re-apply Now'):
    o = [blobs(bottom=False)]
    y = 47 + 40
    o.append(reject_illus(y))
    y += 160 + 24
    s, y = text(195, y, h1, 'h1', anchor='middle')
    o.append(s)
    y += 24
    if permanent:
        s, y = text(195, y - 12, "We can't approve this application.", 'body', anchor='middle')
        o.append(s)
        a, _ = action_area([('link', 'Contact Support', 'support link')])
    else:
        o.append('<!-- Reason banner (by reason code) -->')
        s, y = banner(y, reason, 'reason')
        o.append(s)
        a, _ = action_area([('btn', btn, 'primary', '07')])
    o.append(a)
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def gen_11():
    F, ID, N = '11_Verification-Result', '11', 'Verification-Result'
    frame(F, ID, N, 'A-Approved', s11_approved(), note='Coral CTA allowed: emotional moment')
    for code, txt in REASONS:
        frame(F, ID, N, f'B-Rejected-{code}', s11_rejected(txt))
    frame(F, ID, N, 'C-Permanent-Rejection', s11_rejected(permanent=True), note='No re-apply; never say how decision was reached')
    frame(F, ID, N, 'B-Rejected-Hindi', s11_rejected('रोशनी बहुत कम थी। किसी ज़्यादा रोशनी वाली जगह पर फिर से कोशिश करें।',
          h1='इस बार हम आपको सत्यापित नहीं कर सके', btn='अभी फिर से आवेदन करें'), note='Hindi draft translation')


# ============================================================ 11A Host Tutorial & Terms
GUIDES = [('book-open', 'Host guidelines'), ('coins', 'Payout structure'), ('heart', 'Code of conduct'), ('phone-call', 'Call handling')]
PLACEHOLDER = 'Placeholder, content from Client. A short explanation of this topic for new hosts, written in a warm and simple way.'


def s11a_content(video=None, cb='hidden', updated=False):
    o = []
    y = 111
    if updated:
        s, y = banner(119, 'Our Host Terms have been updated', 'info')
        o.append(s)
        y += 16
    s, y = text(24, y, 'Before you start', 'h2')
    o.append(s)
    if video is not None:
        y += 16
        o.append('<!-- Tutorial video card 16:9 (only if Client supplies a video) -->')
        o.append(f'<rect x="24" y="{y}" width="342" height="192" rx="16" fill="{NAVY}"/>'
                 f'<circle cx="195" cy="{y + 96}" r="28" fill="{WHITE}" opacity="0.95"/>' + icon('play', 185, y + 84, NAVY))
        y += 192 + 8
        o.append(f'<rect x="24" y="{y}" width="342" height="4" rx="2" fill="{BORDER}"/>'
                 f'<rect x="24" y="{y}" width="{342 * video:.0f}" height="4" rx="2" fill="{SUCCESS if video >= 0.9 else BLUE}"/>')
        y += 8
        cap = f'Watched {int(video * 100)}%. You can continue now.' if video >= 0.9 else 'Watch at least 90% to continue'
        s, y = text(24, y, cap, 'caption')
        o.append(s)
    y += 16
    for ic, ttl in GUIDES:
        n = nlines(PLACEHOLDER, 'body', 310)
        h = 16 + 26 + 8 + n * 22 + 16
        o.append(f'<!-- Guideline card "{ttl}" (expandable) -->' + card(24, y, 342, h))
        o.append(icon(ic, 40, y + 17, BLUE))
        o.append(t1(76, y + 16 + 19, ttl, 18, 700, NAVY))
        o.append(icon('chevron-down', 326, y + 17, TERT))
        o.append(text(40, y + 16 + 26 + 8, PLACEHOLDER, 'body', w=310)[0])
        y += h + 12
    y += 12
    o.append(f'<!-- Checkbox row ({cb}) -->')
    o.append(checkbox(36, y + 12, checked=cb == 'checked', disabled=cb == 'locked', highlight=cb == 'unlocked-highlight'))
    o.append(text(84, y + 12, 'I accept the [[Host Terms & Conditions]]', 'body', w=282, color=NAVY if cb != 'locked' else TERT)[0])
    o.append('<!-- Host Terms & Conditions link → 68 -->')
    if cb == 'locked':
        o.append(text(84, y + 36, 'Finish the guidelines to continue', 'caption', w=282)[0])
    y += 48 + 24
    return '\n'.join(o), y


def s11a_body(video=None, cb='unchecked', scroll=0, btn=None, updated=False, msg=None):
    o = [blobs(bottom=False)]
    content, h = s11a_content(video, cb, updated)
    btn = btn or ('primary' if cb == 'checked' else 'disabled')
    a, top = action_area([('btn', 'Proceed to Dashboard', btn, '24')])
    y0 = 103
    if msg:
        b, bb = top_msg(msg, 107)
        o.append(b)
        y0 = bb + 4
    o.append(clip_group('c11a', y0, top - 24, content, scroll))
    o.append(a)
    o.append(topbar(None, title='Host guidelines'))
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def gen_11a():
    F, ID, N = '11A_Host-Tutorial-Terms', '11A', 'Host-Tutorial-Terms'
    frame(F, ID, N, 'Static-Top', s11a_body(None, 'locked'), note='No back (first-time gate). Static variant: checkbox unlocks at end of scroll (proposal)')
    frame(F, ID, N, 'Static-End-Unchecked', s11a_body(None, 'unchecked', scroll=300))
    frame(F, ID, N, 'Static-End-Checked', s11a_body(None, 'checked', scroll=300))
    frame(F, ID, N, 'Video-Locked', s11a_body(0.4, 'locked'), note='Checkbox locked until 90% watched')
    frame(F, ID, N, 'Video-Locked-End', s11a_body(0.4, 'locked', scroll=520))
    frame(F, ID, N, 'Video-Unlocked', s11a_body(0.92, 'unlocked-highlight', scroll=520), note='Short highlight on unlock')
    frame(F, ID, N, 'Video-Checked', s11a_body(0.92, 'checked', scroll=520))
    frame(F, ID, N, 'Terms-Updated', s11a_body(None, 'locked', updated=True), note='Re-shown when Host Terms version changes')
    frame(F, ID, N, 'Saving', s11a_body(None, 'checked', scroll=300, btn='primary-loading'))
    frame(F, ID, N, 'Error', s11a_body(None, 'checked', scroll=300, msg='error'))
    frame(F, ID, N, 'Offline', s11a_body(None, 'checked', scroll=300, btn='disabled', msg='offline'))


# ============================================================ RESTYLE (reference look) — overrides above
from illus import hero_verify, hero_clock, hero_approved, hero_rejected, girl
from screens_a import cta


def s07_body(sel=False, loading=False, msg=None):
    o = [blobs()]
    y = 103
    if msg:
        b, bb = top_msg(msg, 107)
        o.append(b)
        y = bb - 8
    o.append(hero_verify(y + 8))
    y += 8 + 168 + 8
    s, y = text(195, y, 'Verify Your Identity to Start Hosting', 'h2', anchor='middle', w=300)
    o.append(s)
    s, y = text(195, y + 8, 'A quick video helps us make sure every host is real.', 'body', anchor='middle', w=300)
    o.append(s)
    y += 20
    if loading:
        o.append('<!-- Loading: checking for an existing application (may skip to 10 or 24) -->')
        o.append(f'<rect x="24.75" y="{y + 0.75}" width="340.5" height="94.5" rx="16" fill="{WHITE}" stroke="{CBORDER}" stroke-width="1.5"/>'
                 + f'<circle cx="68" cy="{y + 48}" r="28" fill="{SKEL}"/>' + skeleton(112, y + 26, 150, 16) + skeleton(112, y + 52, 200, 12) + skeleton(112, y + 70, 160, 12))
    else:
        o.append(option_card(y, 'Video (Fast Track)', 'A 15-second recording with a few simple gestures. Review in 1 to 2 hours.',
                             icon_circle('video', BTINT, BLUE), 'selected' if sel else 'unselected', key='card:Video', h=96))
    y += 96 + 12
    o.append(f'<!-- Privacy card -->'
             f'<rect x="24.75" y="{y + 0.75}" width="340.5" height="74.5" rx="16" fill="{CTINT}" fill-opacity="0.6" stroke="{CTINT}" stroke-width="1.5"/>'
             f'<circle cx="64" cy="{y + 38}" r="22" fill="{CTINT}"/>' + icon('shield', 52, y + 26, CORAL)
             + t1(104, y + 30, 'Your privacy matters', 15, 700, NAVY)
             + text(104, y + 36, 'Only our review team sees your video. It is never shown publicly.', 'notice', w=244)[0])
    btn = 'disabled' if loading or not sel or msg == 'offline' else 'primary'
    c, _ = cta('Proceed with Selected Method', btn, '08')
    o.append(c)
    o.append(topbar('back', nav_back='06 (host profile)', step=6))
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def viewfinder(face=True, ring=0.0, review=False, offset=0, dim=False):
    import math
    o = ['<!-- Camera viewfinder (component): live front camera inside a 280 circle -->',
         f'<clipPath id="vf"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>',
         f'<g clip-path="url(#vf)"><rect x="{CX - R}" y="{CY - R}" width="{2 * R}" height="{2 * R}" fill="{CTINT}"/>'
         f'<circle cx="{CX + 70}" cy="{CY - 80}" r="70" fill="{BTINT}"/>']
    if face:
        o.append('<!-- Camera feed placeholder (illustrated person) -->' + girl(CX + offset, CY - 20, 2.0))
    if dim:
        o.append(f'<rect x="{CX - R}" y="{CY - R}" width="{2 * R}" height="{2 * R}" fill="{NAVY}" opacity="0.45"/>')
    o.append('</g>')
    o.append(f'<ellipse cx="{CX}" cy="{CY - 14}" rx="92" ry="112" fill="none" stroke="{WHITE}" stroke-width="2.5" stroke-dasharray="8 8" opacity="0.95"/>')
    rr = R + 6
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{rr}" fill="none" stroke="{BORDER}" stroke-width="4"/>')
    if ring >= 1:
        o.append(f'<circle cx="{CX}" cy="{CY}" r="{rr}" fill="none" stroke="{BLUE}" stroke-width="4"/>')
    elif ring > 0:
        a = 2 * math.pi * ring
        ex, ey = CX + rr * math.sin(a), CY - rr * math.cos(a)
        o.append(f'<path d="M{CX} {CY - rr} A{rr} {rr} 0 {1 if ring > 0.5 else 0} 1 {ex:.1f} {ey:.1f}" fill="none" stroke="{BLUE}" stroke-width="4" stroke-linecap="round"/>')
    if review:
        o.append(f'<circle cx="{CX}" cy="{CY}" r="28" fill="{WHITE}" filter="url(#sh-card)"/>' + icon('play', CX - 10, CY - 12, NAVY, 24))
    return '\n'.join(o)


def s09a_body(sel=('Hindi', 'English', 'Kannada'), query=None, state='list', limit=False, btn=None, msg=None):
    o = [blobs(bottom=False)]
    y = 111
    if msg:
        b, bb = top_msg(msg, 107)
        o.append(b)
        y = bb + 16
    o.append(s09a_content(y, sel, query, state, limit))
    btn = btn or ('primary' if sel and state in ('list', 'noresult') else 'disabled')
    c, _ = cta('Continue', btn, '10 (as sheet from 24/26: save + close)')
    o.append(c)
    o.append(topbar('back', nav_back='08 (hidden while upload runs)', step=7))
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def clock_illus(y):
    return hero_clock(y)


def s11_approved():
    o = [blobs(), hero_approved(150)]
    y = 150 + 96 + 76 + 32
    bw = tw('Host Mode', 14, 600) + 32
    o.append(f'<!-- Host Mode badge -->'
             f'<rect x="{195 - bw / 2:.0f}" y="{y}" width="{bw:.0f}" height="32" rx="16" fill="{BLUE}"/>' + t1(195, y + 21, 'Host Mode', 14, 600, WHITE, 'middle'))
    y += 32 + 16
    s, y = text(195, y, "You're verified!", 'display', anchor='middle')
    o.append(s)
    o.append(text(195, y + 8, 'Welcome to Frndu hosting.', 'bodyL', anchor='middle')[0])
    c, _ = cta('Launch Host Dashboard', 'coral', '11A (first time) / 24')
    o.append(c)
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def reject_illus(y):
    return hero_rejected(y)

def gen_all():
    gen_07(); gen_08(); gen_09a(); gen_10(); gen_11(); gen_11a()
