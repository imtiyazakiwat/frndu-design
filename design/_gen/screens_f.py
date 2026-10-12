"""Girish batch 2 (calls): 17 Outbound Ringing, 18 Incoming Call, 19 Video Call, 20 Voice Call, 22 Low Balance, 23 Call Ended, 38 Moderation."""
import math

from lib2 import *
from illus import portrait, girl, boy, hero_clock, hero_shield
from screens_b import perm_dialog

H = HOSTS[0]


def gem_text(x, y, s, size=15, weight=500, color=NAVY, gcol=BLUE, anchor='start'):
    w = tw(s, size, weight) + 4 + size
    if anchor == 'middle':
        x = x - w / 2
    return gem(round(x), round(y - size * 0.85), size, gcol) + t1(round(x + size + 4), y, s, size, weight, color)


# ============================================================ 17 Outbound Ringing
def ringing(mode='Video', state='ringing'):
    """17 Outbound Ringing (new theme): Cream canvas, host in glowing rings, waveform, Mute / Cancel / Speaker."""
    o = [blobs()]
    p, _ = pill(195, 63, f'{mode} call', WHITE, BLUE, 'video' if mode == 'Video' else 'phone', anchor='middle')
    o.append(p.replace(f'fill="{WHITE}" opacity="1.0"', 'fill="url(#g-glass)" stroke="#FFFFFF" filter="url(#sh-sm)"'))
    rate = '80' if mode == 'Video' else '40'
    if state in ('unavailable', 'dropped', 'offline'):
        title, body = {'unavailable': ('Host unavailable', "You weren't charged."),
                       'dropped': ('Your connection dropped', "You weren't charged. Check your connection and try again."),
                       'offline': ("You're offline", 'Connect to the internet to call Priya.')}[state]
        o.append(call_halo(195, 300, 64, 'girl', CTINT, rings=False, dots=False, dim=True))
        s_, y = text(195, 420, title, 'h2', anchor='middle', w=320)
        o.append(s_ + text(195, y + 8, body, 'body', anchor='middle', w=300)[0])
        a, _ = action_area([('btn', 'Back to profile', 'primary', '16')])
        o.append(a)
    else:
        title = {'ringing': 'Calling Priya…', 'connecting': 'Connecting…', 'busy': 'Priya is on another call'}[state]
        s_, y = text(195, 111, title, 'h2', anchor='middle', w=320)
        o.append(s_)
        if state == 'busy':
            o.append(text(195, y + 4, 'Try again in a few minutes.', 'body', anchor='middle')[0])
        else:
            o.append(gem_text(195, y + 20, f'{rate}/min, charged from pickup.', 15, 400, SLATE, BLUE, 'middle'))
        o.append(call_halo(195, 352, 64, 'girl', CTINT, online=state != 'busy', dim=state == 'busy', rings=state != 'busy'))
        o.append(t1(184, 504, 'Priya', 26, 700, NAVY, 'middle', ls=-0.4) + icon('badge-check', 222, 486, BLUE, 24))
        o.append(icon('star', 104, 520, WARN, 18) + t1(128, 535, '4.8', 14, 600, NAVY) + t1(154, 535, '(120)', 14, 400, SLATE)
                 + f'<rect x="200" y="522" width="1" height="16" fill="{BORDER}"/>' + icon('languages', 214, 520, SLATE, 18) + t1(238, 535, 'Hindi · English', 14, 400, SLATE))
        o.append(waveform(195, 600, live=state == 'ringing'))
        o.append(call_btn(96, 730, 'mic-off', 'btn:Mute', 'Mute'))
        o.append(call_btn(195, 730, 'phone-off', 'btn:Cancel', 'Cancel Call', 'end', 76, NAVY))
        o.append(call_btn(294, 730, 'volume-2', 'btn:Speaker', 'Speaker'))
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def gen_17():
    F, ID, N = '17_Outbound-Ringing', '17', 'Outbound-Ringing'
    frame(F, ID, N, 'Ringing-Video', ringing('Video'), note='Blurred host photo + Navy 40% scrim; no top bar')
    frame(F, ID, N, 'Ringing-Voice', ringing('Voice'))
    frame(F, ID, N, 'Connecting', ringing('Video', 'connecting'), note='After the host accepts')
    frame(F, ID, N, 'Host-Unavailable', ringing('Video', 'unavailable'), note='30 s timeout')
    frame(F, ID, N, 'Host-Busy', ringing('Video', 'busy'))
    frame(F, ID, N, 'Connection-Dropped', ringing('Video', 'dropped'))
    frame(F, ID, N, 'Offline', ringing('Video', 'offline'))


