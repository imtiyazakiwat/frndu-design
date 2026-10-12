"""Girish batch 3: 27 Chat List, 28 Chat Conversation, 30 Recharge Store, 48 Payment Result, 39 Report Sheet.

Drafted WITHOUT the Girish brief file (not saved in docs/design_tasks/). Sources: PRD §7.8, §7.9, §8.4 (origin/dev),
state lists + copy recovered from the earlier unsourced frames. Everything not in those sources is logged in README.
"""
from lib2 import *
from illus import portrait, soft_blob, sparks
from screens_e import compose, overflow_sheet, hp_body
from screens_f import bubble, video_call, gem_text

H = HOSTS[0]


def hero(cy, ic, col=BLUE, bg=BTINT, d=112, isz=56):
    """Centred hero: soft tint blob + white disc + icon + sparks (same recipe as 38 Call-Terminated)."""
    return (soft_blob(195, cy + 6, d * 0.75, d * 0.57, bg) + f'<circle cx="195" cy="{cy}" r="{d / 2}" fill="{WHITE}"/>'
            + icon(ic, 195 - isz / 2, cy - isz / 2, col, isz) + sparks(195 + d / 2 - 2, cy - d / 2 - 10, CORAL))


def host_lead(h, d=48):
    return lambda x, y: host_photo(x, y, d, d, h, r_all=d / 2, scale=d / 120)


# ============================================================ 27 Chat List
USER_CHATS = [(HOSTS[0], '9:41 AM', 'See you tonight at 9?', 2), (HOSTS[1], '8:15 AM', 'That was such a fun call, thanks!', 0),
              (HOSTS[2], 'Yesterday', 'Typing…', 0), (HOSTS[3], 'Mon', 'Haha yes, Kannada movies are the best', 1),
              (HOSTS[5], 'Mon', 'Good night', 0), (HOSTS[4], 'Sun', 'Okay, talk soon', 0)]
HOST_CHATS = [('Rohan_K', '9:52 AM', 'Thanks for the call! Talk tomorrow?', 1), ('Vikram', '9:10 AM', 'Haha, that was fun', 0),
              ('Arjun.S', 'Yesterday', 'Good night 🙂'.replace(' 🙂', ''), 0), ('Kabir_07', 'Mon', 'See you soon', 0)]
REQUESTS = [('Rohan_K', '10:02 AM', 'Recharged 5,000+', 'Hi Priya, can we talk about XXXXXXXX…'),
            ('Vikram', '9:20 AM', 'Recharged 1,000+', 'Hello! Loved your intro audio.'),
            ('Arjun.S', 'Yesterday', 'New user', 'Hey, are you free for a call?')]


def chat_row(y, name, ts, preview, unread=0, lead=None, verified=True, offset=0):
    nm = name if tw(name, 15, 500) < 190 else name[:18] + '…'
    o = [f'<!-- Chat row {name} → 28 -->', f'<g transform="translate({-offset} 0)">',
         f'<rect x="0" y="{y}" width="390" height="72" fill="{CREAM}"/>' if offset else '']
    o.append(glass(12, y + 4, 366, 64, 20, shadow=False))
    if lead is None and name in HOST_IMG:
        o.append(avatar(48, y + 36, 48, img=HOST_IMG[name]))
    else:
        o.append((lead or lead_avatar(name[0]))(24, y + 12))
    o.append(t1(84, y + 31, nm, 15, 500, NAVY))
    if verified:
        o.append(icon('badge-check', round(88 + tw(nm, 15, 500)), y + 17, BLUE, 16))
    pcol = BLUE if preview == 'Typing…' else (NAVY if unread else SLATE)
    pv = preview if tw(preview, 13, 400) < 220 else preview[:30] + '…'
    o.append(t1(84, y + 52, pv, 13, 500 if unread else 400, pcol))
    o.append(t1(366, y + 31, ts, 12, 500, BLUE if unread else TERT, 'end'))
    if unread:
        o.append(f'<circle cx="356" cy="{y + 47}" r="10" fill="{BLUE}"/>' + t1(356, y + 51, str(unread), 11, 700, WHITE, 'middle'))
    o.append('</g>')
    if not offset:
        o.append(hit(24, y, 342, 72, f'chat:{name}'))
    return '\n'.join(o)


def swipe_actions(y):
    o = ['<!-- Swipe actions: Mute / Delete -->']
    for i, (lbl, ic, bg) in enumerate([('Mute', 'bell-off', SLATE), ('Delete', 'trash-2', ERROR)]):
        x = 246 + i * 72
        o.append(f'<rect x="{x}" y="{y}" width="72" height="72" fill="{bg}"/>' + icon(ic, x + 24, y + 14, WHITE)
                 + t1(x + 36, y + 56, lbl, 12, 600, WHITE, 'middle') + hit(x, y, 72, 72, f'swipe:{lbl}'))
    return '\n'.join(o)


