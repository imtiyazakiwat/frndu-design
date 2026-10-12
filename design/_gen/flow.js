// Frndu prototype flow: which hotspot (data-hit key) on which frame goes where.
// Keys: btn:<label>, link:<label>, card:<label>, chip:<label>, input:<placeholder>, switch:<name>,
// tab:<label>, back, close, scrim, otp, keyboard, country, avatar, checkbox, cover, record, ...
// Targets: a frame name, 'BACK', 'BACK_SCREEN' (leave this screen), or 'X:<screen>' for screens owned by other designers.
// Special per-frame fields: auto: [ms, target], down / up: scroll targets (mouse wheel / swipe).

const S = {
  '01': '01_Splash-Welcome', '01.1': '01.1_Language-Sheet', '02': '02_Phone-Input', '03': '03_SMS-OTP',
  '03A': '03A_Account-Restore', '04': '04_Gender', '05': '05_Role-Select', '06': '06_Basic-Profile', '06A': '06A_Live-Photo',
  '06.1': '06.1_Under-18-Blocked', '12': '12_Permissions-Primer', '07': '07_Verification-Method',
  '08': '08_Video-Verification', '09A': '09A_Host-Languages', '10': '10_Verification-Pending',
  '11': '11_Verification-Result', '11A': '11A_Host-Tutorial-Terms', '24': '24_Host-Dashboard',
  '25': '25_Host-Call-History', '26': '26_Host-Profile-Rates',
  // Girish
  '00': '00_App-Shell', '00.1': '00.1_Side-Drawer', '13': '13_Home-Feed', '13.1': '13.1_Quick-Match-Picker',
  '14': '14_Filter-Search', '15': '15_Matching-Radar', '16': '16_Host-Profile', '17': '17_Outbound-Ringing',
  '18': '18_Incoming-Call', '19': '19_Video-Call', '20': '20_Voice-Call', '22': '22_Low-Balance',
  '23': '23_Call-Ended', '38': '38_Moderation-Overlay',
  '27': '27_Chat-List', '28': '28_Chat-Conversation', '30': '30_Recharge-Store', '48': '48_Payment-Result', '39': '39_Report-Sheet',
  // Abid
  '40': '40_Profile-Settings', '40.1': '40.1_Edit-Profile', '60': '60_Notification-Preferences', '41': '41_Blocked-Users',
  '63': '63_About', '65': '65_Help-Center', '68': '68_Legal-Viewer', '64': '64_System-States', '31': '31_Transaction-History',
  '32': '32_Host-Wallet', '33': '33_Withdrawal-Setup', '51': '51_KYC-Status', '34': '34_Withdrawal-Confirm',
  '34.1': '34.1_Withdrawal-Reauth', '35': '35_Withdrawal-History', '42': '42_Account-Deletion', '56': '56_Account-Restricted',
  '57': '57_Strike-Notice', '59': '59_Safety-Center',
};
const f = (id, st) => `${S[id]}_${st}`;

// Placeholder screens (not built yet)
const EXTERNAL = {
  '66': ['Contact Support form (Q3)', 'Abid'], 'OS': ['System settings', 'OS'], 'SUPPORT': ['Support link', 'external'],
  'STORE': ['App Store / Google Play', 'OS'],
};

// Applies to every frame unless the frame overrides the key.
const GLOBAL = {
  back: 'BACK', close: 'BACK', scrim: 'BACK',
  'htab:Dashboard': f('24', 'Offline-Master-Off'), 'htab:Calls': f('25', 'Default'), 'htab:Profile': f('26', 'View'),
  'htab:Messages': f('27', 'Host-Chats'), 'htab:Earnings': f('32', 'Default'),
  'tab:Explore': f('13', 'Default'), 'tab:Messages': f('27', 'Chats'), 'tab:Wallet': f('30', 'Tab-Root'), 'tab:Profile': f('40', 'Default'),
  'pill:balance': f('30', 'Pushed'), 'pill:earnings': f('32', 'Default'),
  'link:Contact Support': 'X:SUPPORT', 'btn:Contact Support': 'X:SUPPORT',
  'btn:Open Settings': 'X:OS', 'btn:Read our policy': f('68', 'Default'),
};

