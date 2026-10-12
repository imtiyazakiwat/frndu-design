"""Brand mark + hero illustrations in the reference style (flat, soft tint blobs, closed happy eyes, sparks).

Illustration-only colours (skin, hair) are NOT UI tokens; they are listed as a question for the owner.
"""
from lib import BLUE, CORAL, NAVY, WHITE, BTINT, CTINT, CSURF, WARN, SUCCESS, SLATE, BORDER, icon, t1

SKIN = '#F8C4A2'      # illustration only
SKIN_SH = '#EDAA86'   # illustration only (neck shade)
HAIR = '#3A2A2B'      # illustration only (girl hair, eyes)
_uid = [0]


def _id(p):
    _uid[0] += 1
    return f'{p}{_uid[0]}'


def sparks(x, y, color, flip=False, s=1.0):
    """Two short rounded strokes (the little 'ping' marks above characters/logo)."""
    d = -1 if flip else 1
    a = (f'<path d="M{x} {y} l{d * 4 * s:.1f} {12 * s:.1f}" stroke="{color}" stroke-width="{4.5 * s:.1f}" stroke-linecap="round"/>'
         f'<path d="M{x + d * 14 * s:.1f} {y + 10 * s:.1f} l{d * 10 * s:.1f} {-7 * s:.1f}" stroke="{color}" stroke-width="{4.5 * s:.1f}" stroke-linecap="round"/>')
    return '<!-- sparks -->' + a


def dashes3(x, y, color, s=1.0, flip=False):
    d = -1 if flip else 1
    return (f'<g stroke="{color}" stroke-width="{4 * s:.1f}" stroke-linecap="round">'
            f'<path d="M{x} {y} l{d * 3 * s:.1f} {-10 * s:.1f}"/><path d="M{x + d * 10 * s:.1f} {y + 4 * s:.1f} l{d * 9 * s:.1f} {-6 * s:.1f}"/>'
            f'<path d="M{x + d * 13 * s:.1f} {y + 15 * s:.1f} l{d * 10 * s:.1f} {-1 * s:.1f}"/></g>')


# ------------------------------------------------------------------ logo
def logo_mark(cx, cy, width, sparks_on=True, cut=None):
    """Frndu mark: coral + blue smiling speech bubbles, translucent overlap, two sparks. Source box 200 x 150."""
    s = width / 200.0
    cid, cid2 = _id('lgA'), _id('lgB')
    eye = 'fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"'
    sp = ''
    if sparks_on:
        sp = (f'<path d="M92 4 L99 22" stroke="{BLUE}" stroke-width="8" stroke-linecap="round"/>'
              f'<path d="M112 24 L124 12" stroke="{CORAL}" stroke-width="8" stroke-linecap="round"/>')
    return (f'<!-- Logo mark (reference style) {width} -->'
            f'<g transform="translate({cx} {cy}) scale({s:.4f}) translate(-100 -82)">'
            f'<clipPath id="{cid}"><ellipse cx="62" cy="86" rx="60" ry="52"/></clipPath>'
            f'<clipPath id="{cid2}"><ellipse cx="140" cy="88" rx="58" ry="52"/></clipPath>'
            # blue bubble (right) + tail
            f'<ellipse cx="140" cy="88" rx="58" ry="52" fill="{BLUE}"/>'
            f'<path d="M168 128 C176 140 184 146 196 150 C182 151 166 147 154 138 Z" fill="{BLUE}"/>'
            # coral bubble (left) + tail
            f'<ellipse cx="62" cy="86" rx="60" ry="52" fill="{CORAL}"/>'
            f'<path d="M30 126 C24 138 16 144 4 148 C18 150 34 146 46 136 Z" fill="{CORAL}"/>'
            # translucent overlap
            f'<g clip-path="url(#{cid})"><ellipse cx="140" cy="88" rx="58" ry="52" fill="#FFFFFF" opacity="0.38"/></g>'
            # faces: closed happy eyes (arches) + smile
            f'<path d="M34 80 q8 -10 16 0" {eye}/><path d="M64 80 q8 -10 16 0" {eye}/>'
            f'<path d="M44 98 q14 14 28 0" {eye}/>'
            f'<path d="M122 84 q8 -10 16 0" {eye}/><path d="M150 84 q8 -10 16 0" {eye}/>'
            f'<path d="M132 102 q14 14 28 0" {eye}/>'
            f'{sp}</g>')