def notice_card(y, ic, title, body, ts, bg=BTINT, col=BLUE):
    n = nlines(body, 'notice', 342 - 32 - 56)
    h = 16 + 22 + 4 + n * 19 + 16
    s, _ = text(88, y + 42, body, 'notice', w=342 - 32 - 56)
    return (f'<!-- System notice "{title}" -->' + card(24, y, 342, h) + f'<circle cx="64" cy="{y + 36}" r="20" fill="{bg}"/>' + icon(ic, 52, y + 24, col)
            + t1(88, y + 33, title, 15, 600, NAVY) + t1(350, y + 33, ts, 12, 500, TERT, 'end') + s), y + h


def s27(host=False, tab='Chats', state='list', query=None, swipe=False, longname=False, chat_off=False):
    o = []
    y = 115
    if state == 'offline':
        b, y2 = offline_banner(y)
        o.append(b)
        y = y2 + 12
    if chat_off:
        b, y2 = banner(y, 'Chat is off. Turn it on from your dashboard to get messages.', 'info', icon_name='message-circle', action='Turn on')
        o.append(b + hit(24, y, 342, y2 - y, 'banner:chat-off'))
        y = y2 + 12
    o.append(input_box(y, query, 'Search messages', 'focused' if query else 'empty', left_icon='search'))
    y += 56 + 16
    labels = ['Chats', 'Requests', 'System Notices'] if host else ['Chats', 'System Notices']
    o.append(seg_tabs(y, labels, labels.index(tab), badges={'Requests': 3} if host and state != 'empty' else {}, key='seg'))
    y += 48 + 12
    if state == 'loading':
        o.append(skeleton_rows(y, 6))
    elif state == 'empty':
        msg = {'Chats': ('message-circle', 'No conversations yet.', 'Find someone to talk to.'),
               'System Notices': ('bell', 'Nothing new.', 'Updates about your account and wallet show up here.'),
               'Requests': ('mail', 'No new requests.', 'New messages from people you haven’t talked to show up here.')}[tab]
        o.append(empty_state(y + 170, msg[0], msg[1], msg[2]))
        if tab == 'Chats' and not host:
            o.append(button(y + 330, 'Explore hosts', 'secondary', x=97, w=196, nav='13'))
    elif state == 'noresults':
        o.append(empty_state(y + 150, 'search', 'No results', 'Try a different name or word.'))
    elif tab == 'System Notices':
        items = ([('gem', 'Recharge successful', '+550 diamonds were added to your wallet, including a 50 bonus.', '9:00 AM', BTINT, BLUE)] if not host else
                 [('badge-check', 'Verification approved', 'You are now a verified host. Go online to start receiving calls.', '9:00 AM', BTINT, SUCCESS)])
        items.append(('shield-check', 'Safety reminder', 'Never share your phone number, OTPs or money with anyone on Frndu.', 'Mon', CTINT, CORAL))
        for it in items:
            s, y = notice_card(y, *it)
            o.append(s)
            y += 12
    elif tab == 'Requests':
        for nm, ts, badge_txt, prev in REQUESTS:
            o.append(f'<!-- Chat request {nm} -->' + card(24, y, 342, 136))
            o.append(avatar(64, y + 36, 40, letter=nm[0]) + t1(96, y + 31, nm, 15, 600, NAVY) + t1(350, y + 31, ts, 12, 500, TERT, 'end'))
            bp, _ = pill(96, y + 40, badge_txt, CTINT if badge_txt != 'New user' else BTINT, CORAL if badge_txt != 'New user' else BLUE, 'gem' if badge_txt != 'New user' else None, h=24)
            o.append(bp.replace('font-size="14"', 'font-size="12"'))
            o.append(t1(40, y + 88, prev, 13, 400, SLATE))
            for i, (lbl, kind) in enumerate([('Accept', 'primary'), ('Decline', 'secondary')]):
                bx = 40 + i * 162
                fill, tc, st = (BLUE, WHITE, '') if kind == 'primary' else (WHITE, BLUE, f' stroke="{BORDER}"')
                o.append(f'<rect x="{bx}" y="{y + 100}" width="148" height="28" rx="14" fill="{fill}"{st}/>'
                         + t1(bx + 74, y + 119, lbl, 13, 600, tc, 'middle') + hit(bx, y + 92, 148, 44, f'{lbl.lower()}:{nm}'))
            y += 136 + 12
        o.append(t1(195, y + 14, 'Requests expire after 7 days', 12, 500, TERT, 'middle'))
    else:
        rows = HOST_CHATS if host else USER_CHATS
        for i, r in enumerate(rows):
            if host:
                nm, ts, pv, un = r
                lead, ver = lead_avatar(nm[0]), False
            else:
                h, ts, pv, un = r
                nm = h['name']
                if longname and i == 0:
                    nm = 'Priyanka Venkataraman'
                lead, ver = host_lead(h), True
            if query and not nm.lower().startswith(query.lower()):
                continue
            off = 144 if (swipe and i == 1) else 0
            if off:
                o.append(swipe_actions(y))
            o.append(chat_row(y, nm, ts, pv, un, lead, ver, off))
            y += 72
    bar = host_bar(1, 3) if host else user_bar(1, 3)
    return compose('\n'.join(o), tab_header('Messages'), bar=bar, clip=(103, TAB_BOTTOM + 24), cid='c27')