# ============================================================ 18 Incoming Call
def incoming(mode='Video', secs=24, state='ringing', overlay=''):
    """18 Incoming Call, host side (ref: Priya's Incoming Video Call): caller photo full-bleed, Frndu mark + type top-left,
    name, recharge badge and countdown at the bottom; Message / Decline / Accept (/ Audio Only on video calls)."""
    o = [video_scene('boy', img='rohan.jpg', blur=state == 'declined', dim=0.35 if state == 'declined' else 0)]
    o.append('<!-- Brand + call type (top-left) -->' + logo_mark(44, 78, 40, sparks_on=True) + t1(70, 84, 'Frndu', 18, 700, WHITE)
             + t1(24, 116, f'Incoming {mode} Call…', 15, 500, WHITE))
    o.append(t1(195, 560, 'Rohan_K', 34, 700, WHITE, 'middle', ls=-0.6))
    bp, _ = pill(195, 578, 'Recharged 5,000+', WHITE, CORAL, 'gem', h=28, anchor='middle')
    o.append(bp.replace(f'fill="{WHITE}" opacity="1.0"', f'fill="{WHITE}" opacity="0.92"'))
    if state == 'declined':
        o.append(t1(195, 644, 'Auto-declined', 16, 700, WHITE, 'middle'))
        o.append(text(195, 656, "You missed this call. We'll let you know if they call again.", 'body', anchor='middle', w=300, color=WHITE)[0])
        a, _ = action_area([('btn', 'Back to dashboard', 'primary', '24')])
        o.append(a)
    else:
        # 30 s countdown: thin progress track + seconds left
        frac = secs / 30
        o.append('<!-- 30 s countdown -->' + f'<rect x="135" y="624" width="120" height="4" rx="2" fill="{WHITE}" opacity="0.3"/>'
                 f'<rect x="135" y="624" width="{120 * frac:.0f}" height="4" rx="2" fill="{BLUE if secs > 5 else CORAL}"/>'
                 + t1(195, 648, f'{secs} s left to answer', 13, 600, WHITE if secs > 5 else CTINT, 'middle'))
        video = mode == 'Video'
        xs = [62, 154, 246, 334] if video else [92, 195, 298]
        o.append(dark_btn(xs[0], 732, 'message-square', 'btn:Message', 'Message', 48))
        o.append(call_btn(xs[1], 732, 'phone-off', 'btn:Decline', 'Decline', 'end', 72, WHITE))
        if state == 'accepting':
            o.append(f'<circle cx="{xs[2]}" cy="732" r="36" fill="url(#g-blue)" filter="url(#gl-blue)"/>' + spinner(xs[2], 732, WHITE, 12)
                     + t1(xs[2], 790, 'Accepting…', 14, 500, WHITE, 'middle'))
        else:
            o.append(call_btn(xs[2], 732, 'video' if video else 'phone', 'btn:Accept', 'Accept', 'accept', 72, WHITE))
        if video:
            o.append(dark_btn(xs[3], 732, 'mic', 'btn:Audio Only', 'Audio Only', 48))
    o.append(status_bar(WHITE))
    o.append(overlay)
    o.append(home_indicator(WHITE))
    return '\n'.join(o)


def dark_btn(cx, cy, ic, key, label, d=48):
    """Secondary call action over video: frosted dark circle, thin white edge, White icon + label."""
    return (f'<circle cx="{cx}" cy="{cy}" r="{d / 2}" fill="{WHITE}" fill-opacity="0.16" stroke="{WHITE}" stroke-opacity="0.45" stroke-width="1.2"/>'
            + icon(ic, cx - 11, cy - 11, WHITE, 22) + hit(cx - 24, cy - 24, 48, 48, key) + t1(cx, cy + 58 - (72 - d) / 2, label, 13, 500, WHITE, 'middle'))


