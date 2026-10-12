# Frndu Layout Constants — PROPOSED

Status: **PROPOSED** (stands in for the missing `00-shared-rules-and-navigation-map.md`; awaiting Project owner approval). `docs/design.md` (origin/dev) wins on any conflict. All coordinates are for the 390 × 844 master frame. Every frame reuses these numbers exactly; no 1–2 px nudging.

Toolchain verified: `xmllint` (libxml 20913) and `rsvg-convert` 2.62.3 are installed.

## 1. Frame & grid
| Item | Value |
|---|---|
| Frame | 390 × 844, `viewBox="0 0 390 844"` |
| Side margin | 24 → content x = 24..366, content width 342 |
| Spacing | 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 80 only |
| Radii | 8, 12, 16, 20, 24, 999 (+ OTP 14, bubble 18) |

## 2. Safe areas
| Zone | Y range | Notes |
|---|---|---|
| Status bar | 0–47 | Clock "9:41" text x=40 baseline y=32, 15/600 Navy. Signal/wifi/battery group as in §9 (x 290–359, y 15–30) |
| Home indicator | 810–844 | Bar `rect x=128 y=826 w=134 h=5 rx=2.5 fill=#10233F` |

## 3. Top bar (TopBar, y 47–103, height 56)
| Element | Coordinates |
|---|---|
| Bar | y=47..103, transparent on cream (no fill, no divider) |
| Back button (T1/T3) | touch target `rect x=12 y=51 w=48 h=48`; Lucide `chevron-left` 24 at `translate(24 63)` (icon box 24..48 × 63..87), stroke Navy #10233F, width 2 |
| Close (X) button | Same touch target and icon box as back; Lucide `x` 24 |
| Title (T1 with title) | H4 18/700 Navy, centred: `x=195 text-anchor=middle`, baseline y=81 (vertical centre 75) |
| Tab-root title (T2) | H2 26/700 Navy, `x=24`, baseline y=86, left-aligned |
| T2 avatar header (24) | Avatar 40 at x=24, y=55 (circle cx=44 cy=75 r=20); greeting H4 at x=72 baseline y=81 |
| Right action slot | touch target `rect x=330 y=51 w=48 h=48`; icon 24 at `translate(342 63)` (icon right edge = 366 = margin) |
| No top bar | Content starts at y=47 + stated gap |
| Content start | y=103 (first gap from brief is added to this) |

Bar types: T1 Standard (back, optional title), T2 Tab root (title or avatar left, right slot), T3 Media (back/close at same spot, may overlay), T4 Sheet (grab handle, no back).

## 4. Bottom action area (no bottom bar)
| Element | Coordinates |
|---|---|
| Primary button | `rect x=24 y=738 w=342 h=56 rx=16`; label Button 16/700 centred x=195 baseline y=772 |
| Gap button → home-indicator area | 16 (794 → 810) |
| 2nd button (stacked, 12 gap) | Primary moves up: primary y=670, second y=738 |
| 3rd element (stacked, 12 gap) | primary y=602, 2nd y=670, 3rd y=738 (text-link rows use a 44 high touch row, centred baseline +27) |
| Legal / notice line above top button | 12 gap above top button. 1 line: baseline = buttonY − 12 − 5 (e.g. 721 for y=738). 2 lines: baselines buttonY − 36 and buttonY − 17 (e.g. 702 / 721) |
| Keyboard open | Button sits 16 above keyboard top |
| Scroll content | Ends ≥24 above the topmost element of the action area |
| Loading | Spinner 20 white (stroke 2.4) centred in the button, label hidden; same size |
| Disabled | fill #D8DDE5, text #FFFFFF |

## 5. Host bottom bar (BottomNavigation, screens 24, 27, 25, 32, 26)
| Element | Coordinates |
|---|---|
| Bar | `rect x=0 y=754 w=390 h=90` White, top border 1 px #EEF1F5 at y=754; tab row y=754..810, home indicator inside 810–844 |
| Tabs | 5 equal columns of 78: centres x = 39, 117, 195, 273, 351 |
| Icon | Lucide 24 at `translate(cx−12 762)` |
| Label | 12/600, centred at cx, baseline y=800 |
| Active | icon + label #5B7CFA; inactive #8794A5 |
| Scroll content | Ends 24 above bar (y ≤ 730) |
| Primary button above bar (26 Save) | `rect x=24 y=682 w=342 h=56` (16 above bar) |