const FLOW = {
  // 01 ---------------------------------------------------------------
  [f('01', 'Loading')]: { auto: [1400, f('01', 'Ready')] },
  [f('01', 'Ready')]: { 'btn:Get Started': f('02', 'Empty'), 'right:languages': f('01.1', 'English-Selected') },
  [f('01', 'Low-Power')]: { 'btn:Get Started': f('02', 'Empty'), 'right:languages': f('01.1', 'English-Selected') },
  // 01.1
  [f('01.1', 'English-Selected')]: { 'lang:हिन्दी': f('01.1', 'Pressed'), 'lang:English': 'BACK' },
  [f('01.1', 'Pressed')]: { auto: [250, f('01.1', 'Switching-Loading')] },
  [f('01.1', 'Switching-Loading')]: { auto: [700, f('01.1', 'Hindi-Selected')] },
  [f('01.1', 'Hindi-Selected')]: { 'lang:English': f('01.1', 'English-Selected'), 'lang:हिन्दी': f('01', 'Ready'), scrim: f('01', 'Ready') },
  // 02 ---------------------------------------------------------------
  [f('02', 'Empty')]: { 'input:98765 43210': f('02', 'Focused'), country: f('02', 'Country-Picker'), back: f('01', 'Ready') },
  [f('02', 'Focused')]: { 'input:98765 43210': f('02', 'Keyboard-Open'), auto: [700, f('02', 'Keyboard-Open')] },
  [f('02', 'Keyboard-Open')]: { keyboard: f('02', 'Filled-Valid'), 'input:98765 43210': f('02', 'Filled-Valid') },
  [f('02', 'Filled-Valid')]: { 'btn:Send Verification Code': f('02', 'Sending'), country: f('02', 'Country-Picker') },
  [f('02', 'Sending')]: { auto: [900, f('03', 'Empty')] },
  [f('02', 'Country-Picker')]: { 'country:*': f('02', 'Filled-Valid') },
  [f('02', 'Invalid-Number')]: { 'input:98765 43210': f('02', 'Keyboard-Open') },
  [f('02', 'Rate-Limited')]: { 'input:98765 43210': f('02', 'Keyboard-Open') },
  [f('02', 'Blocked-Number')]: { 'input:98765 43210': f('02', 'Keyboard-Open') },
  [f('02', 'Send-Failed')]: { 'btn:Send Verification Code': f('02', 'Sending') },
  [f('02', 'Offline')]: { 'input:98765 43210': f('02', 'Filled-Valid') },
  // 03 ---------------------------------------------------------------
  [f('03', 'Empty')]: { otp: f('03', 'Keyboard-Open'), 'link:Change number': f('02', 'Filled-Valid'), back: f('02', 'Filled-Valid'),
                        auto: [6000, f('03', 'Resend-Available')] },
  [f('03', 'Keyboard-Open')]: { keyboard: f('03', 'Partly-Filled'), otp: f('03', 'Partly-Filled') },
  [f('03', 'Partly-Filled')]: { otp: f('03', 'Complete'), auto: [900, f('03', 'Complete')] },
  [f('03', 'Complete')]: { 'btn:Verify': f('03', 'Verifying') },
  [f('03', 'Verifying')]: { auto: [900, f('04', 'Nothing-Selected')] },
  [f('03', 'Wrong-Code')]: { otp: f('03', 'Partly-Filled') },
  [f('03', 'Resend-Available')]: { 'link:Resend code': f('03', 'Resend-Sending'), otp: f('03', 'Keyboard-Open') },
  [f('03', 'Resend-Sending')]: { auto: [800, f('03', 'Code-Sent-Toast')] },
  [f('03', 'Code-Sent-Toast')]: { otp: f('03', 'Keyboard-Open'), auto: [1800, f('03', 'Empty')] },
  [f('03', 'Code-Expired')]: { 'link:Resend code': f('03', 'Resend-Sending') },
  [f('03', 'Offline')]: { otp: f('03', 'Keyboard-Open') },
  // 03A --------------------------------------------------------------
  [f('03A', 'Default')]: { 'btn:Restore My Account': f('03A', 'Restoring'), 'btn:Continue with Deletion': f('01', 'Ready'),
                           down: f('03A', 'Default-Scrolled') },
  [f('03A', 'Default-Scrolled')]: { 'btn:Restore My Account': f('03A', 'Restoring'), 'btn:Continue with Deletion': f('01', 'Ready'),
                                    up: f('03A', 'Default') },
  [f('03A', 'Last-Day')]: { 'btn:Restore My Account': f('03A', 'Restoring'), 'btn:Continue with Deletion': f('01', 'Ready') },
  [f('03A', 'Host-Account')]: { 'btn:Restore My Account': f('03A', 'Restoring'), 'btn:Continue with Deletion': f('01', 'Ready') },
  [f('03A', 'Restoring')]: { auto: [1000, f('13', 'Default')] },
  [f('03A', 'Error')]: { 'btn:Restore My Account': f('03A', 'Restoring') },
  // 04 ---------------------------------------------------------------
  [f('04', 'Nothing-Selected')]: { 'card:Male': f('04', 'Male-Selected'), 'card:Female': f('04', 'Female-Selected') },
  [f('04', 'Male-Selected')]: { 'card:Female': f('04', 'Female-Selected'), 'btn:Continue': f('04', 'Confirm-Male-Dialog') },
  [f('04', 'Female-Selected')]: { 'card:Male': f('04', 'Male-Selected'), 'btn:Continue': f('04', 'Confirm-Female-Dialog') },
  [f('04', 'Confirm-Male-Dialog')]: { 'btn:Confirm': f('06', 'Empty'), 'btn:Go back': 'BACK', scrim: null },
  [f('04', 'Confirm-Female-Dialog')]: { 'btn:Confirm': f('04', 'Saving'), 'btn:Go back': 'BACK', scrim: null },
  [f('04', 'Saving')]: { auto: [900, f('05', 'Nothing-Selected')] },
  [f('04', 'Locked-Re-entry')]: { 'card:Female': f('04', 'Locked-Re-entry'), 'btn:Continue': f('05', 'Nothing-Selected') },
  [f('04', 'Error')]: { 'btn:Continue': f('04', 'Confirm-Male-Dialog') },
  // 05 ---------------------------------------------------------------
  [f('05', 'Nothing-Selected')]: { 'card:Explore as User': f('05', 'User-Selected'), 'card:Become a Host & Earn': f('05', 'Host-Selected'),
                                   back: f('04', 'Locked-Re-entry') },
  [f('05', 'User-Selected')]: { 'card:Become a Host & Earn': f('05', 'Host-Selected'), 'btn:Continue': f('06', 'Empty'), back: f('04', 'Locked-Re-entry') },
  [f('05', 'Host-Selected')]: { 'card:Explore as User': f('05', 'User-Selected'), 'btn:Continue': f('05', 'Loading'), back: f('04', 'Locked-Re-entry') },
  [f('05', 'Loading')]: { auto: [900, f('07', 'Loading')] },
  [f('05', 'Error')]: { 'btn:Continue': f('05', 'Loading') },
  // 06 ---------------------------------------------------------------
  [f('06', 'Empty')]: { avatar: f('06', 'Photo-Sheet'), 'link:Add photo': f('06', 'Photo-Sheet'),
                        'input:Your nickname': f('06', 'Keyboard-Nickname'), 'input:DD / MM / YYYY': f('06', 'Date-Picker') },
  [f('06', 'Keyboard-Nickname')]: { keyboard: f('06', 'Partly-Filled'), auto: [1500, f('06', 'Partly-Filled')] },
  [f('06', 'Partly-Filled')]: { avatar: f('06', 'Photo-Sheet'), 'link:Add photo': f('06', 'Photo-Sheet'),
                                'input:DD / MM / YYYY': f('06', 'Date-Picker'), 'input:Your nickname': f('06', 'Nickname-At-Limit') },
  [f('06', 'Photo-Sheet')]: { 'photo:Take photo': f('06', 'Crop'), 'photo:Choose from gallery': f('06', 'Crop'), 'photo:Remove photo': 'BACK' },
  [f('06', 'Crop')]: { 'btn:Use photo': f('06', 'Avatar-Uploading'), close: f('06', 'Partly-Filled'), 'btn:Choose another': f('06', 'Crop') },
  [f('06', 'Avatar-Uploading')]: { auto: [1200, f('06', 'Date-Picker')] },
  [f('06', 'Date-Picker')]: { 'btn:Done': f('06', 'Ready-Top') },
  [f('06', 'Ready-Top')]: { 'btn:Complete Setup': f('06', 'Saving'), down: f('06', 'Ready'), avatar: f('06', 'Photo-Sheet'),
                            'input:DD / MM / YYYY': f('06', 'Date-Picker') },
  [f('06', 'Ready')]: { 'btn:Complete Setup': f('06', 'Saving'), up: f('06', 'Ready-Top'), 'link:Have a referral code?': f('06', 'Referral-Expanded'),
                        'chip:*': f('06', 'Languages-Limit') },
  [f('06', 'Languages-Limit')]: { 'btn:Complete Setup': f('06', 'Saving'), 'chip:*': f('06', 'Ready'), up: f('06', 'Ready-Top') },
  [f('06', 'Referral-Expanded')]: { 'input:Enter code': f('06', 'Keyboard-Referral'), 'btn:Complete Setup': f('06', 'Saving'),
                                    'link:Have a referral code?': f('06', 'Ready') },
  [f('06', 'Keyboard-Referral')]: { keyboard: f('06', 'Referral-Error') },
  [f('06', 'Referral-Error')]: { 'btn:Complete Setup': f('06', 'Saving'), 'input:Enter code': f('06', 'Keyboard-Referral') },
  [f('06', 'Saving')]: { auto: [900, f('06A', 'Intro')] },
  // 06A Live Photo (NEW, normal users; optional until the owner decides)
  [f('06A', 'Intro')]: { 'btn:Take live photo': f('06A', 'Camera'), 'btn:Skip for now': f('12', 'Default'), back: f('06', 'Ready') },
  [f('06A', 'Camera')]: { 'btn:Take photo': f('06A', 'Review'), back: f('06A', 'Intro') },
  [f('06A', 'No-Face')]: { back: f('06A', 'Intro') },
  [f('06A', 'Permission-Denied')]: { 'btn:Open Settings': 'X:OS', 'btn:Not now': f('06A', 'Intro'), scrim: null },
  [f('06A', 'Review')]: { 'btn:Use photo': f('06A', 'Uploading'), 'btn:Retake': f('06A', 'Camera'), back: f('06A', 'Camera') },
  [f('06A', 'Uploading')]: { auto: [1200, f('12', 'Default')] },
  [f('06A', 'Upload-Failed')]: { 'btn:Try again': f('06A', 'Uploading'), 'btn:Retake': f('06A', 'Camera'), back: f('06A', 'Camera') },
  [f('06', 'Date-Under-18')]: { 'btn:Complete Setup': f('06.1', 'Default') },
  [f('06', 'Avatar-Rejected')]: { 'link:Add photo': f('06', 'Photo-Sheet'), avatar: f('06', 'Photo-Sheet') },
  [f('06', 'Nickname-Error')]: { 'input:Your nickname': f('06', 'Keyboard-Nickname') },
  [f('06', 'Error')]: { 'btn:Complete Setup': f('06', 'Saving') },
  // 06.1
  [f('06.1', 'Default')]: { 'btn:Log Out': f('01', 'Ready') },
  [f('06.1', 'Long-Text')]: { 'btn:Log Out': f('01', 'Ready') },
  [f('06.1', 'Hindi')]: { 'btn:लॉग आउट': f('01', 'Ready'), 'btn:हमारी नीति पढ़ें': f('68', 'Default'), 'btn:सपोर्ट से संपर्क करें': 'X:SUPPORT' },
  // 12 ---------------------------------------------------------------
  [f('12', 'Default')]: { 'btn:Grant Permissions': f('12', 'Dialog-Camera-Off'), 'btn:Not now': f('13', 'Default'), scrim: null },
  [f('12', 'Dialog-Camera-Off')]: { 'btn:Not now': f('12', 'Dialog-Microphone-Off'), scrim: null },
  [f('12', 'Dialog-Microphone-Off')]: { 'btn:Not now': f('12', 'Dialog-Notifications-Off'), scrim: null },
  [f('12', 'Dialog-Notifications-Off')]: { 'btn:Not now': f('13', 'Default'), scrim: null },
  // 07 ---------------------------------------------------------------
  [f('07', 'Loading')]: { auto: [900, f('07', 'Unselected')] },
  [f('07', 'Unselected')]: { 'card:Video': f('07', 'Selected'), back: f('05', 'Host-Selected') },
  [f('07', 'Selected')]: { 'card:Video': f('07', 'Unselected'), 'btn:Proceed with Selected Method': f('08', 'Ready'), back: f('05', 'Host-Selected') },
  [f('07', 'Preselected-Variant')]: { 'btn:Proceed with Selected Method': f('08', 'Ready') },
  // 08 ---------------------------------------------------------------
  [f('08', 'Ready')]: { 'btn:Start': f('08', 'Recording'), back: f('07', 'Selected') },
  [f('08', 'Recording')]: { 'btn:Cancel': f('08', 'Ready'), auto: [2500, f('08', 'Review')] },
  [f('08', 'Review')]: { 'btn:Submit': f('08', 'Uploading'), 'btn:Retake': f('08', 'Ready') },
  [f('08', 'Uploading')]: { auto: [1500, f('09A', 'Prefilled')] },
  [f('08', 'Upload-Failed')]: { 'btn:Try again': f('08', 'Uploading') },
  [f('08', 'Face-Lost')]: { 'btn:Start': f('08', 'Recording') },
  [f('08', 'Permission-Denied')]: { 'btn:Not now': f('08', 'Ready') },
  // 09A --------------------------------------------------------------
  [f('09A', 'Prefilled')]: { 'btn:Continue': f('10', 'Waiting'), 'input:Search languages': f('09A', 'Searching'), 'chip:*': f('09A', 'Limit-Reached') },
  [f('09A', 'Limit-Reached')]: { 'btn:Continue': f('10', 'Waiting'), 'chip:*': f('09A', 'Prefilled') },
  [f('09A', 'None-Selected')]: { 'chip:*': f('09A', 'Prefilled') },
  [f('09A', 'Searching')]: { 'chip:Tamil': f('09A', 'Prefilled'), 'btn:Continue': f('10', 'Waiting'), 'input:Search languages': f('09A', 'No-Result') },
  [f('09A', 'No-Result')]: { 'input:Search languages': f('09A', 'Prefilled'), 'btn:Continue': f('10', 'Waiting') },
  [f('09A', 'Loading')]: { auto: [900, f('09A', 'Prefilled')] },
  [f('09A', 'Load-Failed')]: { 'btn:Try again': f('09A', 'Loading') },
  [f('09A', 'As-Sheet')]: { 'btn:Save': 'BACK', 'chip:*': f('09A', 'As-Sheet') },
  // 10 ---------------------------------------------------------------
  [f('10', 'Waiting')]: { 'btn:Explore App as Guest User': f('13', 'Guest-Verification-Pending'), auto: [3500, f('11', 'A-Approved')] },
  [f('10', 'Taking-Longer')]: { 'btn:Explore App as Guest User': f('13', 'Guest-Verification-Pending'), auto: [2500, f('11', 'A-Approved')] },
  [f('10', 'Offline')]: { 'btn:Explore App as Guest User': f('13', 'Guest-Verification-Pending') },
  // 11 ---------------------------------------------------------------
  [f('11', 'A-Approved')]: { 'btn:Launch Host Dashboard': f('11A', 'Static-Top') },
  [f('11', 'B-Rejected-Hindi')]: { 'btn:अभी फिर से आवेदन करें': f('07', 'Unselected') },
  // 11A --------------------------------------------------------------
  [f('11A', 'Static-Top')]: { down: f('11A', 'Static-End-Unchecked') },
  [f('11A', 'Static-End-Unchecked')]: { checkbox: f('11A', 'Static-End-Checked'), up: f('11A', 'Static-Top') },
  [f('11A', 'Static-End-Checked')]: { checkbox: f('11A', 'Static-End-Unchecked'), 'btn:Proceed to Dashboard': f('11A', 'Saving') },
  [f('11A', 'Video-Locked')]: { down: f('11A', 'Video-Locked-End'), auto: [2500, f('11A', 'Video-Unlocked')] },
  [f('11A', 'Video-Locked-End')]: { up: f('11A', 'Video-Locked'), auto: [2500, f('11A', 'Video-Unlocked')] },
  [f('11A', 'Video-Unlocked')]: { checkbox: f('11A', 'Video-Checked') },
  [f('11A', 'Video-Checked')]: { checkbox: f('11A', 'Video-Unlocked'), 'btn:Proceed to Dashboard': f('11A', 'Saving') },
  [f('11A', 'Terms-Updated')]: { down: f('11A', 'Static-End-Unchecked') },
  [f('11A', 'Saving')]: { auto: [900, f('24', 'Loading')] },
  [f('11A', 'Error')]: { 'btn:Proceed to Dashboard': f('11A', 'Saving') },
  // 24 ---------------------------------------------------------------
  [f('24', 'Loading')]: { auto: [1000, f('24', 'Offline-Master-Off')] },
  [f('24', 'Offline-Master-Off')]: { 'switch:master': f('24', 'Before-Online-Sheet'), 'switch:Voice Mode': f('24', 'Voice-Video-Off'),
                                    'switch:Video Mode': f('24', 'Voice-Video-Off'), 'quick:Call history': f('25', 'Default'),
                                    'quick:Profile & rates': f('26', 'View'), 'quick:Earnings': f('32', 'Default'), avatar: f('00.1', 'Open-Host'),
                                    down: f('24', 'Online-Scrolled') },
  [f('24', 'Before-Online-Sheet')]: { 'fix:Permissions': f('24', 'Before-Online-Permission-Dialog'), 'fix:Terms accepted': f('11A', 'Terms-Updated') },
  [f('24', 'Before-Online-Permission-Dialog')]: { 'btn:Open Settings': f('24', 'Online-Master-On'), 'btn:Not now': f('24', 'Offline-Master-Off') },
  [f('24', 'Online-Master-On')]: { 'switch:master': f('24', 'Offline-Master-Off'), down: f('24', 'Online-Scrolled'), avatar: f('00.1', 'Open-Host'),
                                  auto: [5000, f('18', 'Video-30s')] },
  [f('24', 'On-A-Call')]: { auto: [3000, f('24', 'Online-Master-On')] },
  [f('24', 'Online-Scrolled')]: { up: f('24', 'Online-Master-On'), 'quick:Call history': f('25', 'Default'),
                                 'quick:Profile & rates': f('26', 'View'), 'quick:Earnings': f('32', 'Default'), avatar: f('00.1', 'Open-Host') },
  [f('24', 'Voice-Video-Off')]: { 'switch:Voice Mode': f('24', 'Offline-Master-Off'), 'switch:Video Mode': f('24', 'Offline-Master-Off') },
  [f('24', 'Auto-Offline-Notice')]: { 'switch:master': f('24', 'Before-Online-Sheet') },
  [f('24', 'Connection-Offline')]: { 'switch:master': f('24', 'Before-Online-Sheet') },
  [f('24', 'Error')]: { 'btn:Try again': f('24', 'Loading') },
  // 25 ---------------------------------------------------------------
  [f('25', 'Default')]: { 'call:*': f('25', 'Call-Detail-Sheet'), 'right:calendar': f('25', 'Date-Range-Sheet'),
                          'chip:Missed': f('25', 'Filter-Missed'), 'chip:Rejected': f('25', 'Empty-Filtered'), down: f('25', 'Loading-More') },
  [f('25', 'Loading-More')]: { 'call:*': f('25', 'Call-Detail-Sheet'), up: f('25', 'Default') },
  [f('25', 'Filter-Missed')]: { 'chip:All': f('25', 'Default'), 'chip:Rejected': f('25', 'Empty-Filtered'), 'call:*': f('25', 'Call-Detail-Sheet') },
  [f('25', 'Empty-Filtered')]: { 'link:Reset filters': f('25', 'Default'), 'chip:All': f('25', 'Default'), 'chip:Missed': f('25', 'Filter-Missed') },
  [f('25', 'Empty')]: { 'link:Go to dashboard': f('24', 'Offline-Master-Off') },
  [f('25', 'Date-Range-Sheet')]: { 'btn:Apply': f('25', 'Default'), 'btn:Reset': f('25', 'Default') },
  [f('25', 'Loading')]: { auto: [1000, f('25', 'Default')] },
  [f('25', 'Error')]: { 'btn:Try again': f('25', 'Loading') },
  [f('25', 'Offline-Cached')]: { 'call:*': f('25', 'Call-Detail-Sheet') },
  // 26 ---------------------------------------------------------------
  [f('26', 'View')]: { 'input:Say hello to your callers': f('26', 'Edited'), cover: f('26', 'Cover-Uploading'), down: f('26', 'View-Scrolled'),
                       record: f('26', 'Audio-Empty') },
  [f('26', 'View-Scrolled')]: { up: f('26', 'View'), 'row:Account settings': f('40', 'Host-Account'), 'row:Switch to User view': f('13', 'Default'), 'link:Edit': f('09A', 'As-Sheet') },
  [f('26', 'Edited')]: { 'btn:Save': f('26', 'Saving'), 'htab:Dashboard': f('26', 'Unsaved-Changes-Dialog'), 'htab:Calls': f('26', 'Unsaved-Changes-Dialog'),
                         'htab:Messages': f('26', 'Unsaved-Changes-Dialog'), 'htab:Earnings': f('26', 'Unsaved-Changes-Dialog'),
                         'input:Say hello to your callers': f('26', 'Greeting-At-Limit') },
  [f('26', 'Greeting-At-Limit')]: { 'btn:Save': f('26', 'Saving') },
  [f('26', 'Unsaved-Changes-Dialog')]: { 'btn:Save': f('26', 'Saving'), 'btn:Discard': f('24', 'Offline-Master-Off'), scrim: null },
  [f('26', 'Saving')]: { auto: [900, f('26', 'Saved-Toast')] },
  [f('26', 'Saved-Toast')]: { auto: [1500, f('26', 'View')] },
  [f('26', 'Cover-Empty')]: { cover: f('26', 'Cover-Uploading'), record: f('26', 'Audio-Recording') },
  [f('26', 'Cover-Uploading')]: { auto: [1400, f('26', 'Cover-Under-Review')] },
  [f('26', 'Cover-Under-Review')]: { cover: f('26', 'Cover-Rejected') },
  [f('26', 'Cover-Rejected')]: { cover: f('26', 'Cover-Uploading') },
  [f('26', 'Audio-Empty')]: { record: f('26', 'Audio-Recording') },
  [f('26', 'Audio-Recording')]: { record: f('26', 'Audio-Recorded') },
  [f('26', 'Audio-Recorded')]: { 'btn:Save': f('26', 'Audio-Uploading') },
  [f('26', 'Audio-Uploading')]: { auto: [1400, f('26', 'Audio-Under-Review')] },
  [f('26', 'Rate-Locked')]: { up: f('26', 'View') },
  [f('26', 'Error')]: { 'btn:Save': f('26', 'Saving') },
};

