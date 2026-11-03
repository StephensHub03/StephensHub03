#!/usr/bin/env python3
"""Build the README hero card and its matching link badges.

Usage: python3 tools/build_hero.py

Writes:
  assets/hero-burgundy.svg        — hero card (portrait embedded as base64)
  assets/badges/<name>.svg        — clickable link badges placed under the card

The portrait is embedded because GitHub renders README SVGs via <img>, which
blocks external resources. Badges are separate files so each stays a real link.
"""
import base64
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORTRAIT = ROOT / "public" / "portrait-executive.jpg"
OUT = ROOT / "assets" / "hero-burgundy.svg"
BADGE_DIR = ROOT / "assets" / "badges"

SERIF = "Georgia, 'Times New Roman', 'DejaVu Serif', serif"
MONO = "'SF Mono', 'JetBrains Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# Palette
BG = "#0F0A0A"
CREAM = "#F3E6D3"
GOLD = "#D9B48A"
PEACH = "#E8B98A"
WINE = "#8E2B3A"
LINE = "#C9A27A"

W, H = 1000, 412
PX, PY, PW, PH = 678, 21, 220, 308          # portrait frame
OCX, OCY, ORX, ORY = 788, 172, 152, 160     # orbit ellipse


def orbit_pt(deg):
    a = math.radians(deg)
    return OCX + ORX * math.cos(a), OCY + ORY * math.sin(a)


def arc(d0, d1):
    x0, y0 = orbit_pt(d0)
    x1, y1 = orbit_pt(d1)
    large = 1 if abs(d1 - d0) > 180 else 0
    return f"M{x0:.1f},{y0:.1f} A{ORX},{ORY} 0 {large} 1 {x1:.1f},{y1:.1f}"


def node(deg, label, side, delay):
    x, y = orbit_pt(deg)
    tx, anchor = (x + 13, "start") if side == "r" else (x - 13, "end")
    return f"""
    <circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{GOLD}" opacity="0.2">
      <animate attributeName="r" values="6;11;6" dur="3.2s" begin="{delay}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.35;0;0.35" dur="3.2s" begin="{delay}s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{GOLD}"/>
    <text x="{tx:.1f}" y="{y + 5:.1f}" text-anchor="{anchor}" font-family="{MONO}" font-size="14" font-weight="700" fill="{CREAM}">{label}</text>"""