| Tab | Screen | Label | Lucide icon |
|---|---|---|---|
| 1 | 24 Host Dashboard | Dashboard | `layout-dashboard` |
| 2 | 27 Messages | Messages | `message-circle` |
| 3 | 25 Call History | Calls | `phone` |
| 4 | 32 Host Wallet | Wallet | `wallet` |
| 5 | 26 Profile & Rates | Profile | `user` |

Derived from PRD "Host bottom bar: Host Dashboard · Messages/Chat · Call History · Host Wallet & Payout · Host Profile". Short labels are PROPOSED to fit 78 px (Hindi check required).

## 6. Bottom sheet (BottomSheet)
| Element | Value |
|---|---|
| Scrim | full frame, `#10233F` opacity 0.4 |
| Sheet | White, x=0, w=390, top corners radius 24 (bottom square, extends to 844) |
| Grab handle | `rect x=175 w=40 h=4 rx=2 fill=#E2E7EF`, 8 below sheet top |
| Content | starts 24 below sheet top; side padding 24; title H3 22/700 Navy |
| Bottom | 24 padding + 34 home-indicator safe area; primary button bottom at y=794 |
| T4 full-height sheet (12) | sheet top y=59 (12 below status bar) |
| Shadow | Large `0 12px 40px rgba(16,35,63,0.10)` |

## 7. Dialog
| Element | Value |
|---|---|
| Scrim | `#10233F` opacity 0.4 |
| Card | White, x=24, w=342, radius 24, padding 24, vertically centred on 844 |
| Title | H3 22/700 Navy; 8 gap; body Body 15 Slate |
| Buttons | 24 below body; stacked full-width (294 × 56): primary, 12, ghost |
| Scrim tap | Does not dismiss when brief says "not dismissible" (e.g. 04 confirm) |

## 8. Persistent banner (PersistentBanner) & toast
| Element | Value |
|---|---|
| Banner position | y = top bar bottom + 16 (default 119), x=24, w=342 |
| Banner | radius 12, padding 12 × 16, min height 44; icon 20 at x=40; text Notice 13 Navy at x=68 |
| Variants | Info: Blue Tint #EAF0FF + Blue icon. Warning: Coral Tint #FDE8E8 + Warning #E6A21A icon. Error: Coral Tint + Error #D9363E icon. Offline: Info with `wifi-off` |
| Toast | Navy #10233F pill-radius 16, x=24 w=342 h=48, white Body Medium; 16 above action area/bottom bar |

## 9. SVG conventions to reuse (from `design/01-splash-welcome.svg`)
Root:
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844" viewBox="0 0 390 844" font-family="'Plus Jakarta Sans', Inter, system-ui, -apple-system, sans-serif">
  <title>Frndu – {ID} {Screen} – {State} (390 x 844)</title>
  <defs>
    <style>@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;display=swap');</style>
    <clipPath id="screen"><rect width="390" height="844"/></clipPath>
  </defs>
  <g clip-path="url(#screen)">
    <rect width="390" height="844" fill="#FFF4D6"/>
    ...
  </g>
</svg>
```
Organic shapes (login direction; low contrast, cropped, never under text):
```xml
<path d="M262 -24 C344 -36 424 36 414 128 C404 210 334 204 302 162 C272 122 222 112 230 60 C236 18 240 -14 262 -24 Z" fill="#EAF0FF"/>
<path d="M-48 628 C18 600 92 650 82 724 C72 798 124 820 94 876 L-48 876 Z" fill="#E94B4B" opacity="0.12"/>
```
Status bar:
```xml
<text x="40" y="32" font-size="15" font-weight="600" fill="#10233F">9:41</text>
<g fill="#10233F">
  <rect x="290" y="24" width="3" height="6" rx="1"/>
  <rect x="295" y="21" width="3" height="9" rx="1"/>
  <rect x="300" y="18" width="3" height="12" rx="1"/>
  <rect x="305" y="15" width="3" height="15" rx="1"/>
  <path d="M314 20 a10 10 0 0 1 14 0 l-2 2 a7 7 0 0 0 -10 0 Z M318 24 a4.5 4.5 0 0 1 6 0 l-3 3 Z"/>
  <rect x="334" y="17" width="22" height="12" rx="3" fill="none" stroke="#10233F" stroke-width="1.2"/>
  <rect x="336" y="19" width="16" height="8" rx="1.5"/>
  <rect x="357.5" y="21" width="1.6" height="4" rx="0.8"/>