// Re-apply on all six rejection frames
['Poor-Lighting', 'Script-Mismatch', 'Liveness-Failed', 'Face-Not-Visible', 'Suspected-Minor', 'Duplicate-Account']
  .forEach((r) => { FLOW[f('11', `B-Rejected-${r}`)] = { 'btn:Re-apply Now': f('07', 'Unselected') }; });

// ======================= Girish: 00, 00.1, 13–23, 38 =======================
const put = (id, states, map) => states.forEach((st) => { FLOW[f(id, st)] = Object.assign({}, FLOW[f(id, st)] || {}, map); });

// 00 App Shell: tab roots show the real screen; tabs use GLOBAL (real screens). Content hotspots are copied below.
put('00', ['Keyboard-Bar-Hidden'], { keyboard: f('00', 'User-Tab-Messages'), 'input:Hello': f('00', 'User-Tab-Messages') });

// 00.1 Side Drawer (row targets from the drawer menu spec)
const drawerCommon = {
  'row:Profile & Settings': f('40', 'Default'), 'row:Notifications': f('60', 'Default'), 'row:Language': f('01.1', 'English-Selected'), 'row:Safety Center': f('59', 'Default'),
  'row:Help Center': f('65', 'Default'), 'row:About Frndu': f('63', 'Default'), 'row:Log Out': f('01', 'Ready'),
  avatar: f('40', 'Default'), 'link:Edit profile': f('40', 'Default'), copy: f('00.1', 'ID-Copied'), scrim: f('00.1', 'Closing'), sheet: null,
};
const drawerUser = Object.assign({}, drawerCommon, { 'row:Recharge Diamonds': f('30', 'Pushed'), 'row:Transaction History': f('31', 'All'), 'row:Blocked Users': f('41', 'Default') });
put('00.1', ['Open-User', 'Open-Scrolled', 'Row-Pressed', 'ID-Copied', 'Long-Nickname', 'Approved-Host-User-Drawer', 'Hindi-Labels'], drawerUser);
put('00.1', ['Approved-Host-User-Drawer'], { 'row:Switch to Host mode': f('24', 'Offline-Master-Off') });
put('00.1', ['Open-Host'], Object.assign({}, drawerCommon, { scrim: f('24', 'Offline-Master-Off'), 'row:Switch to User view': f('13', 'Default'),
  'row:Earnings': f('32', 'Default'), 'row:Call History': f('25', 'Default') }));