def gen_27():
    F, ID, N = '27_Chat-List', '27', 'Chat-List'
    frame(F, ID, N, 'Loading', s27(state='loading'))
    frame(F, ID, N, 'Chats', s27(), note='Realtime list; blocked users hidden. User side has no Requests tab (requests are host side, PRD §7.8)')
    frame(F, ID, N, 'Chats-Swipe-Actions', s27(swipe=True), note='Swipe left: Mute (notifications only) / Delete')
    frame(F, ID, N, 'Chats-Empty', s27(state='empty'))
    frame(F, ID, N, 'System-Notices', s27(tab='System Notices'), note='Announcements, recharge credits, verification updates')
    frame(F, ID, N, 'Notices-Empty', s27(tab='System Notices', state='empty'))
    frame(F, ID, N, 'Search-Results', s27(query='Pri'))
    frame(F, ID, N, 'Search-No-Results', s27(query='Zxq', state='noresults'))
    frame(F, ID, N, 'Long-Name', s27(longname=True))
    frame(F, ID, N, 'Offline', s27(state='offline'), note='Cached list')
    frame(F, ID, N, 'Host-Chats', s27(host=True))
    frame(F, ID, N, 'Host-Requests', s27(host=True, tab='Requests'), note='Contact details masked; Decline is silent; auto-expire after 7 days')
    frame(F, ID, N, 'Requests-Empty', s27(host=True, tab='Requests', state='empty'))
    frame(F, ID, N, 'Host-Chat-Off', s27(host=True, chat_off=True), note='Chat Mode off: no new requests')


# ============================================================ 28 Chat Conversation
def chat_header(host_view=False, name='Priya'):
    o = ['<!-- Chat header: back, avatar, name, online dot; call buttons (users only); overflow -->',
         icon('arrow-left', 24, 63, NAVY) + hit(12, 51, 48, 48, 'back')]
    if host_view:
        o.append(avatar(84, 75, 40, letter=name[0]))
    else:
        o.append(f'<g>{host_photo(64, 55, 40, 40, H, r_all=20, scale=0.33)}</g>')
    o.append(t1(116, 72, name, 16, 700, NAVY) + f'<circle cx="120" cy="88" r="4" fill="{SUCCESS}"/>' + t1(130, 92, 'Online', 12, 500, SLATE))
    o.append(hit(60, 51, 140, 48, 'avatar'))
    if not host_view:
        o.append(icon('phone', 246, 63, BLUE) + hit(234, 51, 48, 48, 'right:phone') + icon('video', 294, 63, BLUE) + hit(282, 51, 48, 48, 'right:video'))
    o.append(icon('more-vertical', 342, 63, NAVY) + hit(330, 51, 48, 48, 'right:more'))
    o.append(f'<rect x="0" y="103" width="390" height="1" fill="{CBORDER}"/>')
    return '\n'.join(o)


def quota_bar(left=7, n=10):
    col = WARN if left <= 2 else BLUE
    return (f'<!-- Quota banner -->' + f'<rect x="24" y="115" width="342" height="36" rx="12" fill="{BTINT}"/>' + icon('message-circle', 40, 123, col, 20)
            + t1(68, 138, f'{left} of {n} free messages left today', 13, 600, NAVY))


def composer(y=754, state='empty', value=None, note=None):
    """Composer bar: input + send. Attachment (+) hidden at Launch (PRD phase note)."""
    o = [f'<rect x="0" y="{y - 16}" width="390" height="{844 - y + 16}" fill="{CREAM}" opacity="0.75"/>'
         f'<rect x="0" y="{y - 16}" width="390" height="{844 - y + 16}" fill="{WHITE}" fill-opacity="0.55"/><rect x="0" y="{y - 16}" width="390" height="1" fill="{WHITE}"/>']
    if note is not None:
        if note:
            s, _ = text(195, y + 14, note, 'notice', anchor='middle', w=320)
            o.append(s)
        return '\n'.join(o)
    dis = state == 'disabled'
    o.append(input_box(y, value, 'Type a message', 'disabled' if dis else ('focused' if state == 'focused' else 'empty'), w=278, h=48))
    on = bool(value) and not dis
    o.append(f'<circle cx="342" cy="{y + 24}" r="24" fill="{BLUE if on else DIS_BG}"/>' + icon('send', 330, y + 12, WHITE) + (hit(318, y, 48, 48, 'btn:Send') if on else ''))
    return '\n'.join(o)