# ------------------------------------------------------------------ characters
def _face(eye_col=HAIR):
    st = f'fill="none" stroke="{eye_col}" stroke-width="2.6" stroke-linecap="round"'
    return (f'<path d="M-15 2 q5 -6 10 0" {st}/><path d="M5 2 q5 -6 10 0" {st}/>'
            f'<path d="M-8 13 q8 8 16 0" {st}/>'
            f'<ellipse cx="-19" cy="11" rx="5" ry="3" fill="{CORAL}" opacity="0.35"/>'
            f'<ellipse cx="19" cy="11" rx="5" ry="3" fill="{CORAL}" opacity="0.35"/>')


def girl(x, y, s=1.0, shirt=CORAL):
    """Girl, head centre at (x, y), head radius ~32*s. Long wavy hair, closed happy eyes."""
    return (f'<g transform="translate({x} {y}) scale({s:.3f})">'
            f'<path d="M-50 -6 C-54 -50 -26 -64 0 -64 C28 -64 54 -50 52 -6 C52 20 62 44 54 70 C44 84 22 78 0 80 '
            f'C-22 78 -44 86 -56 70 C-64 46 -50 22 -50 -6 Z" fill="{HAIR}"/>'
            f'<path d="M-50 66 C-44 44 -22 38 0 38 C22 38 44 44 50 66 L56 120 L-56 120 Z" fill="{shirt}"/>'
            f'<rect x="-9" y="22" width="18" height="20" rx="6" fill="{SKIN_SH}"/>'
            f'<path d="M-9 40 Q0 48 9 40" fill="none" stroke="{SKIN_SH}" stroke-width="6"/>'
            f'<ellipse cx="0" cy="0" rx="31" ry="34" fill="{SKIN}"/>'
            f'<path d="M-32 -2 C-32 -38 -6 -46 8 -44 C26 -42 36 -26 32 -2 C26 -20 12 -26 -2 -24 C-14 -22 -26 -14 -32 -2 Z" fill="{HAIR}"/>'
            f'{_face()}</g>')


def boy(x, y, s=1.0, shirt=BLUE):
    return (f'<g transform="translate({x} {y}) scale({s:.3f})">'
            f'<path d="M-50 66 C-44 44 -22 38 0 38 C22 38 44 44 50 66 L56 120 L-56 120 Z" fill="{shirt}"/>'
            f'<rect x="-9" y="22" width="18" height="20" rx="6" fill="{SKIN_SH}"/>'
            f'<ellipse cx="-31" cy="4" rx="6" ry="8" fill="{SKIN}"/><ellipse cx="31" cy="4" rx="6" ry="8" fill="{SKIN}"/>'
            f'<ellipse cx="0" cy="0" rx="31" ry="34" fill="{SKIN}"/>'
            f'<path d="M-33 0 C-38 -30 -18 -46 2 -44 C8 -54 28 -50 30 -40 C40 -34 40 -14 33 0 C28 -16 18 -22 4 -22 '
            f'C-8 -22 -22 -16 -33 0 Z" fill="{NAVY}"/>'
            f'{_face(NAVY)}</g>')


def portrait(cx, cy, r, who='girl', bg=CTINT):
    """Character inside a soft tint circle; the body dissolves at the circle edge."""
    cid = _id('pt')
    fig = girl(cx, cy - r * 0.12, r / 60) if who == 'girl' else boy(cx, cy - r * 0.12, r / 60)
    return (f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/><g clip-path="url(#{cid})">{fig}</g>')


def soft_blob(cx, cy, rx, ry, color, op=1.0, rot=0):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" opacity="{op}" '
            f'transform="rotate({rot} {cx} {cy})"/>')


# ------------------------------------------------------------------ hero illustrations (centre x=195)
def hero_gender(y):
    """Boy + girl in overlapping tint circles (04). y = top of hero area; height ~150."""
    cy = y + 82
    return ('<!-- Hero: boy + girl (illustration) -->'
            + portrait(160, cy, 58, 'boy', BTINT) + portrait(232, cy, 58, 'girl', CTINT)
            + sparks(112, cy - 72, BLUE, flip=False) + sparks(282, cy - 66, CORAL, flip=True))


