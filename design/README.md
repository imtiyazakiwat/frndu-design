# Frndu design: all screens

> **Note:** screens marked DRAFT (27, 28, 30, 39, 48 and all Abid screens) were built from the PRD without the Girish/Abid brief files, which are not saved in `docs/design_tasks/`. Check them against the briefs (see questions 36–50).

Briefs: `docs/design_tasks/01-imtiyaz.md` (Imtiyaz, done), Girish (done; 27, 28, 30, 39, 48 are DRAFT), Abid (all DRAFT). System: `docs/design.md` (origin/dev). Layout constants: `LAYOUT-CONSTANTS.md` (PROPOSED).

**499 screen frames** across 58 screens, plus 3 shared component sheets. All frames are 390 × 844 SVG, named `{ID}_{Screen}_{State}.svg`.
Every tappable element carries an XML comment with its navigation target (e.g. `<!-- Button primary: "Get Started" → 02 -->`).

Not drawn: 360 / 412 / 430 width variants and Hindi variants (except the explicit Hindi checks on 06.1 and 11).

## Interactive prototype

Open `design/prototype/index.html` in a browser (no server needed).

- **Canvas**: every screen with its states, connected by arrows. Drag or scroll to pan, ⌘/Ctrl + scroll to zoom. Click any frame to run from it.
- **▶ Run**: click through the real frames on a phone, starting at 01. Buttons, cards, chips, inputs, switches and tabs are live; loading states auto-advance; scroll on the phone for long screens.
- **‹ ›** arrows (or ← →) step through every state of the current screen, then roll on to the next screen. **▶ Play all** (or Space) walks every frame in order. Auto-advance pauses while stepping.
- Side panel jumps to any screen/state. Keys: Esc = canvas, Backspace / B = back, H = show hotspots, R = restart. Only the Q3 Contact Support form (66), the store, OS settings and the support link show a placeholder.
- Live: https://frndu-prototype.vercel.app
- Click targets live in `design/_gen/flow.js`.

## Regenerate

Frames are generated from one component library so geometry stays identical across frames:

```sh
python3 design/_gen/build.py            # writes every SVG, validates with xmllint, rebuilds the prototype
python3 design/_gen/sheet.py "design/02_*/*.svg" /tmp/02.png   # contact sheet for review
```

## Screens

