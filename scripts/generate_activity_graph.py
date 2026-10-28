#!/usr/bin/env python3
"""
Generate a luxury GitHub activity / contribution graph SVG matching the editorial obsidian-wine theme
using 100% genuine GitHub contribution calendar data.
"""

import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta

USERNAME = "StephensHub03"

# Burgundy & Antique Gold Theme Palette
COLORS = {
    0: "#200c19", # empty dark wine cell
    1: "#4a182b", # level 1 burgundy
    2: "#7d2243", # level 2 medium wine
    3: "#b53360", # level 3 bright wine
    4: "#e25b86", # level 4 vibrant rose/pink
    5: "#fce4ec"  # level 5 peak cream-pink highlight
}

LEVEL_MAP = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}


def get_auth_token():
    """Retrieve GitHub token from environment or local gh CLI."""
    token = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
    if token and token.strip():
        return token.strip()

    # Try local GitHub CLI if present
    try:
        res = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass

    return None


def fetch_from_graphql(token):
    """Query GitHub GraphQL API for the official contribution calendar."""
    query = """
    {
      user(login: "%s") {
        login
        name
        contributionsCollection {
          startedAt
          endedAt
          contributionCalendar {
            totalContributions
            weeks {
              firstDay
              contributionDays {
                date
                contributionCount
                contributionLevel
                weekday
              }
            }
          }
        }
      }
    }
    """ % USERNAME

    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": f"{USERNAME}-Activity-Graph"
        }
    )

    with urllib.request.urlopen(req, timeout=12) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    if "errors" in result:
        raise RuntimeError(f"GraphQL error: {result['errors']}")

    user_data = result.get("data", {}).get("user")
    if not user_data:
        raise RuntimeError(f"User {USERNAME} not found in GraphQL response")

    actual_login = user_data.get("login", "")
    if actual_login.lower() != USERNAME.lower():
        raise RuntimeError(f"Queried user mismatch: expected {USERNAME}, got {actual_login}")

    cal = user_data["contributionsCollection"]["contributionCalendar"]
    return cal["weeks"], cal["totalContributions"]


def fetch_from_public_api():
    """Fallback to verified public contribution API if no token is available."""
    api_url = f"https://github-contributions-api.jogruber.de/v4/{USERNAME}?y=last"
    req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=12) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    raw_contribs = data.get("contributions", [])
    if not raw_contribs:
        raise RuntimeError(f"No contributions returned for {USERNAME} from public API")

    total_contributions = data.get("total", {}).get("lastYear", sum(c.get("count", 0) for c in raw_contribs))

    # Reconstruct weeks in exact GitHub GraphQL structure
    # raw_contribs is chronological starting on a Sunday
    weeks = []
    current_week = []
    for c in raw_contribs:
        dt = datetime.strptime(c["date"], "%Y-%m-%d")
        gh_weekday = (dt.weekday() + 1) % 7 # Sunday=0, Monday=1, ..., Saturday=6

        level_names = {0: "NONE", 1: "FIRST_QUARTILE", 2: "SECOND_QUARTILE", 3: "THIRD_QUARTILE", 4: "FOURTH_QUARTILE"}
        lvl_num = c.get("level", 0)

        day_obj = {
            "date": c["date"],
            "contributionCount": c.get("count", 0),
            "contributionLevel": level_names.get(lvl_num, "NONE"),
            "weekday": gh_weekday
        }

        if gh_weekday == 0 and current_week:
            weeks.append({
                "firstDay": current_week[0]["date"],
                "contributionDays": current_week
            })
            current_week = []

        current_week.append(day_obj)

    if current_week:
        weeks.append({
            "firstDay": current_week[0]["date"],
            "contributionDays": current_week
        })

    return weeks, total_contributions


def load_genuine_data():
    """Retrieve genuine contribution data with strict validation."""
    token = get_auth_token()
    if token:
        try:
            print("Fetching contribution calendar from GitHub GraphQL API...")
            weeks, total = fetch_from_graphql(token)
            print(f"Successfully retrieved {total} contributions from GraphQL API for @{USERNAME}")
            return weeks, total
        except Exception as e:
            print(f"Warning: GraphQL API fetch failed ({e}). Attempting public fallback...")

    try:
        print("Fetching contribution calendar from public fallback API...")
        weeks, total = fetch_from_public_api()
        print(f"Successfully retrieved {total} contributions from public endpoint for @{USERNAME}")
        return weeks, total
    except Exception as e:
        print(f"Error: All genuine data sources failed ({e})")
        raise RuntimeError(
            f"Cannot retrieve authentic GitHub contribution data for @{USERNAME}. "
            f"Please verify your internet connection or configure a valid GitHub token/secret."
        )