put('00.1', ['Opening'], { auto: [350, f('00.1', 'Open-User')] });
put('00.1', ['Closing'], { auto: [300, f('13', 'Default')] });
put('00.1', ['Open-User'], { down: f('00.1', 'Open-Scrolled') });
put('00.1', ['Open-Scrolled'], { up: f('00.1', 'Open-User') });
put('00.1', ['ID-Copied'], { auto: [1500, f('00.1', 'Open-User')] });
put('00.1', ['Row-Pressed'], { auto: [300, f('30', 'Pushed')] });

// 13 Home Feed
const home = {
  avatar: f('00.1', 'Opening'), search: f('14', 'Default'), filters: f('14', 'Default'), banner: f('16', 'Loading'),
  'host:*': f('16', 'Loading'), 'btn:Quick Match': f('13.1', 'Video-Selected'),
  'chip:Video Hosts': f('13', 'Filters-Active'), 'chip:Popular': f('13', 'Default'), 'chip:*': f('13', 'Default'),
};
put('13', ['Default', 'Scrolled', 'Filters-Active', 'Load-More', 'Pull-To-Refresh', 'Empty', 'Offline-Cached', 'Guest-Verification-Pending',
  'Balance-Zero', 'Balance-Five-Digit', 'Long-Name-Missing-Photo', 'Without-Nearby', 'Busy-Status-Change'], home);
put('13', ['Loading'], { auto: [1000, f('13', 'Default')], avatar: f('00.1', 'Opening') });
put('13', ['Default'], { down: f('13', 'Scrolled') });
put('13', ['Scrolled'], { up: f('13', 'Default'), down: f('13', 'Load-More') });
put('13', ['Load-More'], { up: f('13', 'Scrolled'), auto: [1200, f('13', 'Scrolled')] });
put('13', ['Pull-To-Refresh'], { auto: [1000, f('13', 'Default')] });

// 13.1 Quick Match Picker
put('13.1', ['Video-Selected', 'Voice-Selected', 'Balance-Too-Low', 'Few-Hosts-Online', 'Loading-Prices', 'Offline'],
  { 'mode:video': f('13.1', 'Video-Selected'), 'mode:voice': f('13.1', 'Voice-Selected'), scrim: f('13', 'Default'), sheet: null,
    'switch:languages': null, 'btn:Recharge to continue': f('30', 'Pushed') });
put('13.1', ['Video-Selected'], { 'btn:Start Matching': f('15', 'Searching') });
put('13.1', ['Voice-Selected', 'Few-Hosts-Online'], { 'btn:Start Matching': f('15', 'Searching-Voice') });
put('13.1', ['Loading-Prices'], { auto: [900, f('13.1', 'Video-Selected')] });

// 14 Filter & Search
const filt = { close: f('13', 'Default'), scrim: f('13', 'Default'), sheet: null, 'input:Search by name or Host ID': f('14', 'Searching'),
  'mode:*': f('14', 'Filters-Changed'), 'chip:*': f('14', 'Filters-Changed'), 'slider:price': f('14', 'Filters-Changed'),
  'link:Show all': null, 'recent:*': f('14', 'Searching'), 'remove:*': null,
  'btn:Apply Filters': f('13', 'Filters-Active'), 'btn:Reset Filters': f('14', 'Nothing-Selected'), 'host:*': f('16', 'Loading') };
put('14', ['Default', 'Filters-Changed', 'Nothing-Selected', 'Searching', 'Results', 'No-Results', 'Offline', 'Error'], filt);
put('14', ['Searching'], { auto: [900, f('14', 'Results')] });
put('14', ['No-Results'], { 'input:Search by name or Host ID': f('14', 'Default') });
put('14', ['Offline', 'Error'], { 'btn:Try again': f('14', 'Default') });

// 15 Matching Radar (match-found → call is a prototype assumption; see README)
put('15', ['Searching', 'Searching-Voice', 'Still-Looking', 'Reduced-Motion', 'Offline'], { 'btn:Cancel Match': f('15', 'Cancelled') });
put('15', ['Searching', 'Searching-Voice', 'Reduced-Motion'], { auto: [3000, f('15', 'Still-Looking')] });
put('15', ['Still-Looking'], { auto: [3000, f('15', 'No-Hosts-Available')] });
put('15', ['Cancelled'], { auto: [700, f('13', 'Default')] });
put('15', ['No-Hosts-Available'], { 'btn:Try again': f('15', 'Searching'), 'btn:Back to home': f('13', 'Default') });

// 16 Host Public Profile
const hp = { back: f('13', 'Default'), 'right:more': f('16', 'Overflow-Sheet'), 'right2:heart': f('16', 'Favorite-On'),
  'btn:Message': f('28', 'Default'), 'btn:Voice': f('17', 'Ringing-Voice'), 'btn:Video': f('17', 'Ringing-Video'),
  'link:Read more': f('16', 'Long-Bio'), 'link:Show more': null, 'btn:Play intro': null, 'chip:*': null };
put('16', ['Default', 'Scrolled-Pricing', 'Scrolled-Reviews', 'Long-Bio', 'No-Reviews', 'Missing-Photos', 'Favorite-On', 'Host-Busy',
  'Host-Offline', 'Video-Mode-Off', 'Chat-Off-Toast', 'Low-Balance-Toast', 'Offline', 'Error', 'Loading'], hp);
put('16', ['Loading'], { auto: [900, f('16', 'Default')] });
put('16', ['Default'], { down: f('16', 'Scrolled-Pricing') });
put('16', ['Scrolled-Pricing'], { up: f('16', 'Default'), down: f('16', 'Scrolled-Reviews') });
put('16', ['Scrolled-Reviews'], { up: f('16', 'Scrolled-Pricing') });
put('16', ['Favorite-On'], { 'right2:heart': f('16', 'Default') });
put('16', ['Chat-Off-Toast'], { auto: [1800, f('16', 'Default')] });
put('16', ['Low-Balance-Toast'], { auto: [1500, f('30', 'Pushed')] });
put('16', ['Overflow-Sheet'], { scrim: f('16', 'Default'), sheet: null, 'row:Report': f('39', 'No-Reason'), 'row:Block': f('39', 'No-Reason') });
put('16', ['Error'], { 'btn:Try again': f('16', 'Loading') });

// 17 Outbound Ringing
put('17', ['Ringing-Video', 'Ringing-Voice', 'Connecting', 'Host-Busy'], { 'btn:Cancel': f('16', 'Default'), 'btn:Mute': null, 'btn:Speaker': null });
put('17', ['Ringing-Video'], { auto: [2500, f('17', 'Connecting')] });
put('17', ['Ringing-Voice'], { auto: [2500, f('20', 'Connected')] });
put('17', ['Connecting'], { auto: [900, f('19', 'Connected')] });
put('17', ['Host-Unavailable', 'Connection-Dropped', 'Offline'], { 'btn:Back to profile': f('16', 'Default') });

// 18 Incoming Call (host side)
put('18', ['Video-30s', 'Voice-30s', 'Countdown-10s', 'Countdown-3s', 'Camera-Permission-Missing'],
  { 'btn:Accept': f('18', 'Accepting'), 'btn:Decline': f('24', 'Online-Master-On') });