| ID | Screen | Frames | Key navigation |
|---|---|---|---|
| 00C | Shared components (Imtiyaz sheets) | 3: Buttons-Inputs-OTP, Cards-Selection-Controls, Sheets-Dialogs-Pickers-Camera | — |
| 01 | Splash & Welcome | 3: Loading, Ready, Low-Power | Get Started → 02; language icon → 01.1; Terms/Privacy → 68; auto-routing → 13 / 24 / 56 / 03A / 68 / 64 |
| 01.1 | Language Sheet (NEW) | 4: English-Selected, Hindi-Selected, Pressed, Switching-Loading | Select → apply + close, back to caller (01, 40, 00.1) |
| 02 | Phone Input | 11: Empty, Focused, Filled-Valid, Invalid-Number, Rate-Limited, Send-Failed, Blocked-Number, Sending, Offline, Country-Picker, Keyboard-Open | Send Verification Code → 03; back → 01; country → picker sheet; links → 68 |
| 03 | SMS OTP | 12: Empty, Partly-Filled, Complete, Verifying, Wrong-Code, Lockout, Resend-Available, Resend-Sending, Code-Sent-Toast, Code-Expired, Offline, Keyboard-Open | Verify → 04 (new) / 13 or 24 (returning) / 56 / 03A / 06.1; Change number & back → 02 |
| 03A | Account Restore | 8: Default, Default-Scrolled, Host-Account, Last-Day, Restoring, Restore-Limit-Reached, Error, Offline | Restore → 13 (24 host); Continue with Deletion → 01; Contact Support → link |
| 04 | Gender | 9: Nothing-Selected, Male-Selected, Female-Selected, Confirm-Male-Dialog, Confirm-Female-Dialog, Saving, Locked-Re-entry, Error, Offline | Continue → confirm dialog → 06 (Male) / 05 (Female) |
| 05 | Role Select | 5: Nothing-Selected, User-Selected, Host-Selected, Loading, Error | Explore as User → 06; Become a Host → 07; back → 04 (locked) |
| 06 | Basic Profile | 20: Empty, Partly-Filled, Ready, Ready-Top, Photo-Sheet, Crop, Avatar-Uploading, Avatar-Rejected, Nickname-Error, Nickname-At-Limit, Date-Picker, Date-Under-18, Languages-Limit, Referral-Expanded, Referral-Error, Keyboard-Nickname, Keyboard-Referral, Saving, Error, Offline | Complete Setup → 06A (under 18 → 06.1); back → 04/05; avatar → photo sheet → crop |
| 06A | Live Photo (NEW, normal users) | 7: Intro, Camera, No-Face, Review, Uploading, Upload-Failed, Permission-Denied | Take live photo → camera → review → Use photo → 12; Skip for now → 12; back → 06 |
| 06.1 | Under-18 Blocked (NEW) | 3: Default, Hindi, Long-Text | Read our policy → 68; Contact Support → link; Log Out → 01 |
| 12 | Permissions Primer | 4: Default, Dialog-Camera-Off, Dialog-Microphone-Off, Dialog-Notifications-Off | Grant Permissions → OS prompts → 13; Not now → 13 |
| 07 | Verification Method | 5: Unselected, Selected, Preselected-Variant, Loading, Offline | Proceed → 08; back → 05 |
| 08 | Video Verification | 11: Ready, Precheck-Low-Light, Precheck-Face-Off-Centre, Recording, Review, Face-Lost, Uploading, Upload-Failed, Permission-Denied, Daily-Limit, Offline | Start → recording; Submit → 09A; Retake → ready; back → 07 |
| 09A | Host Languages | 9: Prefilled, None-Selected, Limit-Reached, Searching, No-Result, Loading, Load-Failed, Offline, As-Sheet | Continue → 10 (as sheet from 24/26: Save + close) |
| 10 | Verification Pending | 4: Waiting, Taking-Longer, Offline, Persistent-Banner-Component | Explore App as Guest User → 13; decision → 11 |
| 11 | Verification Result | 9: A-Approved, B-Rejected-Poor-Lighting, B-Rejected-Script-Mismatch, B-Rejected-Liveness-Failed, B-Rejected-Face-Not-Visible, B-Rejected-Suspected-Minor, B-Rejected-Duplicate-Account, C-Permanent-Rejection, B-Rejected-Hindi | Approved → 11A / 24; Re-apply Now → 07; permanent → Contact Support |
| 11A | Host Tutorial & Terms | 11: Static-Top, Static-End-Unchecked, Static-End-Checked, Video-Locked, Video-Locked-End, Video-Unlocked, Video-Checked, Terms-Updated, Saving, Error, Offline | Proceed to Dashboard → 24; terms link → 68 |
| 24 | Host Dashboard (tab 1) | 11: Offline-Master-Off, Online-Master-On, Online-Scrolled, On-A-Call, Voice-Video-Off, Before-Online-Sheet, Before-Online-Permission-Dialog, Auto-Offline-Notice, Loading, Error, Connection-Offline | Avatar → 00.1; quick links → 25 / 32 / 26; bar → 24 / 27 / 25 / 32 / 26 |
| 25 | Host Call History (tab 3) | 10: Default, Filter-Missed, Loading-More, Date-Range-Sheet, Call-Detail-Sheet, Loading, Empty, Empty-Filtered, Error, Offline-Cached | Row → call detail sheet; calendar → date-range sheet |
| 26 | Host Profile & Rates (tab 5) | 19: View, View-Scrolled, Edited, Saving, Saved-Toast, Cover-Empty, Cover-Uploading, Cover-Under-Review, Cover-Rejected, Audio-Empty, Audio-Recording, Audio-Recorded, Audio-Uploading, Audio-Under-Review, Greeting-At-Limit, Rate-Locked, Offline, Error, Unsaved-Changes-Dialog | Save → toast; Account settings → 40; Switch to User view → 13; Edit languages → 09A sheet |
| 00 | App Shell (Girish) | 23: User-Tab-Explore, User-Tab-Messages, User-Tab-Wallet, User-Tab-Profile, Host-Tab-Dashboard, Host-Tab-Messages, Host-Tab-Calls, Host-Tab-Earnings, Host-Tab-Profile, Badge-0, Badge-1-Digit, Badge-2-Digits, Badge-99-Plus, Tab-Pressed, Keyboard-Bar-Hidden, TopBar-T1-No-Title, TopBar-T1-Title, TopBar-T1-One-Action, TopBar-T1-Two-Actions, TopBar-T2-Tab-Root, TopBar-T3-Media, TopBar-T4-Sheet, TopBar-Ruler | User bar → 13 / 27 / 30 / 40; host bar → 24 / 27 / 25 / 32 / 26; TopBar T1–T4 specimens |
| 00.1 | Side Drawer (Girish) | 10: Opening, Open-User, Open-Scrolled, Row-Pressed, ID-Copied, Long-Nickname, Approved-Host-User-Drawer, Hindi-Labels, Open-Host, Closing | Rows → 40 / 30 / 31 / 41 / 60 / 01.1 / 59 / 65 / 63; host rows → 13 / 32 / 25; Log Out → 01; scrim → close |
| 13 | Home Feed (Girish) | 14: Loading, Default, Scrolled, Filters-Active, Load-More, Pull-To-Refresh, Empty, Offline-Cached, Guest-Verification-Pending, Balance-Zero, Balance-Five-Digit, Long-Name-Missing-Photo, Without-Nearby, Busy-Status-Change | Avatar → 00.1; DiamondPill → 30; search / filters → 14; banner / host card → 16; Quick Match → 13.1 |
| 13.1 | Quick Match Picker (Girish) | 6: Video-Selected, Voice-Selected, Balance-Too-Low, Few-Hosts-Online, Loading-Prices, Offline | Start Matching → 15; Recharge to continue → 30; scrim → 13 |
| 14 | Filter & Search (Girish) | 8: Default, Filters-Changed, Nothing-Selected, Searching, Results, No-Results, Offline, Error | Apply Filters → 13 (filtered); result row → 16; close → 13 |
| 15 | Matching Radar (Girish) | 7: Searching, Searching-Voice, Still-Looking, No-Hosts-Available, Cancelled, Reduced-Motion, Offline | Cancel Match → 13; Try again → restart; Back to home → 13 |
| 16 | Host Profile (Girish) | 16: Loading, Default, Scrolled-Pricing, Scrolled-Reviews, Long-Bio, No-Reviews, Missing-Photos, Favorite-On, Host-Busy, Host-Offline, Video-Mode-Off, Chat-Off-Toast, Low-Balance-Toast, Overflow-Sheet, Offline, Error | Voice / Video → 17 (or 30 if balance short); Message → 28; overflow → 39; back → caller |
| 17 | Outbound Ringing (Girish) | 7: Ringing-Video, Ringing-Voice, Connecting, Host-Unavailable, Host-Busy, Connection-Dropped, Offline | Connected → 19 / 20; Cancel / Back to profile → 16 |
| 18 | Incoming Call (Girish) | 7: Video-30s, Voice-30s, Countdown-10s, Countdown-3s, Accepting, Auto-Declined, Camera-Permission-Missing | Swipe to accept → 19 / 20; Decline / auto-decline → 24 |
| 19 | Video Call (Girish) | 11: Connected, Muted, Camera-Off, Remote-Camera-Off, Low-Balance-Banner, Zero-Balance-Countdown, Weak-Connection, Reconnecting, Screen-Recording-Warning, Shield-Sheet, Chat-Drawer | Shield → sheet → 39 / 59; low-balance banner → 22; End → 23; violation → 38 |
| 20 | Voice Call (Girish) | 9: Connected, Muted, Speaker-On, Bluetooth-Connected, Low-Balance-Banner, Zero-Balance-Countdown, Reconnecting, Host-Muted, Reduced-Motion | Low-balance banner → 22; End → 23 |
| 22 | Low Balance Drawer (Girish) | 7: Banner-Only, Sheet-Open, Purchasing, Success-Toast, Failed, Grace-Countdown, Voice-Call-Sheet | Bundle → store purchase → toast; See all bundles → 30 (call keeps running) |
| 23 | Call Ended (Girish) | 8: User-Rate, User-Rated, Low-Rating-Prompt, Short-Call, Submitting, Error, Offline-Queued, Host-Summary | Submit / Skip / close → 13 (host → 24); ≤ 2 stars → Report → 39 |
| 38 | Moderation Overlay (Girish) | 3: First-Warning, Own-Camera-Flagged, Call-Terminated | I understand → 19 (video stays blurred); terminated OK → 57 |
| 27 | Chat List (Girish, DRAFT) | 14: Loading, Chats, Chats-Swipe-Actions, Chats-Empty, System-Notices, Notices-Empty, Search-Results, Search-No-Results, Long-Name, Offline, Host-Chats, Host-Requests, Requests-Empty, Host-Chat-Off | Row → 28; host Requests: Accept → Chats, Decline (silent); chat-off banner → 24 |
| 28 | Chat Conversation (Girish, DRAFT) | 21: Default, Empty-Thread, Keyboard-Open, Sending, Read, Failed, Typing-Indicator, Long-Message, Contact-Masked, Quota-Used-Up, Balance-Too-Low, Request-Pending, Host-Not-Accepting, Overflow-Sheet, Mute-Sheet, Block-Dialog, Clear-Chat-Dialog, Blocked-User, Offline, Hindi, Host-View | Call icons → 17; overflow → View profile 16 / Mute / Report 39 / Block / Clear; Recharge → 30 |
| 30 | Recharge Store (Girish, DRAFT) | 9: Tab-Root, Pushed, Loading, Balance-Zero, Balance-Five-Digit, Negative-Balance, Prices-Failed, Purchase-Processing, Offline | Bundle → store sheet → 48; History → 31 Purchases; tab root (Wallet) or pushed with back |
| 48 | Payment Result (Girish, DRAFT) | 12: Success-Bonus, Success-No-Bonus, Success-Long-Order-ID, Pending, Pending-Checking, Failed-Declined, Failed-Funds, Failed-Store, Failed-Timeout, Compact-Success, Compact-Pending, Compact-Failed | Continue → origin; View receipt → 31; Try again → same bundle; compact sheet over 19 for in-call buys |
| 39 | Report Sheet (Girish, DRAFT) | 7: No-Reason, Reason-Selected, Screenshot-Uploading, Submitting, Success, Error, Offline | Submit Report & Block → success (case ID) → Done closes; opened from 16, 19, 23, 27, 28, 59 |
| 40 | Profile & Settings (Abid, DRAFT) | 8: Default, Scrolled, ID-Copied, Theme-Sheet, Log-Out-Dialog, Logging-Out, Host-Account, Offline | Rows → 40.1 / 60 / 01.1 / 31 / 41 / 65 / 59 / 63 / 68; Log Out → dialog → 01; Delete → 42 |
| 40.1 | Edit Profile (Abid, DRAFT) | 7: Default, Editing, Nickname-Error, Locked-Field-Toast, Photo-Sheet, Saving, Saved-Toast | Save → toast → 40; DOB and gender locked |
| 60 | Notification Preferences (Abid, DRAFT) | 6: Default, Presence-Off, OS-Notifications-Off, Quiet-Hours-Sheet, Host, Save-Failed-Toast | Toggles save instantly; Quiet hours → sheet; OS off → Open Settings |
| 41 | Blocked Users (Abid, DRAFT) | 6: Default, Unblock-Dialog, Unblocked-Toast, Empty, Loading, Error | Unblock → confirm dialog → toast |
| 63 | About (Abid, DRAFT) | 6: Default, Scrolled, Checking-Update, Update-Available, Up-To-Date, Diagnostic-ID-Copied | Check for update; legal rows → 68; Rate → store; Copy diagnostic ID |
| 65 | Help Center (Abid, DRAFT) | 7: Default, Category, Article-Open, Helpful-Thanks, Search-Results, No-Results, Offline-Cached | Category → accordions → Was this helpful?; Contact Support → support link (66 is Q3) |
| 68 | Legal Viewer (Abid, DRAFT) | 9: Default, Scrolled, Large-Text, Hindi, Privacy-Policy, Loading, Offline-Cached, Blocking-Unchecked, Blocking-Checked | Language toggle, text size, scroll progress; blocking variant: checkbox → Accept & Continue |
| 64 | System States (Abid, DRAFT) | 8: No-Internet, Retrying, Server-Error, Maintenance, Force-Update, Soft-Update-Sheet, Region-Unavailable, Offline-Banner | No internet / server error / maintenance / force + soft update / region |
| 31 | Transaction History (Abid, DRAFT) | 11: All, Filtered-Recharges, Purchases, Receipt-Sheet, Pending-Sheet, Call-Detail-Sheet, Export-Toast, Load-More, Loading, Empty, Error | Tabs All / Purchases; row → receipt / pending / call detail sheet; mail → export |
| 32 | Host Wallet (Abid, DRAFT) | 8: Default, Below-Minimum, KYC-Pending, KYC-Action-Needed, No-Payout-Method, Commission-Sheet, Loading, Offline | Request Cash Out → 34; payout method → 33; KYC → 51; history → 35 |
| 33 | Withdrawal Setup (Abid, DRAFT) | 8: Select-Method, Method-Selected, UPI-Empty, UPI-Filled, Bank-Filled, PAN-Error, Submitting, Edit-Cooldown | Method → form (UPI / Bank) → Submit → 51 |
| 51 | KYC Status (Abid, DRAFT) | 6: Not-Started, In-Review, Verified, Rejected-Name-Mismatch, Rejected-Invalid-PAN, Manual-Review | Stepper Identity → Bank / UPI → Review; Re-upload → 33; Verified → 34 |
| 34 | Withdrawal Confirm (Abid, DRAFT) | 6: Default, Typing, Empty, Below-Minimum, Above-Available, KYC-Blocked | Confirm Withdrawal → 34.1; blocked unless KYC verified |
| 34.1 | Withdrawal Re-auth (Abid, DRAFT) | 6: OTP-Empty, OTP-Filled, OTP-Wrong, Biometric, Confirming, Requested | OTP or biometric → requested → 35 |
| 35 | Withdrawal History (Abid, DRAFT) | 5: Default, Detail-Completed, Detail-Failed, Empty, Loading | Row → detail sheet (completed / failed with refund) |
| 42 | Account Deletion (Abid, DRAFT) | 6: Default, Checked, Pending-Payout, OTP-Reauth, Deleting, Deleted | Checkbox → Permanently Delete → OTP → scheduled → 01 |
| 56 | Account Restricted (Abid, DRAFT) | 3: Suspended-Temporary, Suspended-Host, Banned-Permanent | Contact Support; Community Guidelines → 68; Log Out → 01 |
| 57 | Strike Notice (Abid, DRAFT) | 5: Warning, Strike-1, Strike-2-Thumbnail, Final-Warning, Acknowledging | I Understand (required) → 13 / 24; guidelines → 68; Appeal → support link |
| 59 | Safety Center (Abid, DRAFT) | 4: Default, Scrolled-Protections, Scrolled-Emergency, Emergency-Dialog | How to report → 39; Blocked → 41; Report an emergency → dialog |

