"""00 Components: shared component sheets owned by Imtiyaz (brief: 'Shared components you own')."""
import os

from lib import *
import lib
from screens_b import gender_card, role_card, date_sheet, photo_sheet, crop_screen, s06_body
from screens_c import viewfinder, s08_body
from screens_a import s011_body


def write_sheet(name, w, h, body, title):
    path = os.path.join(ROOT, '00_Components', f'00_Components_{name}.svg')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    d = defs_block().replace('<clipPath id="screen"><rect width="390" height="844"/></clipPath>',
                             f'<clipPath id="screen"><rect width="{w}" height="{h}"/></clipPath>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">\n'
           f'<title>Frndu – 00 Components – {title}</title>\n{d}\n<g clip-path="url(#screen)">\n'
           f'<rect width="{w}" height="{h}" fill="{CREAM}"/>\n{body}\n</g>\n</svg>\n')
    with open(path, 'w') as f:
        f.write(svg)
    REGISTRY.append(('00', 'Components', name, os.path.relpath(path, ROOT), title))


def heading(x, y, s):
    return t1(x, y, s, 22, 700, NAVY, ls=-0.2)


def lbl(x, y, s):
    return t1(x, y, s, 12, 500, SLATE)


def at(x, y, body):
    return f'<g transform="translate({x} {y})">{body}</g>'