def gen_18():
    F, ID, N = '18_Incoming-Call', '18', 'Incoming-Call'
    frame(F, ID, N, 'Video-30s', incoming('Video', 30), note='Locked phone uses the OS call screen (not designed)')
    frame(F, ID, N, 'Voice-30s', incoming('Voice', 30))
    frame(F, ID, N, 'Countdown-10s', incoming('Video', 10))
    frame(F, ID, N, 'Countdown-3s', incoming('Video', 3))
    frame(F, ID, N, 'Accepting', incoming('Video', 18, 'accepting'))
    frame(F, ID, N, 'Auto-Declined', incoming('Video', 0, 'declined'), note='After 30 s; 3 unattended calls set the host Offline (banner on 24)')
    frame(F, ID, N, 'Camera-Permission-Missing', incoming('Video', 20, overlay=perm_dialog('Camera')))


# ============================================================ 19 Video Call
def call_pills(dark=True, dur='03:25', rate='80'):
    bg, fg, op = (NAVY, WHITE, 0.4) if dark else (WHITE, NAVY, 0.75)
    p1, w1 = pill(24, 63, dur, bg, fg, h=32, op=op)
    w = tw(f'-{rate}/min', 14, 600) + 24 + 22
    p2 = (f'<rect x="{24 + w1 + 8:.0f}" y="63" width="{w:.0f}" height="32" rx="16" fill="{bg}" opacity="{op}"/>'
          + gem(round(24 + w1 + 20), 70, 18, WHITE if dark else BLUE) + t1(round(24 + w1 + 42), 84, f'-{rate}/min', 14, 600, fg))
    return '<!-- Call pills: duration + ticker -->' + p1 + p2


def pip(cam_off=False):
    o = [f'<!-- Local video PiP 96x128 (drag, snaps to corners) -->', f'<clipPath id="pip"><rect x="270" y="115" width="96" height="128" rx="20"/></clipPath>',
         f'<rect x="270" y="115" width="96" height="128" rx="20" fill="{NAVY}" opacity="0.3" filter="url(#sh-card)"/>',
         f'<g clip-path="url(#pip)"><rect x="270" y="115" width="96" height="128" fill="{BTINT if not cam_off else NAVY}"/>']
    o.append((boy(318, 172, 0.95) + photo_img(270, 115, 96, 128, 'rohan.jpg', 'xMidYMid')) if not cam_off else avatar(318, 179, 48, letter='A'))
    o.append(f'</g><rect x="270" y="115" width="96" height="128" rx="20" fill="none" stroke="{WHITE}" stroke-opacity="0.85" stroke-width="2"/>')
    return ''.join(o)


def video_controls(muted=False, cam_off=False):
    """Glossy ref: frosted dark panel, white round buttons with labels, red End Call in the middle."""
    o = ['<!-- Call controls (owner: Girish): Mute, Video, End Call, Chat, Flip in a frosted dark panel; no Gift at Launch -->',
         f'<rect x="16" y="680" width="358" height="128" rx="32" fill="{NAVY}" fill-opacity="0.35" stroke="{WHITE}" stroke-opacity="0.25" stroke-width="1.2"/>']
    btns = [(56, 'mic-off' if muted else 'mic', 'btn:Mute', 'Unmute' if muted else 'Mute', muted),
            (126, 'video-off' if cam_off else 'video', 'btn:Video', 'Start Video' if cam_off else 'Stop Video', cam_off),
            (264, 'message-circle', 'btn:Chat', 'Chat', False), (334, 'camera', 'btn:Flip camera', 'Flip', False)]
    for x, ic, k, lbl, on in btns:
        fill = 'url(#g-blue)' if on else WHITE
        o.append(f'<circle cx="{x}" cy="730" r="26" fill="{fill}" fill-opacity="{1 if on else 0.92}"/>' + icon(ic, x - 11, 719, WHITE if on else NAVY, 22)
                 + hit(x - 26, 704, 52, 52, k) + t1(x, 778, lbl, 12, 500, WHITE, 'middle'))
    o.append(f'<circle cx="195" cy="728" r="34" fill="{ERROR}" filter="url(#gl-red)"/>' + icon('phone-off', 181, 714, WHITE, 28)
             + hit(161, 694, 68, 68, 'btn:End Call') + t1(195, 784, 'End Call', 12, 600, WHITE, 'middle'))
    return '\n'.join(o)