put('18', ['Voice-30s'], { 'btn:Accept': f('20', 'Connected') });
put('18', ['Video-30s'], { auto: [4000, f('18', 'Countdown-10s')] });
put('18', ['Countdown-10s'], { auto: [3000, f('18', 'Countdown-3s')] });
put('18', ['Countdown-3s'], { auto: [2000, f('18', 'Auto-Declined')] });
put('18', ['Accepting'], { auto: [800, f('19', 'Connected')] });
put('18', ['Auto-Declined'], { 'btn:Back to dashboard': f('24', 'Online-Master-On') });
put('18', ['Camera-Permission-Missing'], { 'btn:Not now': f('18', 'Video-30s'), scrim: null, dialog: null });

// 19 Video Call
const vc = { 'btn:Mute': f('19', 'Muted'), 'btn:Video': f('19', 'Camera-Off'), 'btn:Chat': f('19', 'Chat-Drawer'), 'btn:Flip camera': null,
  'right:shield': f('19', 'Shield-Sheet'), 'btn:End Call': f('23', 'User-Rate'), 'banner:low': f('22', 'Sheet-Open') };
put('19', ['Connected', 'Muted', 'Camera-Off', 'Remote-Camera-Off', 'Low-Balance-Banner', 'Zero-Balance-Countdown', 'Weak-Connection',
  'Reconnecting', 'Screen-Recording-Warning', 'Shield-Sheet', 'Chat-Drawer'], vc);
put('19', ['Muted'], { 'btn:Mute': f('19', 'Connected') });
put('19', ['Camera-Off'], { 'btn:Video': f('19', 'Connected') });
put('19', ['Zero-Balance-Countdown'], { 'banner:low': f('22', 'Grace-Countdown') });
put('19', ['Screen-Recording-Warning'], { 'banner:low': null });
put('19', ['Weak-Connection'], { 'btn:Switch to audio': f('20', 'Connected'), 'btn:Keep video': f('19', 'Connected') });
put('19', ['Reconnecting'], { auto: [2500, f('19', 'Connected')] });
put('19', ['Shield-Sheet'], { scrim: f('19', 'Connected'), sheet: null, 'row:Report or block': f('39', 'No-Reason'), 'row:Safety tips': f('59', 'Default') });
put('19', ['Chat-Drawer'], { scrim: f('19', 'Connected'), close: f('19', 'Connected'), sheet: null, 'input:Type a message': null });

// 20 Voice Call
const vo = { 'btn:Mute': f('20', 'Muted'), 'btn:Speaker': f('20', 'Speaker-On'), 'btn:End Call': f('23', 'User-Rate'), 'banner:low': f('22', 'Voice-Call-Sheet') };
put('20', ['Connected', 'Muted', 'Speaker-On', 'Bluetooth-Connected', 'Low-Balance-Banner', 'Zero-Balance-Countdown', 'Reconnecting',
  'Host-Muted', 'Reduced-Motion'], vo);
put('20', ['Muted'], { 'btn:Mute': f('20', 'Connected') });
put('20', ['Speaker-On'], { 'btn:Speaker': f('20', 'Connected') });
put('20', ['Reconnecting'], { auto: [2500, f('20', 'Connected')] });

// 22 Low Balance Drawer
put('22', ['Banner-Only', 'Sheet-Open', 'Purchasing', 'Success-Toast', 'Failed', 'Grace-Countdown'],
  { 'btn:End Call': f('23', 'User-Rate'), 'btn:Mute': null, 'btn:Flip camera': null, 'btn:Video': null, 'btn:Chat': null, 'right:shield': null });
put('22', ['Banner-Only'], { 'banner:low': f('22', 'Sheet-Open') });
put('22', ['Sheet-Open', 'Failed', 'Grace-Countdown'], { 'bundle:*': f('22', 'Purchasing'), 'link:See all bundles': f('30', 'Pushed'),
  scrim: f('22', 'Banner-Only'), sheet: null, 'banner:low': null });
put('22', ['Purchasing'], { auto: [1200, f('22', 'Success-Toast')], scrim: null, sheet: null, 'bundle:*': null, 'link:See all bundles': null });
put('22', ['Success-Toast'], { auto: [1500, f('19', 'Connected')] });
put('22', ['Voice-Call-Sheet'], { 'bundle:*': f('20', 'Connected'), 'link:See all bundles': f('30', 'Pushed'), scrim: f('20', 'Low-Balance-Banner'),
  sheet: null, 'btn:End Call': f('23', 'User-Rate'), 'btn:Mute': null, 'btn:Speaker': null, 'banner:low': null });

// 23 Call Ended
const ce = { 'right:x': f('13', 'Default'), 'star:1': f('23', 'Low-Rating-Prompt'), 'star:2': f('23', 'Low-Rating-Prompt'), 'star:*': f('23', 'User-Rated'),
  'chip:*': f('23', 'User-Rated'), 'toggle:*': f('23', 'User-Rated'), 'input:Add a comment (optional)': null,
  'btn:Submit': f('23', 'Submitting'), 'btn:Skip': f('13', 'Default'), 'link:Report': f('39', 'No-Reason') };
put('23', ['User-Rate', 'User-Rated', 'Low-Rating-Prompt', 'Error', 'Offline-Queued', 'Submitting'], ce);
put('23', ['Submitting'], { auto: [900, f('13', 'Default')] });
put('23', ['Offline-Queued'], { 'btn:Submit': f('13', 'Default') });
put('23', ['Short-Call'], { 'right:x': f('13', 'Default'), 'toggle:*': null, 'btn:Done': f('13', 'Default') });
put('23', ['Host-Summary'], { 'right:x': f('24', 'Online-Master-On'), 'btn:Done': f('24', 'Online-Master-On') });

// 38 Moderation Overlay (controls are behind the dialog)
put('38', ['First-Warning', 'Own-Camera-Flagged'], { 'btn:I understand': f('19', 'Connected'), 'btn:Mute': null, 'btn:Flip camera': null,
  'btn:Video': null, 'btn:Chat': null, 'btn:End Call': f('23', 'User-Rate') });
put('38', ['Call-Terminated'], { 'btn:OK': f('23', 'User-Rate') });

// 00 App Shell tab roots behave like the screens they show
put('00', ['User-Tab-Explore', 'Badge-0', 'Badge-1-Digit', 'Badge-2-Digits', 'Badge-99-Plus', 'Tab-Pressed'], home);
put('00', ['Host-Tab-Dashboard'], FLOW[f('24', 'Offline-Master-Off')]);
put('00', ['Host-Tab-Calls'], FLOW[f('25', 'Default')]);
put('00', ['Host-Tab-Profile'], FLOW[f('26', 'View')]);

// ======================= Girish batch 3: 27, 28, 30, 48, 39 =======================
// 27 Chat List
const userChats = ['Loading', 'Chats', 'Chats-Swipe-Actions', 'Chats-Empty', 'System-Notices', 'Notices-Empty', 'Search-Results', 'Search-No-Results', 'Long-Name', 'Offline'];
const hostChats = ['Host-Chats', 'Host-Requests', 'Requests-Empty', 'Host-Chat-Off'];
put('27', userChats, { 'seg:Chats': f('27', 'Chats'), 'seg:System Notices': f('27', 'System-Notices'), 'input:Search messages': f('27', 'Search-Results'),
  'chat:*': f('28', 'Default'), 'btn:Explore hosts': f('13', 'Default') });
put('27', hostChats, { 'seg:Chats': f('27', 'Host-Chats'), 'seg:Requests': f('27', 'Host-Requests'), 'seg:System Notices': f('27', 'System-Notices'),
  'input:Search messages': null, 'chat:*': f('28', 'Host-View'), 'banner:chat-off': f('24', 'Offline-Master-Off') });
put('27', ['Loading'], { auto: [900, f('27', 'Chats')] });
put('27', ['Chats'], { 'chat:Ananya': f('27', 'Chats-Swipe-Actions') });
put('27', ['Chats-Swipe-Actions'], { 'swipe:*': f('27', 'Chats'), 'chat:*': f('27', 'Chats') });
put('27', ['Search-Results'], { 'input:Search messages': f('27', 'Search-No-Results') });
put('27', ['Search-No-Results'], { 'input:Search messages': f('27', 'Chats') });
put('27', ['Host-Requests'], { 'accept:*': f('27', 'Host-Chats'), 'decline:*': f('27', 'Requests-Empty') });

// 28 Chat Conversation
const conv = ['Default', 'Empty-Thread', 'Keyboard-Open', 'Sending', 'Read', 'Failed', 'Typing-Indicator', 'Long-Message', 'Contact-Masked', 'Quota-Used-Up',
  'Balance-Too-Low', 'Request-Pending', 'Host-Not-Accepting', 'Overflow-Sheet', 'Mute-Sheet', 'Block-Dialog', 'Clear-Chat-Dialog', 'Blocked-User', 'Offline', 'Hindi', 'Host-View'];
put('28', conv, { back: f('27', 'Chats'), avatar: f('16', 'Default'), 'right:more': f('28', 'Overflow-Sheet'), 'right:phone': f('17', 'Ringing-Voice'),
  'right:video': f('17', 'Ringing-Video'), 'input:Type a message': f('28', 'Keyboard-Open') });
put('28', ['Host-View'], { back: f('27', 'Host-Chats'), avatar: null });
put('28', ['Keyboard-Open'], { 'btn:Send': f('28', 'Sending'), keyboard: f('28', 'Sending') });
put('28', ['Sending'], { auto: [900, f('28', 'Default')] });
put('28', ['Failed'], { retry: f('28', 'Sending') });
put('28', ['Balance-Too-Low'], { 'btn:Recharge': f('30', 'Pushed') });
put('28', ['Overflow-Sheet'], { scrim: f('28', 'Default'), sheet: null, 'row:View profile': f('16', 'Default'), 'row:Mute': f('28', 'Mute-Sheet'),
  'row:Report': f('39', 'No-Reason'), 'row:Block': f('28', 'Block-Dialog'), 'row:Clear chat': f('28', 'Clear-Chat-Dialog') });