</g>
```
Home indicator: `<rect x="128" y="826" width="134" height="5" rx="2.5" fill="#10233F"/>`

Logo mark (two overlapping smiling chat bubbles; coral front-left, blue back-right, cream #FFF9EA cut-out stroke 12 around coral). Source geometry spans ~118..274 × 228..360 (≈156 box) in 01; reuse it via `transform="translate(..) scale(..)"` to 80 / 56 sizes rather than redrawing:
```xml
<circle cx="222" cy="302" r="50" fill="#5B7CFA"/>
<path d="M258 326 L274 360 L236 344 Z" fill="#5B7CFA" stroke="#5B7CFA" stroke-width="6" stroke-linejoin="round"/>
<circle cx="234" cy="298" r="4.5" fill="#FFFFFF"/><circle cx="256" cy="298" r="4.5" fill="#FFFFFF"/>
<path d="M230 313 Q245 326 260 313" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
<g fill="#FFF9EA" stroke="#FFF9EA" stroke-width="12" stroke-linejoin="round"><circle cx="168" cy="278" r="50"/><path d="M132 304 L118 338 L154 322 Z"/></g>
<circle cx="168" cy="278" r="50" fill="#E94B4B"/>
<path d="M132 304 L118 338 L154 322 Z" fill="#E94B4B" stroke="#E94B4B" stroke-width="6" stroke-linejoin="round"/>
<circle cx="154" cy="272" r="4.5" fill="#FFFFFF"/><circle cx="180" cy="272" r="4.5" fill="#FFFFFF"/>
<path d="M150 288 Q167 302 184 288" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
```
(On a cream #FFF4D6 canvas the cut-out stroke should use the canvas colour of the context.)

Icons: Lucide paths inline, 24 grid, `<g transform="translate(x y)" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">`. For 20 px use `scale(0.8333)` and set stroke-width 2.4 so the rendered stroke stays 2. Never filled icons.

Text: use `<text>`/`<tspan>` with explicit baselines; baseline = line top + (lineHeight − size)/2 + size×0.8 approximately (e.g. Button 16/22 in a 56 box at y → baseline y+34). Colours only from design.md tokens; never #000.

Primary button: `<rect x="24" y="738" width="342" height="56" rx="16" fill="#5B7CFA"/>` + label 16/700 #FFFFFF centred x=195 baseline 772.

Note: the old `01-splash-welcome.svg` deviates from the brief (language pill instead of 48 icon slot, headline, button at y=680). It is a style reference only; screen 01 is redrawn into `01_Splash-Welcome/` and the old file deleted then.

## 10. File naming
`design/{ID}_{Folder}/{ID}_{Screen-Name}_{State}.svg`, e.g. `02_Phone-Input/02_Phone-Input_Empty.svg`. Shared components in `00_Components/`.

## 11. Navigation map (from brief)
| From | Action → To |
|---|---|
| 01 | Get Started → 02; language icon → 01.1; Terms/Privacy → 68; auto: user session → 13, host → 24, banned → 56, deleting → 03A, new legal → 68, offline/maintenance/update/error → 64 |
| 01.1 | select → apply + close to caller (01, 40, 00.1) |
| 02 | Send code → 03; back → 01; links → 68; country → picker sheet |
| 03 | new → 04; returning → 13/24; banned → 56; deleting → 03A; under-18 → 06.1; Change number / back → 02 |
| 03A | Restore → 13/24; Continue with Deletion → 01; Contact Support → link |
| 04 | Confirm Male → 06; Female → 05 |
| 05 | Explore as User → 06; Become a Host → 07; back → 04 (locked) |
| 06 | Complete Setup → 12; under 18 → 06.1; back → 04/05; Terms → 68 |
| 06.1 | Read policy → 68; Contact Support → link; Log Out → 01 |
| 12 | Grant / Not now → 13 |
| 07 | Proceed → 08; back → 05 |
| 08 | Submit → 09A; back → 07 |
| 09A | Continue → 10 (sheet from 24/26: save + close) |
| 10 | Explore as Guest → 13; decision → 11 |
| 11 | Approved → 11A (first time) / 24; Rejected → 07; Permanent → Contact Support |
| 11A | Proceed → 24; terms → 68 |
| 24 | avatar → 00.1; quick links → 25, 32, 26; incoming → 18; bar → 24/27/25/32/26 |
| 25 | row → detail sheet; calendar → date sheet; bar |
| 26 | Save → toast; Account settings → 40; Switch to User view → 13; languages Edit → 09A sheet; photo → picker/crop |