def generate_svg():
    weeks, total_contributions = load_genuine_data()

    all_days = [d for w in weeks for d in w["contributionDays"]]
    total_calendar_days = len(all_days)

    if not all_days:
        raise ValueError("Calendar data contains no days")

    # Verify active days
    active_days_count = sum(1 for d in all_days if d["contributionCount"] > 0)

    # Date range string
    first_dt = datetime.strptime(all_days[0]["date"], "%Y-%m-%d")
    last_dt = datetime.strptime(all_days[-1]["date"], "%Y-%m-%d")
    range_str = f"{first_dt.strftime('%b %Y')} – {last_dt.strftime('%b %Y')}"

    # Busiest day calculation
    busiest_day = max(all_days, key=lambda d: d["contributionCount"])
    busiest_count = busiest_day["contributionCount"]
    if busiest_count > 0:
        b_dt = datetime.strptime(busiest_day["date"], "%Y-%m-%d")
        busiest_date_str = b_dt.strftime("%d %b %Y").lstrip("0")
    else:
        busiest_date_str = "None"

    # Longest streak calculation
    cur_streak = 0
    cur_start_dt = None
    cur_col_start = None
    longest_streak = 0
    streak_start = None
    streak_end = None
    streak_col_start = None
    streak_col_end = None

    for c_idx, w in enumerate(weeks):
        for d in w["contributionDays"]:
            if d["contributionCount"] > 0:
                if cur_streak == 0:
                    cur_start_dt = datetime.strptime(d["date"], "%Y-%m-%d")
                    cur_col_start = c_idx
                cur_streak += 1
                if cur_streak > longest_streak:
                    longest_streak = cur_streak
                    streak_start = cur_start_dt
                    streak_end = datetime.strptime(d["date"], "%Y-%m-%d")
                    streak_col_start = cur_col_start
                    streak_col_end = c_idx
            else:
                cur_streak = 0

    streak_date_str = ""
    if streak_start and streak_end:
        streak_date_str = f"{streak_start.strftime('%d %b %Y').upper().lstrip('0')} — {streak_end.strftime('%d %b %Y').upper().lstrip('0')}"

    streak_subtext = "consecutive days" if longest_streak != 1 else "consecutive day"

    # Layout parameters matching the card aesthetic
    cell_size = 12.5
    gap = 4.0
    start_x = 94.0
    start_y = 175.0

    # Build month labels dynamically
    last_month = None
    last_label_x = -100.0
    month_labels = []

    for c_idx, w in enumerate(weeks):
        days = w["contributionDays"]
        if not days:
            continue
        # Use mid-day of the week to identify current month
        mid_d = days[len(days) // 2]
        m_dt = datetime.strptime(mid_d["date"], "%Y-%m-%d")
        m_name = m_dt.strftime("%b")

        x_pos = start_x + c_idx * (cell_size + gap)

        if m_name != last_month:
            # Ensure at least 45px separation to prevent label overlaps
            if (x_pos - last_label_x) >= 45.0:
                month_labels.append((m_name, x_pos))
                last_label_x = x_pos
                last_month = m_name

    month_svg = "\n".join([
        f'  <text x="{pos:.1f}" y="156" font-family="\'SF Mono\', Monaco, monospace" font-size="10" fill="#9E8C94">{name}</text>'
        for name, pos in month_labels
    ])

    # Render heatmap cells
    svg_cells = []
    peak_coords = None

    for c_idx, w in enumerate(weeks):
        x = start_x + c_idx * (cell_size + gap)
        days_map = {d["weekday"]: d for d in w["contributionDays"]}
        for r_idx in range(7):
            y = start_y + r_idx * (cell_size + gap)
            day = days_map.get(r_idx)
            if day is None:
                color = COLORS[0]
            else:
                cnt = day["contributionCount"]
                lvl_str = day.get("contributionLevel", "NONE")
                lvl = LEVEL_MAP.get(lvl_str, 0)
                if cnt > 0 and cnt == busiest_count and busiest_count >= 10:
                    lvl = 5
                    peak_coords = (x, y)
                color = COLORS[lvl]
            svg_cells.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_size:.1f}" height="{cell_size:.1f}" rx="3" fill="{color}"/>')

    # Peak Easter Egg
    face_svg = ""
    if peak_coords:
        px, py = peak_coords
        face_svg = f'''
    <!-- Easter Egg commit face on peak day -->
    <circle cx="{px + 3.8:.1f}" cy="{py + 6.0:.1f}" r="1.1" fill="#160910"/>
    <circle cx="{px + 8.7:.1f}" cy="{py + 6.0:.1f}" r="1.1" fill="#160910"/>
'''

    # Longest Streak Indicator
    streak_svg = ""
    if longest_streak > 1 and streak_col_start is not None and streak_col_end is not None:
        sx1 = start_x + streak_col_start * (cell_size + gap)
        sx2 = start_x + streak_col_end * (cell_size + gap) + cell_size
        sy = start_y + 7 * (cell_size + gap) + 12

        # Align text nicely
        text_x = min(max(sx2 + 20, 600.0), 964.5)
        streak_svg = f'''
    <!-- Longest streak indicator -->
    <path d="M{sx1:.1f},{sy-5:.1f} L{sx1:.1f},{sy:.1f} L{sx2:.1f},{sy:.1f} L{sx2:.1f},{sy-5:.1f}" fill="none" stroke="#C58B98" stroke-width="1.2" opacity="0.8"/>
    <text x="{text_x:.1f}" y="{sy + 14:.1f}" font-family="'SF Mono', Monaco, monospace" font-size="9" letter-spacing="1.5" fill="#C58B98" font-weight="600" text-anchor="end">LONGEST STREAK · {longest_streak} DAYS · {streak_date_str}</text>
'''

    today_str = datetime.now().strftime("%d %b %Y").lstrip("0")

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" width="1000" height="440" role="img" aria-label="Commit Log — Real GitHub Activity for @{USERNAME}">
  <title>Commit Log — Real GitHub Activity for @{USERNAME}</title>
  <defs>
    <!-- Background Base Gradient -->
    <linearGradient id="act-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#160910"/>
      <stop offset="60%"  stop-color="#1a0b14"/>
      <stop offset="100%" stop-color="#240c1c"/>
    </linearGradient>

    <!-- Top-right Ambient Wine Glow -->
    <radialGradient id="act-glow" cx="88%" cy="18%" r="62%">
      <stop offset="0%"   stop-color="#5a1832" stop-opacity="0.42"/>
      <stop offset="55%"  stop-color="#240c1c" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#160910" stop-opacity="0"/>
    </radialGradient>

    <!-- Subtle Tech Pattern -->
    <pattern id="act-pattern" width="40" height="40" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="40" y2="0" stroke="#76243B" stroke-width="0.4" stroke-opacity="0.08"/>
      <line x1="0" y1="0" x2="0" y2="40" stroke="#76243B" stroke-width="0.4" stroke-opacity="0.08"/>
    </pattern>
  </defs>

  <!-- Card Container -->
  <rect width="1000" height="440" rx="20" fill="url(#act-bg)" stroke="#40202B" stroke-width="1.2"/>
  <rect width="1000" height="440" rx="20" fill="url(#act-glow)"/>
  <rect width="1000" height="440" rx="20" fill="url(#act-pattern)"/>

  <!-- Corner accent dots -->
  <circle cx="22" cy="22" r="2.5" fill="#C5A46D" opacity="0.35"/>
  <circle cx="978" cy="22" r="2.5" fill="#C5A46D" opacity="0.35"/>

  <!-- ═══ TOP-LEFT: EDITORIAL HEADLINE ═══ -->
  <text x="44" y="56" font-family="'SF Mono', Monaco, monospace" font-size="10" letter-spacing="2" fill="#C58B98" font-weight="600">COMMIT LOG · REAL GITHUB ACTIVITY</text>
  <text x="44" y="92" font-family="Georgia, 'Times New Roman', serif" font-size="21.5" font-weight="700" fill="#F2EAE0">A year of building, <tspan font-style="italic" fill="#E27396">one square</tspan> at a time.</text>

  <!-- ═══ TOP-RIGHT: 4 STAT METRICS ═══ -->
  <!-- Col 1: Contributions -->
  <g transform="translate(520, 48)">
    <text font-family="'SF Mono', Monaco, monospace" font-size="9.5" letter-spacing="1.5" fill="#9E8C94" font-weight="600">CONTRIBUTIONS</text>
    <text y="36" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="700" fill="#FFFFFF">{total_contributions:,}</text>
    <text y="52" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#9E8C94">{range_str}</text>
  </g>

  <!-- Col 2: Active Days -->
  <g transform="translate(645, 48)">
    <text font-family="'SF Mono', Monaco, monospace" font-size="9.5" letter-spacing="1.5" fill="#9E8C94" font-weight="600">ACTIVE DAYS</text>
    <text y="36" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="700" fill="#FFFFFF">{active_days_count}</text>
    <text y="52" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#9E8C94">of {total_calendar_days} days</text>
  </g>

  <!-- Col 3: Longest Streak -->
  <g transform="translate(760, 48)">
    <text font-family="'SF Mono', Monaco, monospace" font-size="9.5" letter-spacing="1.5" fill="#9E8C94" font-weight="600">LONGEST STREAK</text>
    <text y="36" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="700" fill="#FFFFFF">{longest_streak}</text>
    <text y="52" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#9E8C94">{streak_subtext}</text>
  </g>

  <!-- Col 4: Busiest Day -->
  <g transform="translate(880, 48)">
    <text font-family="'SF Mono', Monaco, monospace" font-size="9.5" letter-spacing="1.5" fill="#9E8C94" font-weight="600">BUSIEST DAY</text>
    <text y="36" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="700" fill="#FFFFFF">{busiest_count}</text>
    <text y="52" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#9E8C94">{busiest_date_str}</text>
  </g>

  <!-- ═══ MONTH LABELS ═══ -->
{month_svg}

  <!-- ═══ DAY LABELS (LEFT, RIGHT-ALIGNED TO GRID) ═══ -->
  <text x="80" y="201" font-family="'SF Mono', Monaco, monospace" font-size="9.5" fill="#9E8C94" text-anchor="end">Mon</text>
  <text x="80" y="234" font-family="'SF Mono', Monaco, monospace" font-size="9.5" fill="#9E8C94" text-anchor="end">Wed</text>
  <text x="80" y="267" font-family="'SF Mono', Monaco, monospace" font-size="9.5" fill="#9E8C94" text-anchor="end">Fri</text>

  <!-- ═══ HEATMAP CELLS ═══ -->
  {"".join(svg_cells)}
{face_svg}
{streak_svg}
  <!-- ═══ FOOTER & LEGEND ═══ -->
  <!-- Source attribution -->
  <text x="44" y="404" font-family="'SF Mono', Monaco, monospace" font-size="9.5" fill="#7A6870">Source: GitHub contribution calendar for <tspan fill="#C58B98">@{USERNAME}</tspan> · snapshot {today_str} · refreshed daily</text>

  <!-- Legend -->
  <g transform="translate(790, 394)">
    <text x="0" y="9" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#7A6870" text-anchor="end">Less</text>
    <rect x="8" y="0" width="10" height="10" rx="2.5" fill="{COLORS[0]}"/>
    <rect x="22" y="0" width="10" height="10" rx="2.5" fill="{COLORS[1]}"/>
    <rect x="36" y="0" width="10" height="10" rx="2.5" fill="{COLORS[2]}"/>
    <rect x="50" y="0" width="10" height="10" rx="2.5" fill="{COLORS[3]}"/>
    <rect x="64" y="0" width="10" height="10" rx="2.5" fill="{COLORS[4]}"/>
    <rect x="78" y="0" width="10" height="10" rx="2.5" fill="{COLORS[5]}"/>
    <text x="96" y="9" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#7A6870">More</text>
  </g>
</svg>
'''
    return svg_content


if __name__ == "__main__":
    svg = generate_svg()
    out_path = "assets/section-06-activity.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Successfully generated {out_path} with verified genuine data.")