def day_sep(y, label='Today'):
    w = tw(label, 12, 600) + 24
    return f'<rect x="{195 - w / 2:.0f}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{WHITE}"/>' + t1(195, y + 16, label, 12, 600, SLATE, 'middle')


def typing_bubble(y):
    return (f'<rect x="24" y="{y}" width="72" height="40" rx="18" fill="{WHITE}" stroke="{CBORDER}"/>'
            + ''.join(f'<circle cx="{44 + i * 16}" cy="{y + 20}" r="4" fill="{TERT}" opacity="{1 - i * 0.25}"/>' for i in range(3)))


THREAD = [('in', 'Hi! Thanks for following me', None), ('out', 'Hey Priya, how are you?', 'read'),
          ('in', 'I am good! Just finished a long day.', None), ('in', 'What about you?', None),
          ('out', 'Pretty relaxed. Want to call later tonight?', 'delivered')]


def thread(msgs, y=167):
    o = [day_sep(y)]
    y += 40
    for side, txt, st in msgs:
        s, y = bubble(y, txt, side, st)
        o.append(s)
        y += 8
    return '\n'.join(o), y


def s28(msgs=None, quota=7, comp=None, overlay='', host_view=False, top_note=None, extra='', name='Priya', kb=False, show_quota=True):
    msgs = THREAD if msgs is None else msgs
    o = []
    y0 = 115
    if show_quota and not host_view:
        o.append(quota_bar(quota) if quota is not None else '')
        y0 = 167
    if top_note:
        b, y0b = top_note
        o.append(b)
        y0 = y0b + 12
    s, y = thread(msgs, y0)
    o.append(s)
    o.append((extra(y) if callable(extra) else extra) if extra else '')
    bottom = KB_TOP - 64 if kb else 738
    body = clip_group('c28', 104, bottom, '\n'.join(o))
    comp = comp if comp is not None else composer()
    if kb:
        comp = composer(KB_TOP - 64 + 0, 'focused', 'Sounds great, 9 pm?')
    return (blobs(bottom=False) + body + comp + (keyboard('alpha') if kb else '') + chat_header(host_view, name)
            + status_bar() + overlay + home_indicator())