def sheet_controls_1():
    o = [t1(40, 64, 'Buttons, inputs, OTP', 32, 700, NAVY, ls=-0.6),
         lbl(40, 90, 'One canonical definition per component. Variants, not copies. H56, radius 16, Button 16/700.')]
    # Buttons grid
    o.append(heading(40, 140, 'Button'))
    states = ['Default', 'Pressed', 'Disabled', 'Loading']
    variants = [('Primary', {'Default': 'primary', 'Pressed': 'pressed', 'Disabled': 'disabled', 'Loading': 'primary-loading'}),
                ('Primary (Coral, emotional)', {'Default': 'coral', 'Pressed': 'coral', 'Disabled': 'disabled', 'Loading': 'coral-loading'}),
                ('Secondary', {'Default': 'secondary', 'Pressed': 'secondary', 'Disabled': 'secondary-disabled', 'Loading': 'secondary-loading'}),
                ('Ghost', {'Default': 'ghost', 'Pressed': 'ghost', 'Disabled': 'ghost-disabled', 'Loading': 'ghost-loading'}),
                ('Destructive', {'Default': 'destructive', 'Pressed': 'destructive', 'Disabled': 'disabled', 'Loading': 'destructive-loading'})]
    for c, st in enumerate(states):
        o.append(lbl(220 + c * 250, 172, st))
    for r, (vn, m) in enumerate(variants):
        y = 184 + r * 76
        o.append(t1(40, y + 33, vn, 14, 600, NAVY))
        for c, st in enumerate(states):
            x = 220 + c * 250
            kind = m[st]
            b = button(y, 'Continue', kind, x=x, w=230)
            if st == 'Pressed' and kind in ('coral', 'destructive'):
                b += f'<rect x="{x}" y="{y}" width="230" height="56" rx="16" fill="{NAVY}" opacity="0.1"/>'
            if st == 'Pressed' and kind in ('secondary', 'ghost'):
                b = f'<rect x="{x}" y="{y}" width="230" height="56" rx="16" fill="{BTINT}"/>' + b
            o.append(b)
    y = 184 + 5 * 76 + 40
    # Inputs
    o.append(heading(40, y, 'Input'))
    y += 24
    ins = [('Empty', None, 'empty'), ('Focused', 'Aarav', 'focused'), ('Filled', 'Aarav_22', 'filled'), ('Error', 'Aarav 98765', 'error'),
           ('Disabled', '12 / 03 / 1998', 'disabled')]
    for i, (n, v, st) in enumerate(ins):
        x = 40 + (i % 3) * 400
        yy = y + (i // 3) * 120
        o.append(lbl(x, yy + 14, n))
        o.append(input_box(yy + 24, v, 'Your nickname', st, x=x, w=342))
        if st == 'error':
            o.append(err_msg(x, yy + 88, "That number doesn't look right.", w=342)[0])
    y += 260
    o.append(heading(40, y, 'Phone input'))
    o.append(at(16, y - 80, phone_input(104, None, 'empty')) + at(416, y - 80, phone_input(104, '98765 43210', 'focused'))
             + at(816, y - 80, phone_input(104, '98765 4321', 'error')))
    y += 130
    o.append(heading(40, y, 'OTP field (box 50x56, radius 14, gap 8)'))
    y += 16
    for i, (n, d, st, f) in enumerate([('Empty', '', 'empty', 0), ('Focused / partly filled', '482', 'empty', 3),
                                       ('Filled', '482913', 'empty', None), ('Error', '482193', 'error', None), ('Disabled (lockout)', '', 'disabled', None)]):
        x = 15 + (i % 3) * 400
        yy = y + (i // 3) * 100
        o.append(lbl(x + 25, yy + 14, n))
        o.append(at(x, yy + 24, otp_boxes(0, d, st, f)))
    return '\n'.join(o), 1240, y + 240


def sheet_controls_2():
    o = [t1(40, 64, 'Cards, selection and controls', 32, 700, NAVY, ls=-0.6)]
    o.append(heading(40, 130, 'Card'))
    o.append(card(40, 150, 342, 96) + t1(56, 186, 'Card title', 18, 700, NAVY) + t1(56, 214, 'White, border #EEF1F5, radius 16, padding 16', 13, 400, SLATE))
    o.append(card(400, 150, 342, 96, 20) + t1(416, 186, 'Feature card', 18, 700, NAVY) + t1(416, 214, 'Radius 20', 13, 400, SLATE))
    o.append(heading(40, 300, 'Selectable card (04 / 05 / 07)'))
    o.append(at(16, 216, gender_card(24, 104, 'Male', 'mars', 'unselected')) + at(196, 216, gender_card(24, 104, 'Female', 'venus', 'selected'))
             + at(376, 216, gender_card(24, 104, 'Male', 'mars', 'disabled')))
    o.append(at(560, 216, role_card(104, 'Explore as User', 'Talk to hosts and enjoy conversations.', 'users', 'unselected'))
             + at(560, 352, role_card(104, 'Become a Host & Earn', 'Get verified and earn from your conversations.', 'badge-check', 'selected')))
    y = 620
    o.append(heading(40, y, 'Checkbox'))
    for i, (n, c, d, hl) in enumerate([('Unchecked', False, False, False), ('Checked', True, False, False), ('Locked', False, True, False),
                                       ('Unlocked highlight', False, False, True)]):
        x = 52 + i * 150
        o.append(checkbox(x, y + 40, c, d, hl) + lbl(x - 12, y + 108, n))
    o.append(heading(660, y, 'Switch'))
    for i, (n, on, col, lg, d) in enumerate([('Off', False, BLUE, False, False), ('On', True, BLUE, False, False), ('Disabled', True, BLUE, False, True),
                                             ('Master off', False, SUCCESS, True, False), ('Master on', True, SUCCESS, True, False)]):
        x = 660 + i * 110
        o.append(switch(x, y + 40, on, col, lg, d) + lbl(x, y + 108, n))
    y += 160
    o.append(heading(40, y, 'Slider (rates)'))
    o.append(slider(52, y + 50, 300, 0.2) + lbl(40, y + 90, 'Default') + slider(452, y + 50, 300, 0.33, True) + lbl(440, y + 90, 'Locked'))
    o.append(heading(860, y, 'Countdown'))
    o.append(t1(860, y + 55, 'Resend code in 00:42', 13, 400, SLATE) + t1(860, y + 85, '00:15', 14, 600, NAVY))
    y += 140
    o.append(heading(40, y, 'Multi-select chip (H40, pill)'))
    x = 40
    for n, st in [('Hindi', 'selected'), ('English', 'unselected'), ('Kannada', 'pressed'), ('Tamil', 'disabled')]:
        s, w = chip(x, y + 24, n, st)
        o.append(s + lbl(x, y + 86, st.capitalize()))
        x += w + 40
    o.append(heading(660, y, 'Avatar 40 / 48 / 56 / 72 + fallback'))
    x = 680
    for d in (40, 48, 56, 72):
        o.append(avatar(x + d / 2, y + 60, d, photo=True))
        x += d + 24
    o.append(avatar(x + 36, y + 60, 72, letter='A') + avatar(x + 132, y + 60, 72) + lbl(x, y + 116, 'Fallback: initial / no name'))
    y += 160
    o.append(heading(40, y, 'PersistentBanner'))
    for i, (v, s) in enumerate([('info', 'Our Host Terms have been updated'), ('clock', 'Host verification in progress'),
                                ('offline', "You're offline. Check your connection and try again."),
                                ('warning', 'Diamonds and earnings are lost when your account is deleted.'),
                                ('error', "We couldn't connect right now. Try again in a moment."), ('lock', 'Gender cannot be altered once confirmed.')]):
        x = 40 + (i % 3) * 400
        yy = y + 24 + (i // 3) * 76
        o.append(banner(yy, s, v, x=x)[0])
    y += 200
    o.append(heading(40, y, 'Toast'))
    o.append(at(16, y + 24, toast(0, 'Saved')) + at(416, y + 24, toast(0, 'Code sent again')))
    o.append(heading(816, y, 'Diamond glyph (owner: Girish)'))
    o.append(gem(816, y + 30, 24) + t1(848, y + 50, '480', 26, 700, NAVY))
    return '\n'.join(o), 1240, y + 120


def nested(x, y, body, label, scale=0.75):
    return (lbl(x, y - 10, label)
            + f'<svg x="{x}" y="{y}" width="{390 * scale:.0f}" height="{844 * scale:.0f}" viewBox="0 0 390 844">'
              f'<rect width="390" height="844" fill="{CREAM}"/>{body}</svg>')


def sheet_overlays():
    o = [t1(40, 64, 'BottomSheet, Dialog, pickers, camera', 32, 700, NAVY, ls=-0.6)]
    items = [(s011_body('en'), 'BottomSheet (Language, 01.1)'),
             (dialog('Confirm Male?', 'This is permanent.', [('Confirm', 'primary', '06'), ('Go back', 'ghost', 'close')]), 'Dialog (04)'),
             (s06_body(av='done', nick='Aarav_22', nick_state='filled', overlay=date_sheet()), 'Date picker (06)'),
             (s06_body(av='letter', nick='Aarav_22', nick_state='filled', overlay=photo_sheet()).replace('id="c06"', 'id="c06b"').replace('url(#c06)', 'url(#c06b)'),
              'Photo picker (06)'),
             (crop_screen(), '1:1 crop (06, 40.1, 26)'),
             (s08_body('recording'), 'Camera viewfinder + progress ring (08)')]
    for i, (b, n) in enumerate(items):
        x = 40 + (i % 3) * 320
        y = 120 + (i // 3) * 680
        o.append(nested(x, y, b, n))
    return '\n'.join(o), 1000, 120 + 2 * 680


def gen_all():
    for fn, name, title in [(sheet_controls_1, 'Buttons-Inputs-OTP', 'Buttons, inputs, OTP'),
                            (sheet_controls_2, 'Cards-Selection-Controls', 'Cards, selection, controls, banners, toast'),
                            (sheet_overlays, 'Sheets-Dialogs-Pickers-Camera', 'Sheets, dialogs, pickers, camera')]:
        body, w, h = fn()
        write_sheet(name, w, h, body, title)
