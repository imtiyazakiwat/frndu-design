"""Write design/README.md from the frame registry (/tmp/frndu_registry.tsv)."""
import collections
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCREENS = [
    ('00C', 'Shared components (Imtiyaz sheets)', '—'),
    ('01', 'Splash & Welcome', 'Get Started → 02; language icon → 01.1; Terms/Privacy → 68; auto-routing → 13 / 24 / 56 / 03A / 68 / 64'),
    ('01.1', 'Language Sheet (NEW)', 'Select → apply + close, back to caller (01, 40, 00.1)'),
    ('02', 'Phone Input', 'Send Verification Code → 03; back → 01; country → picker sheet; links → 68'),
    ('03', 'SMS OTP', 'Verify → 04 (new) / 13 or 24 (returning) / 56 / 03A / 06.1; Change number & back → 02'),
    ('03A', 'Account Restore', 'Restore → 13 (24 host); Continue with Deletion → 01; Contact Support → link'),
    ('04', 'Gender', 'Continue → confirm dialog → 06 (Male) / 05 (Female)'),
    ('05', 'Role Select', 'Explore as User → 06; Become a Host → 07; back → 04 (locked)'),
    ('06', 'Basic Profile', 'Complete Setup → 06A (under 18 → 06.1); back → 04/05; avatar → photo sheet → crop'),
    ('06A', 'Live Photo (NEW, normal users)', 'Take live photo → camera → review → Use photo → 12; Skip for now → 12; back → 06'),
    ('06.1', 'Under-18 Blocked (NEW)', 'Read our policy → 68; Contact Support → link; Log Out → 01'),
    ('12', 'Permissions Primer', 'Grant Permissions → OS prompts → 13; Not now → 13'),
    ('07', 'Verification Method', 'Proceed → 08; back → 05'),
    ('08', 'Video Verification', 'Start → recording; Submit → 09A; Retake → ready; back → 07'),
    ('09A', 'Host Languages', 'Continue → 10 (as sheet from 24/26: Save + close)'),
    ('10', 'Verification Pending', 'Explore App as Guest User → 13; decision → 11'),
    ('11', 'Verification Result', 'Approved → 11A / 24; Re-apply Now → 07; permanent → Contact Support'),
    ('11A', 'Host Tutorial & Terms', 'Proceed to Dashboard → 24; terms link → 68'),
    ('24', 'Host Dashboard (tab 1)', 'Avatar → 00.1; quick links → 25 / 32 / 26; bar → 24 / 27 / 25 / 32 / 26'),
    ('25', 'Host Call History (tab 3)', 'Row → call detail sheet; calendar → date-range sheet'),
    ('26', 'Host Profile & Rates (tab 5)', 'Save → toast; Account settings → 40; Switch to User view → 13; Edit languages → 09A sheet'),
    # Girish
    ('00', 'App Shell (Girish)', 'User bar → 13 / 27 / 30 / 40; host bar → 24 / 27 / 25 / 32 / 26; TopBar T1–T4 specimens'),
    ('00.1', 'Side Drawer (Girish)', 'Rows → 40 / 30 / 31 / 41 / 60 / 01.1 / 59 / 65 / 63; host rows → 13 / 32 / 25; Log Out → 01; scrim → close'),
    ('13', 'Home Feed (Girish)', 'Avatar → 00.1; DiamondPill → 30; search / filters → 14; banner / host card → 16; Quick Match → 13.1'),
    ('13.1', 'Quick Match Picker (Girish)', 'Start Matching → 15; Recharge to continue → 30; scrim → 13'),
    ('14', 'Filter & Search (Girish)', 'Apply Filters → 13 (filtered); result row → 16; close → 13'),
    ('15', 'Matching Radar (Girish)', 'Cancel Match → 13; Try again → restart; Back to home → 13'),
    ('16', 'Host Profile (Girish)', 'Voice / Video → 17 (or 30 if balance short); Message → 28; overflow → 39; back → caller'),
    ('17', 'Outbound Ringing (Girish)', 'Connected → 19 / 20; Cancel / Back to profile → 16'),
    ('18', 'Incoming Call (Girish)', 'Swipe to accept → 19 / 20; Decline / auto-decline → 24'),
    ('19', 'Video Call (Girish)', 'Shield → sheet → 39 / 59; low-balance banner → 22; End → 23; violation → 38'),
    ('20', 'Voice Call (Girish)', 'Low-balance banner → 22; End → 23'),
    ('22', 'Low Balance Drawer (Girish)', 'Bundle → store purchase → toast; See all bundles → 30 (call keeps running)'),
    ('23', 'Call Ended (Girish)', 'Submit / Skip / close → 13 (host → 24); ≤ 2 stars → Report → 39'),
    ('38', 'Moderation Overlay (Girish)', 'I understand → 19 (video stays blurred); terminated OK → 57'),
    # Drafted without the briefs (see note at top)
    ('27', 'Chat List (Girish, DRAFT)', 'Row → 28; host Requests: Accept → Chats, Decline (silent); chat-off banner → 24'),
    ('28', 'Chat Conversation (Girish, DRAFT)', 'Call icons → 17; overflow → View profile 16 / Mute / Report 39 / Block / Clear; Recharge → 30'),
    ('30', 'Recharge Store (Girish, DRAFT)', 'Bundle → store sheet → 48; History → 31 Purchases; tab root (Wallet) or pushed with back'),
    ('48', 'Payment Result (Girish, DRAFT)', 'Continue → origin; View receipt → 31; Try again → same bundle; compact sheet over 19 for in-call buys'),
    ('39', 'Report Sheet (Girish, DRAFT)', 'Submit Report & Block → success (case ID) → Done closes; opened from 16, 19, 23, 27, 28, 59'),
    ('40', 'Profile & Settings (Abid, DRAFT)', 'Rows → 40.1 / 60 / 01.1 / 31 / 41 / 65 / 59 / 63 / 68; Log Out → dialog → 01; Delete → 42'),
    ('40.1', 'Edit Profile (Abid, DRAFT)', 'Save → toast → 40; DOB and gender locked'),
    ('60', 'Notification Preferences (Abid, DRAFT)', 'Toggles save instantly; Quiet hours → sheet; OS off → Open Settings'),
    ('41', 'Blocked Users (Abid, DRAFT)', 'Unblock → confirm dialog → toast'),
    ('63', 'About (Abid, DRAFT)', 'Check for update; legal rows → 68; Rate → store; Copy diagnostic ID'),
    ('65', 'Help Center (Abid, DRAFT)', 'Category → accordions → Was this helpful?; Contact Support → support link (66 is Q3)'),
    ('68', 'Legal Viewer (Abid, DRAFT)', 'Language toggle, text size, scroll progress; blocking variant: checkbox → Accept & Continue'),
    ('64', 'System States (Abid, DRAFT)', 'No internet / server error / maintenance / force + soft update / region'),
    ('31', 'Transaction History (Abid, DRAFT)', 'Tabs All / Purchases; row → receipt / pending / call detail sheet; mail → export'),
    ('32', 'Host Wallet (Abid, DRAFT)', 'Request Cash Out → 34; payout method → 33; KYC → 51; history → 35'),
    ('33', 'Withdrawal Setup (Abid, DRAFT)', 'Method → form (UPI / Bank) → Submit → 51'),
    ('51', 'KYC Status (Abid, DRAFT)', 'Stepper Identity → Bank / UPI → Review; Re-upload → 33; Verified → 34'),
    ('34', 'Withdrawal Confirm (Abid, DRAFT)', 'Confirm Withdrawal → 34.1; blocked unless KYC verified'),
    ('34.1', 'Withdrawal Re-auth (Abid, DRAFT)', 'OTP or biometric → requested → 35'),
    ('35', 'Withdrawal History (Abid, DRAFT)', 'Row → detail sheet (completed / failed with refund)'),
    ('42', 'Account Deletion (Abid, DRAFT)', 'Checkbox → Permanently Delete → OTP → scheduled → 01'),
    ('56', 'Account Restricted (Abid, DRAFT)', 'Contact Support; Community Guidelines → 68; Log Out → 01'),
    ('57', 'Strike Notice (Abid, DRAFT)', 'I Understand (required) → 13 / 24; guidelines → 68; Appeal → support link'),
    ('59', 'Safety Center (Abid, DRAFT)', 'How to report → 39; Blocked → 41; Report an emergency → dialog'),
]

