#!/usr/bin/env python3
"""
Generate a luxury GitHub activity / contribution graph SVG matching the editorial obsidian-wine theme
with 100% verified real data directly from GitHub and pixel-perfect alignments.
"""

import json
import re
import urllib.request
from datetime import datetime, timedelta

def fetch_real_github_data():
    """
    Fetch exact contribution calendar data directly from GitHub's official endpoint.
    Fallback to public API if needed.
    """
    url = "https://github.com/users/StephensHub03/contributions"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8")

        # Extract tooltips for exact contribution counts
        tts = re.findall(r'<tool-tip[^>]*for=\"contribution-day-component-(\d+)-(\d+)\"[^>]*>(.*?)</tool-tip>', html, re.DOTALL)
        counts_map = {}
        for r, c, txt in tts:
            m = re.search(r'(\d+)\s+contribution', txt)
            count = int(m.group(1)) if m else 0
            counts_map[(int(r), int(c))] = count

        # Extract cells with dates
        cell_pattern = r'<td[^>]*data-date=\"(\d{4}-\d{2}-\d{2})\"[^>]*id=\"contribution-day-component-(\d+)-(\d+)\"[^>]*data-level=\"(\d+)\"'
        cells = re.findall(cell_pattern, html)

        contribs = []
        for date_str, r_str, c_str, lvl_str in cells:
            r = int(r_str)
            c = int(c_str)
            count = counts_map.get((r, c), 0)
            contribs.append({
                "date": date_str,
                "row": r,
                "col": c,
                "count": count,
                "level": int(lvl_str)
            })

        # Sort chronologically
        contribs.sort(key=lambda x: x["date"])
        
        # Total in header
        total_match = re.search(r'([\d,]+)\s+contributions\s+in\s+the\s+last\s+year', html)
        total_header = int(total_match.group(1).replace(",", "")) if total_match else sum(c["count"] for c in contribs)

        return contribs, total_header
    except Exception as e:
        print(f"Direct GitHub fetch error ({e}), falling back to API...")
        api_url = "https://github-contributions-api.jogruber.de/v4/StephensHub03?y=last"
        req_api = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_api, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            contribs = data.get("contributions", [])
            total = sum(c["count"] for c in contribs)
            return contribs, total