def build_hero():
    img = base64.b64encode(PORTRAIT.read_bytes()).decode()
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Jeya Stephen — AI/ML Engineer, Full-Stack Developer, AI and Data Science">
  <title>Jeya Stephen — AI/ML Engineer · Full-Stack Developer · AI &amp; Data Science</title>
  <defs>
    <radialGradient id="bg" cx="40%" cy="40%" r="80%">
      <stop offset="0%" stop-color="#1A1111"/>
      <stop offset="100%" stop-color="{BG}"/>
    </radialGradient>
    <radialGradient id="orb" cx="35%" cy="40%" r="65%">
      <stop offset="0%" stop-color="#6E1E2C"/>
      <stop offset="60%" stop-color="#4A1520"/>
      <stop offset="100%" stop-color="#2A0C12" stop-opacity="0.6"/>
    </radialGradient>
    <linearGradient id="wave" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7A2433"/>
      <stop offset="100%" stop-color="#2A0C12"/>
    </linearGradient>
    <linearGradient id="stephen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#A3374A"/>
      <stop offset="100%" stop-color="#7A2433"/>
    </linearGradient>
    <linearGradient id="underline" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{WINE}"/>
      <stop offset="70%" stop-color="{WINE}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{WINE}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{LINE}" stop-opacity="0.25"/>
      <stop offset="50%" stop-color="{LINE}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{LINE}" stop-opacity="0.25"/>
    </linearGradient>
    <linearGradient id="band" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5A1A26"/>
      <stop offset="100%" stop-color="#3A0F18"/>
    </linearGradient>
    <linearGradient id="frame" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F0CFA6"/>
      <stop offset="100%" stop-color="#B98A5E"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
    <clipPath id="card"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20"/></clipPath>
    <clipPath id="photo"><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="16"/></clipPath>
  </defs>

  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>

    <!-- Burgundy silk waves: bottom-left and top-right corners -->
    <g opacity="0.85">
      <path d="M-20,250 C40,300 60,380 150,430 L-20,430 Z" fill="url(#wave)" opacity="0.55"/>
      <path d="M-20,300 C30,340 50,400 110,430" stroke="#9C3446" stroke-width="1.2" fill="none" opacity="0.6"/>
      <path d="M-20,280 C40,330 70,400 140,430" stroke="#7A2433" stroke-width="1" fill="none" opacity="0.5"/>
      <path d="M1020,-10 C980,40 990,90 1020,150 Z" fill="url(#wave)" opacity="0.6"/>
      <path d="M960,-10 C990,30 1000,70 1020,110" stroke="#9C3446" stroke-width="1.2" fill="none" opacity="0.6"/>
      <path d="M930,-10 C975,40 995,100 1020,170" stroke="#7A2433" stroke-width="1" fill="none" opacity="0.45"/>
      <animateTransform attributeName="transform" type="translate" values="0,0;0,-3;0,0" dur="8s" repeatCount="indefinite"/>
    </g>

    <!-- Large burgundy orb behind portrait -->
    <circle cx="670" cy="186" r="108" fill="url(#orb)" opacity="0.9"/>

    <!-- Terminal pill -->
    <rect x="35" y="19" width="336" height="33" rx="16.5" fill="#1A0F10" stroke="{WINE}" stroke-width="1.4"/>
    <circle cx="55" cy="35.5" r="6" fill="#E0705A">
      <animate attributeName="opacity" values="1;0.45;1" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <text x="71" y="40.5" font-family="{MONO}" font-size="14" fill="{CREAM}">~/stephen $ build --intelligent</text>

    <!-- Eyebrow -->
    <line x1="38" y1="72" x2="74" y2="72" stroke="{GOLD}" stroke-width="1.6"/>
    <text x="88" y="77" font-family="{MONO}" font-size="14" letter-spacing="1.6" fill="{CREAM}">AI · MACHINE LEARNING · FULL-STACK</text>

    <!-- Name -->
    <text x="36" y="168" font-family="{SERIF}" font-weight="700" font-size="96" letter-spacing="-1" fill="{CREAM}">Jeya</text>
    <text x="36" y="252" font-family="{SERIF}" font-weight="700" font-size="96" letter-spacing="-1" fill="url(#stephen)">Stephen</text>
    <rect x="38" y="264" width="300" height="2.4" fill="url(#underline)">
      <animate attributeName="width" values="260;320;260" dur="6s" repeatCount="indefinite"/>
    </rect>

    <!-- Roles + tagline -->
    <text x="38" y="294" font-family="{MONO}" font-size="14.5" letter-spacing="0.6" fill="{CREAM}">AI/ML ENGINEER · FULL-STACK DEVELOPER · AI &amp; DATA SCIENCE</text>
    <text x="38" y="323" font-family="{SERIF}" font-style="italic" font-weight="700" font-size="18" fill="{PEACH}">Engineering intelligence. Designing experiences.</text>

    <!-- Bottom bar -->
    <rect x="38" y="348" width="{W - 60}" height="1" fill="url(#rule)"/>
    <rect x="38" y="389" width="{W - 60}" height="1" fill="url(#rule)"/>
    <text x="44" y="374" font-family="{MONO}" font-size="13" letter-spacing="0.8" fill="{CREAM}">B.TECH AI &amp; DATA SCIENCE · RAMCO INSTITUTE OF TECHNOLOGY</text>
    <line x1="590" y1="360" x2="590" y2="378" stroke="{LINE}" stroke-opacity="0.6"/>
    <path d="M622,352 L{W - 18},352 L{W - 34},386 L606,386 Z" fill="url(#band)"/>
    <text x="{(622 + W - 34) / 2 + 2:.0f}" y="374" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="1" fill="{PEACH}">CHENNAI, INDIA · OPEN TO COLLABORATION</text>

    <!-- Orbit -->
    <path d="{arc(-72, 72)}" stroke="{CREAM}" stroke-opacity="0.75" stroke-width="1.5" fill="none" stroke-dasharray="5 6">
      <animate attributeName="stroke-dashoffset" values="0;22" dur="2.5s" repeatCount="indefinite"/>
    </path>
    <path d="{arc(140, 220)}" stroke="{CREAM}" stroke-opacity="0.6" stroke-width="1.5" fill="none" stroke-dasharray="5 6">
      <animate attributeName="stroke-dashoffset" values="0;-22" dur="2.5s" repeatCount="indefinite"/>
    </path>

    <!-- Portrait -->
    <rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="16" fill="none" stroke="{PEACH}" stroke-width="6" opacity="0.45" filter="url(#glow)"/>
    <image href="data:image/jpeg;base64,{img}" xlink:href="data:image/jpeg;base64,{img}" x="{PX}" y="{PY}" width="{PW}" height="{PH}" preserveAspectRatio="xMidYMin slice" clip-path="url(#photo)"/>
    <rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="16" fill="none" stroke="url(#frame)" stroke-width="2.2"/>
    {node(-40, "LLM", "r", 0)}
    {node(-3, "API", "r", 0.8)}
    {node(36, "DATA", "r", 1.6)}
    {node(184, "UI", "l", 2.4)}
  </g>

  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="none" stroke="{LINE}" stroke-opacity="0.8" stroke-width="1.4"/>