def call_head(dark=True, dur='03:25', rate='80', name='Priya'):
    """Glossy / Secure-call header: name + verified badge, then duration · ticker."""
    col, sub = (WHITE, WHITE) if dark else (NAVY, SLATE)
    return ('<!-- Call header: name, duration and per-minute ticker -->'
            + t1(24, 84, name, 20, 700, col) + icon('badge-check', 30 + tw(name, 20, 700), 68, BLUE, 20)
            + t1(24, 106, dur, 13, 600, sub) + f'<rect x="{30 + tw(dur, 13, 600):.0f}" y="96" width="1" height="12" fill="{sub}" opacity="0.5"/>'
            + gem(round(38 + tw(dur, 13, 600)), 94, 14, WHITE if dark else BLUE) + t1(round(56 + tw(dur, 13, 600)), 106, f'-{rate}/min', 13, 600, sub))


def video_call(state='connected', overlay='', banner_txt=None, muted=False, cam_off=False):
    o = []
    if state == 'remote-off':
        o.append(f'<rect width="390" height="844" fill="{NAVY}"/>' + avatar(195, 380, 72, img='priya.jpg')
                 + t1(195, 444, 'Priya turned off the camera', 13, 500, WHITE, 'middle'))
    else:
        o.append(video_scene('girl', blur=state == 'blur', dim=0.45 if state in ('reconnecting', 'weak') else 0))
    o.append(call_head())
    o.append(media_btn(318, 55, 'shield', 'right:shield').replace(f'fill="{NAVY}" opacity="0.4"', f'fill="{WHITE}" fill-opacity="0.18" stroke="{WHITE}" stroke-opacity="0.45"'))
    o.append(pip(cam_off))
    if banner_txt:
        kind, txt = banner_txt
        b, _ = banner(259, txt, kind, action='Add' if kind == 'warning' else None)
        o.append(b + hit(24, 259, 342, 44, 'banner:low'))
    if state == 'reconnecting':
        o.append(spinner(195, 400, WHITE, 18) + t1(195, 450, 'Reconnecting…', 18, 700, WHITE, 'middle'))
    if state == 'weak':
        o.append(card(24, 330, 342, 156, 24) + text(48, 354, 'Your connection is weak. Switch to audio only?', 'h4', w=294)[0]
                 + button(414, 'Switch to audio', 'primary', x=48, w=140) + button(414, 'Keep video', 'ghost', x=202, w=140))
    o.append(video_controls(muted, cam_off))
    o.append(status_bar(WHITE))
    o.append(overlay)
    o.append(home_indicator(WHITE))
    return '\n'.join(o)


def shield_sheet():
    return '<!-- Shield sheet -->' + __import__('screens_e').overflow_sheet(
        [('Report or block', 'flag', NAVY, '39'), ('Safety tips', 'shield-check', NAVY, '59')], 'Stay safe')


def chat_drawer():
    top = 422
    b = [text(24, top + 24, 'Chat with Priya', 'h4')[0], icon('x', 342, top + 22, NAVY) + hit(330, top + 10, 48, 48, 'close')]
    y = top + 70
    for side, txt in [('in', 'Hi! How was your day?'), ('out', 'Pretty good, thanks!'), ('in', 'Glad to hear that 😊'.replace(' 😊', ''))]:
        s, y = bubble(y, txt, side)
        b.append(s)
        y += 8
    b.append(input_box(746, None, 'Type a message', 'empty', x=24, w=278) + f'<circle cx="342" cy="774" r="24" fill="{DIS_BG}"/>' + icon('send', 330, 762, WHITE))
    return scrim(0.2) + sheet(top, '\n'.join(b))