QUESTIONS = [
    '**From the brief**',
    '1. 06: is the profile photo required? (Drawn as optional.)',
    '2. 07: should the single Video card come preselected? Both variants drawn (`07_..._Unselected`, `07_..._Preselected-Variant`).',
    '3. 05: select-then-Continue vs tap-to-go; is "You can change this later." correct for Launch?',
    '4. 11A static variant: unlock the checkbox when the user scrolls to the end? (Drawn that way.)',
    '5. 26: max length of the intro audio and the greeting. Greeting drawn with 120 characters as a placeholder.',
    '6. 02: final blocked-number copy (open item D8 / tasks.md T-11). Placeholder copy used, not final.',
    '7. Confirm every line marked *(proposed copy)* in the brief.',
    '',
    '**Assumptions made because `00-shared-rules-and-navigation-map.md` was not available**',
    '8. All layout constants (TopBar, back button, bottom action area, sheet, dialog, banner, toast, host bottom bar) are PROPOSED in `LAYOUT-CONSTANTS.md`. Please approve or send the shared file.',
    '9. TopBar and BottomNavigation are owned by Girish; they are drawn here as placeholders to be swapped for his components.',
    '10. Host bottom bar labels/icons: Dashboard (layout-dashboard), Messages (message-circle), Calls (phone), Wallet (wallet), Profile (user). Short labels to fit 78 px tabs.',
    '11. ListRow/MenuRow and StatusPill (Abid), Diamond glyph (Girish) are placeholders. The Diamond is drawn with Lucide `gem`.',
    '',
    '**Design decisions to confirm**',
    '12. Secondary button = white fill, 1 px #E2E7EF border, Blue label. Ghost = no fill, Blue label. Pressed = Blue darkened ~10% (#5270E1), per design.md "darken 8–12%".',
    '13. Checkbox radius 8 (nearest token). Switch 52×32, master switch 64×36.',
    '14. Country flags are image assets (India flag in real colours; other countries shown as placeholders). This is content imagery, not UI colour.',
    '15. Plus Jakarta Sans has no Devanagari. Hindi frames use Noto Sans Devanagari / Kohinoor Devanagari as fallback. Final Hindi font pairing needed.',
    '16. Illustrations are simple placeholders (brand shapes + Lucide icons) for 03A, 06.1, 10, 11, 12. Final illustrations needed.',
    '17. 24 online caption "You can receive calls now." and on-call caption "You\'re in a call right now." are new proposed copy.',
    '18. 08: recording state shows a ghost "Cancel"; back is hidden while recording and uploading.',
    '19. 25 call detail: commission shown as 30% (PRD default, OPEN #6).',
    '20. 26 "Switch to User view" and "Account settings" use MenuRow; 26 Save button appears 16 px above the bottom bar only when something changed.',
    '21. Error/offline banners sit 16 px under the top bar (or status bar) and push content down; offline disables the primary action.',
    '',
    '**Visual restyle (reference images from Imtiyaz) to confirm**',
    '22. New logo: coral + blue smiling speech bubbles with a translucent overlap and two sparks.',
    '23. Hero illustrations (boy/girl characters, phones, shield, clock, calendar) use two illustration-only colours not in design.md: skin #F8C4A2 / #EDAA86 and hair #3A2A2B. Approve or add an illustration palette.',
    '24. New component: step progress bar in the top bar (02–09A). Not in design.md; needs owner approval.',
    '25. 01: language pill (globe + "English") replaces the bare `languages` icon; headline "Talk to someone who gets you." + description replace the single tagline; legal line moved below the CTA (brief puts it above). Same for 02.',
    '26. 02 and 03: hero illustration replaces the 56 px logo + tagline from the brief.',
    '27. 04: list cards with radio (Female, Male) replace the side-by-side cards. The reference also shows "Prefer not to say"; NOT added, because the PRD needs a binary, permanent gender for the role flow. Confirm.',
    '28. 05: crown icon for host role (brief says badge-check). Onboarding CTAs carry a → arrow.',
    '',
    '**Girish screens (00–38): assumptions to confirm**',
    '29. D-COLOUR: there is no status colour token for Busy. Busy uses Coral; Online uses Success; Offline uses Tertiary text.',
    '30. All prices are placeholders: call rates (30–80 diamonds/min), 22 micro-bundles (50 / 120 / 300 for $0.49 / $0.99 / $1.99), 23 host commission 30%.',
    '31. 16: the sticky bar has three CTAs (Message + Voice + Video). This conflicts with "one primary button per screen" (PRD §16.3).',
    '32. 38: who sees the moderation overlay (the user, the host, or both)? Copy is softened; a confirmed violation shows 57 afterwards.',
    '33. 00.1: Log Out should open a confirm dialog first. The dialog is not drawn; the prototype goes straight to 01.',
    '34. Prototype-only navigation (not product behaviour): 15 has no "match found" frame, so the radar runs Searching → Still looking → No hosts. 19 is drawn from the user side; an accepted incoming call (18) also lands on 19. On 24, going online auto-plays an incoming call (18) after 5 s.',
    '35. The Girish and Abid briefs are now saved in `docs/design_tasks/`. The DRAFT screens have the new theme but have NOT yet been compared line by line with them.',
    '',
    '**New theme (11 Oct), matching `design/_refs/` (Home is the master)**',
    '51. Translucency: frosted cards, blurred background blobs and glows use White, Cream, Blue and Coral tokens at less than 100% opacity, plus gradients of those tokens. design.md says "no new tints". Imtiyaz will discuss this with Rahul.',
    '52. Photos: hosts and callers use real placeholder photos cropped from the refs. They are hosted on the prototype deploy (`https://frndu-prototype.vercel.app/img/`; source in `design/_assets/photos/`). The refs only contain two women and one man, so the 6 demo hosts reuse those two faces (some mirrored). Onboarding heroes stay illustrated.',
    '53. 13 Home: a horizontal host carousel (the next card peeks) and an "All hosts" grid further down, as in the ref. The brief asks for a two-column grid only. The card shows ★ rating and one rate (video, or voice if video is off) plus a chevron. The brief asks for both rates; both are shown on 16.',
    '54. 06A Live Photo for normal users is new behaviour (the PRD only has the host liveness check, 08). It is placed after 06 and can be skipped ("Skip for now"). Should it block progress? Is it a photo or a short liveness video?',
    '55. 18 Incoming Call (host side) follows `Priya’s Incoming Video Call.png`: a full-bleed caller photo with Message, Decline, Accept and Audio Only (video calls only). The brief has a swipe-to-accept track and Decline only. Message and Audio Only are new behaviour and need confirmation.',
    '56. 19 Video Call follows `Glossy Video Call with Priya.png`: name, duration and ticker top-left, Rohan in the PiP, and five controls (Mute, Stop Video, End Call, Chat, Flip) in a frosted dark panel. The brief says "no bar behind them". The ref’s “End-to-end encrypted”, add-friend, reactions and floating comments are NOT added (not in the PRD).',
    '57. 17 and 20 use the Cream themed canvas (`Pastel Calling Screen for Priya.png`, `Frndu Secure Call with Priya.png`). The 17 brief asks for a blurred photo with a Navy scrim; 20 asks for two avatars side by side. 20 has the Frndu mark and a -40/min ticker in place of the ref’s “Secure Call” pill. The ref’s Video and Chat buttons are not added (the brief says no Request Video).',
    '58. 16: the followers count is removed from the stats card (rating + talk time only).',
    '',
    '**DRAFT screens (27, 28, 30, 39, 48 and all Abid screens): built without the Girish/Abid brief files**',
    '36. Layout, states and copy come from PRD §5, §7.8–7.12, §8.4–8.8 and §10.2. For 27, 28, 30, 39 and 48 the state lists and most copy were recovered from earlier unsourced frames. Recheck every DRAFT screen against the briefs once they are saved.',
    '37. Q1 scope only. Menu rows link only to Q1 screens. Not shown: Favorites (43), My Reports (58), Earn with Us (36/37), Earnings Analytics (50), Levels (53), the Contact Support form (66) and My Tickets (67). Support actions open a support link for now.',
    '38. 27: the Requests tab is on the host side only. Users see their pending first message inside 28 ("Waiting for Priya to accept").',
    '39. 28: the price after the free quota ("3 diamonds") is a placeholder (PRD: ₹0.30 or the diamond equivalent; OPEN #2 says 3 vs 10 free messages). Attachments are hidden at Launch.',
    '40. 30: bundles and ₹ prices come from the PRD table and are placeholders (OPEN #4). VIP ribbon on the 3,000 bundle. The first-recharge ribbon and promo field are Q3.',
    '41. 39 success has no "Track this report" link, because 58 is Q3.',
    '42. 40: added a Theme row (System / Light / Dark). Dark mode is open decision D5. Remove the row if dark mode is cut.',
    '43. 40.1 Edit Profile is a new ID for the edit form behind "Edit profile". Nickname rule shown as "3 to 20 letters, numbers or underscores" (proposed).',
    '44. 32: fiat estimate (10,000 diamonds = $70.00), minimum withdrawal 5,000 diamonds, 30% commission and the $1.00 platform fee on 34 are placeholders (OPEN #6).',
    '45. 34.1 is a new ID for the OTP / biometric re-auth sheet before a payout.',
    '46. 56: the appeal form and tracker are Q3, so the Q1 screen offers Contact Support, Community Guidelines and Log Out.',
    '47. 57: consequence copy per strike ("shown less in search for 3 / 7 days") is a placeholder; the ladder and expiry follow §8.6 (OPEN #24).',
    '48. 59: helplines 112 / 1930 must be verified by Legal before launch (PRD says so). The emergency dialog is proposed.',
    '49. 63: company name, Grievance Officer and support emails are placeholders.',
    '50. 68: legal text is placeholder copy, not real terms.',
]