</svg>
"""
    OUT.write_text(svg)
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")


# ── Badges ────────────────────────────────────────────────────────────────
GITHUB_PATH = (
    "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 "
    "0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7"
    "c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998"
    ".108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22"
    "-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 "
    "2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 "
    "0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 "
    "0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"
)

ICONS = {
    "vercel": f'<path d="M0,20 L11,1 L22,20 Z" fill="{GOLD}"/>',
    "github": f'<path d="{GITHUB_PATH}" fill="{GOLD}" transform="scale(0.9)"/>',
    "gmail": f'<path d="M1,19 V4 L11,12 L21,4 V19" stroke="{GOLD}" stroke-width="3.2" fill="none" stroke-linejoin="round"/>',
    None: "",
}

EXT_ICON = (
    '<g fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M7,1 H1 V13 H13 V7"/><path d="M8,1 H13 V6"/><path d="M13,1 L6,8"/></g>'
)

CH = 8.6  # approx advance of 14px bold monospace incl. letter-spacing


def badge(name, icon, label, value, ext=True):
    h = 40
    icon_w = 30 if icon else 0
    label_w = len(label) * 8.7
    gap = 22
    pill_x = icon_w + label_w + gap
    pill_w = len(value) * CH + 32 + (26 if ext else 0)
    w = pill_x + pill_w + 2
    ext_svg = ""
    if ext:
        ex = pill_x + pill_w - 30
        ext_svg = f'<g transform="translate({ex:.1f},13)">{EXT_ICON.format(c=CREAM)}</g>'
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h}" width="{w:.0f}" height="{h}" role="img" aria-label="{label}: {value}">
  <g transform="translate(2,9)">{ICONS[icon]}</g>
  <text x="{icon_w + 2}" y="25" font-family="{MONO}" font-size="13.5" letter-spacing="0.6" fill="{CREAM}">{label}</text>
  <rect x="{pill_x:.1f}" y="2" width="{pill_w:.1f}" height="{h - 4}" rx="7" fill="#6B1F2D" stroke="#8E2B3A" stroke-width="1"/>
  <text x="{pill_x + 16:.1f}" y="25.5" font-family="{MONO}" font-size="14" font-weight="700" letter-spacing="0.2" fill="#FBEFE0">{value}</text>
  {ext_svg}
</svg>
"""
    BADGE_DIR.mkdir(exist_ok=True)
    (BADGE_DIR / f"{name}.svg").write_text(svg)


def build_badges():
    badge("portfolio", "vercel", "PORTFOLIO", "STEPHEN-S-PORTFOLIO-PSI.VERCEL.APP")
    badge("linkedin", None, "LINKEDIN", "STEPHEN-PROFILE")
    badge("github", "github", "GITHUB", "STEPHENSHUB03", ext=False)
    badge("email", "gmail", "EMAIL", "CONNECT.STEPHEN01@GMAIL.COM", ext=False)
    print(f"wrote badges to {BADGE_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    build_hero()
    build_badges()
