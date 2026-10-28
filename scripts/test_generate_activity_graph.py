#!/usr/bin/env python3
"""Tests for generate_activity_graph.py. Run: python3 -m unittest scripts/test_generate_activity_graph.py"""

import copy
import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_activity_graph as g  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEVELS = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]


def make_snap(first="2025-10-26", last="2026-10-28", counts=None):
    """Structurally valid calendar in IST (UTC+05:30), like the owner's GraphQL response."""
    d0, d1 = date.fromisoformat(first), date.fromisoformat(last)
    days = []
    for i in range((d1 - d0).days + 1):
        dt = d0 + timedelta(days=i)
        c = (counts or {}).get(dt.isoformat(), 0)
        days.append({"date": dt.isoformat(), "weekday": g.gh_weekday(dt), "count": c,
                     "level": LEVELS[min(c, 4)], "color": "#ebedf0"})
    return {
        "username": g.USERNAME, "fetchedAt": f"{last}T12:00:00Z",
        "startedAt": f"{(d0 - timedelta(days=1)).isoformat()}T18:30:00Z",
        "endedAt": f"{last}T18:29:59Z",
        "totalContributions": sum(d["count"] for d in days),
        "restrictedContributionsCount": 0, "githubColors": [], "profileVerified": False, "days": days,
    }


def profile_html(snap, total=None):
    rows = []
    for i, d in enumerate(snap["days"]):
        cid = f"contribution-day-component-{d['weekday']}-{i}"
        rows.append(f'<td data-date="{d["date"]}" id="{cid}" data-level="{g.LEVEL_MAP[d["level"]]}" '
                    f'class="ContributionCalendar-day"></td>')
        text = f"{d['count']} contributions on X." if d["count"] else "No contributions on X."
        rows.append(f'<tool-tip for="{cid}" class="sr-only">{text}</tool-tip>')
    total = snap["totalContributions"] if total is None else total
    return f"<h2> {total} contributions\n in the last year </h2>" + "".join(rows)


class ValidateTests(unittest.TestCase):
    now = datetime(2026, 10, 28, 20, tzinfo=timezone.utc)

    def test_valid_calendar_passes(self):
        self.assertEqual(g.validate_calendar(make_snap(counts={"2026-10-28": 3}), now=self.now), [])

    def test_gap_rejected(self):
        snap = make_snap(); del snap["days"][100]
        with self.assertRaisesRegex(g.ValidationError, "contiguous"):
            g.validate_calendar(snap, now=self.now)

    def test_duplicate_rejected(self):
        snap = make_snap(); snap["days"].insert(5, copy.deepcopy(snap["days"][5]))
        with self.assertRaisesRegex(g.ValidationError, "duplicate"):
            g.validate_calendar(snap, now=self.now)

    def test_weekday_mismatch_rejected(self):
        snap = make_snap(); snap["days"][10]["weekday"] = (snap["days"][10]["weekday"] + 1) % 7
        with self.assertRaisesRegex(g.ValidationError, "weekday"):
            g.validate_calendar(snap, now=self.now)

    def test_count_level_inconsistency_rejected(self):
        snap = make_snap(); snap["days"][10]["count"] = 4
        with self.assertRaisesRegex(g.ValidationError, "inconsistent"):
            g.validate_calendar(snap, now=self.now)

    def test_window_shift_rejected(self):
        # A calendar computed in UTC would start/end a day off from an IST collection window.
        snap = make_snap(); snap["startedAt"] = "2025-10-27T00:00:00Z"
        with self.assertRaisesRegex(g.ValidationError, "collection window"):
            g.validate_calendar(snap, now=self.now)

    def test_stale_rejected(self):
        with self.assertRaisesRegex(g.ValidationError, "stale"):
            g.validate_calendar(make_snap(), now=self.now + timedelta(days=5))

    def test_total_differs_from_sum_is_warning_not_error(self):
        snap = make_snap(); snap["totalContributions"] += 1
        self.assertEqual(len(g.validate_calendar(snap, now=self.now)), 1)


class FetchTests(unittest.TestCase):
    def test_non_owner_token_rejected(self):
        # Root cause of the old 93-vs-238 graph: a non-owner token returns a public-only calendar.
        body = json.dumps({"data": {"viewer": {"login": "github-actions[bot]"},
                                    "user": {"login": g.USERNAME, "contributionsCollection": {}}}}).encode()
        resp = mock.MagicMock(); resp.__enter__.return_value.read.return_value = body
        with mock.patch("urllib.request.urlopen", return_value=resp):
            with self.assertRaisesRegex(g.ValidationError, "private contributions"):
                g.fetch_calendar("token")


def pages(default, years=None):
    """Fake profile fetcher: '' -> rolling-window page, '?from=YYYY-..' -> calendar-year page."""
    return lambda q: default if not q else years[q[6:10]]


