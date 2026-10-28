#!/usr/bin/env python3
"""
Generate the editorial obsidian-wine GitHub contribution graph SVG from
GitHub's own contribution calendar.

Data pipeline (each step must pass, otherwise nothing is written and the
last verified SVG/JSON stay in place):

  1. Fetch the calendar from GitHub GraphQL as the profile owner. Only the
     owner's own token sees private-repo contributions; any other token
     (e.g. the Actions GITHUB_TOKEN) silently returns a smaller,
     public-only calendar, which is what made earlier graphs wrong.
  2. Validate the calendar structure (contiguous dates, Sunday-first weeks,
     weekday/date agreement, GitHub levels, staleness).
  3. Cross-check every day's count and level against the public profile
     at https://github.com/users/<user>/contributions.
  4. Render cells using GitHub's contributionLevel mapped 1:1 onto the
     theme palette (no invented thresholds), and write the SVG plus the
     verified JSON snapshot.

Usage:
  GH_TOKEN=<owner PAT> python3 scripts/generate_activity_graph.py
  python3 scripts/generate_activity_graph.py --from-json   # re-render saved snapshot
"""

import argparse
import html
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone

USERNAME = "StephensHub03"
SVG_PATH = "assets/section-06-activity.svg"
JSON_PATH = "assets/section-06-activity.json"
PROFILE_URL = f"https://github.com/users/{USERNAME}/contributions"

# Burgundy & Antique Gold theme palette, one swatch per GitHub contribution level
COLORS = {
    0: "#200c19",  # NONE            - empty dark wine cell
    1: "#4a182b",  # FIRST_QUARTILE  - burgundy
    2: "#7d2243",  # SECOND_QUARTILE - medium wine
    3: "#b53360",  # THIRD_QUARTILE  - bright wine
    4: "#e25b86",  # FOURTH_QUARTILE - vibrant rose
}

LEVEL_MAP = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}

QUERY = """
query($login: String!) {
  viewer { login }
  user(login: $login) {
    login
    contributionsCollection {
      startedAt
      endedAt
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        colors
        weeks {
          firstDay
          contributionDays {
            date
            weekday
            contributionCount
            contributionLevel
            color
          }
        }
      }
    }
  }
}
"""


class ValidationError(Exception):
    pass


def parse_date(s):
    # Calendar dates are already in GitHub's calendar timezone; never convert them.
    return date.fromisoformat(s)


def gh_weekday(d):
    return (d.weekday() + 1) % 7  # GitHub: Sunday=0 ... Saturday=6


# ─── Fetch ────────────────────────────────────────────────────────────────

def get_auth_token():
    """GH_TOKEN secret/env first, then the local GitHub CLI login."""
    token = os.environ.get("GH_TOKEN", "").strip()
    if token:
        return token
    try:
        res = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=10)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return None


def fetch_calendar(token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USERNAME}}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": f"{USERNAME}-activity-graph",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    if result.get("errors"):
        raise ValidationError(f"GraphQL errors: {[e.get('message') for e in result['errors']]}")
    data = result.get("data") or {}
    user = data.get("user")
    if not user:
        raise ValidationError(f"User {USERNAME} not found")
    if user["login"].lower() != USERNAME.lower():
        raise ValidationError(f"Queried user mismatch: expected {USERNAME}, got {user['login']}")

    viewer = (data.get("viewer") or {}).get("login", "")
    if viewer.lower() != USERNAME.lower():
        raise ValidationError(
            f"Token belongs to '{viewer}', not {USERNAME}. Only the owner's token sees private "
            f"contributions, so the calendar would not match the profile. Set GH_TOKEN to a "
            f"personal access token of {USERNAME}."
        )

    cc = user["contributionsCollection"]
    cal = cc["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    return {
        "username": USERNAME,
        "source": "GitHub GraphQL API · user.contributionsCollection.contributionCalendar",
        "fetchedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "startedAt": cc["startedAt"],
        "endedAt": cc["endedAt"],
        "totalContributions": cal["totalContributions"],
        "restrictedContributionsCount": cc["restrictedContributionsCount"],
        "githubColors": cal["colors"],
        "profileVerified": False,
        "days": [
            {
                "date": d["date"],
                "weekday": d["weekday"],
                "count": d["contributionCount"],
                "level": d["contributionLevel"],
                "color": d["color"],
            }
            for d in days
        ],
    }