def hero_girl_clean(y):
    """Girl in coral tint blob, body clipped to the blob (dissolves)."""
    cy = y + 90
    cid = _id('hg')
    clip = (f'<clipPath id="{cid}"><path d="M86 {cy + 74} L86 {cy - 120} L306 {cy - 120} L306 {cy + 74} '
            f'C270 {cy + 82} 230 {cy + 70} 196 {cy + 74} C160 {cy + 78} 120 {cy + 84} 86 {cy + 74} Z"/></clipPath>')
    return ('<!-- Hero: girl (illustration) -->' + clip
            + f'<path d="M98 {cy + 30} C92 {cy - 30} 140 {cy - 44} 170 {cy - 30} C210 {cy - 12} 250 {cy - 50} 286 {cy - 8} '
              f'C312 {cy + 22} 296 {cy + 74} 250 {cy + 76} C200 {cy + 78} 150 {cy + 84} 120 {cy + 72} C104 {cy + 64} 100 {cy + 46} 98 {cy + 30} Z" fill="{CTINT}"/>'
            + f'<g clip-path="url(#{cid})">{girl(196, cy - 6, 1.0)}</g>'
            + sparks(252, cy - 78, CORAL))


def phone_shape(x, y, w, h, rot=0, screen=BTINT, inner=''):
    return (f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w * 0.2:.0f}" fill="{WHITE}" stroke="{BLUE}" stroke-width="5"/>'
            f'<rect x="{x + 8}" y="{y + 18}" width="{w - 16}" height="{h - 36}" rx="{w * 0.12:.0f}" fill="{screen}"/>'
            f'<circle cx="{x + w / 2}" cy="{y + 10}" r="3" fill="{BLUE}"/>'
            f'<rect x="{x + w / 2 - 12}" y="{y + h - 12}" width="24" height="4" rx="2" fill="{BORDER}"/>'
            f'{inner}</g>')


def hero_phone_call(y):
    """Tilted phone with a call icon (02)."""
    cy = y + 82
    inner = icon('phone', 195 - 18, cy - 18, BLUE, 36) + dashes3(212, cy - 22, CORAL, 0.8)
    return ('<!-- Hero: phone (illustration) -->' + soft_blob(214, cy + 22, 64, 56, CTINT, 1, -10)
            + phone_shape(158, cy - 72, 74, 140, 18, BTINT, inner)
            + dashes3(262, cy - 46, CORAL) + dashes3(132, cy + 44, CORAL, 1, True))


def hero_phone_otp(y):
    """Phone with an OTP message bubble (03)."""
    cy = y + 82
    bub = (f'<rect x="206" y="{cy - 52}" width="96" height="48" rx="16" fill="{WHITE}" filter="url(#sh-card)"/>'
           f'<path d="M222 {cy - 6} l-6 12 l16 -10 Z" fill="{WHITE}"/>'
           + ''.join(f'<circle cx="{226 + i * 19}" cy="{cy - 28}" r="5" fill="{BLUE if i < 3 else BORDER}"/>' for i in range(4)))
    return ('<!-- Hero: phone + code bubble (illustration) -->' + soft_blob(190, cy + 24, 66, 54, BTINT)
            + phone_shape(140, cy - 70, 74, 140, -10, CSURF, icon('message-square', 159, cy - 20, BLUE, 34))
            + bub + sparks(306, cy - 76, CORAL) + dashes3(118, cy + 40, BLUE, 0.9, True))