def main():
    rows = [l.rstrip('\n').split('\t') for l in open('/tmp/frndu_registry.tsv')]
    by = collections.OrderedDict()
    seen = set()
    for sid, screen, state, rel, note in rows:
        if rel in seen:
            continue
        seen.add(rel)
        by.setdefault('00C' if screen == 'Components' else sid, []).append((state, rel, note))
    total = sum(len(v) for k, v in by.items() if k != '00C')
    nscreens = sum(1 for k in by if k != '00C')
    out = ['# Frndu design: all screens', '',
           '> **Note:** screens marked DRAFT (27, 28, 30, 39, 48 and all Abid screens) were built from the PRD without the Girish/Abid brief files, '
           'which are not saved in `docs/design_tasks/`. Check them against the briefs (see questions 36–50).', '',
           'Briefs: `docs/design_tasks/01-imtiyaz.md` (Imtiyaz, done), Girish (done; 27, 28, 30, 39, 48 are DRAFT), Abid (all DRAFT). '
           'System: `docs/design.md` (origin/dev). Layout constants: `LAYOUT-CONSTANTS.md` (PROPOSED).',
           '',
           f'**{total} screen frames** across {nscreens} screens, plus 3 shared component sheets. All frames are 390 × 844 SVG, named `{{ID}}_{{Screen}}_{{State}}.svg`.',
           'Every tappable element carries an XML comment with its navigation target (e.g. `<!-- Button primary: "Get Started" → 02 -->`).',
           '',
           'Not drawn: 360 / 412 / 430 width variants and Hindi variants (except the explicit Hindi checks on 06.1 and 11).',
           '',
           '## Interactive prototype', '',
           'Open `design/prototype/index.html` in a browser (no server needed).', '',
           '- **Canvas**: every screen with its states, connected by arrows. Drag or scroll to pan, ⌘/Ctrl + scroll to zoom. Click any frame to run from it.',
           '- **▶ Run**: click through the real frames on a phone, starting at 01. Buttons, cards, chips, inputs, switches and tabs are live; loading states auto-advance; scroll on the phone for long screens.',
           '- **‹ ›** arrows (or ← →) step through every state of the current screen, then roll on to the next screen. **▶ Play all** (or Space) walks every frame in order. Auto-advance pauses while stepping.',
           '- Side panel jumps to any screen/state. Keys: Esc = canvas, Backspace / B = back, H = show hotspots, R = restart. Only the Q3 Contact Support form (66), the store, OS settings and the support link show a placeholder.',
           '- Live: https://frndu-prototype.vercel.app',
           '- Click targets live in `design/_gen/flow.js`.', '',
           '## Regenerate', '',
           'Frames are generated from one component library so geometry stays identical across frames:', '',
           '```sh', 'python3 design/_gen/build.py            # writes every SVG, validates with xmllint, rebuilds the prototype',
           'python3 design/_gen/sheet.py "design/02_*/*.svg" /tmp/02.png   # contact sheet for review', '```', '',
           '## Screens', '',
           '| ID | Screen | Frames | Key navigation |', '|---|---|---|---|']
    for sid, name, nav in SCREENS:
        frames = by.get(sid, [])
        states = ', '.join(s for s, _, _ in frames)
        out.append(f'| {sid} | {name} | {len(frames)}: {states} | {nav} |')
    out += ['', '## Frame notes', '']
    for sid, name, _ in SCREENS:
        notes = [(s, n) for s, _, n in by.get(sid, []) if n]
        if notes:
            out.append(f'- **{sid} {name}**: ' + '; '.join(f'{s}: {n}' for s, n in notes))
    out += ['', '## Questions for the Project owner', ''] + QUESTIONS + ['']
    with open(os.path.join(ROOT, 'README.md'), 'w') as f:
        f.write('\n'.join(out))
    print('README written,', total, 'frames')


if __name__ == '__main__':
    main()