## Frame notes

- **00C Shared components (Imtiyaz sheets)**: Buttons-Inputs-OTP: Buttons, inputs, OTP; Cards-Selection-Controls: Cards, selection, controls, banners, toast; Sheets-Dialogs-Pickers-Camera: Sheets, dialogs, pickers, camera
- **01 Splash & Welcome**: Loading: Checking saved session, max 2 s; Low-Power: Static background frame; battery shows low-power
- **01.1 Language Sheet (NEW)**: English-Selected: Same sheet opened from 01, 40 and 00.1; Switching-Loading: 200 ms while language applies
- **02 Phone Input**: Rate-Limited: Live MM:SS countdown; Blocked-Number: PLACEHOLDER copy. OPEN decision D8 / tasks.md T-11; do not finalise; Country-Picker: Auto-detected country preselected; Keyboard-Open: Button 16 above keyboard
- **03 SMS OTP**: Empty: Resend counting down (60 s); Complete: Autofilled/pasted boxes look identical; Lockout: After 5 wrong tries; live countdown
- **03A Account Restore**: Default: No top bar, no back. Content scrolls under pinned actions; Restore-Limit-Reached: Max 3 restores in 12 months
- **04 Gender**: Nothing-Selected: No top bar at first entry; Confirm-Male-Dialog: Scrim tap does not dismiss; Confirm-Female-Dialog: Scrim tap does not dismiss; Locked-Re-entry: Reached with Back from 05; gender not reset
- **05 Role Select**: Nothing-Selected: Female users only. "You can change this later." needs owner confirmation
- **06 Basic Profile**: Empty: Form scrolls; Complete Setup pinned. Photo optional? (question); Crop: Full-screen state of 06, reused by 40.1 and 26; Avatar-Rejected: Default avatar + moderation message; Date-Under-18: Complete Setup → 06.1; Referral-Error: Non-blocking; Launch accepts code without validation
- **06A Live Photo (NEW, normal users)**: Intro: NEW: after 06 for normal users. Optional (Skip for now) until the owner decides; Camera: Front camera, live capture only; No-Face: Shutter disabled until a face is found; Uploading: Back hidden while saving; Permission-Denied: Camera dialog from 12
- **06.1 Under-18 Blocked (NEW)**: Default: NEW screen; no back, not dismissible; no primary button; Hindi: Hindi translation is draft; needs review; Long-Text: Stress test for long copy
- **12 Permissions Primer**: Default: T4 full-height sheet, no back. System prompts not designed; Dialog-Camera-Off: Reused before first call and on 08; Dialog-Microphone-Off: Reused before first call and on 08; Dialog-Notifications-Off: Reused before first call and on 08
- **07 Verification Method**: Unselected: Owner to choose: preselected or not (both drawn); Preselected-Variant: Alternative: card selected on entry
- **08 Video Verification**: Ready: Permissions granted, pre-checks pass; Recording: Ring animates over 15 s; back hidden; Review: Recorded clip plays inside the circle; Face-Lost: Face lost > 2 s, ring resets; Uploading: Back hidden while uploading; Upload-Failed: Try again resumes; Permission-Denied: Dialog from 12; Daily-Limit: 5 attempts per day
- **09A Host Languages**: Prefilled: Profile languages preselected; As-Sheet: Opened from 24 pre-online check and 26 edit languages
- **10 Verification Pending**: Waiting: No back. Decision arrives by push/live update → cross-fade to 11; Persistent-Banner-Component: Banner placed under top bar on 13
- **11 Verification Result**: A-Approved: Coral CTA allowed: emotional moment; C-Permanent-Rejection: No re-apply; never say how decision was reached; B-Rejected-Hindi: Hindi draft translation
- **11A Host Tutorial & Terms**: Static-Top: No back (first-time gate). Static variant: checkbox unlocks at end of scroll (proposal); Video-Locked: Checkbox locked until 90% watched; Video-Unlocked: Short highlight on unlock; Terms-Updated: Re-shown when Host Terms version changes
- **24 Host Dashboard (tab 1)**: Offline-Master-Off: No bell at Launch. Reviews/Levels/Followers/Analytics/Leaderboard/Schedule not shown; Online-Scrolled: Stats, connection health, quick links; Voice-Video-Off: Master switch disabled + helper line; Auto-Offline-Notice: Shown on next open
- **25 Host Call History (tab 3)**: Default: Grouped by date, sticky headers, pull-to-refresh; Loading-More: Spinner row at end while next page loads; Call-Detail-Sheet: Commission default 30% per PRD
- **26 Host Profile & Rates (tab 5)**: View: No changes: no Save button; Edited: Save appears above the bar; Audio-Recording: Max length not in PRD (question); Greeting-At-Limit: Limit not in PRD; 120 assumed (question)
- **00 App Shell (Girish)**: User-Tab-Explore: User bar 4 × 97.5; tab 1 active → 13; User-Tab-Messages: User bar 4 × 97.5; tab 2 active → 27; User-Tab-Wallet: User bar 4 × 97.5; tab 3 active → 30; User-Tab-Profile: User bar 4 × 97.5; tab 4 active → 40; Host-Tab-Dashboard: Host bar 5 × 78; tab 1 active → 24; Host-Tab-Messages: Host bar 5 × 78; tab 2 active → 27; Host-Tab-Calls: Host bar 5 × 78; tab 3 active → 25; Host-Tab-Earnings: Host bar 5 × 78; tab 4 active → 32; Host-Tab-Profile: Host bar 5 × 78; tab 5 active → 26; Badge-0: Messages badge = 0; Badge-1-Digit: Messages badge = 7; Badge-2-Digits: Messages badge = 24; Badge-99-Plus: Messages badge = 140; Tab-Pressed: Messages tab pressed; TopBar-Ruler: Positions for every designer to check against
- **00.1 Side Drawer (Girish)**: Opening: Panel slides in 250–350 ms, scrim fades in; Open-User: Opened from 13 avatar or left-edge swipe; Open-Scrolled: Menu scrolls; Log Out stays pinned; Approved-Host-User-Drawer: Approved host browsing as user; Hindi-Labels: Labels wrap to 2 lines max; row grows to 64; Open-Host: Opened from 24 avatar
- **13 Home Feed (Girish)**: Default: Banners auto-scroll every 4 s; Busy/Online changes cross-fade 200 ms; Scrolled: 88 px bottom padding keeps the last card above Quick Match; Guest-Verification-Pending: Banner component from 10; Without-Nearby: If Nearby is cut (tasks.md T-31); Busy-Status-Change: Online → Busy: 200 ms cross-fade, no flicker
- **13.1 Quick Match Picker (Girish)**: Video-Selected: Last used mode is preselected
- **14 Filter & Search (Girish)**: Default: 90% height sheet; Nothing-Selected: Reset disabled; Results: Results never include hosts without the selected mode
- **15 Matching Radar (Girish)**: Searching: Orbiting avatars are decorative, not real hosts. No top bar; Still-Looking: After 10 s; No-Hosts-Available: After 30 s; Reduced-Motion: Rings static, no orbit
- **16 Host Profile (Girish)**: Default: 3 CTAs (Message + Voice + Video): PRD §16.3 one-primary question; Low-Balance-Toast: Then pushes 30
- **17 Outbound Ringing (Girish)**: Ringing-Video: Blurred host photo + Navy 40% scrim; no top bar; Connecting: After the host accepts; Host-Unavailable: 30 s timeout
- **18 Incoming Call (Girish)**: Video-30s: Locked phone uses the OS call screen (not designed); Auto-Declined: After 30 s; 3 unattended calls set the host Offline (banner on 24)
- **19 Video Call (Girish)**: Connected: Portrait only. PiP never overlaps controls at 360 × 800; Camera-Off: Your PiP shows your avatar; Low-Balance-Banner: Tap banner → 22 sheet; Reconnecting: Up to 10 s, then the call ends → 23; Chat-Drawer: 50% height text chat drawer
- **20 Voice Call (Girish)**: Connected: No Gift, no Request Video at Launch; Reduced-Motion: Static waveform
- **22 Low Balance Drawer (Girish)**: Banner-Only: Prices are placeholders from the Client; Success-Toast: Sheet closes
- **23 Call Ended (Girish)**: User-Rate: Rating block for calls ≥ 30 s; Low-Rating-Prompt: ≤ 2 stars → Report link → 39; Short-Call: < 30 s: no rating; Offline-Queued: Rating queued until online; Host-Summary: No rating UI for hosts
- **38 Moderation Overlay (Girish)**: First-Warning: Softened copy; calm tone. Who sees it is an open question; Call-Terminated: Confirmed violation shows 57 afterwards
- **27 Chat List (Girish, DRAFT)**: Chats: Realtime list; blocked users hidden. User side has no Requests tab (requests are host side, PRD §7.8); Chats-Swipe-Actions: Swipe left: Mute (notifications only) / Delete; System-Notices: Announcements, recharge credits, verification updates; Offline: Cached list; Host-Requests: Contact details masked; Decline is silent; auto-expire after 7 days; Host-Chat-Off: Chat Mode off: no new requests
- **28 Chat Conversation (Girish, DRAFT)**: Default: First 10 messages per pair per UTC day are free (PRD OPEN #2: banner says 3, logic says 10); Read: Read receipts can be turned off (61, Q3); Failed: Tap the bubble to retry; Typing-Indicator: Typing indicator via socket; Contact-Masked: Server redacts phone numbers, emails and handles before delivery; Quota-Used-Up: Price per paid message is a placeholder (PRD: ₹0.30 or diamond equivalent); Request-Pending: First message to a host is a request until she accepts; Mute-Sheet: Mutes notifications only; Host-View: Hosts see no call buttons and no quota banner
- **30 Recharge Store (Girish, DRAFT)**: Tab-Root: Wallet tab root. Bundle prices are placeholders (PRD §7.9, OPEN #4). First-recharge ribbon and promo field arrive in Q3; Pushed: Pushed from 16, 22, 13.1 or the DiamondPill; back returns to the caller; Negative-Balance: Refund/chargeback reversal can make the balance negative; Purchase-Processing: After the store sheet confirms; then 48
- **48 Payment Result (Girish, DRAFT)**: Success-Bonus: Bonus shown separately; Success-Long-Order-ID: Long order IDs truncate with …; full ID in the receipt (31); Pending: Auto-polls every 5 s for 2 min, then background + push. Never blocks an active call; Compact-Success: In-call purchase from 22; the call keeps running
- **39 Report Sheet (Girish, DRAFT)**: No-Reason: Opened from 16 overflow, 19 shield, 28 overflow, 27 request, 23 low rating; Success: "Track this report" (58) arrives in Q3, so no link at Launch
- **40 Profile & Settings (Abid, DRAFT)**: Default: Q1 menu shows only built destinations (PRD phase notes). Earn with Us (36), Favorites (43), My Reports (58) arrive later; Theme-Sheet: Dark mode is an open decision (PRD §16 D5); Host-Account: Opened from 26 "Account settings"; pushed with back
- **40.1 Edit Profile (Abid, DRAFT)**: Default: Save stays disabled until something changes. DOB and gender are locked (PRD §7.11)
- **60 Notification Preferences (Abid, DRAFT)**: Default: Saved instantly on toggle (server-side). Account & safety locked on (PRD §10.2); Host: Incoming calls cannot be disabled while Online
- **63 About (Abid, DRAFT)**: Default: Company name and emails are placeholders. Grievance Officer contact required by Indian IT rules; Update-Available: Opens the store; force updates use 64
- **65 Help Center (Abid, DRAFT)**: Default: CMS articles (Hindi/English). Contact Support form (66) and My Tickets (67) are Q3: button opens the support link for now
- **68 Legal Viewer (Abid, DRAFT)**: Default: One viewer for Terms, Privacy, Community Guidelines, Host Terms, Refund Policy. Copy is placeholder legal text; Blocking-Unchecked: Version bump: cannot be bypassed by relaunch; acceptance is logged
- **64 System States (Abid, DRAFT)**: No-Internet: Unsent input is kept (PRD §7.12); Maintenance: Message and ETA from remote config; Force-Update: Blocking (min_supported_version); Soft-Update-Sheet: Dismissible; shown again after 3 days; Region-Unavailable: Optional state; Offline-Banner: Transient loss: non-blocking top banner on any screen
- **31 Transaction History (Abid, DRAFT)**: All: Mail icon = export receipts to email. Paginated; Purchases: Purchases tab is optional at Q1 (PRD phase notes)
- **32 Host Wallet (Abid, DRAFT)**: Default: Fiat estimate 10,000 diamonds = $70.00 (server config, OPEN #6). Earnings Analytics (50) and Levels (53) are Q3; Below-Minimum: Minimum withdrawal 5,000 diamonds (configurable); No-Payout-Method: First time: set up payout method (33)
- **33 Withdrawal Setup (Abid, DRAFT)**: Select-Method: Methods per PRD §7.9: Bank, UPI, PayPal, Local wallet; Edit-Cooldown: Changing details resets bank verification; 7-day cooldown before withdrawal
- **51 KYC Status (Abid, DRAFT)**: Not-Started: Identity (PAN / Tax ID) → Bank / UPI → Review. Data masked; Manual-Review: Max 3 automatic retries, then manual review
- **34 Withdrawal Confirm (Abid, DRAFT)**: Default: Fee and fiat estimate are placeholders. Unreachable unless KYC Verified, even by deep link
- **34.1 Withdrawal Re-auth (Abid, DRAFT)**: OTP-Empty: OTP or biometric re-auth before payout (PRD §7.9); Requested: Status: Pending → Processing → Completed (or Failed with diamonds refunded)
- **35 Withdrawal History (Abid, DRAFT)**: Default: Documents tab (statements, TDS) arrives in Q3; Detail-Failed: Failed payouts refund diamonds
- **42 Account Deletion (Abid, DRAFT)**: Default: 14-day grace; login during grace offers 03A restore; Pending-Payout: Pending payouts must be withdrawn first [recommended in PRD]
- **56 Account Restricted (Abid, DRAFT)**: Suspended-Temporary: No other screen reachable. Appeal form + tracker arrive in Q3; Suspended-Host: Host earnings held during review; Banned-Permanent: Wallet on permanent ban is OPEN #25
- **57 Strike Notice (Abid, DRAFT)**: Warning: Shown after the call or on next app open; must be acknowledged. Consequence copy is a placeholder; Strike-2-Thumbnail: Blurred thumbnail of flagged content, if any
- **59 Safety Center (Abid, DRAFT)**: Default: Reachable within 2 taps from calls (19 shield) and Settings. CMS content, Hindi/English; Scrolled-Emergency: Helplines by account country; does not replace local authorities

## Questions for the Project owner

**From the brief**
1. 06: is the profile photo required? (Drawn as optional.)
2. 07: should the single Video card come preselected? Both variants drawn (`07_..._Unselected`, `07_..._Preselected-Variant`).
3. 05: select-then-Continue vs tap-to-go; is "You can change this later." correct for Launch?
4. 11A static variant: unlock the checkbox when the user scrolls to the end? (Drawn that way.)
5. 26: max length of the intro audio and the greeting. Greeting drawn with 120 characters as a placeholder.
6. 02: final blocked-number copy (open item D8 / tasks.md T-11). Placeholder copy used, not final.
7. Confirm every line marked *(proposed copy)* in the brief.

**Assumptions made because `00-shared-rules-and-navigation-map.md` was not available**
8. All layout constants (TopBar, back button, bottom action area, sheet, dialog, banner, toast, host bottom bar) are PROPOSED in `LAYOUT-CONSTANTS.md`. Please approve or send the shared file.
9. TopBar and BottomNavigation are owned by Girish; they are drawn here as placeholders to be swapped for his components.
10. Host bottom bar labels/icons: Dashboard (layout-dashboard), Messages (message-circle), Calls (phone), Wallet (wallet), Profile (user). Short labels to fit 78 px tabs.
11. ListRow/MenuRow and StatusPill (Abid), Diamond glyph (Girish) are placeholders. The Diamond is drawn with Lucide `gem`.

**Design decisions to confirm**
12. Secondary button = white fill, 1 px #E2E7EF border, Blue label. Ghost = no fill, Blue label. Pressed = Blue darkened ~10% (#5270E1), per design.md "darken 8–12%".
13. Checkbox radius 8 (nearest token). Switch 52×32, master switch 64×36.
14. Country flags are image assets (India flag in real colours; other countries shown as placeholders). This is content imagery, not UI colour.
15. Plus Jakarta Sans has no Devanagari. Hindi frames use Noto Sans Devanagari / Kohinoor Devanagari as fallback. Final Hindi font pairing needed.
16. Illustrations are simple placeholders (brand shapes + Lucide icons) for 03A, 06.1, 10, 11, 12. Final illustrations needed.
17. 24 online caption "You can receive calls now." and on-call caption "You're in a call right now." are new proposed copy.
18. 08: recording state shows a ghost "Cancel"; back is hidden while recording and uploading.
19. 25 call detail: commission shown as 30% (PRD default, OPEN #6).
20. 26 "Switch to User view" and "Account settings" use MenuRow; 26 Save button appears 16 px above the bottom bar only when something changed.
21. Error/offline banners sit 16 px under the top bar (or status bar) and push content down; offline disables the primary action.

**Visual restyle (reference images from Imtiyaz) to confirm**
22. New logo: coral + blue smiling speech bubbles with a translucent overlap and two sparks.
23. Hero illustrations (boy/girl characters, phones, shield, clock, calendar) use two illustration-only colours not in design.md: skin #F8C4A2 / #EDAA86 and hair #3A2A2B. Approve or add an illustration palette.
24. New component: step progress bar in the top bar (02–09A). Not in design.md; needs owner approval.
25. 01: language pill (globe + "English") replaces the bare `languages` icon; headline "Talk to someone who gets you." + description replace the single tagline; legal line moved below the CTA (brief puts it above). Same for 02.
26. 02 and 03: hero illustration replaces the 56 px logo + tagline from the brief.
27. 04: list cards with radio (Female, Male) replace the side-by-side cards. The reference also shows "Prefer not to say"; NOT added, because the PRD needs a binary, permanent gender for the role flow. Confirm.
28. 05: crown icon for host role (brief says badge-check). Onboarding CTAs carry a → arrow.

**Girish screens (00–38): assumptions to confirm**
29. D-COLOUR: there is no status colour token for Busy. Busy uses Coral; Online uses Success; Offline uses Tertiary text.
30. All prices are placeholders: call rates (30–80 diamonds/min), 22 micro-bundles (50 / 120 / 300 for $0.49 / $0.99 / $1.99), 23 host commission 30%.
31. 16: the sticky bar has three CTAs (Message + Voice + Video). This conflicts with "one primary button per screen" (PRD §16.3).
32. 38: who sees the moderation overlay (the user, the host, or both)? Copy is softened; a confirmed violation shows 57 afterwards.
33. 00.1: Log Out should open a confirm dialog first. The dialog is not drawn; the prototype goes straight to 01.
34. Prototype-only navigation (not product behaviour): 15 has no "match found" frame, so the radar runs Searching → Still looking → No hosts. 19 is drawn from the user side; an accepted incoming call (18) also lands on 19. On 24, going online auto-plays an incoming call (18) after 5 s.
35. The Girish and Abid briefs are now saved in `docs/design_tasks/`. The DRAFT screens have the new theme but have NOT yet been compared line by line with them.

**New theme (11 Oct), matching `design/_refs/` (Home is the master)**
51. Translucency: frosted cards, blurred background blobs and glows use White, Cream, Blue and Coral tokens at less than 100% opacity, plus gradients of those tokens. design.md says "no new tints". Imtiyaz will discuss this with Rahul.
52. Photos: hosts and callers use real placeholder photos cropped from the refs. They are hosted on the prototype deploy (`https://frndu-prototype.vercel.app/img/`; source in `design/_assets/photos/`). The refs only contain two women and one man, so the 6 demo hosts reuse those two faces (some mirrored). Onboarding heroes stay illustrated.
53. 13 Home: a horizontal host carousel (the next card peeks) and an "All hosts" grid further down, as in the ref. The brief asks for a two-column grid only. The card shows ★ rating and one rate (video, or voice if video is off) plus a chevron. The brief asks for both rates; both are shown on 16.
54. 06A Live Photo for normal users is new behaviour (the PRD only has the host liveness check, 08). It is placed after 06 and can be skipped ("Skip for now"). Should it block progress? Is it a photo or a short liveness video?
55. 18 Incoming Call (host side) follows `Priya’s Incoming Video Call.png`: a full-bleed caller photo with Message, Decline, Accept and Audio Only (video calls only). The brief has a swipe-to-accept track and Decline only. Message and Audio Only are new behaviour and need confirmation.
56. 19 Video Call follows `Glossy Video Call with Priya.png`: name, duration and ticker top-left, Rohan in the PiP, and five controls (Mute, Stop Video, End Call, Chat, Flip) in a frosted dark panel. The brief says "no bar behind them". The ref’s “End-to-end encrypted”, add-friend, reactions and floating comments are NOT added (not in the PRD).
57. 17 and 20 use the Cream themed canvas (`Pastel Calling Screen for Priya.png`, `Frndu Secure Call with Priya.png`). The 17 brief asks for a blurred photo with a Navy scrim; 20 asks for two avatars side by side. 20 has the Frndu mark and a -40/min ticker in place of the ref’s “Secure Call” pill. The ref’s Video and Chat buttons are not added (the brief says no Request Video).
58. 16: the followers count is removed from the stats card (rating + talk time only).

**DRAFT screens (27, 28, 30, 39, 48 and all Abid screens): built without the Girish/Abid brief files**
36. Layout, states and copy come from PRD §5, §7.8–7.12, §8.4–8.8 and §10.2. For 27, 28, 30, 39 and 48 the state lists and most copy were recovered from earlier unsourced frames. Recheck every DRAFT screen against the briefs once they are saved.
37. Q1 scope only. Menu rows link only to Q1 screens. Not shown: Favorites (43), My Reports (58), Earn with Us (36/37), Earnings Analytics (50), Levels (53), the Contact Support form (66) and My Tickets (67). Support actions open a support link for now.
38. 27: the Requests tab is on the host side only. Users see their pending first message inside 28 ("Waiting for Priya to accept").
39. 28: the price after the free quota ("3 diamonds") is a placeholder (PRD: ₹0.30 or the diamond equivalent; OPEN #2 says 3 vs 10 free messages). Attachments are hidden at Launch.
40. 30: bundles and ₹ prices come from the PRD table and are placeholders (OPEN #4). VIP ribbon on the 3,000 bundle. The first-recharge ribbon and promo field are Q3.
41. 39 success has no "Track this report" link, because 58 is Q3.
42. 40: added a Theme row (System / Light / Dark). Dark mode is open decision D5. Remove the row if dark mode is cut.
43. 40.1 Edit Profile is a new ID for the edit form behind "Edit profile". Nickname rule shown as "3 to 20 letters, numbers or underscores" (proposed).
44. 32: fiat estimate (10,000 diamonds = $70.00), minimum withdrawal 5,000 diamonds, 30% commission and the $1.00 platform fee on 34 are placeholders (OPEN #6).
45. 34.1 is a new ID for the OTP / biometric re-auth sheet before a payout.
46. 56: the appeal form and tracker are Q3, so the Q1 screen offers Contact Support, Community Guidelines and Log Out.
47. 57: consequence copy per strike ("shown less in search for 3 / 7 days") is a placeholder; the ladder and expiry follow §8.6 (OPEN #24).
48. 59: helplines 112 / 1930 must be verified by Legal before launch (PRD says so). The emergency dialog is proposed.
49. 63: company name, Grievance Officer and support emails are placeholders.
50. 68: legal text is placeholder copy, not real terms.