def bubble(y, txt, side, status=None, maxw=256, failed=False):
    """ChatBubble: sent Blue/White text; received White + border, Navy. r18."""
    lines = wrap(txt, maxw - 32, 15)
    w = min(maxw, max(tw(' '.join(x[0] for x in ln), 15) for ln in lines) + 32)
    h = len(lines) * 22 + 20
    x = 366 - w if side == 'out' else 24
    fill, st, col = (BLUE, None, WHITE) if side == 'out' else (WHITE, CBORDER, NAVY)
    o = [f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="18" fill="{fill}"' + (f' stroke="{st}"' if st else '') + '/>',
         text(x + 16, y + 10, txt, 'body', w=maxw - 32, color=col)[0]]
    yy = y + h
    if status:
        ic, col2, lbl = {'sending': ('clock', SLATE, 'Sending'), 'sent': ('check', SLATE, 'Sent'), 'delivered': ('check-check', SLATE, 'Delivered'),
                         'read': ('check-check', BLUE, 'Read'), 'failed': ('alert-circle', ERROR, 'Failed · Tap to retry')}[status]
        lw = tw(lbl, 12, 500) + 20
        o.append(icon(ic, round(366 - lw), yy + 4, col2, 16) + t1(366, yy + 16, lbl, 12, 500, col2, 'end'))
        if status == 'failed':
            o.append(hit(round(x), y, round(w), h + 22, 'retry'))
        yy += 22
    return '\n'.join(o), yy


def gen_19():
    F, ID, N = '19_Video-Call', '19', 'Video-Call'
    frame(F, ID, N, 'Connected', video_call(), note='Portrait only. PiP never overlaps controls at 360 × 800')
    frame(F, ID, N, 'Muted', video_call(muted=True))
    frame(F, ID, N, 'Camera-Off', video_call(cam_off=True), note='Your PiP shows your avatar')
    frame(F, ID, N, 'Remote-Camera-Off', video_call('remote-off'))
    frame(F, ID, N, 'Low-Balance-Banner', video_call(banner_txt=('warning', 'Running low on diamonds.')), note='Tap banner → 22 sheet')
    frame(F, ID, N, 'Zero-Balance-Countdown', video_call(banner_txt=('error', 'Your call will end in 0:12 unless you add diamonds.')))
    frame(F, ID, N, 'Weak-Connection', video_call('weak'))
    frame(F, ID, N, 'Reconnecting', video_call('reconnecting'), note='Up to 10 s, then the call ends → 23')
    frame(F, ID, N, 'Screen-Recording-Warning', video_call(banner_txt=('info', 'Screen recording is on. Please respect Priya’s privacy.')))
    frame(F, ID, N, 'Shield-Sheet', video_call(overlay=shield_sheet()))
    frame(F, ID, N, 'Chat-Drawer', video_call(overlay=chat_drawer()), note='50% height text chat drawer')