class ProfileTests(unittest.TestCase):
    def test_matching_profile_passes(self):
        snap = make_snap(counts={"2026-07-12": 27, "2026-10-28": 1})
        g.verify_against_profile(snap, pages(profile_html(snap)))

    def test_count_mismatch_detected(self):
        snap = make_snap(counts={"2026-07-12": 2})
        other = copy.deepcopy(snap); other["days"][-1].update(count=1, level="FIRST_QUARTILE")
        with self.assertRaisesRegex(g.ValidationError, "2026-10-28"):
            g.verify_against_profile(snap, pages(profile_html(other, total=snap["totalContributions"])))

    def test_total_mismatch_detected(self):
        snap = make_snap()
        with self.assertRaisesRegex(g.ValidationError, "profile total 93"):
            g.verify_against_profile(snap, pages(profile_html(snap, total=93)))

    def test_utc_profile_one_day_behind_ist_api_passes(self):
        # Actions run at 18:33 UTC: the IST API calendar already has 29 Oct (1 contribution),
        # the logged-out profile still ends on 28 Oct UTC. Totals 240 vs 239.
        snap = make_snap(last="2026-10-29", counts={"2026-07-12": 27, "2026-10-29": 1})
        utc = make_snap(last="2026-10-28", counts={"2026-07-12": 27})
        year = make_snap(first="2026-01-01", last="2026-12-31", counts={"2026-07-12": 27, "2026-10-29": 1})
        with mock.patch("sys.stdout"):
            g.verify_against_profile(snap, pages(profile_html(utc), {"2026": profile_html(year)}))

    def test_edge_day_count_mismatch_detected(self):
        snap = make_snap(last="2026-10-29", counts={"2026-10-29": 2})
        utc = make_snap(last="2026-10-28")
        year = make_snap(first="2026-01-01", last="2026-12-31", counts={"2026-10-29": 1})
        with self.assertRaisesRegex(g.ValidationError, "2026-10-29: API count 2 != profile 1"):
            g.verify_against_profile(snap, pages(profile_html(utc), {"2026": profile_html(year)}))


class RenderTests(unittest.TestCase):
    def test_month_labels_follow_github_rule(self):
        # Labels GitHub's own profile showed for this exact window.
        weeks = g.group_weeks(make_snap()["days"])
        self.assertEqual(len(weeks), 53)
        self.assertEqual([m for m, _ in g.month_labels(weeks)],
                         ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"])

    def test_no_invented_levels(self):
        snap = make_snap(counts={"2026-07-12": 27})
        fills = set(re.findall(r'data-level="\d"', g.render_svg(snap)))
        self.assertLessEqual(fills, {f'data-level="{i}"' for i in range(5)})


class CommittedSnapshotTests(unittest.TestCase):
    """The committed SVG must render exactly the committed, verified JSON snapshot."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(REPO, g.JSON_PATH), encoding="utf-8") as f:
            cls.snap = json.load(f)
        with open(os.path.join(REPO, g.SVG_PATH), encoding="utf-8") as f:
            cls.svg = f.read()

    def test_snapshot_valid(self):
        fetched = datetime.fromisoformat(self.snap["fetchedAt"].replace("Z", "+00:00"))
        g.validate_calendar(self.snap, now=fetched)
        self.assertTrue(self.snap["profileVerified"])

    def test_every_cell_maps_to_its_date_and_level(self):
        cells = re.findall(r'<rect x="([\d.]+)" y="([\d.]+)"[^>]*fill="(#\w+)" data-date="([\d-]+)" '
                           r'data-count="(\d+)" data-level="(\d)"', self.svg)
        days = self.snap["days"]
        self.assertEqual(len(cells), len(days))
        self.assertEqual([c[3] for c in cells], [d["date"] for d in days])
        first = date.fromisoformat(days[0]["date"])
        week0 = first - timedelta(days=g.gh_weekday(first))
        for (x, y, fill, dt, cnt, lvl), d in zip(cells, days):
            col = (date.fromisoformat(dt) - week0).days // 7
            self.assertAlmostEqual(float(x), 94.0 + col * 16.5, places=1, msg=dt)
            self.assertAlmostEqual(float(y), 175.0 + d["weekday"] * 16.5, places=1, msg=dt)
            self.assertEqual(int(cnt), d["count"])
            self.assertEqual(int(lvl), g.LEVEL_MAP[d["level"]])
            self.assertEqual(fill, g.COLORS[int(lvl)])

    def test_headline_total_is_api_total(self):
        self.assertIn(f'>{self.snap["totalContributions"]:,}</text>', self.svg)

    def test_no_token_in_outputs(self):
        for text in (self.svg, json.dumps(self.snap)):
            self.assertNotRegex(text, r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_")


class FailureKeepsLastGraphTests(unittest.TestCase):
    def test_failed_fetch_writes_nothing(self):
        tmp = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(tmp, "assets"))
            for p in (g.SVG_PATH, g.JSON_PATH):
                with open(os.path.join(tmp, p), "w") as f:
                    f.write("last verified")
            cwd = os.getcwd(); os.chdir(tmp)
            try:
                with mock.patch.object(g, "get_auth_token", return_value="x"), \
                     mock.patch.object(g, "fetch_calendar", side_effect=g.ValidationError("boom")), \
                     mock.patch("sys.stderr"), mock.patch("sys.stdout"):
                    self.assertEqual(g.main([]), 1)
            finally:
                os.chdir(cwd)
            for p in (g.SVG_PATH, g.JSON_PATH):
                with open(os.path.join(tmp, p)) as f:
                    self.assertEqual(f.read(), "last verified")
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