def hero_verify(y):
    """Girl holding a phone + face-scan bubble with check (07)."""
    cy = y + 92
    cid = _id('hv')
    clip = (f'<clipPath id="{cid}"><path d="M60 {cy + 74} L60 {cy - 120} L280 {cy - 120} L280 {cy + 74} '
            f'C240 {cy + 80} 200 {cy + 70} 170 {cy + 74} C130 {cy + 78} 90 {cy + 84} 60 {cy + 74} Z"/></clipPath>')
    bx, by = 236, cy - 88
    bubble = (f'<rect x="{bx}" y="{by}" width="92" height="92" rx="20" fill="{WHITE}" stroke="{BTINT}" stroke-width="3" filter="url(#sh-card)"/>'
              f'<path d="M{bx + 18} {by + 92} l-10 16 l26 -16 Z" fill="{WHITE}"/>'
              + ''.join(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="3.5" stroke-linecap="round"/>' for d in [
                  f'M{bx + 16} {by + 30} v-12 h12', f'M{bx + 64} {by + 18} h12 v12', f'M{bx + 76} {by + 62} v12 h-12', f'M{bx + 28} {by + 74} h-12 v-12'])
              + f'<g transform="translate({bx + 46} {by + 50}) scale(0.42) translate({-bx - 46} {-by - 50})">'
              + f'<clipPath id="{cid}f"><circle cx="{bx + 46}" cy="{by + 50}" r="56"/></clipPath><g clip-path="url(#{cid}f)">{girl(bx + 46, by + 44, 1)}</g></g>'
              + f'<circle cx="{bx + 82}" cy="{by + 84}" r="14" fill="{BLUE}" stroke="{WHITE}" stroke-width="3"/>' + icon('check', bx + 74, by + 76, WHITE, 16, 2.4))
    hand_phone = (f'<g transform="rotate(16 214 {cy + 34})"><rect x="196" y="{cy - 6}" width="38" height="70" rx="9" fill="{BLUE}"/>'
                  f'<rect x="201" y="{cy + 2}" width="28" height="52" rx="6" fill="#7F98FB"/>'
                  f'<circle cx="215" cy="{cy + 8}" r="2.5" fill="{WHITE}"/></g>'
                  f'<ellipse cx="204" cy="{cy + 44}" rx="11" ry="9" fill="{SKIN}"/>')
    return ('<!-- Hero: girl verifying with phone (illustration) -->' + clip
            + f'<path d="M70 {cy + 30} C64 {cy - 30} 110 {cy - 40} 140 {cy - 26} C180 {cy - 8} 220 {cy - 30} 250 {cy + 4} '
              f'C270 {cy + 30} 262 {cy + 74} 220 {cy + 76} C170 {cy + 78} 120 {cy + 84} 92 {cy + 72} C76 {cy + 64} 72 {cy + 46} 70 {cy + 30} Z" fill="{CTINT}"/>'
            + f'<g clip-path="url(#{cid})">{girl(160, cy - 6, 1.0)}{hand_phone}</g>'
            + bubble + sparks(98, cy - 78, CORAL, flip=True))


def hero_shield(y):
    cy = y + 80
    return ('<!-- Hero: shield 18+ (illustration) -->' + soft_blob(195, cy + 6, 78, 66, BTINT)
            + f'<path d="M195 {cy - 58} C214 {cy - 42} 236 {cy - 36} 252 {cy - 36} C252 {cy + 10} 238 {cy + 46} 195 {cy + 64} '
              f'C152 {cy + 46} 138 {cy + 10} 138 {cy - 36} C154 {cy - 36} 176 {cy - 42} 195 {cy - 58} Z" fill="{WHITE}" stroke="{BLUE}" stroke-width="5" stroke-linejoin="round"/>'
            + t1(195, cy + 12, '18+', 30, 700, BLUE, 'middle')
            + sparks(256, cy - 66, CORAL) + dashes3(122, cy + 40, CORAL, 0.9, True))


def hero_clock(y):
    cy = y + 80
    return ('<!-- Hero: clock (illustration) -->' + soft_blob(195, cy + 8, 82, 66, BTINT)
            + f'<circle cx="195" cy="{cy}" r="54" fill="{WHITE}" stroke="{BLUE}" stroke-width="5"/>'
            + ''.join(f'<circle cx="{195 + 40 * c:.1f}" cy="{cy + 40 * s:.1f}" r="3" fill="{BORDER}"/>' for c, s in [(1, 0), (-1, 0), (0, 1), (0, -1)])
            + f'<path d="M195 {cy - 30} V{cy} L216 {cy + 12}" fill="none" stroke="{NAVY}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
            + f'<circle cx="195" cy="{cy}" r="5" fill="{CORAL}"/>'
            + f'<rect x="248" y="{cy - 70}" width="62" height="38" rx="14" fill="{CORAL}"/><path d="M262 {cy - 34} l-6 12 l16 -12 Z" fill="{CORAL}"/>'
            + ''.join(f'<circle cx="{266 + i * 13}" cy="{cy - 51}" r="3.5" fill="{WHITE}"/>' for i in range(3))
            + sparks(120, cy - 64, BLUE, flip=True))


def hero_approved(y):
    cy = y + 96
    conf = ''.join(f'<rect x="{x}" y="{yy}" width="8" height="14" rx="3" fill="{c}" transform="rotate({r} {x + 4} {yy + 7})"/>'
                   for x, yy, c, r in [(84, cy - 70, BLUE, -20), (300, cy - 80, CORAL, 30), (66, cy + 10, CORAL, 40), (318, cy + 4, BLUE, -30),
                                       (120, cy - 100, CORAL, 10), (270, cy - 108, BLUE, 60)])
    badge = (f'<circle cx="250" cy="{cy + 40}" r="26" fill="{BLUE}" stroke="{WHITE}" stroke-width="5"/>' + icon('badge-check', 236, cy + 26, WHITE, 28, 2.4))
    return '<!-- Hero: approved host (illustration) -->' + conf + portrait(195, cy, 76, 'girl', CTINT) + badge + sparks(262, cy - 92, CORAL)


