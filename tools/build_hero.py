#!/usr/bin/env python3
"""Build assets/hero-spectrum.svg — neon-violet spectrum hero card.

Usage: python3 tools/build_hero.py
The portrait is embedded as base64 because GitHub renders README SVGs via
<img>, which blocks external resources (fonts, linked images).
"""
import base64
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORTRAIT = ROOT / "public" / "portrait-executive.jpg"
OUT = ROOT / "assets" / "hero-spectrum.svg"

W, H = 1000, 412
SERIF = "Georgia, 'Times New Roman', 'DejaVu Serif', serif"
MONO = "'SF Mono', 'JetBrains Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# Portrait frame
PX, PY, PW, PH = 650, 16, 228, 306
# Orbit around the portrait
OCX, OCY, ORX, ORY = 764, 168, 148, 158


def orbit_pt(deg):
    a = math.radians(deg)
    return OCX + ORX * math.cos(a), OCY + ORY * math.sin(a)


def arc(d0, d1):
    x0, y0 = orbit_pt(d0)
    x1, y1 = orbit_pt(d1)
    large = 1 if abs(d1 - d0) > 180 else 0
    sweep = 1 if d1 > d0 else 0
    return f"M{x0:.1f},{y0:.1f} A{ORX},{ORY} 0 {large} {sweep} {x1:.1f},{y1:.1f}"


def node(deg, label, color, side, delay):
    x, y = orbit_pt(deg)
    tx = x + 11 if side == "r" else x - 11
    anchor = "start" if side == "r" else "end"
    return f"""
    <g>
      <circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{color}" opacity="0.18" filter="url(#soft)">
        <animate attributeName="r" values="7;11;7" dur="3s" begin="{delay}s" repeatCount="indefinite"/>
      </circle>
      <circle cx="{x:.1f}" cy="{y:.1f}" r="4.6" fill="{color}"/>
      <circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="#FFFFFF"/>
      <text x="{tx:.1f}" y="{y + 4.6:.1f}" text-anchor="{anchor}" font-family="{MONO}" font-size="13.5" font-weight="600" fill="#F4F1FF">{label}</text>
    </g>"""


def spectrum_arc(path, width, blur_id, opacity=1.0):
    """Stack of offset coloured strokes forming a prismatic light streak."""
    colors = ["#FF3B6B", "#FF9A3C", "#FFE45C", "#4CFF9A", "#3CD8FF", "#4F6BFF", "#B04CFF"]
    layers = []
    n = len(colors)
    for i, c in enumerate(colors):
        off = (i - n / 2) * width * 0.9
        layers.append(
            f'<path d="{path}" transform="translate({off * 0.55:.2f},{off:.2f})" '
            f'stroke="{c}" stroke-width="{width * 1.6:.1f}" fill="none" stroke-linecap="round"/>'
        )
    return f"""
    <g filter="url(#{blur_id})" opacity="{opacity}" mask="url(#streak-fade)">
      {''.join(layers)}
    </g>
    <path d="{path}" stroke="#FFFFFF" stroke-width="{width * 0.7:.1f}" fill="none" stroke-linecap="round" opacity="0.85" filter="url(#soft)" mask="url(#streak-fade)"/>"""


