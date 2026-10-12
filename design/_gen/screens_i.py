"""06A Live Photo (NEW, normal users): a quick selfie after 06 Basic Profile. Optional ("Skip for now") until the
owner decides whether it blocks progress (README question)."""
from lib2 import *
from illus import sparks
from screens_b import perm_dialog

CX, CY, R = 195, 330, 130


def lp_viewfinder(face=True, captured=False, dim=False, offset=0):
    """Front camera inside a 260 circle with a glowing ring; dashed face guide while live."""
    o = ['<!-- Live camera (front) inside a circle -->', f'<circle cx="{CX}" cy="{CY}" r="{R * 1.6:.0f}" fill="url(#g-halo)"/>',
         f'<circle cx="{CX}" cy="{CY}" r="{R + 22}" fill="none" stroke="{BLUE}" stroke-opacity="0.14" stroke-width="1.5"/>',
         f'<circle cx="{CX}" cy="{CY}" r="{R + 8}" fill="{WHITE}" filter="url(#sh-card)"/>',
         f'<clipPath id="lpv"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath><g clip-path="url(#lpv)">'
         f'<rect x="{CX - R}" y="{CY - R}" width="{2 * R}" height="{2 * R}" fill="{BTINT}"/>']
    if face:
        o.append(photo_img(CX - R + offset, CY - R, 2 * R, 2 * R, 'rohan.jpg'))
    if dim:
        o.append(f'<rect x="{CX - R}" y="{CY - R}" width="{2 * R}" height="{2 * R}" fill="{NAVY}" opacity="0.4"/>')
    o.append('</g>')
    if not captured:
        o.append(f'<ellipse cx="{CX}" cy="{CY - 10}" rx="84" ry="104" fill="none" stroke="{WHITE}" stroke-width="2.5" stroke-dasharray="8 8"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R + 8}" fill="none" stroke="{SUCCESS if captured else BLUE}" stroke-width="3" stroke-opacity="{1 if captured else 0.5}"/>')
    if captured:
        o.append(f'<circle cx="{CX + 92}" cy="{CY + 92}" r="18" fill="{SUCCESS}" stroke="{WHITE}" stroke-width="3"/>' + icon('check', CX + 82, CY + 82, WHITE, 20))
    return '\n'.join(o)


def shutter(enabled=True):
    col = BLUE if enabled else DIS_BG
    return ('<!-- Shutter (take photo) -->'
            f'<circle cx="195" cy="726" r="40" fill="{WHITE}" fill-opacity="0.85" stroke="{WHITE}" filter="url(#sh-card)"/>'
            f'<circle cx="195" cy="726" r="30" fill="{col}"' + (' filter="url(#gl-blue)"' if enabled else '') + '/>'
            + icon('camera', 183, 714, WHITE, 24) + (hit(155, 686, 80, 80, 'btn:Take photo') if enabled else ''))


def s06a(state='intro'):
    o = [blobs()]
    if state == 'intro':
        o.append(f'<circle cx="195" cy="250" r="110" fill="url(#g-halo)"/>' + glass(115, 170, 160, 160, 80)
                 + f'<clipPath id="lpi"><circle cx="195" cy="250" r="68"/></clipPath><g clip-path="url(#lpi)"><rect x="127" y="182" width="136" height="136" fill="{BTINT}"/>'
                 + photo_img(127, 182, 136, 136, 'rohan.jpg') + '</g>'
                 + f'<circle cx="262" cy="306" r="22" fill="url(#g-blue)" filter="url(#gl-blue)"/>' + icon('camera', 251, 295, WHITE, 22)
                 + sparks(118, 168, BLUE) + sparks(280, 160, CORAL, flip=True))
        s, y = text(195, 380, 'Add a live photo', 'h2', anchor='middle')
        o.append(s)
        s, y = text(195, y + 8, 'Take a quick selfie so hosts know they are talking to a real person.', 'body', anchor='middle', w=300)
        o.append(s)
        y += 24
        for ic, line in [('scan-face', 'Face the camera in good light'), ('eye-off', 'No sunglasses, masks or filters')]:
            o.append(glass(24, y, 342, 56, 20) + icon_box(36, y + 8, ic, 40, BTINT, BLUE, 20, 20) + t1(88, y + 33, line, 15, 500, NAVY))
            y += 64
        a, _ = action_area([('btn', 'Take live photo', 'primary', '06A Camera'), ('btn', 'Skip for now', 'ghost', '12')])
        o.append(a)
    else:
        title = {'camera': 'Look at the camera', 'no-face': 'Look at the camera', 'review': 'Looking good!',
                 'uploading': 'Saving your photo…', 'failed': 'Looking good!', 'permission': 'Look at the camera'}[state]
        s, y = text(195, 111, title, 'h2', anchor='middle')
        o.append(s)
        sub = {'review': 'Use this photo or take another one.', 'failed': 'Use this photo or take another one.',
               'uploading': 'This only takes a moment.'}.get(state, 'Keep your face inside the circle.')
        o.append(text(195, y + 4, sub, 'body', anchor='middle')[0])
        o.append(lp_viewfinder(face=state != 'no-face', captured=state in ('review', 'uploading', 'failed'), offset=0))
        if state == 'no-face':
            o.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="{NAVY}" opacity="0.08"/>' + icon('scan-face', CX - 28, CY - 28, BLUE, 56))
            o.append(banner(512, "We can't see your face. Move into the circle.", 'warning')[0])
        elif state == 'failed':
            o.append(banner(512, "We couldn't save your photo. Try again.", 'error')[0])
        elif state in ('camera', 'permission'):
            p, _ = pill(195, 512, 'Face found', WHITE, SUCCESS, 'check-circle', h=32, anchor='middle')
            o.append(p.replace(f'fill="{WHITE}" opacity="1.0"', 'fill="url(#g-glass)" stroke="#FFFFFF" filter="url(#sh-sm)"'))
        if state in ('camera', 'no-face', 'permission'):
            o.append(shutter(state == 'camera'))
        elif state == 'review':
            a, _ = action_area([('btn', 'Use photo', 'primary', 'save → 12'), ('btn', 'Retake', 'ghost', 'camera')])
            o.append(a)
        elif state == 'uploading':
            a, _ = action_area([('progress', 'Saving… 60%', 60)])
            o.append(a)
        elif state == 'failed':
            a, _ = action_area([('btn', 'Try again', 'primary', 'uploading'), ('btn', 'Retake', 'ghost', 'camera')])
            o.append(a)
    o.append(topbar('back' if state != 'uploading' else None, nav_back='06'))
    o.append(status_bar())
    if state == 'permission':
        o.append(perm_dialog('Camera'))
    o.append(home_indicator())
    return '\n'.join(o)


def gen_06a():
    F, ID, N = '06A_Live-Photo', '06A', 'Live-Photo'
    frame(F, ID, N, 'Intro', s06a('intro'), note='NEW: after 06 for normal users. Optional (Skip for now) until the owner decides')
    frame(F, ID, N, 'Camera', s06a('camera'), note='Front camera, live capture only')
    frame(F, ID, N, 'No-Face', s06a('no-face'), note='Shutter disabled until a face is found')
    frame(F, ID, N, 'Review', s06a('review'))
    frame(F, ID, N, 'Uploading', s06a('uploading'), note='Back hidden while saving')
    frame(F, ID, N, 'Upload-Failed', s06a('failed'))
    frame(F, ID, N, 'Permission-Denied', s06a('permission'), note='Camera dialog from 12')


def gen_all():
    gen_06a()