put('28', ['Mute-Sheet'], { scrim: f('28', 'Default'), sheet: null, 'row:*': f('28', 'Default') });
put('28', ['Block-Dialog'], { 'btn:Block': f('28', 'Blocked-User'), 'btn:Cancel': f('28', 'Default'), scrim: null, dialog: null });
put('28', ['Clear-Chat-Dialog'], { 'btn:Clear chat': f('28', 'Empty-Thread'), 'btn:Cancel': f('28', 'Default'), scrim: null, dialog: null });
put('28', ['Blocked-User'], { 'link:Unblock': f('28', 'Default') });

// 30 Recharge Store
const store = ['Tab-Root', 'Pushed', 'Loading', 'Balance-Zero', 'Balance-Five-Digit', 'Negative-Balance', 'Prices-Failed', 'Purchase-Processing', 'Offline'];
put('30', store, { 'link:Purchase History': f('31', 'Purchases'), 'bundle:*': f('30', 'Purchase-Processing'), 'btn:Retry': f('30', 'Loading') });
put('30', ['Loading'], { auto: [900, f('30', 'Tab-Root')] });
put('30', ['Purchase-Processing'], { auto: [1400, f('48', 'Success-Bonus')] });

// 48 Payment Result
put('48', ['Success-Bonus', 'Success-No-Bonus', 'Success-Long-Order-ID'], { 'btn:Continue': f('13', 'Default'), 'link:View receipt': f('31', 'Receipt-Sheet') });
put('48', ['Pending'], { 'btn:Check status': f('48', 'Pending-Checking'), 'link:Back to app': f('13', 'Default') });
put('48', ['Pending-Checking'], { auto: [1600, f('48', 'Success-Bonus')], 'link:Back to app': f('13', 'Default') });
put('48', ['Failed-Declined', 'Failed-Funds', 'Failed-Store', 'Failed-Timeout'], { 'btn:Try again': f('30', 'Purchase-Processing'),
  'link:Choose another bundle': f('30', 'Tab-Root'), 'link:Contact support': 'X:SUPPORT' });
put('48', ['Compact-Success'], { 'btn:Continue call': f('19', 'Connected'), scrim: null, sheet: null });
put('48', ['Compact-Pending'], { 'btn:Back to call': f('19', 'Connected'), scrim: null, sheet: null });
put('48', ['Compact-Failed'], { 'btn:Try again': f('22', 'Sheet-Open'), 'link:Back to call': f('19', 'Connected'), scrim: null, sheet: null });
put('22', ['Purchasing'], { auto: [1200, f('48', 'Compact-Success')] });

// 39 Report Sheet
const rep = ['No-Reason', 'Reason-Selected', 'Screenshot-Uploading', 'Submitting', 'Error', 'Offline'];
put('39', rep, { close: 'BACK_SCREEN', scrim: 'BACK_SCREEN', sheet: null, 'reason:*': f('39', 'Reason-Selected'), 'add:screenshot': f('39', 'Screenshot-Uploading'),
  'input:Tell us what happened (optional)': null, 'btn:Submit Report & Block': f('39', 'Submitting') });
put('39', ['Screenshot-Uploading'], { auto: [1200, f('39', 'Reason-Selected')] });
put('39', ['Submitting'], { auto: [1000, f('39', 'Success')] });
put('39', ['Success'], { 'btn:Done': f('13', 'Default'), scrim: f('13', 'Default'), sheet: null });

// ======================= Abid =======================
// 40 Profile & Settings
const setRows = { 'row:Edit profile': f('40.1', 'Default'), 'link:Edit': f('40.1', 'Default'), 'row:Notification preferences': f('60', 'Default'),
  'row:Language': f('01.1', 'English-Selected'), 'row:Theme': f('40', 'Theme-Sheet'), 'row:Purchase history': f('31', 'All'),
  'row:Blocked users': f('41', 'Default'), 'row:Help & Support': f('65', 'Default'), 'row:Safety Center': f('59', 'Default'),
  'row:About Frndu': f('63', 'Default'), 'row:Terms of Service': f('68', 'Default'), 'row:Privacy Policy': f('68', 'Privacy-Policy'),
  'row:Log Out': f('40', 'Log-Out-Dialog'), 'row:Delete account': f('42', 'Default'), copy: f('40', 'ID-Copied') };
put('40', ['Default', 'Scrolled', 'ID-Copied', 'Offline', 'Host-Account'], setRows);
put('40', ['Default'], { down: f('40', 'Scrolled') });
put('40', ['Scrolled'], { up: f('40', 'Default') });
put('40', ['ID-Copied'], { auto: [1500, f('40', 'Default')] });
put('40', ['Host-Account'], { back: f('26', 'View-Scrolled') });
put('40', ['Theme-Sheet'], { scrim: f('40', 'Default'), sheet: null, 'theme:*': f('40', 'Default') });
put('40', ['Log-Out-Dialog'], { 'btn:Log Out': f('40', 'Logging-Out'), 'btn:Cancel': f('40', 'Scrolled'), scrim: null, dialog: null });
put('40', ['Logging-Out'], { auto: [900, f('01', 'Ready')], scrim: null, dialog: null });
put('00.1', ['Open-User', 'Open-Scrolled', 'Row-Pressed', 'ID-Copied', 'Long-Nickname', 'Approved-Host-User-Drawer', 'Hindi-Labels', 'Open-Host'],
  { 'row:Log Out': f('40', 'Log-Out-Dialog') });

// 40.1 Edit Profile
put('40.1', ['Default', 'Editing', 'Nickname-Error', 'Locked-Field-Toast', 'Saved-Toast'], { back: f('40', 'Default'), avatar: f('40.1', 'Photo-Sheet'),
  'link:Change photo': f('40.1', 'Photo-Sheet'), 'input:Your nickname': f('40.1', 'Editing'), 'locked:*': f('40.1', 'Locked-Field-Toast'), 'chip:*': f('40.1', 'Editing') });
put('40.1', ['Editing'], { 'btn:Save': f('40.1', 'Saving'), 'input:Your nickname': f('40.1', 'Nickname-Error') });
put('40.1', ['Nickname-Error'], { 'input:Your nickname': f('40.1', 'Editing') });
put('40.1', ['Locked-Field-Toast'], { auto: [1500, f('40.1', 'Default')] });
put('40.1', ['Photo-Sheet'], { scrim: f('40.1', 'Default'), sheet: null, 'row:*': f('40.1', 'Editing') });
put('40.1', ['Saving'], { auto: [900, f('40.1', 'Saved-Toast')] });
put('40.1', ['Saved-Toast'], { auto: [1500, f('40', 'Default')] });

// 60 Notification Preferences
put('60', ['Default', 'Presence-Off', 'OS-Notifications-Off', 'Host', 'Save-Failed-Toast'], { 'row:Quiet hours': f('60', 'Quiet-Hours-Sheet'),
  'switch:*': f('60', 'Default'), 'freq:*': null, 'btn:Open Settings': 'X:OS' });
put('60', ['Default'], { 'switch:Presence alerts': f('60', 'Presence-Off') });
put('60', ['Save-Failed-Toast'], { auto: [1800, f('60', 'Default')] });
put('60', ['Quiet-Hours-Sheet'], { scrim: f('60', 'Default'), sheet: null, 'btn:Save': f('60', 'Default'), 'input:*': null });

// 41 Blocked Users
put('41', ['Default', 'Unblocked-Toast'], { 'unblock:*': f('41', 'Unblock-Dialog') });
put('41', ['Unblock-Dialog'], { 'btn:Unblock': f('41', 'Unblocked-Toast'), 'btn:Cancel': f('41', 'Default'), scrim: null, dialog: null });
put('41', ['Unblocked-Toast'], { auto: [1800, f('41', 'Default')] });
put('41', ['Error'], { 'btn:Try again': f('41', 'Loading') });
put('41', ['Loading'], { auto: [900, f('41', 'Default')] });

// 63 About
const legalRows = { 'row:Terms of Service': f('68', 'Default'), 'row:Privacy Policy': f('68', 'Privacy-Policy'), 'row:Community Guidelines': f('68', 'Default'),
  'row:Refund Policy': f('68', 'Default'), 'row:Open-source licences': null, 'row:Rate Frndu': 'X:STORE', 'row:Copy diagnostic ID': f('63', 'Diagnostic-ID-Copied') };
put('63', ['Default', 'Scrolled', 'Checking-Update', 'Update-Available', 'Up-To-Date', 'Diagnostic-ID-Copied'], legalRows);
put('63', ['Default', 'Scrolled', 'Diagnostic-ID-Copied'], { 'btn:Check for update': f('63', 'Checking-Update') });
put('63', ['Default'], { down: f('63', 'Scrolled') });
put('63', ['Scrolled'], { up: f('63', 'Default') });
put('63', ['Checking-Update'], { auto: [1200, f('63', 'Up-To-Date')] });
put('63', ['Up-To-Date', 'Diagnostic-ID-Copied'], { auto: [1600, f('63', 'Default')] });
put('63', ['Update-Available'], { 'btn:Update': 'X:STORE' });