def gen_28():
    F, ID, N = '28_Chat-Conversation', '28', 'Chat-Conversation'
    frame(F, ID, N, 'Default', s28(), note='First 10 messages per pair per UTC day are free (PRD OPEN #2: banner says 3, logic says 10)')
    frame(F, ID, N, 'Empty-Thread', s28(msgs=[], quota=10, extra=empty_state(420, 'message-circle', 'Say hi to Priya', 'Start with something friendly.')))
    frame(F, ID, N, 'Keyboard-Open', s28(kb=True))
    frame(F, ID, N, 'Sending', s28(msgs=THREAD + [('out', 'Sounds great, 9 pm?', 'sending')], quota=6))
    frame(F, ID, N, 'Read', s28(msgs=THREAD[:-1] + [('out', 'Pretty relaxed. Want to call later tonight?', 'read')]), note='Read receipts can be turned off (61, Q3)')
    frame(F, ID, N, 'Failed', s28(msgs=THREAD + [('out', 'Want to call later tonight?', 'failed')], quota=6), note='Tap the bubble to retry')
    frame(F, ID, N, 'Typing-Indicator', s28(extra=typing_bubble), note='Typing indicator via socket')
    frame(F, ID, N, 'Long-Message', s28(msgs=[('in', 'Long words and links wrap inside the bubble: frndu.app/help/calls-and-billing', None),
                                              ('out', 'And then a long message about my whole day, from the morning walk to the late dinner with my cousins.', 'read'),
                                              ('in', 'Wow, that is a long one!', None)]))
    frame(F, ID, N, 'Contact-Masked', s28(msgs=THREAD[:2] + [('in', 'My number is XXXXXXXX, message me there', None)]), note='Server redacts phone numbers, emails and handles before delivery')
    qb = banner(115, 'Free messages used for today. Each message now costs 3 diamonds.', 'warning', icon_name='gem')
    frame(F, ID, N, 'Quota-Used-Up', s28(show_quota=False, top_note=qb), note='Price per paid message is a placeholder (PRD: ₹0.30 or diamond equivalent)')
    low = (f'<rect x="24" y="666" width="342" height="56" rx="16" fill="{CTINT}"/>' + gem(40, 684, 20) + t1(68, 699, 'Add diamonds to keep chatting', 13, 600, NAVY)
           + f'<rect x="274" y="678" width="80" height="32" rx="16" fill="{BLUE}"/>' + t1(314, 699, 'Recharge', 13, 600, WHITE, 'middle') + hit(266, 666, 100, 56, 'btn:Recharge'))
    frame(F, ID, N, 'Balance-Too-Low', s28(show_quota=False, top_note=qb, overlay=low, comp=composer(state='disabled')))
    pend = [('out', 'Hi Priya! Loved your intro.', 'sent')]
    frame(F, ID, N, 'Request-Pending', s28(msgs=pend, quota=9, extra=lambda y: t1(195, y + 16, 'Message sent. Waiting for Priya.', 13, 500, SLATE, 'middle'), comp=composer(note='Waiting for Priya to accept')),
          note='First message to a host is a request until she accepts')
    hb = banner(115, "This host isn't accepting messages", 'info', icon_name='message-circle')
    frame(F, ID, N, 'Host-Not-Accepting', s28(show_quota=False, top_note=hb, comp=composer(state='disabled')))
    rows = [('View profile', 'user', NAVY, '16'), ('Mute', 'bell-off', NAVY, 'mute sheet'), ('Report', 'flag', NAVY, '39'),
            ('Block', 'user-x', ERROR, 'block dialog'), ('Clear chat', 'trash-2', ERROR, 'clear dialog')]
    frame(F, ID, N, 'Overflow-Sheet', s28(overlay=overflow_sheet(rows)))
    frame(F, ID, N, 'Mute-Sheet', s28(overlay=overflow_sheet([(l, 'bell-off', NAVY, 'mute') for l in ['1 hour', '8 hours', '1 week', 'Always']], 'Mute notifications')),
          note='Mutes notifications only')
    frame(F, ID, N, 'Block-Dialog', s28(overlay=dialog('Block Priya?', "She won't be able to message or call you.",
                                                         [('Block', 'destructive', 'Blocked-User'), ('Cancel', 'ghost', 'close')], 'user-x', ERROR, CTINT)))
    frame(F, ID, N, 'Clear-Chat-Dialog', s28(overlay=dialog('Clear this chat?', 'Messages are removed from this phone only.',
                                                              [('Clear chat', 'destructive', 'Empty-Thread'), ('Cancel', 'ghost', 'close')], 'trash-2', ERROR, CTINT)))
    blk = composer(note='') + t1(195, 756, 'You blocked this person.', 13, 400, SLATE, 'middle') + link_row(762, 'Unblock', 'Default')
    frame(F, ID, N, 'Blocked-User', s28(comp=blk))
    ob = banner(167, "You're offline. Messages will send when you reconnect.", 'offline')
    frame(F, ID, N, 'Offline', s28(msgs=THREAD + [('out', 'Sounds great, 9 pm?', 'sending')], top_note=ob))
    frame(F, ID, N, 'Hindi', s28(msgs=[('in', 'नमस्ते! आप कैसे हैं?', None), ('out', 'मैं ठीक हूँ, धन्यवाद!', 'read'), ('in', 'आज रात बात करें?', None)]))
    frame(F, ID, N, 'Host-View', s28(msgs=[('in', 'Thanks for the call! Talk tomorrow?', None), ('out', 'Sure, see you at 9!', 'read')],
                                     host_view=True, name='Rohan_K'), note='Hosts see no call buttons and no quota banner')


# ============================================================ 30 Recharge Store
BUNDLES = [('100', '₹299', None), ('550', '₹499', '+10% bonus'), ('1,200', '₹699', '+20% bonus'), ('3,000', '₹999', '+30% bonus')]


def balance_card(y, bal='1,250', neg=False):
    o = [f'<!-- Balance header -->', f'<rect x="24" y="{y}" width="342" height="112" rx="20" fill="{BLUE}"/>',
         f'<circle cx="340" cy="{y + 10}" r="70" fill="{WHITE}" opacity="0.10"/>',
         t1(44, y + 34, 'Your balance', 14, 600, WHITE), gem(44, y + 50, 28, WHITE),
         t1(80, y + 75, bal, 30, 700, WHITE, ls=-0.6)]
    o.append(f'<rect x="232" y="{y + 64}" width="118" height="32" rx="16" fill="{WHITE}"/>' + icon('receipt', 244, y + 71, BLUE, 18)
             + t1(268, y + 85, 'History', 13, 600, BLUE) + hit(226, y + 58, 130, 44, 'link:Purchase History'))
    return '\n'.join(o)