# ============================================================ 20 Voice Call
def voice_call(muted=False, speaker=False, bt=False, banner_txt=None, state='connected', host_muted=False, reduced=False):
    """20 Voice Call (ref: Frndu Secure Call): Cream canvas, Frndu mark, ticker pill, large photo in glowing rings,
    name + duration, gradient waveform, Mute / Speaker / End Call."""
    o = [blobs()]
    o.append(logo_mark(46, 79, 40, sparks_on=True) + t1(72, 85, 'Frndu', 18, 700, NAVY))
    w = tw('-40/min', 14, 600) + 48
    o.append('<!-- Ticker pill (frosted) -->' + glass(round(366 - w), 59, round(w), 40, 20) + gem(round(366 - w + 14), 69, 18) + t1(round(366 - w + 38), 84, '-40/min', 14, 600, NAVY))
    top = 111
    if banner_txt:
        o.append(banner(top, banner_txt[1], banner_txt[0], action='Add' if banner_txt[0] == 'warning' else None)[0] + hit(24, top, 342, 44, 'banner:low'))
    cy = 318
    o.append(call_halo(195, cy, 84, 'girl', CTINT, online=False, rings=not reduced, dots=not reduced, img='priya_full.jpg'))
    if state == 'reconnecting':
        o.append(f'<circle cx="195" cy="{cy}" r="84" fill="{NAVY}" opacity="0.35"/>' + spinner(195, cy, WHITE, 16))
    o.append(t1(184, cy + 160, 'Priya', 30, 700, NAVY, 'middle', ls=-0.5) + icon('badge-check', 226, cy + 140, BLUE, 26))
    sub = 'Reconnecting…' if state == 'reconnecting' else ('Priya muted her mic' if host_muted else '03:25')
    o.append(t1(195, cy + 188, sub, 15, 500, CORAL if host_muted else SLATE, 'middle'))
    if host_muted:
        o.append(icon('mic-off', 112, cy + 174, CORAL, 18))
    if bt:
        p, _ = pill(195, cy + 204, 'Bluetooth headset', WHITE, NAVY, 'bluetooth', h=32, anchor='middle')
        o.append(p.replace(f'fill="{WHITE}" opacity="1.0"', 'fill="url(#g-glass)" stroke="#FFFFFF"'))
    o.append('<linearGradient id="g-wave" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5B7CFA" stop-opacity="0.6"/><stop offset="0.5" stop-color="#5B7CFA"/><stop offset="1" stop-color="#5B7CFA" stop-opacity="0.6"/></linearGradient>')
    o.append(waveform(195, cy + (272 if bt else 256), live=not reduced and state != 'reconnecting', color='url(#g-wave)'))
    o.append(call_btn(96, 730, 'mic-off' if muted else 'mic', 'btn:Mute', 'Muted' if muted else 'Mute', 'on' if muted else 'glass'))
    o.append(call_btn(195, 730, 'phone-off', 'btn:End Call', 'End Call', 'end', 80, NAVY))
    o.append(call_btn(294, 730, 'volume-2', 'btn:Speaker', 'Speaker', 'on' if speaker else 'glass'))
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def gen_20():
    F, ID, N = '20_Voice-Call', '20', 'Voice-Call'
    frame(F, ID, N, 'Connected', voice_call(), note='No Gift, no Request Video at Launch')
    frame(F, ID, N, 'Muted', voice_call(muted=True))
    frame(F, ID, N, 'Speaker-On', voice_call(speaker=True))
    frame(F, ID, N, 'Bluetooth-Connected', voice_call(bt=True))
    frame(F, ID, N, 'Low-Balance-Banner', voice_call(banner_txt=('warning', 'Running low on diamonds.')))
    frame(F, ID, N, 'Zero-Balance-Countdown', voice_call(banner_txt=('error', 'Your call will end in 0:12 unless you add diamonds.')))
    frame(F, ID, N, 'Reconnecting', voice_call(state='reconnecting'))
    frame(F, ID, N, 'Host-Muted', voice_call(host_muted=True))
    frame(F, ID, N, 'Reduced-Motion', voice_call(reduced=True), note='Static waveform')


# ============================================================ 22 Low Balance Drawer
BUNDLES22 = [('50', '$0.49'), ('120', '$0.99'), ('300', '$1.99')]


def low_sheet(state='open'):
    top = 844 - (24 + 30 + 8 + 22 + 16 + 3 * 84 + 4 + 44 + 34) - (30 if state == 'failed' else 0)
    b = [text(24, top + 24, 'Add diamonds to keep talking', 'h3')[0], text(24, top + 62, 'You have about 1 minute left.', 'body')[0]]
    y = top + 100
    if state == 'failed':
        b.append(err_msg(24, y, "That payment didn't go through. Try again.")[0])
        y += 30
    for i, (amt, price) in enumerate(BUNDLES22):
        dis = state == 'purchasing' and i != 0
        b.append(f'<!-- Micro-bundle {amt} → store purchase → 48 compact -->'
                 f'<rect x="24.5" y="{y + 0.5}" width="341" height="71" rx="16" fill="{WHITE}" stroke="{CBORDER}" opacity="{0.5 if dis else 1}"/>'
                 + gem(40, y + 24, 24) + t1(72, y + 45, amt, 22, 700, DIS_T if dis else NAVY))
        pw = tw(price, 14, 600) + 32
        if state == 'purchasing' and i == 0:
            b.append(f'<rect x="{350 - pw:.0f}" y="{y + 16}" width="{pw:.0f}" height="40" rx="20" fill="{BLUE}"/>' + spinner(350 - pw / 2, y + 36, WHITE, 8))
        else:
            b.append(f'<rect x="{350 - pw:.0f}" y="{y + 16}" width="{pw:.0f}" height="40" rx="20" fill="{DIS_BG if dis else BLUE}"/>' + t1(f'{350 - pw / 2:.0f}', y + 41, price, 14, 600, WHITE, 'middle'))
        if not dis:
            b.append(hit(24, y, 342, 72, f'bundle:{amt}'))
        y += 84
    b.append(link_row(y + 4, 'See all bundles', '30 (pushed; call keeps running)'))
    return scrim(0.3) + sheet(top, '\n'.join(b))