// 65 Help Center
put('65', ['Default', 'Category', 'Article-Open', 'Helpful-Thanks', 'Search-Results', 'No-Results', 'Offline-Cached'],
  { 'input:Search help articles': f('65', 'Search-Results'), 'cat:*': f('65', 'Category'), 'faq:*': f('65', 'Article-Open') });
put('65', ['Category', 'Article-Open', 'Helpful-Thanks'], { back: f('65', 'Default') });
put('65', ['Article-Open'], { 'chip:Yes': f('65', 'Helpful-Thanks'), 'chip:No': f('65', 'Category'), 'faq:How am I charged for a c': f('65', 'Category') });
put('65', ['Helpful-Thanks'], { 'chip:*': null, auto: [1800, f('65', 'Article-Open')] });
put('65', ['Search-Results'], { 'input:Search help articles': f('65', 'No-Results') });
put('65', ['No-Results'], { 'input:Search help articles': f('65', 'Default') });

// 68 Legal Viewer
put('68', ['Default', 'Scrolled', 'Large-Text', 'Hindi', 'Privacy-Policy', 'Loading', 'Offline-Cached'],
  { 'lang:English': f('68', 'Default'), 'lang:हिन्दी': f('68', 'Hindi'), 'textsize:large': f('68', 'Large-Text'), 'textsize:small': f('68', 'Default'),
    'link:Open in browser': null });
put('68', ['Default'], { down: f('68', 'Scrolled') });
put('68', ['Scrolled'], { up: f('68', 'Default') });
put('68', ['Loading'], { auto: [900, f('68', 'Default')] });
put('68', ['Blocking-Unchecked', 'Blocking-Checked'], { 'lang:English': null, 'lang:हिन्दी': null, 'textsize:large': null, 'textsize:small': null });
put('68', ['Blocking-Unchecked'], { checkbox: f('68', 'Blocking-Checked') });
put('68', ['Blocking-Checked'], { checkbox: f('68', 'Blocking-Unchecked'), 'btn:Accept & Continue': f('13', 'Default') });

// 64 System States
put('64', ['No-Internet'], { 'btn:Retry': f('64', 'Retrying'), 'btn:Open Settings': 'X:OS' });
put('64', ['Retrying'], { auto: [1200, f('13', 'Default')], 'btn:Open Settings': 'X:OS' });
put('64', ['Server-Error'], { 'btn:Retry': f('13', 'Loading'), copy: null });
put('64', ['Maintenance'], { auto: [3500, f('13', 'Default')] });
put('64', ['Force-Update'], { 'btn:Update Now': 'X:STORE' });
put('64', ['Soft-Update-Sheet'], { 'btn:Update': 'X:STORE', 'btn:Not now': f('13', 'Default'), scrim: f('13', 'Default'), sheet: null });
put('64', ['Region-Unavailable'], { 'btn:Contact Support': 'X:SUPPORT' });
put('64', ['Offline-Banner'], home);

// 31 Transaction History
put('31', ['All', 'Filtered-Recharges', 'Purchases', 'Export-Toast', 'Load-More', 'Loading', 'Empty', 'Error', 'Receipt-Sheet', 'Pending-Sheet', 'Call-Detail-Sheet'],
  { 'seg:All': f('31', 'All'), 'seg:Purchases': f('31', 'Purchases'), 'right:mail': f('31', 'Export-Toast'), 'chip:All types': f('31', 'All'),
    'chip:Recharges': f('31', 'Filtered-Recharges'), 'chip:*': f('31', 'All'), 'tx:Recharge:+550': f('31', 'Receipt-Sheet'),
    'tx:Recharge:+100': f('31', 'Pending-Sheet'), 'tx:Recharge:+1,200': f('31', 'Receipt-Sheet'), 'tx:*': f('31', 'Call-Detail-Sheet') });
put('31', ['Purchases'], { 'chip:*': f('31', 'Purchases') });
put('31', ['All'], { down: f('31', 'Load-More') });
put('31', ['Load-More'], { up: f('31', 'All'), auto: [1200, f('31', 'All')] });
put('31', ['Export-Toast'], { auto: [1600, f('31', 'All')] });
put('31', ['Loading'], { auto: [900, f('31', 'All')] });
put('31', ['Error'], { 'btn:Try again': f('31', 'Loading') });
put('31', ['Receipt-Sheet'], { scrim: f('31', 'Purchases'), close: f('31', 'Purchases'), sheet: null, 'btn:Download PDF': null, 'link:Payment issue?': 'X:SUPPORT' });
put('31', ['Pending-Sheet'], { scrim: f('31', 'Purchases'), close: f('31', 'Purchases'), sheet: null, 'btn:Check status': f('48', 'Pending-Checking') });
put('31', ['Call-Detail-Sheet'], { scrim: f('31', 'All'), close: f('31', 'All'), sheet: null });

// 32 Host Wallet
put('32', ['Default', 'Below-Minimum', 'KYC-Pending', 'KYC-Action-Needed', 'No-Payout-Method', 'Offline', 'Commission-Sheet'],
  { 'chip:KYC': f('51', 'In-Review'), 'info:commission': f('32', 'Commission-Sheet'), 'row:Withdrawal history': f('35', 'Default'),
    'row:Payout method': f('33', 'Select-Method'), 'row:KYC status': f('51', 'In-Review'), 'btn:Request Cash Out': f('34', 'Default'),
    'btn:Add payout method': f('33', 'Select-Method') });
put('32', ['Default'], { 'chip:KYC': f('51', 'Verified'), 'row:KYC status': f('51', 'Verified') });
put('32', ['KYC-Action-Needed', 'No-Payout-Method'], { 'chip:KYC': f('51', 'Rejected-Name-Mismatch'), 'row:KYC status': f('51', 'Rejected-Name-Mismatch') });
put('32', ['Commission-Sheet'], { scrim: f('32', 'Default'), sheet: null });
put('32', ['Loading'], { auto: [900, f('32', 'Default')] });

// 33 Withdrawal Setup
put('33', ['Select-Method', 'Method-Selected', 'Edit-Cooldown'], { 'card:UPI': f('33', 'Method-Selected'), 'card:*': f('33', 'Method-Selected'),
  back: f('32', 'Default') });
put('33', ['Method-Selected', 'Edit-Cooldown'], { 'btn:Continue': f('33', 'UPI-Empty') });
put('33', ['UPI-Empty'], { 'input:*': f('33', 'UPI-Filled') });
put('33', ['UPI-Filled', 'Bank-Filled'], { 'btn:Submit': f('33', 'Submitting'), 'input:PAN': f('33', 'PAN-Error'), 'input:*': null });
put('33', ['PAN-Error'], { 'input:*': f('33', 'UPI-Filled') });
put('33', ['Submitting'], { auto: [1000, f('51', 'In-Review')], 'input:*': null });

// 51 KYC Status
put('51', ['Not-Started'], { 'btn:Complete KYC': f('33', 'Select-Method') });
put('51', ['In-Review'], { auto: [3500, f('51', 'Verified')], 'link:Contact support': 'X:SUPPORT' });
put('51', ['Manual-Review'], { 'link:Contact support': 'X:SUPPORT' });
put('51', ['Rejected-Name-Mismatch', 'Rejected-Invalid-PAN'], { 'btn:Re-upload details': f('33', 'Bank-Filled'), 'link:Contact support': 'X:SUPPORT' });
put('51', ['Verified'], { 'btn:Request Cash Out': f('34', 'Default') });

// 34 Withdrawal Confirm + 34.1 re-auth
put('34', ['Default', 'Typing', 'Empty', 'Below-Minimum', 'Above-Available'], { back: f('32', 'Default'), 'input:0': f('34', 'Typing'), 'btn:Max': f('34', 'Default') });
put('34', ['Typing'], { keyboard: f('34', 'Default'), 'input:0': f('34', 'Default') });
put('34', ['Default'], { 'btn:Confirm Withdrawal': f('34.1', 'OTP-Empty') });
put('34', ['KYC-Blocked'], { 'btn:Go to KYC status': f('51', 'In-Review'), 'link:Back to wallet': f('32', 'KYC-Pending') });
const reauthBase = { 'input:0': null, 'btn:Max': null, 'btn:Confirm Withdrawal': null, back: null, scrim: f('34', 'Default'), close: f('34', 'Default'), sheet: null };
put('34.1', ['OTP-Empty', 'OTP-Filled', 'OTP-Wrong', 'Confirming', 'Biometric'], reauthBase);
put('34.1', ['OTP-Empty'], { otp: f('34.1', 'OTP-Filled') });
put('34.1', ['OTP-Filled'], { otp: f('34.1', 'OTP-Wrong'), 'btn:Confirm': f('34.1', 'Confirming') });
put('34.1', ['OTP-Wrong'], { otp: f('34.1', 'OTP-Filled'), 'btn:Confirm': f('34.1', 'Confirming') });
put('34.1', ['Confirming'], { auto: [1000, f('34.1', 'Requested')], otp: null });
put('34.1', ['Biometric'], { 'btn:Use code instead': f('34.1', 'OTP-Empty') });
put('34.1', ['Requested'], { 'btn:View withdrawal': f('35', 'Default'), 'link:Back to wallet': f('32', 'Default') });