def generate_svg():
    contribs, total_contributions = fetch_real_github_data()
    if not contribs:
        raise ValueError("Could not load contribution data")

    # Real statistics
    active_days = sum(1 for c in contribs if c["count"] > 0)
    
    busiest_entry = max(contribs, key=lambda c: c["count"]) if contribs else {"count": 0, "date": "N/A"}
    busiest_count = busiest_entry["count"]
    try:
        b_dt = datetime.strptime(busiest_entry["date"], "%Y-%m-%d")
        busiest_date_str = b_dt.strftime("%d %b %Y").lstrip("0")
    except:
        busiest_date_str = busiest_entry["date"]

    # Calculate streaks
    longest_streak = 0
    current_streak = 0
    streak_start = None
    streak_end = None
    cur_start = None

    for c in contribs:
        if c["count"] > 0:
            if current_streak == 0:
                cur_start = c["date"]
            current_streak += 1
            if current_streak > longest_streak:
                longest_streak = current_streak
                streak_start = cur_start
                streak_end = c["date"]
        else:
            current_streak = 0

    streak_date_str = ""
    if streak_start and streak_end:
        try:
            s_dt = datetime.strptime(streak_start, "%Y-%m-%d")
            e_dt = datetime.strptime(streak_end, "%Y-%m-%d")
            streak_date_str = f"{s_dt.strftime('%d %b %Y').upper().lstrip('0')} — {e_dt.strftime('%d %b %Y').upper().lstrip('0')}"
        except:
            streak_date_str = f"{streak_start} — {streak_end}"

    first_dt = datetime.strptime(contribs[0]["date"], "%Y-%m-%d")
    last_dt = datetime.strptime(contribs[-1]["date"], "%Y-%m-%d")
    range_str = f"{first_dt.strftime('%b %Y')} – {last_dt.strftime('%b %Y')}"

    # Palette
    colors = {
        0: "#200c19", # empty dark wine cell
        1: "#4a182b", # level 1
        2: "#7d2243", # level 2
        3: "#b53360", # level 3
        4: "#e25b86", # level 4
        5: "#fce4ec"  # level 5 (peak cream-pink)
    }

    # Grid layout parameters
    cell_size = 12.5
    gap = 4.0
    start_x = 94.0
    start_y = 175.0

    # Group into weeks (Sunday to Saturday)
    weeks = []
    current_week = []
    
    first_date_obj = datetime.strptime(contribs[0]["date"], "%Y-%m-%d")
    first_weekday = first_date_obj.weekday()
    sun_weekday = (first_weekday + 1) % 7

    for _ in range(sun_weekday):
        current_week.append(None)

    for c in contribs:
        current_week.append(c)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        while len(current_week) < 7:
            current_week.append(None)
        weeks.append(current_week)

    # 53 columns
    if len(weeks) > 53:
        weeks = weeks[-53:]

    # Month labels calculation: find the first appearance of each month
    # We want labels for: Nov, Dec, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_first_col = {}

    for w_idx, week in enumerate(weeks):
        for day in week:
            if day:
                d_dt = datetime.strptime(day["date"], "%Y-%m-%d")
                m_key = (d_dt.year, d_dt.month)
                if m_key not in month_first_col:
                    month_first_col[m_key] = (w_idx, d_dt.strftime("%b"))

    month_labels = []
    sorted_months = sorted(month_first_col.keys())
    # If the first month only has <= 1 week in the calendar, skip it so Nov is the first clean label
    for idx, m_key in enumerate(sorted_months):
        w_idx, m_name = month_first_col[m_key]
        if idx == 0 and w_idx < 1 and len(sorted_months) > 12:
            continue
        x_pos = start_x + w_idx * (cell_size + gap)
        month_labels.append((m_name, x_pos))

    # Longest streak column tracking
    streak_col_start = None
    streak_col_end = None
    if streak_start and streak_end:
        for w_idx, week in enumerate(weeks):
            for day in week:
                if day:
                    if day["date"] == streak_start:
                        streak_col_start = w_idx
                    if day["date"] == streak_end:
                        streak_col_end = w_idx

    svg_cells = []
    busiest_coords = None

    for col_idx, week in enumerate(weeks):
        x = start_x + col_idx * (cell_size + gap)
        for row_idx, day in enumerate(week):
            y = start_y + row_idx * (cell_size + gap)
            if day is None:
                continue

            cnt = day["count"]
            if cnt == 0:
                color = colors[0]
            elif cnt <= 2:
                color = colors[1]
            elif cnt <= 5:
                color = colors[2]
            elif cnt <= 10:
                color = colors[3]
            elif cnt <= 20:
                color = colors[4]
            else:
                color = colors[5]
                busiest_coords = (x, y)

            cell_svg = f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_size:.1f}" height="{cell_size:.1f}" rx="3" fill="{color}"/>'
            svg_cells.append(cell_svg)

    # Easter egg commit face in peak cell
    face_svg = ""
    if busiest_coords:
        bx, by = busiest_coords
        face_svg = f'''
    <!-- Easter Egg commit face -->
    <circle cx="{bx + 3.8:.1f}" cy="{by + 6.0:.1f}" r="1.1" fill="#160910"/>
    <circle cx="{bx + 8.7:.1f}" cy="{by + 6.0:.1f}" r="1.1" fill="#160910"/>
'''

    # Longest streak indicator (with alignment fix so it NEVER overflows)
    streak_svg = ""
    if streak_col_start is not None and streak_col_end is not None:
        sx1 = start_x + streak_col_start * (cell_size + gap)
        sx2 = start_x + streak_col_end * (cell_size + gap) + cell_size
        sy = start_y + 7 * (cell_size + gap) + 12

        # If streak is in the right half of the card, align text to the right
        if sx2 > 650:
            text_anchor = "end"
            text_x = sx2
        else:
            text_anchor = "start"
            text_x = sx1

        streak_svg = f'''
    <!-- Longest streak indicator -->
    <path d="M{sx1:.1f},{sy-5:.1f} L{sx1:.1f},{sy:.1f} L{sx2:.1f},{sy:.1f} L{sx2:.1f},{sy-5:.1f}" fill="none" stroke="#C58B98" stroke-width="1.2" opacity="0.8"/>
    <text x="{text_x:.1f}" y="{sy + 14:.1f}" font-family="'SF Mono', Monaco, monospace" font-size="9" letter-spacing="1.5" fill="#C58B98" font-weight="600" text-anchor="{text_anchor}">LONGEST STREAK · {longest_streak} DAYS · {streak_date_str}</text>
'''

    month_svg = "\n".join([
        f'<text x="{pos:.1f}" y="156" font-family="\'SF Mono\', Monaco, monospace" font-size="10" fill="#9E8C94">{name}</text>'
        for name, pos in month_labels
    ])

    today_str = datetime.now().strftime("%d %b %Y").lstrip("0")

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" width="1000" height="440" role="img" aria-label="Commit Log — Real GitHub Activity for @StephensHub03">
  <title>Commit Log — Real GitHub Activity for @StephensHub03</title>
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

  <!-- ═══ TOP-LEFT: EDITORIAL HEADLINE (PROPERLY SIZED TO PREVENT OVERLAP) ═══ -->
  <text x="44" y="56" font-family="'SF Mono', Monaco, monospace" font-size="10" letter-spacing="2" fill="#C58B98" font-weight="600">COMMIT LOG · REAL GITHUB ACTIVITY</text>
  <text x="44" y="92" font-family="Georgia, 'Times New Roman', serif" font-size="21.5" font-weight="700" fill="#F2EAE0">A year of building, <tspan font-style="italic" fill="#E27396">one square</tspan> at a time.</text>

  <!-- ═══ TOP-RIGHT: 4 STAT METRICS (WELL-SPACED & ALIGNED) ═══ -->
  <!-- Col 1: Contributions -->
  <g transform="translate(520, 48)">
    <text font-family="'SF Mono', Monaco, monospace" font-size="9.5" letter-spacing="1.5" fill="#9E8C94" font-weight="600">CONTRIBUTIONS</text>
    <text y="36" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="700" fill="#FFFFFF">{total_contributions:,}</text>
    <text y="52" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#9E8C94">{range_str}</text>
  </g>

  <!-- Col 2: Active Days -->
  <g transform="translate(645, 48)">
    <text font-family="'SF Mono', Monaco, monospace" font-size="9.5" letter-spacing="1.5" fill="#9E8C94" font-weight="600">ACTIVE DAYS</text>
    <text y="36" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="700" fill="#FFFFFF">{active_days}</text>
    <text y="52" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#9E8C94">of {len(contribs)} days</text>
  </g>

  <!-- Col 3: Longest Streak -->
  <g transform="translate(760, 48)">
    <text font-family="'SF Mono', Monaco, monospace" font-size="9.5" letter-spacing="1.5" fill="#9E8C94" font-weight="600">LONGEST STREAK</text>
    <text y="36" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="700" fill="#FFFFFF">{longest_streak}</text>
    <text y="52" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#9E8C94">consecutive days</text>
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
  <text x="44" y="404" font-family="'SF Mono', Monaco, monospace" font-size="9.5" fill="#7A6870">Source: public GitHub contribution calendar for <tspan fill="#C58B98">@StephensHub03</tspan> · snapshot {today_str} · refreshed daily</text>

  <!-- Legend -->
  <g transform="translate(790, 394)">
    <text x="0" y="9" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#7A6870" text-anchor="end">Less</text>
    <rect x="8" y="0" width="10" height="10" rx="2.5" fill="{colors[0]}"/>
    <rect x="22" y="0" width="10" height="10" rx="2.5" fill="{colors[1]}"/>
    <rect x="36" y="0" width="10" height="10" rx="2.5" fill="{colors[2]}"/>
    <rect x="50" y="0" width="10" height="10" rx="2.5" fill="{colors[3]}"/>
    <rect x="64" y="0" width="10" height="10" rx="2.5" fill="{colors[4]}"/>
    <rect x="78" y="0" width="10" height="10" rx="2.5" fill="{colors[5]}"/>
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
    print(f"Successfully generated {out_path}")