def hero_rejected(y):
    cy = y + 82
    return ('<!-- Hero: verification retry (illustration) -->' + soft_blob(195, cy + 16, 80, 62, CTINT)
            + phone_shape(158, cy - 70, 74, 140, -8, BTINT,
                          ''.join(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="3.5" stroke-linecap="round"/>' for d in [
                              f'M175 {cy - 20} v-10 h10', f'M205 {cy - 30} h10 v10', f'M215 {cy + 20} v10 h-10', f'M185 {cy + 30} h-10 v-10'])
                          + icon('smile', 181, cy - 14, SLATE, 28))
            + f'<circle cx="252" cy="{cy - 46}" r="20" fill="{CORAL}"/>' + t1(252, cy - 38, '!', 24, 700, WHITE, 'middle')
            + dashes3(126, cy + 40, BLUE, 0.9, True))


def hero_permissions(y):
    cy = y + 62
    chips = [(118, cy - 30, CORAL, CTINT, 'camera'), (276, cy - 38, BLUE, BTINT, 'mic'), (282, cy + 34, WARN, CSURF, 'bell')]
    out = soft_blob(195, cy + 8, 74, 54, BTINT) + phone_shape(166, cy - 52, 58, 110, 8, CSURF, logo_mark(195, cy + 4, 40, sparks_on=False))
    for x, yy, c, bg, ic in chips:
        out += f'<circle cx="{x}" cy="{yy}" r="22" fill="{WHITE}" filter="url(#sh-card)"/>' + icon(ic, x - 11, yy - 11, c, 22)
    return '<!-- Hero: permissions (illustration) -->' + out


def hero_languages(y):
    cy = y + 60
    return ('<!-- Hero: languages (illustration) -->' + soft_blob(195, cy + 10, 80, 46, BTINT)
            + f'<rect x="128" y="{cy - 40}" width="72" height="60" rx="22" fill="{CORAL}"/><path d="M140 {cy + 14} l-8 16 l22 -14 Z" fill="{CORAL}"/>'
            + t1(164, cy + 2, 'अ', 30, 700, WHITE, 'middle')
            + f'<rect x="190" y="{cy - 22}" width="72" height="60" rx="22" fill="{BLUE}"/><path d="M250 {cy + 32} l8 16 l-22 -14 Z" fill="{BLUE}"/>'
            + t1(226, cy + 19, 'A', 30, 700, WHITE, 'middle') + sparks(266, cy - 50, CORAL))


def hero_calendar(y):
    cy = y + 78
    return ('<!-- Hero: deletion countdown (illustration) -->' + soft_blob(195, cy + 10, 84, 60, CTINT)
            + f'<rect x="150" y="{cy - 50}" width="90" height="92" rx="18" fill="{WHITE}" filter="url(#sh-card)"/>'
            + f'<path d="M150 {cy - 32} a18 18 0 0 1 18 -18 h54 a18 18 0 0 1 18 18 v8 h-90 Z" fill="{CORAL}"/>'
            + f'<rect x="170" y="{cy - 60}" width="6" height="16" rx="3" fill="{NAVY}"/><rect x="214" y="{cy - 60}" width="6" height="16" rx="3" fill="{NAVY}"/>'
            + t1(195, cy + 28, '12', 34, 700, NAVY, 'middle')
            + logo_mark(268, cy + 26, 58, sparks_on=False) + sparks(118, cy - 56, BLUE, flip=True))


def hero_guidelines(y):
    cy = y + 60
    rows = ''.join(f'<circle cx="182" cy="{cy - 22 + i * 22}" r="7" fill="{SUCCESS if i < 2 else BORDER}"/>'
                   f'<rect x="196" y="{cy - 25 + i * 22}" width="{52 - i * 8}" height="6" rx="3" fill="{BORDER}"/>' for i in range(3))
    return ('<!-- Hero: guidelines (illustration) -->' + soft_blob(195, cy + 8, 76, 48, BTINT)
            + f'<rect x="160" y="{cy - 52}" width="104" height="110" rx="16" fill="{WHITE}" filter="url(#sh-card)"/>'
            + f'<rect x="192" y="{cy - 60}" width="40" height="16" rx="8" fill="{BLUE}"/>' + rows + sparks(272, cy - 60, CORAL))