// 35 Withdrawal History
put('35', ['Default', 'Detail-Completed', 'Detail-Failed'], { back: f('32', 'Default'), 'wd:WD-29711': f('35', 'Detail-Failed'), 'wd:*': f('35', 'Detail-Completed') });
put('35', ['Detail-Completed', 'Detail-Failed'], { scrim: f('35', 'Default'), sheet: null, 'link:Download receipt': null });
put('35', ['Loading'], { auto: [900, f('35', 'Default')] });

// 42 Account Deletion
put('42', ['Default', 'Checked', 'Pending-Payout'], { back: f('40', 'Scrolled'), 'btn:Keep my account': f('40', 'Scrolled') });
put('42', ['Default'], { checkbox: f('42', 'Checked') });
put('42', ['Checked'], { checkbox: f('42', 'Default'), 'btn:Permanently Delete Account': f('42', 'OTP-Reauth') });
put('42', ['Pending-Payout'], { checkbox: null });
put('42', ['OTP-Reauth'], { 'btn:Delete account': f('42', 'Deleting'), scrim: f('42', 'Checked'), close: f('42', 'Checked'), sheet: null, otp: null,
  checkbox: null, 'btn:Permanently Delete Account': null, 'btn:Keep my account': null, back: null });
put('42', ['Deleting'], { auto: [1000, f('42', 'Deleted')], scrim: null, close: null, sheet: null, otp: null, checkbox: null,
  'btn:Permanently Delete Account': null, 'btn:Keep my account': null, back: null });
put('42', ['Deleted'], { 'btn:OK': f('01', 'Ready') });

// 56 Account Restricted / 57 Strike Notice / 59 Safety Center
put('56', ['Suspended-Temporary', 'Suspended-Host', 'Banned-Permanent'], { 'link:Community Guidelines': f('68', 'Default'), 'link:Log Out': f('01', 'Ready') });
put('57', ['Warning', 'Strike-1', 'Strike-2-Thumbnail', 'Final-Warning'], { 'btn:I Understand': f('57', 'Acknowledging'),
  'link:Community guidelines': f('68', 'Default'), 'link:Disagree? Appeal': 'X:SUPPORT' });
put('57', ['Acknowledging'], { auto: [900, f('13', 'Default')] });
put('38', ['Call-Terminated'], { 'btn:OK': f('57', 'Strike-1') });
put('59', ['Default', 'Scrolled-Protections', 'Scrolled-Emergency'], { 'btn:Report an emergency': f('59', 'Emergency-Dialog'),
  'row:How to report someone': f('39', 'No-Reason'), 'row:Blocked users': f('41', 'Default'), 'row:Community Guidelines': f('68', 'Default') });
put('59', ['Default'], { down: f('59', 'Scrolled-Protections') });
put('59', ['Scrolled-Protections'], { up: f('59', 'Default'), down: f('59', 'Scrolled-Emergency') });
put('59', ['Scrolled-Emergency'], { up: f('59', 'Scrolled-Protections') });
put('59', ['Emergency-Dialog'], { 'btn:Call 112': 'X:OS', 'btn:Report to Frndu': 'X:SUPPORT', 'btn:Cancel': f('59', 'Default'), scrim: null, dialog: null });

// 00 App Shell tab roots that now show 27 / 30 / 40 / 32
put('00', ['User-Tab-Messages'], FLOW[f('27', 'Chats')]);
put('00', ['User-Tab-Wallet'], FLOW[f('30', 'Tab-Root')]);
put('00', ['User-Tab-Profile'], FLOW[f('40', 'Default')]);
put('00', ['Host-Tab-Messages'], FLOW[f('27', 'Host-Chats')]);
put('00', ['Host-Tab-Earnings'], FLOW[f('32', 'Default')]);
[['User-Tab-Messages', 'btn:Explore hosts'], ['User-Tab-Wallet', 'btn:Retry'], ['Host-Tab-Messages', 'banner:chat-off'],
 ['Host-Tab-Earnings', 'btn:Add payout method']].forEach(([st, k]) => { delete FLOW[f('00', st)][k]; });

// Screen-level connections for the canvas (from the brief "Goes to" rows).
const EDGES = [
  ['01', '01.1', 'Language'], ['01', '02', 'Get Started'], ['02', '03', 'Send code'], ['03', '04', 'New user'],
  ['03', '03A', 'Deleting'], ['03', '06.1', 'Under 18'], ['04', '05', 'Female'], ['04', '06', 'Male'],
  ['05', '06', 'User'], ['05', '07', 'Host'], ['06', '06A', 'Complete'], ['06A', '12', 'Photo / Skip'], ['06', '06.1', 'Under 18'],
  ['07', '08', 'Proceed'], ['08', '09A', 'Submit'], ['09A', '10', 'Continue'], ['10', '11', 'Decision'],
  ['11', '11A', 'Approved'], ['11', '07', 'Re-apply'], ['11A', '24', 'Proceed'], ['24', '25', 'Calls'],
  ['24', '26', 'Profile'], ['26', '09A', 'Edit languages'],
  // Girish
  ['12', '13', 'Done'], ['10', '13', 'Guest'], ['00', '13', 'Explore tab'], ['13', '00.1', 'Avatar'], ['24', '00.1', 'Avatar'],
  ['13', '13.1', 'Quick Match'], ['13', '14', 'Search'], ['13', '16', 'Host card'], ['13.1', '15', 'Start'], ['14', '16', 'Result'],
  ['16', '17', 'Call'], ['17', '19', 'Video'], ['17', '20', 'Voice'], ['24', '18', 'Incoming'], ['18', '19', 'Accept'],
  ['19', '22', 'Low balance'], ['19', '38', 'Flagged'], ['19', '23', 'End'], ['20', '23', 'End'], ['38', '23', 'Terminated'],
  ['27', '28', 'Open chat'], ['16', '28', 'Message'], ['28', '39', 'Report'], ['16', '39', 'Report'], ['13', '30', 'Diamonds'],
  ['30', '48', 'Purchase'], ['22', '48', 'In-call buy'], ['48', '31', 'Receipt'], ['38', '57', 'Strike'],
  ['40', '40.1', 'Edit'], ['40', '60', 'Notifications'], ['40', '41', 'Blocked'], ['40', '65', 'Help'], ['40', '59', 'Safety'],
  ['40', '63', 'About'], ['40', '42', 'Delete'], ['63', '68', 'Legal'], ['40', '31', 'Purchases'],
  ['32', '33', 'Payout method'], ['33', '51', 'Submit'], ['32', '34', 'Cash out'], ['34', '34.1', 'Confirm'], ['34.1', '35', 'Requested'],
];

// Canvas layout: rows of screens in journey order.
const LAYOUT = [
  { title: 'Launch & sign-in', screens: ['01', '01.1', '02', '03', '03A'] },
  { title: 'Profile set-up', screens: ['04', '05', '06', '06A', '06.1', '12'] },
  { title: 'Host verification', screens: ['07', '08', '09A', '10', '11', '11A'] },
  { title: 'Host daily screens', screens: ['24', '25', '26'] },
  { title: 'App shell', screens: ['00', '00.1'] },
  { title: 'Explore & match', screens: ['13', '13.1', '14', '15', '16'] },
  { title: 'Calls', screens: ['17', '18', '19', '20'] },
  { title: 'After the call & safety', screens: ['22', '23', '38', '39', '57'] },
  { title: 'Messages', screens: ['27', '28'] },
  { title: 'Diamonds & payments', screens: ['30', '48', '31'] },
  { title: 'Profile & settings', screens: ['40', '40.1', '60', '41', '42'] },
  { title: 'Help, legal & safety', screens: ['59', '65', '63', '68'] },
  { title: 'Host earnings & payouts', screens: ['32', '33', '51', '34', '34.1', '35'] },
  { title: 'System & restricted states', screens: ['64', '56'] },
];

const DEFAULT_STATE = {
  '01': 'Ready', '01.1': 'English-Selected', '02': 'Empty', '03': 'Empty', '03A': 'Default', '04': 'Nothing-Selected',
  '05': 'Nothing-Selected', '06': 'Empty', '06A': 'Intro', '06.1': 'Default', '12': 'Default', '07': 'Unselected', '08': 'Ready',
  '09A': 'Prefilled', '10': 'Waiting', '11': 'A-Approved', '11A': 'Static-Top', '24': 'Offline-Master-Off',
  '25': 'Default', '26': 'View',
  '00': 'User-Tab-Explore', '00.1': 'Open-User', '13': 'Default', '13.1': 'Video-Selected', '14': 'Default', '15': 'Searching',
  '16': 'Default', '17': 'Ringing-Video', '18': 'Video-30s', '19': 'Connected', '20': 'Connected', '22': 'Sheet-Open',
  '23': 'User-Rate', '38': 'First-Warning',
  '27': 'Chats', '28': 'Default', '30': 'Tab-Root', '48': 'Success-Bonus', '39': 'Reason-Selected',
  '40': 'Default', '40.1': 'Default', '60': 'Default', '41': 'Default', '63': 'Default', '65': 'Default', '68': 'Default',
  '64': 'No-Internet', '31': 'All', '32': 'Default', '33': 'Select-Method', '51': 'In-Review', '34': 'Default',
  '34.1': 'OTP-Filled', '35': 'Default', '42': 'Default', '56': 'Suspended-Temporary', '57': 'Strike-1', '59': 'Default',
};
const START = f('01', 'Loading');