def main():
    img_b64 = base64.b64encode(PORTRAIT.read_bytes()).decode()

    main_streak = "M395,175 C470,95 560,35 690,-25"
    lower_streak = "M880,402 C920,370 960,340 1010,318"
    thin_arc = "M420,190 C500,120 580,70 700,30"

    left_arc = arc(130, 230)   # UI side
    right_arc = arc(-62, 62)   # LLM / API / DATA side

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Jeya Stephen — AI/ML Engineer, Full-Stack Developer, AI and Data Science">
  <title>Jeya Stephen — AI/ML Engineer · Full-Stack Developer · AI &amp; Data Science</title>
  <defs>
    <radialGradient id="bg" cx="55%" cy="35%" r="75%">
      <stop offset="0%" stop-color="#140B26"/>
      <stop offset="55%" stop-color="#07050D"/>
      <stop offset="100%" stop-color="#030207"/>
    </radialGradient>
    <radialGradient id="glow-l" cx="0.3" cy="0.6" r="0.5">
      <stop offset="0%" stop-color="#3B1D73" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#3B1D73" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="card-stroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#C084FC"/>
      <stop offset="50%" stop-color="#8B5CF6" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#E879F9"/>
    </linearGradient>
    <linearGradient id="name-grad" x1="0" y1="0" x2="1" y2="0.35">
      <stop offset="0%" stop-color="#F5F3FF"/>
      <stop offset="28%" stop-color="#B9E9FF"/>
      <stop offset="52%" stop-color="#7DE3F5"/>
      <stop offset="70%" stop-color="#F0C8FF"/>
      <stop offset="88%" stop-color="#FFF6D6"/>
      <stop offset="100%" stop-color="#E9B6FF"/>
      <animate attributeName="x1" values="0;-0.25;0" dur="9s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="1;0.75;1" dur="9s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="underline" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#60A5FA" stop-opacity="0"/>
      <stop offset="25%" stop-color="#818CF8"/>
      <stop offset="75%" stop-color="#C084FC"/>
      <stop offset="100%" stop-color="#C084FC" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="divider" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.15"/>
      <stop offset="50%" stop-color="#A78BFA" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0.15"/>
    </linearGradient>
    <linearGradient id="photo-stroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E879F9"/>
      <stop offset="40%" stop-color="#FDE68A"/>
      <stop offset="70%" stop-color="#C4B5FD"/>
      <stop offset="100%" stop-color="#F0ABFC"/>
    </linearGradient>
    <linearGradient id="orbit-r" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FCD34D"/>
      <stop offset="50%" stop-color="#F472B6"/>
      <stop offset="100%" stop-color="#C084FC"/>
    </linearGradient>
    <linearGradient id="orbit-l" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#C084FC" stop-opacity="0.2"/>
      <stop offset="50%" stop-color="#F472B6"/>
      <stop offset="100%" stop-color="#C084FC" stop-opacity="0.2"/>
    </linearGradient>
    <linearGradient id="pill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1E1240"/>
      <stop offset="100%" stop-color="#120B24"/>
    </linearGradient>
    <linearGradient id="streak-fade-grad" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="35%" stop-color="#FFF" stop-opacity="1"/>
      <stop offset="80%" stop-color="#FFF" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#FFF" stop-opacity="0.2"/>
    </linearGradient>
    <mask id="streak-fade" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <rect x="0" y="0" width="{W}" height="{H}" fill="url(#streak-fade-grad)"/>
    </mask>
    <filter id="streak-blur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
    <filter id="streak-blur-wide" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>
    <filter id="soft" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.2"/>
    </filter>
    <filter id="name-glow" x="-10%" y="-20%" width="120%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="7" result="b"/>
      <feFlood flood-color="#A78BFA" flood-opacity="0.45"/>
      <feComposite in2="b" operator="in" result="g"/>
      <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="photo-glow" x="-15%" y="-15%" width="130%" height="130%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
    <clipPath id="card-clip">
      <rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="22"/>
    </clipPath>
    <clipPath id="photo-clip">
      <rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="16"/>
    </clipPath>
  </defs>

  <!-- Card -->
  <g clip-path="url(#card-clip)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#glow-l)"/>

    <!-- Prismatic light streaks -->
    <g>
      {spectrum_arc(main_streak, 5.5, "streak-blur-wide", 0.7)}
      {spectrum_arc(main_streak, 3.0, "streak-blur", 1.0)}
      <animate attributeName="opacity" values="0.85;1;0.85" dur="6s" repeatCount="indefinite"/>
    </g>
    <path d="{thin_arc}" stroke="#7C83FF" stroke-width="1.4" fill="none" opacity="0.55" filter="url(#soft)" mask="url(#streak-fade)"/>
    <g>
      {spectrum_arc(lower_streak, 3.2, "streak-blur", 0.9)}
    </g>

    <!-- Star specks -->
    <g fill="#E9D5FF">
      <circle cx="292" cy="155" r="1.4" opacity="0.8"><animate attributeName="opacity" values="0.2;0.9;0.2" dur="4s" repeatCount="indefinite"/></circle>
      <circle cx="574" cy="108" r="1.2" opacity="0.6"><animate attributeName="opacity" values="0.7;0.15;0.7" dur="5s" repeatCount="indefinite"/></circle>
      <circle cx="610" cy="42" r="1" opacity="0.5"/>
      <circle cx="940" cy="30" r="1.1" opacity="0.5"/>
      <circle cx="420" cy="60" r="0.9" opacity="0.4"/>
    </g>

    <!-- Terminal pill -->
    <rect x="32" y="21" width="288" height="31" rx="15.5" fill="url(#pill)" stroke="#8B5CF6" stroke-opacity="0.7" stroke-width="1"/>
    <circle cx="51" cy="36.5" r="7" fill="#C084FC" opacity="0.35" filter="url(#soft)">
      <animate attributeName="opacity" values="0.15;0.6;0.15" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="51" cy="36.5" r="4.4" fill="#F5F3FF"/>
    <text x="66" y="41" font-family="{MONO}" font-size="13" fill="#E9E5FF">~/stephen $ build --intelligent</text>

    <!-- Eyebrow -->
    <line x1="34" y1="70" x2="66" y2="70" stroke="#C4B5FD" stroke-width="1.4"/>
    <text x="80" y="75" font-family="{MONO}" font-size="12.5" letter-spacing="2.2" fill="#D8B4FE">AI · MACHINE LEARNING · FULL-STACK</text>

    <!-- Name -->
    <g filter="url(#name-glow)" font-family="{SERIF}" font-weight="700" fill="url(#name-grad)">
      <text x="30" y="166" font-size="88" letter-spacing="-1">Jeya</text>
      <text x="30" y="250" font-size="88" letter-spacing="-1">Stephen</text>
    </g>
    <circle cx="290" cy="128" r="1.6" fill="#E9D5FF"/>
    <rect x="52" y="270" width="270" height="2" fill="url(#underline)">
      <animate attributeName="width" values="220;290;220" dur="6s" repeatCount="indefinite"/>
    </rect>

    <!-- Roles + tagline -->
    <text x="32" y="294" font-family="{MONO}" font-size="12.5" letter-spacing="1.9" fill="#EDE9FE">AI/ML ENGINEER · FULL-STACK DEVELOPER · AI &amp; DATA SCIENCE</text>
    <text x="32" y="320" font-family="{SERIF}" font-style="italic" font-size="16" fill="#F5D98B">Engineering intelligence. Designing experiences.</text>

    <!-- Bottom bar -->
    <rect x="20" y="346" width="{W - 40}" height="1" fill="url(#divider)"/>
    <text x="32" y="372" font-family="{MONO}" font-size="12" letter-spacing="1.6" fill="#E4E0F5">B.TECH AI &amp; DATA SCIENCE · RAMCO INSTITUTE OF TECHNOLOGY</text>
    <text x="935" y="372" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="1.6" fill="#D8B4FE">CHENNAI, INDIA · OPEN TO COLLABORATION</text>
    <rect x="20" y="390" width="{W - 40}" height="1" fill="url(#divider)"/>

    <!-- Orbit -->
    <path d="{left_arc}" stroke="url(#orbit-l)" stroke-width="1.6" fill="none" stroke-dasharray="5 5">
      <animate attributeName="stroke-dashoffset" values="0;-20" dur="2s" repeatCount="indefinite"/>
    </path>
    <path d="{right_arc}" stroke="url(#orbit-r)" stroke-width="1.6" fill="none" stroke-dasharray="6 5">
      <animate attributeName="stroke-dashoffset" values="0;22" dur="2s" repeatCount="indefinite"/>
    </path>

    <!-- Portrait -->
    <rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="16" fill="none" stroke="url(#photo-stroke)" stroke-width="5" opacity="0.55" filter="url(#photo-glow)"/>
    <image href="data:image/jpeg;base64,{img_b64}" xlink:href="data:image/jpeg;base64,{img_b64}" x="{PX}" y="{PY}" width="{PW}" height="{PH}" preserveAspectRatio="xMidYMin slice" clip-path="url(#photo-clip)"/>
    <rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="16" fill="none" stroke="url(#photo-stroke)" stroke-width="2.4"/>

    {node(-42, "LLM", "#FBBF24", "r", 0)}
    {node(-2, "API", "#F472B6", "r", 0.8)}
    {node(36, "DATA", "#C084FC", "r", 1.6)}
    {node(180, "UI", "#F472B6", "l", 2.4)}
  </g>

  <rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="22" fill="none" stroke="url(#card-stroke)" stroke-width="1.6"/>
</svg>
"""
    OUT.write_text(svg)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