def gen_22():
    F, ID, N = '22_Low-Balance', '22', 'Low-Balance'
    frame(F, ID, N, 'Banner-Only', video_call(banner_txt=('warning', 'Running low on diamonds.')), note='Prices are placeholders from the Client')
    frame(F, ID, N, 'Sheet-Open', video_call(overlay=low_sheet()))
    frame(F, ID, N, 'Purchasing', video_call(overlay=low_sheet('purchasing')))
    frame(F, ID, N, 'Success-Toast', video_call(overlay=toast(660, '+50 diamonds added')), note='Sheet closes')
    frame(F, ID, N, 'Failed', video_call(overlay=low_sheet('failed')))
    frame(F, ID, N, 'Grace-Countdown', video_call(banner_txt=('error', 'Balance is 0. Your call ends in 0:15 unless you add diamonds.'), overlay=low_sheet()))
    frame(F, ID, N, 'Voice-Call-Sheet', voice_call(banner_txt=('warning', 'Running low on diamonds.')) + low_sheet())


# ============================================================ 23 Call Ended
def ended_user(state='rate', rating=0, tags=(), friend=False, fav=False, low=False, short=False, btn='primary', msg=None):
    o = [blobs(bottom=False)]
    o.append(topbar(None, right='x', nav_right='13'))
    c = []
    y = 111
    if msg:
        b, y2 = (offline_banner(y) if msg == 'offline' else banner(y, "We couldn't send your rating. Try again.", 'error'))
        c.append(b)
        y = y2 + 12
    c.append(t1(24, y + 26, 'Call ended', 26, 700, NAVY, ls=-0.4))
    y += 34 + 16
    c.append(avatar(195, y + 28, 56, img='priya.jpg') + t1(195, y + 56 + 8 + 19, 'Priya', 18, 700, NAVY, 'middle'))
    y += 56 + 8 + 26 + 16
    for i, (lab, val, g) in enumerate([('Duration', '12:40' if not short else '0:24', False), ('Spent', '480' if not short else '40', True)]):
        x = 24 + i * 177
        c.append(card(x, y, 165, 80) + t1(x + 16, y + 30, lab, 12, 500, SLATE))
        c.append((gem(x + 16, y + 42, 22) + t1(x + 44, y + 62, val, 22, 700, NAVY)) if g else t1(x + 16, y + 62, val, 22, 700, NAVY))
    y += 80 + 24
    if not short:
        c.append(t1(195, y + 19, 'How was your call?', 18, 700, NAVY, 'middle'))
        y += 26 + 12
        c.append(stars(195 - (5 * 40 + 4 * 8) / 2, y, rating, 40, 8, key='star'))
        y += 40 + 16
        if low:
            c.append(f'<rect x="24" y="{y}" width="342" height="56" rx="16" fill="{CTINT}"/>' + icon('flag', 40, y + 16, CORAL)
                     + t1(72, y + 33, 'Want to report something?', 15, 500, NAVY) + t1(350, y + 33, 'Report', 14, 600, BLUE, 'end') + hit(270, y + 6, 96, 44, 'link:Report'))
            y += 56 + 16
        s, y = chips_wrap(24, y, [(t, 'selected' if t in tags else 'unselected') for t in ['Friendly', 'Great Voice', 'Polite']])
        c.append(s)
        y += 16
        c.append(input_box(y, None, 'Add a comment (optional)', 'empty', h=80, multiline=True))
        y += 80 + 16
    for i, (lbl, ic, on) in enumerate([('Add Friend', 'user-plus', friend), ('Add to Favorites', 'heart', fav)]):
        x = 24 + i * 177
        c.append(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="164" height="55" rx="16" fill="{BTINT if on else WHITE}" stroke="{BLUE if on else BORDER}"/>'
                 + icon('check' if on else ic, x + 16, y + 18, BLUE, 20) + t1(x + 44, y + 33, lbl if not on else lbl.replace('Add ', 'Added ').replace('Added to', 'In'), 14, 600, BLUE)
                 + hit(x, y, 165, 56, f'toggle:{lbl}'))
    items = [('btn', 'Submit' if not short else 'Done', btn, '13'), ('btn', 'Skip', 'ghost', '13')] if not short else [('btn', 'Done', 'primary', '13')]
    a, top = action_area(items)
    o.insert(1, clip_group('c23', 103, top - 16, '\n'.join(c)))
    o.append(a)
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def ended_host():
    o = [blobs(bottom=False), topbar(None, right='x', nav_right='24')]
    o.append(t1(24, 137, 'Call ended', 26, 700, NAVY, ls=-0.4))
    o.append(avatar(195, 189, 56, img='rohan.jpg') + t1(195, 245, 'Rohan_K', 18, 700, NAVY, 'middle'))
    s, _ = kv_card(276, [('Duration', '12:40'), ('Gross earned', '1,016', 'gem'), ('Commission (30%)', '−305', 'gem'), ('Net credited', '711', 'bold', SUCCESS)])
    o.append(s)
    a, _ = action_area([('btn', 'Done', 'primary', '24')])
    o.append(a + status_bar() + home_indicator())
    return '\n'.join(o)