def bundle_grid(y, state='ok', processing=None):
    o = []
    for i, (amt, price, bonus) in enumerate(BUNDLES):
        x = 24 + (i % 2) * 177
        by = y + (i // 2) * 144
        if state == 'loading':
            o.append(skeleton(x, by, 165, 132, 16))
            continue
        dim = state == 'offline' or (processing is not None and processing != i)
        op = ' opacity="0.5"' if dim else ''
        vip = i == 3
        o.append(f'<!-- Bundle {amt} → store purchase → 48 --><g{op}>' + card(x, by, 165, 132, 16, stroke=CORAL if vip else CBORDER, sw=1.5 if vip else 1))
        if vip:
            o.append(f'<path d="M{x + 165 - 60} {by} H{x + 165 - 16} a16 16 0 0 1 16 16 V{by + 24} H{x + 165 - 60} a12 12 0 0 1 -12 -12 a12 12 0 0 1 12 -12 Z" fill="{CORAL}"/>'
                     + icon('crown', x + 165 - 60, by + 4, WHITE, 16) + t1(x + 165 - 40, by + 17, 'VIP', 11, 700, WHITE))
        o.append(gem(x + 16, by + 18, 24) + t1(x + 46, by + 39, amt, 22, 700, NAVY, ls=-0.3))
        if bonus:
            o.append(f'<rect x="{x + 16}" y="{by + 52}" width="{tw(bonus, 12, 600) + 16:.0f}" height="22" rx="11" fill="{CTINT}"/>' + t1(x + 24, by + 67, bonus, 12, 600, CORAL))
        else:
            o.append(t1(x + 16, by + 67, 'Starter', 12, 500, SLATE))
        if processing == i:
            o.append(f'<rect x="{x + 16}" y="{by + 84}" width="133" height="36" rx="18" fill="{BLUE}"/>' + spinner(x + 82, by + 102, WHITE, 8))
        else:
            o.append(f'<rect x="{x + 16}" y="{by + 84}" width="133" height="36" rx="18" fill="{DIS_BG if dim else BLUE}"/>' + t1(x + 82, by + 107, price, 15, 700, WHITE, 'middle'))
        o.append('</g>')
        if not dim and processing is None:
            o.append(hit(x, by, 165, 132, f'bundle:{amt}'))
    return '\n'.join(o), y + 2 * 144 - 12


def s30(pushed=False, state='ok', bal='1,250', neg=False, processing=None):
    o = []
    y = 115
    if state == 'offline':
        b, y2 = offline_banner(y)
        o.append(b)
        y = y2 + 12
    if neg:
        b, y2 = banner(y, 'Your balance is below zero because of a refund. Add diamonds to continue.', 'warning')
        o.append(b)
        y = y2 + 12
    if state == 'loading':
        o.append(skeleton(24, y, 342, 112, 20))
    else:
        o.append(balance_card(y, bal, neg))
    y += 112 + 24
    o.append(t1(24, y + 19, 'Choose a bundle', 18, 700, NAVY))
    y += 26 + 12
    if state == 'failed':
        o.append(empty_state(y + 110, 'cloud-off', "We couldn't load prices.", 'Try again.'))
        o.append(button(y + 250, 'Retry', 'secondary', x=97, w=196, nav='Loading'))
    else:
        s, y = bundle_grid(y, state, processing)
        o.append(s)
        s, _ = text(195, y + 20, 'Payments are handled securely by the App Store or Google Play.', 'notice', anchor='middle', w=300)
        o.append(s)
    if processing is not None:
        o.append(toast(TAB_BOTTOM - 56 if not pushed else 738, 'Processing…', 'clock'))
    if pushed:
        return compose('\n'.join(o), topbar1('Recharge', nav_back='caller (16, 22, 13.1)'), clip=(103, 820), cid='c30')
    return compose('\n'.join(o), tab_header('Wallet'), bar=user_bar(2, 3), clip=(103, TAB_BOTTOM + 24), cid='c30')


def gen_30():
    F, ID, N = '30_Recharge-Store', '30', 'Recharge-Store'
    frame(F, ID, N, 'Tab-Root', s30(), note='Wallet tab root. Bundle prices are placeholders (PRD §7.9, OPEN #4). First-recharge ribbon and promo field arrive in Q3')
    frame(F, ID, N, 'Pushed', s30(pushed=True), note='Pushed from 16, 22, 13.1 or the DiamondPill; back returns to the caller')
    frame(F, ID, N, 'Loading', s30(state='loading'))
    frame(F, ID, N, 'Balance-Zero', s30(bal='0'))
    frame(F, ID, N, 'Balance-Five-Digit', s30(bal='12,480'))
    frame(F, ID, N, 'Negative-Balance', s30(bal='-120', neg=True), note='Refund/chargeback reversal can make the balance negative')
    frame(F, ID, N, 'Prices-Failed', s30(state='failed'))
    frame(F, ID, N, 'Purchase-Processing', s30(processing=1), note='After the store sheet confirms; then 48')
    frame(F, ID, N, 'Offline', s30(state='offline'))


# ============================================================ 48 Payment Result
def result_page(kind, title, body, rows=None, buttons=(), note=None, amount=None, sub=None):
    ic, col, bg = {'success': ('check-circle', SUCCESS, BTINT), 'pending': ('clock', BLUE, BTINT), 'failed': ('x-circle', ERROR, CTINT)}[kind]
    o = [blobs(), hero(230, ic, col, bg)]
    y = 318
    if amount:
        o.append(gem_text(195, y + 30, amount, 30, 700, NAVY, BLUE, 'middle'))
        y += 44
        if sub:
            o.append(t1(195, y + 14, sub, 13, 500, SLATE, 'middle'))
            y += 22
        y += 8
    s, y = text(195, y, title, 'h2' if not amount else 'h4', anchor='middle', w=320)
    o.append(s)
    if body:
        s, y = text(195, y + 8, body, 'body', anchor='middle', w=320)
        o.append(s)
    y += 24
    if rows:
        s, y = kv_card(y, rows)
        o.append(s)
    a, top = action_area(([('note', note, 'notice')] if note else []) + list(buttons))
    o.append(a)
    o.append(status_bar())
    o.append(home_indicator())
    return '\n'.join(o)


def compact(kind):
    """In-call compact result sheet over 19 (never ends the call)."""
    top = 844 - 300
    ic, col, bg = {'success': ('check-circle', SUCCESS, BTINT), 'pending': ('clock', BLUE, BTINT), 'failed': ('x-circle', ERROR, CTINT)}[kind]
    title, body, btn = {'success': ('+50 added', 'New balance 62. Keep talking!', 'Continue call'),
                        'pending': ('Payment processing…', 'Diamonds arrive in under 5 minutes.', 'Back to call'),
                        'failed': ("Payment didn't go through", 'Your card was declined.', 'Try again')}[kind]
    b = [f'<circle cx="52" cy="{top + 52}" r="28" fill="{bg}"/>' + icon(ic, 40, top + 40, col),
         t1(96, top + 47, title, 18, 700, NAVY), t1(96, top + 70, body, 14, 400, SLATE)]
    b.append(button(top + 120, btn, 'primary', nav='19' if kind != 'failed' else '22 sheet'))
    if kind == 'failed':
        b.append(link_row(top + 188, 'Back to call', '19'))
    return video_call(overlay=scrim(0.3) + sheet(top, '\n'.join(b)))


FAIL = {'Declined': 'Your card or account declined the payment.', 'Funds': "There wasn't enough money in the account.",
        'Store': 'The store had a problem. Try again in a moment.', 'Timeout': 'The payment took too long to confirm.'}


def gen_48():
    F, ID, N = '48_Payment-Result', '48', 'Payment-Result'
    btn_s = [('btn', 'Continue', 'primary', 'origin (call, 16 or 13)'), ('link', 'View receipt', '31 Purchases')]
    frame(F, ID, N, 'Success-Bonus', result_page('success', 'Payment successful', None, [('New balance', '1,800', 'gem'), ('Order ID', 'ORD-88415')], btn_s,
                                                 amount='+550 added', sub='Includes 50 bonus diamonds'), note='Bonus shown separately')
    frame(F, ID, N, 'Success-No-Bonus', result_page('success', 'Payment successful', None, [('New balance', '1,350', 'gem'), ('Order ID', 'ORD-88416')], btn_s, amount='+100 added'))
    frame(F, ID, N, 'Success-Long-Order-ID', result_page('success', 'Payment successful', None, [('New balance', '1,750', 'gem'), ('Order ID', 'ORD-2026-10-09-8841-5512…')], btn_s,
                                                         amount='+500 added'), note='Long order IDs truncate with …; full ID in the receipt (31)')
    pend_btn = [('btn', 'Check status', 'primary', 'poll'), ('link', 'Back to app', 'origin')]
    pbody = 'Your diamonds will arrive as soon as the bank confirms, usually in under 5 minutes.'
    frame(F, ID, N, 'Pending', result_page('pending', 'Payment processing…', pbody, [('Order ID', 'ORD-88415')], pend_btn),
          note='Auto-polls every 5 s for 2 min, then background + push. Never blocks an active call')
    frame(F, ID, N, 'Pending-Checking', result_page('pending', 'Payment processing…', pbody, [('Order ID', 'ORD-88415')],
                                                    [('btn', 'Check status', 'primary-loading', 'poll'), ('link', 'Back to app', 'origin')]))
    fail_btn = [('btn', 'Try again', 'primary', 'same bundle'), ('link', 'Choose another bundle', '30'), ('link', 'Contact support', '66 (prefilled)')]
    for k, reason in FAIL.items():
        frame(F, ID, N, f'Failed-{k}', result_page('failed', "That payment didn't go through.", reason, None, fail_btn,
                                                   note='If any money was taken, it comes back automatically in 5 to 7 business days.'))
    frame(F, ID, N, 'Compact-Success', compact('success'), note='In-call purchase from 22; the call keeps running')
    frame(F, ID, N, 'Compact-Pending', compact('pending'))
    frame(F, ID, N, 'Compact-Failed', compact('failed'))


# ============================================================ 39 Report Sheet
REASONS = ['Nudity or inappropriate content', 'Harassment or abuse', 'Underage suspect', 'Fraud or scam', 'Impersonation']


def report_sheet(sel=None, state='form', shot=None, comment=None):
    top = 140
    b = []
    if state == 'success':
        top = 844 - 420
        b.append(hero(top + 92, 'check-circle', SUCCESS, BTINT, 96, 48))
        s, y = text(195, top + 164, 'Thanks for letting us know', 'h3', anchor='middle')
        b.append(s)
        s, y = text(195, y + 8, 'Priya has been blocked. Our safety team will review your report.', 'body', anchor='middle', w=300)
        b.append(s + t1(195, y + 24, 'Case ID: RPT-20481', 13, 600, SLATE, 'middle'))
        b.append(button(844 - 34 - 56, 'Done', 'primary', nav='13 (Priya hidden)'))
        return scrim() + sheet(top, '\n'.join(b))
    b.append(text(24, top + 24, 'Report Priya', 'h3')[0] + icon('x', 342, top + 22, NAVY) + hit(330, top + 10, 48, 48, 'close'))
    b.append(text(24, top + 58, "Your report is private. They won't know it was you.", 'notice', w=342)[0])
    y = top + 92
    if state in ('error', 'offline'):
        bb, y2 = (offline_banner(y) if state == 'offline' else banner(y, "We couldn't send your report. Try again.", 'error'))
        b.append(bb)
        y = y2 + 8
    for r in REASONS:
        on = r == sel
        b.append(f'<!-- Reason "{r}" -->' + radio(42, y + 22, on) + t1(66, y + 27, r, 15, 500 if on else 400, NAVY) + hit(24, y, 342, 44, f'reason:{r}'))
        y += 44
    y += 8
    # screenshot tile
    b.append(t1(24, y + 15, 'Screenshot (optional)', 14, 600, NAVY))
    y += 28
    if shot == 'uploading':
        b.append(f'<rect x="24" y="{y}" width="64" height="64" rx="12" fill="{SKEL}"/>' + spinner(56, y + 32, BLUE, 10)
                 + f'<rect x="24" y="{y + 70}" width="64" height="4" rx="2" fill="{BORDER}"/><rect x="24" y="{y + 70}" width="38" height="4" rx="2" fill="{BLUE}"/>')
    else:
        b.append(f'<rect x="24.5" y="{y + 0.5}" width="63" height="63" rx="12" fill="{WHITE}" stroke="{BORDER}" stroke-dasharray="4 4"/>'
                 + icon('image-plus', 44, y + 20, BLUE) + hit(24, y, 64, 64, 'add:screenshot'))
    y += 64 + 16
    b.append(input_box(y, comment, 'Tell us what happened (optional)', 'empty', h=72, multiline=True))
    y += 72 + 12
    b.append(err_msg(24, y, 'Reporting also blocks this person.', color=SLATE, icon_name='user-x')[0])
    kind = 'destructive' if sel else 'disabled'
    if state == 'submitting':
        kind = 'destructive-loading'
    if state == 'offline':
        kind = 'disabled'
    b.append(button(844 - 34 - 56, 'Submit Report & Block', kind, nav='success state; auto-block; case created'))
    return scrim() + sheet(top, '\n'.join(b))


def gen_39():
    F, ID, N = '39_Report-Sheet', '39', 'Report-Sheet'
    base = hp_body()
    frame(F, ID, N, 'No-Reason', base + report_sheet(), note='Opened from 16 overflow, 19 shield, 28 overflow, 27 request, 23 low rating')
    frame(F, ID, N, 'Reason-Selected', base + report_sheet('Harassment or abuse'))
    frame(F, ID, N, 'Screenshot-Uploading', base + report_sheet('Harassment or abuse', shot='uploading'))
    frame(F, ID, N, 'Submitting', base + report_sheet('Harassment or abuse', 'submitting'))
    frame(F, ID, N, 'Success', base + report_sheet(state='success'), note='"Track this report" (58) arrives in Q3, so no link at Launch')
    frame(F, ID, N, 'Error', base + report_sheet('Harassment or abuse', 'error'))
    frame(F, ID, N, 'Offline', base + report_sheet('Harassment or abuse', 'offline'))


def gen_all():
    gen_27(); gen_28(); gen_30(); gen_48(); gen_39()