def fetch_profile_html():
    req = urllib.request.Request(PROFILE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8")


# ─── Validate ─────────────────────────────────────────────────────────────

def validate_calendar(snap, now=None):
    """Structural checks on the GraphQL calendar. Returns a list of warnings."""
    days = snap["days"]
    if not days:
        raise ValidationError("Calendar contains no days")

    warnings = []
    dates = [parse_date(d["date"]) for d in days]
    if len(set(dates)) != len(dates):
        raise ValidationError("Calendar contains duplicate dates")
    for prev, cur in zip(dates, dates[1:]):
        if cur - prev != timedelta(days=1):
            raise ValidationError(f"Calendar is not contiguous between {prev} and {cur}")

    for d, dt in zip(days, dates):
        if d["weekday"] != gh_weekday(dt):
            raise ValidationError(f"{d['date']}: weekday {d['weekday']} does not match its date")
        if d["level"] not in LEVEL_MAP:
            raise ValidationError(f"{d['date']}: unknown contribution level {d['level']}")
        if d["count"] < 0:
            raise ValidationError(f"{d['date']}: negative count")
        if (d["count"] == 0) != (d["level"] == "NONE"):
            raise ValidationError(f"{d['date']}: count {d['count']} inconsistent with level {d['level']}")

    if len(days) > 7 * 54:
        raise ValidationError(f"Calendar spans {len(days)} days, more than a year")

    # startedAt is local midnight of the first day in GitHub's calendar timezone,
    # which gives the offset used to read endedAt as a calendar date.
    started = datetime.fromisoformat(snap["startedAt"].replace("Z", "+00:00"))
    ended = datetime.fromisoformat(snap["endedAt"].replace("Z", "+00:00"))
    since_midnight = started - started.replace(hour=0, minute=0, second=0, microsecond=0)
    offset = (timedelta(days=1) - since_midnight) % timedelta(days=1)
    if (started + offset).date() != dates[0] or (ended + offset).date() != dates[-1]:
        raise ValidationError(
            f"Calendar days {dates[0]}..{dates[-1]} do not match collection window "
            f"{snap['startedAt']}..{snap['endedAt']}"
        )
    now = now or datetime.now(timezone.utc)
    if (now.date() - dates[-1]).days > 2:
        raise ValidationError(f"Calendar is stale: last day {dates[-1]}, now {now.date()}")

    summed = sum(d["count"] for d in days)
    if summed != snap["totalContributions"]:
        # Not fatal: GitHub's total is authoritative and is what we display.
        warnings.append(f"Daily counts sum to {summed}, API totalContributions is {snap['totalContributions']}")
    return warnings


def parse_profile(page):
    """Extract {date: (count, level)} and the headline total from the profile calendar HTML."""
    cells = {}
    ids = {}
    for tag in re.findall(r"<td\b[^>]*\bContributionCalendar-day\b[^>]*>", page):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
        if "data-date" in attrs:
            ids[attrs.get("id")] = attrs["data-date"]
            cells[attrs["data-date"]] = [None, int(attrs.get("data-level", -1))]
    for cid, text in re.findall(r'<tool-tip\b[^>]*\bfor="([^"]+)"[^>]*>([^<]*)</tool-tip>', page):
        if cid in ids:
            m = re.match(r"\s*([\d,]+) contributions? on", html.unescape(text))
            cells[ids[cid]][0] = int(m.group(1).replace(",", "")) if m else 0
    m = re.search(r"([\d,]+)\s+contributions?\s+in the last year", re.sub(r"\s+", " ", page))
    total = int(m.group(1).replace(",", "")) if m else None
    return {k: tuple(v) for k, v in cells.items()}, total


def verify_against_profile(snap, page):
    cells, total = parse_profile(page)
    if not cells:
        raise ValidationError("Could not parse any days from the profile calendar")
    problems = []
    if total is not None and total != snap["totalContributions"]:
        problems.append(f"profile total {total} != API total {snap['totalContributions']}")
    api = {d["date"]: (d["count"], LEVEL_MAP[d["level"]]) for d in snap["days"]}
    if set(api) != set(cells):
        problems.append(
            f"date range differs: API {min(api)}..{max(api)}, profile {min(cells)}..{max(cells)}"
        )
    for day in sorted(set(api) & set(cells)):
        if api[day] != cells[day]:
            problems.append(f"{day}: API count/level {api[day]} != profile {cells[day]}")
    if problems:
        raise ValidationError("Profile mismatch:\n  " + "\n  ".join(problems[:20]))


# ─── Render ───────────────────────────────────────────────────────────────

def group_weeks(days):
    """Group contiguous days into Sunday-first week columns, as GitHub does."""
    weeks = []
    for d in days:
        if not weeks or d["weekday"] == 0:
            weeks.append([])
        weeks[-1].append(d)
    return weeks


def month_labels(weeks):
    """GitHub's rule: label each run of columns by the month of the week's first day,
    hiding runs too short to fit a label (the partial leading/trailing month)."""
    runs = []
    for c_idx, w in enumerate(weeks):
        m = parse_date(w[0]["date"]).strftime("%b")
        if runs and runs[-1][0] == m:
            runs[-1][2] += 1
        else:
            runs.append([m, c_idx, 1])
    return [(name, col) for name, col, span in runs if span >= 3]


def compute_stats(snap, weeks):
    days = snap["days"]
    active = sum(1 for d in days if d["count"] > 0)
    busiest = max(days, key=lambda d: d["count"])

    col_of = {d["date"]: c for c, w in enumerate(weeks) for d in w}
    longest = (0, None, None)
    run_start = None
    for i, d in enumerate(days):
        if d["count"] > 0:
            run_start = run_start if run_start is not None else i
            length = i - run_start + 1
            if length > longest[0]:
                longest = (length, days[run_start], d)
        else:
            run_start = None
    return {
        "active": active,
        "busiest": busiest,
        "streak": longest[0],
        "streak_start": longest[1],
        "streak_end": longest[2],
        "streak_cols": (col_of[longest[1]["date"]], col_of[longest[2]["date"]]) if longest[0] else None,
    }


def fmt_day(s, upper=False):
    out = parse_date(s).strftime("%d %b %Y").lstrip("0")
    return out.upper() if upper else out


def render_svg(snap):
    days = snap["days"]
    weeks = group_weeks(days)
    stats = compute_stats(snap, weeks)
    total_contributions = snap["totalContributions"]

    range_str = f"{parse_date(days[0]['date']).strftime('%b %Y')} – {parse_date(days[-1]['date']).strftime('%b %Y')}"
    busiest_count = stats["busiest"]["count"]
    busiest_date_str = fmt_day(stats["busiest"]["date"]) if busiest_count > 0 else "None"
    longest_streak = stats["streak"]
    streak_subtext = "consecutive days" if longest_streak != 1 else "consecutive day"

    # Layout parameters matching the card aesthetic
    cell_size = 12.5
    gap = 4.0
    start_x = 94.0
    start_y = 175.0

    month_svg = "\n".join(
        f'  <text x="{start_x + col * (cell_size + gap):.1f}" y="156" font-family="\'SF Mono\', Monaco, monospace" font-size="10" fill="#9E8C94">{name}</text>'
        for name, col in month_labels(weeks)
    )

    # Heatmap cells: GitHub's contributionLevel mapped 1:1 onto the theme palette
    svg_cells = []
    peak_coords = None
    for c_idx, w in enumerate(weeks):
        x = start_x + c_idx * (cell_size + gap)
        for d in w:
            y = start_y + d["weekday"] * (cell_size + gap)
            lvl = LEVEL_MAP[d["level"]]
            if d is stats["busiest"] and busiest_count >= 10:
                peak_coords = (x, y)
            svg_cells.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_size:.1f}" height="{cell_size:.1f}" rx="3" '
                f'fill="{COLORS[lvl]}" data-date="{d["date"]}" data-count="{d["count"]}" data-level="{lvl}"/>'
            )

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
    if longest_streak > 1:
        col_start, col_end = stats["streak_cols"]
        sx1 = start_x + col_start * (cell_size + gap)
        sx2 = start_x + col_end * (cell_size + gap) + cell_size
        sy = start_y + 7 * (cell_size + gap) + 12
        streak_date_str = f"{fmt_day(stats['streak_start']['date'], True)} — {fmt_day(stats['streak_end']['date'], True)}"

        # Align text nicely
        text_x = min(max(sx2 + 20, 600.0), 964.5)
        streak_svg = f'''
    <!-- Longest streak indicator -->
    <path d="M{sx1:.1f},{sy-5:.1f} L{sx1:.1f},{sy:.1f} L{sx2:.1f},{sy:.1f} L{sx2:.1f},{sy-5:.1f}" fill="none" stroke="#C58B98" stroke-width="1.2" opacity="0.8"/>
    <text x="{text_x:.1f}" y="{sy + 14:.1f}" font-family="'SF Mono', Monaco, monospace" font-size="9" letter-spacing="1.5" fill="#C58B98" font-weight="600" text-anchor="end">LONGEST STREAK · {longest_streak} DAYS · {streak_date_str}</text>
'''

    fetched = datetime.fromisoformat(snap["fetchedAt"].replace("Z", "+00:00"))
    fetched_str = fetched.strftime("%d %b %Y %H:%M UTC").lstrip("0")

    legend_svg = "\n".join(
        f'    <rect x="{8 + i * 14}" y="0" width="10" height="10" rx="2.5" fill="{COLORS[i]}"/>'
        for i in range(5)
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" width="1000" height="440" role="img" aria-label="Commit Log — {total_contributions} GitHub contributions for @{USERNAME}, {days[0]['date']} to {days[-1]['date']}">
  <title>Commit Log — {total_contributions} GitHub contributions for @{USERNAME}, {days[0]['date']} to {days[-1]['date']}</title>
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
  <!-- Col 1: Contributions (GitHub's totalContributions) -->
  <g transform="translate(520, 48)">
    <text font-family="'SF Mono', Monaco, monospace" font-size="9.5" letter-spacing="1.5" fill="#9E8C94" font-weight="600">CONTRIBUTIONS</text>
    <text y="36" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="700" fill="#FFFFFF">{total_contributions:,}</text>
    <text y="52" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#9E8C94">{range_str}</text>
  </g>

  <!-- Col 2: Active Days -->
  <g transform="translate(645, 48)">
    <text font-family="'SF Mono', Monaco, monospace" font-size="9.5" letter-spacing="1.5" fill="#9E8C94" font-weight="600">ACTIVE DAYS</text>
    <text y="36" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="700" fill="#FFFFFF">{stats["active"]}</text>
    <text y="52" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#9E8C94">of {len(days)} days</text>
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
  <text x="44" y="404" font-family="'SF Mono', Monaco, monospace" font-size="9.5" fill="#7A6870">Source: GitHub contribution calendar for <tspan fill="#C58B98">@{USERNAME}</tspan> · fetched {fetched_str}</text>

  <!-- Legend: GitHub's five contribution levels -->
  <g transform="translate(804, 394)">
    <text x="0" y="9" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#7A6870" text-anchor="end">Less</text>
{legend_svg}
    <text x="82" y="9" font-family="'SF Mono', Monaco, monospace" font-size="9" fill="#7A6870">More</text>
  </g>
</svg>
'''


# ─── Main ─────────────────────────────────────────────────────────────────

def write_atomic(path, content):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, path)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from-json", action="store_true", help=f"re-render from the saved {JSON_PATH} (no network)")
    ap.add_argument("--skip-profile-check", action="store_true", help="do not cross-check the public profile")
    args = ap.parse_args(argv)

    try:
        if args.from_json:
            with open(JSON_PATH, encoding="utf-8") as f:
                snap = json.load(f)
            for w in validate_calendar(snap, now=datetime.fromisoformat(snap["fetchedAt"].replace("Z", "+00:00"))):
                print(f"Warning: {w}")
        else:
            token = get_auth_token()
            if not token:
                raise ValidationError("No token: set GH_TOKEN (owner PAT) or log in with `gh auth login`")
            print(f"Fetching contribution calendar for @{USERNAME} from GitHub GraphQL...")
            snap = fetch_calendar(token)
            for w in validate_calendar(snap):
                print(f"Warning: {w}")
            if args.skip_profile_check:
                print("Warning: profile cross-check skipped; snapshot marked profileVerified=false")
            else:
                print(f"Cross-checking against {PROFILE_URL} ...")
                verify_against_profile(snap, fetch_profile_html())
                snap["profileVerified"] = True
        svg = render_svg(snap)
    except Exception as e:  # keep the last verified graph on any failure
        print(f"ERROR: {e}\nNo files were changed; the last verified graph is kept.", file=sys.stderr)
        return 1

    days = snap["days"]
    print(f"totalContributions={snap['totalContributions']} "
          f"range={days[0]['date']}..{days[-1]['date']} ({len(days)} days) "
          f"fetchedAt={snap['fetchedAt']} profileVerified={snap['profileVerified']}")
    if not args.from_json:
        write_atomic(JSON_PATH, json.dumps(snap, indent=1) + "\n")
    write_atomic(SVG_PATH, svg)
    print(f"Wrote {SVG_PATH}" + ("" if args.from_json else f" and {JSON_PATH}"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