def gen_23():
    F, ID, N = '23_Call-Ended', '23', 'Call-Ended'
    frame(F, ID, N, 'User-Rate', ended_user(), note='Rating block for calls ≥ 30 s')
    frame(F, ID, N, 'User-Rated', ended_user(rating=5, tags=('Friendly', 'Polite'), friend=True))
    frame(F, ID, N, 'Low-Rating-Prompt', ended_user(rating=2, low=True), note='≤ 2 stars → Report link → 39')
    frame(F, ID, N, 'Short-Call', ended_user(short=True), note='< 30 s: no rating')
    frame(F, ID, N, 'Submitting', ended_user(rating=4, btn='primary-loading'))
    frame(F, ID, N, 'Error', ended_user(rating=4, msg='error'))
    frame(F, ID, N, 'Offline-Queued', ended_user(rating=4, msg='offline'), note='Rating queued until online')
    frame(F, ID, N, 'Host-Summary', ended_host(), note='No rating UI for hosts')


# ============================================================ 38 Moderation Overlay
def moderation(state='first'):
    o = [video_scene('girl', blur=True, dim=0.4), call_head(), video_controls()]
    if state == 'terminated':
        o = [f'<rect width="390" height="844" fill="{CREAM}"/>', blobs(), soft_blob(195, 236, 84, 64, CTINT), f'<circle cx="195" cy="230" r="56" fill="{WHITE}"/>', icon('shield-alert', 163, 198, WARN, 64), sparks(250, 160, CORAL)]
        s, y = text(195, 350, 'This call was ended because of a policy violation.', 'h2', anchor='middle', w=320)
        o.append(s + text(195, y + 8, 'If you think this is a mistake, contact support.', 'body', anchor='middle')[0])
        a, _ = action_area([('btn', 'OK', 'primary', '23')])
        o.append(a)
    else:
        body = ("Please keep calls respectful. If this continues, the call will end and your account may be restricted."
                if state == 'first' else 'Your camera was flagged. Please check what is visible.')
        n = nlines(body, 'body', 294)
        h = 24 + 32 + 12 + 60 + 8 + n * 22 + 24 + 56 + 24
        y = (844 - h) // 2
        o.append(card(24, y, 342, h, 24) + icon('shield-alert', 179, y + 24, WARN, 32))
        s, yy = text(195, y + 68, 'Potential policy violation detected', 'h3', anchor='middle', w=294)
        o.append(s + text(195, yy + 8, body, 'body', anchor='middle', w=294)[0])
        o.append(button(y + h - 80, 'I understand', 'primary', x=48, w=294, nav='19 (video stays blurred)'))
    o.append(status_bar(WHITE if state != 'terminated' else NAVY))
    o.append(home_indicator(WHITE if state != 'terminated' else NAVY))
    return '\n'.join(o)


def gen_38():
    F, ID, N = '38_Moderation-Overlay', '38', 'Moderation-Overlay'
    frame(F, ID, N, 'First-Warning', moderation(), note='Softened copy; calm tone. Who sees it is an open question')
    frame(F, ID, N, 'Own-Camera-Flagged', moderation('own'))
    frame(F, ID, N, 'Call-Terminated', moderation('terminated'), note='Confirmed violation shows 57 afterwards')


def gen_all():
    gen_17(); gen_18(); gen_19(); gen_20(); gen_22(); gen_23(); gen_38()
