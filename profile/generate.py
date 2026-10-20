"""Generate the profile README images (light and dark SVGs) from config.toml.

Fonts are subset to the glyphs actually used and embedded as WOFF2 data URIs,
because GitHub serves README images through a proxy that blocks external fonts.

Usage: python profile/generate.py            (needs: pip install fonttools brotli)
       GITHUB_TOKEN=... raises the API rate limit when reading milestones.
"""

from __future__ import annotations

import base64
import io
import json
import os
import sys
import tomllib
import urllib.request
from html import escape
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "assets"
FONT_DIR = HERE / "fonts"

# family -> weight -> font files (latin first, then latin-ext for Polish letters)
FONT_FILES = {
    "SG": {
        500: ["space-grotesk-latin-500-normal.woff2", "space-grotesk-latin-ext-500-normal.woff2"],
        700: ["space-grotesk-latin-700-normal.woff2", "space-grotesk-latin-ext-700-normal.woff2"],
    },
    "Plex": {
        400: ["ibm-plex-sans-latin-400-normal.woff2", "ibm-plex-sans-latin-ext-400-normal.woff2"],
        500: ["ibm-plex-sans-latin-500-normal.woff2", "ibm-plex-sans-latin-ext-500-normal.woff2"],
    },
}

THEMES = {
    "light": {
        "surface": "#FFFFFF", "border": "#D3DCE6", "text": "#12233A", "muted": "#566679",
        "faint": "#E6ECF2", "edge": "#C6D2DE", "node": "#FFFFFF",
        "active": "#B06A0B", "done": "#167A6B",
    },
    "dark": {
        "surface": "#101B2A", "border": "#24364B", "text": "#E4EBF3", "muted": "#90A2B6",
        "faint": "#1C2B3E", "edge": "#2C425C", "node": "#0D1117",
        "active": "#F2AE45", "done": "#4CC2B0",
    },
}

W = 840  # GitHub's README column is ~838 px wide


# ---------------------------------------------------------------- fonts
class Fonts:
    def __init__(self) -> None:
        self.fonts: dict[tuple[str, int], list[tuple[str, TTFont, set[int]]]] = {}
        for fam, weights in FONT_FILES.items():
            for wt, files in weights.items():
                entries = []
                for f in files:
                    font = TTFont(FONT_DIR / f)
                    entries.append((f, font, set(font.getBestCmap())))
                self.fonts[(fam, wt)] = entries

    def width(self, s: str, fam: str, wt: int, size: float) -> float:
        total = 0.0
        for ch in s:
            for _, font, cmap in self.fonts[(fam, wt)]:
                if ord(ch) in cmap:
                    glyph = font.getBestCmap()[ord(ch)]
                    total += font["hmtx"][glyph][0] / font["head"].unitsPerEm
                    break
            else:
                total += 0.55
        return total * size

    def wrap(self, s: str, fam: str, wt: int, size: float, max_w: float) -> list[str]:
        lines, line = [], ""
        for word in s.split():
            trial = f"{line} {word}".strip()
            if self.width(trial, fam, wt, size) <= max_w or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    def css(self, used: dict[tuple[str, int], set[str]]) -> str:
        """@font-face rules with subset fonts for exactly the characters used."""
        rules = []
        for (fam, wt), chars in sorted(used.items()):
            codepoints = {ord(c) for c in chars if not c.isspace()} | {0x20}
            for fname, _, cmap in self.fonts[(fam, wt)]:
                cps = sorted(codepoints & cmap)
                if not cps:
                    continue
                font = TTFont(FONT_DIR / fname)
                opts = subset.Options()
                opts.flavor = "woff2"
                opts.layout_features = ["kern", "liga"]
                sub = subset.Subsetter(opts)
                sub.populate(unicodes=cps)
                sub.subset(font)
                buf = io.BytesIO()
                font.flavor = "woff2"
                font.save(buf)
                data = base64.b64encode(buf.getvalue()).decode()
                urange = ",".join(f"U+{cp:04X}" for cp in cps)
                rules.append(
                    f"@font-face{{font-family:'{fam}';font-weight:{wt};"
                    f"src:url(data:font/woff2;base64,{data}) format('woff2');unicode-range:{urange}}}"
                )
                codepoints -= set(cps)
        return "\n".join(rules)


FONTS = Fonts()


# ---------------------------------------------------------------- svg canvas
class Svg:
    def __init__(self, width: int, height: int, theme: str, title: str) -> None:
        self.w, self.h, self.t, self.title = width, height, THEMES[theme], title
        self.parts: list[str] = []
        self.used: dict[tuple[str, int], set[str]] = {}
        self.extra_css = ""

    def add(self, s: str) -> None:
        self.parts.append(s)

    def text(self, x, y, s, fam="Plex", wt=400, size=15, fill="text", anchor="start", extra="") -> None:
        self.used.setdefault((fam, wt), set()).update(s)
        color = self.t.get(fill, fill)
        self.add(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-weight="{wt}" '
            f'font-size="{size}" fill="{color}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'
        )

    def render(self) -> str:
        fallback = (
            "text{font-family:'Plex',system-ui,-apple-system,'Segoe UI',sans-serif}"
            "text[font-family='SG']{font-family:'SG',system-ui,sans-serif}"
        )
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{escape(self.title)}">'
            f"<title>{escape(self.title)}</title>"
            f"<style>{FONTS.css(self.used)}\n{fallback}{self.extra_css}</style>"
            + "".join(self.parts)
            + "</svg>\n"
        )


# ---------------------------------------------------------------- header
# A small service mesh: pods (rounded squares) each with a sidecar proxy (dot).
# Edges connect sidecars; one request travels a route and ends in a handshake.
NODES = {
    "a": (548, 58), "b": (636, 34), "c": (724, 70), "d": (806, 40),
    "e": (590, 138), "f": (680, 124), "g": (770, 150), "h": (652, 196), "i": (812, 206),
}
EDGES = [("a", "b"), ("b", "c"), ("c", "d"), ("a", "e"), ("b", "f"), ("c", "f"), ("c", "g"),
         ("d", "g"), ("e", "f"), ("f", "g"), ("e", "h"), ("f", "h"), ("g", "i"), ("h", "i")]
ROUTE = ["a", "e", "f", "c", "d"]


def sidecar(n: str) -> tuple[float, float]:
    x, y = NODES[n]
    return x + 9, y + 9


def header(cfg: dict, theme: str) -> str:
    t = THEMES[theme]
    h = 236
    svg = Svg(W, h, theme, f"{cfg['name']}. {cfg['role']}. {cfg['about']}")

    # text column
    svg.text(2, 74, cfg["name"], fam="SG", wt=700, size=46)
    svg.text(2, 112, cfg["role"], size=17)
    y = 146
    for line in FONTS.wrap(cfg["about"], "Plex", 400, 16, 470):
        svg.text(2, y, line, size=16, fill="muted")
        y += 24

    # mesh
    for a, b in EDGES:
        (x1, y1), (x2, y2) = sidecar(a), sidecar(b)
        svg.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["edge"]}" stroke-width="1.2"/>')
    for i in range(len(ROUTE) - 1):
        (x1, y1), (x2, y2) = sidecar(ROUTE[i]), sidecar(ROUTE[i + 1])
        svg.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["active"]}" '
                f'stroke-opacity=".35" stroke-width="1.6"/>')
    for n, (x, y) in NODES.items():
        on_route = n in (ROUTE[0], ROUTE[-1])
        stroke = t["active"] if on_route else t["muted"]
        svg.add(f'<rect x="{x - 9}" y="{y - 9}" width="18" height="18" rx="4" fill="{t["node"]}" '
                f'stroke="{stroke}" stroke-width="1.4"/>')
        sx, sy = sidecar(n)
        svg.add(f'<circle cx="{sx}" cy="{sy}" r="3.6" fill="{t["node"]}" stroke="{stroke}" stroke-width="1.4"/>')

    # one request every 7 s: travel (0-40 %), handshake ring at the target (40-62 %)
    path = "M" + " L".join(f"{x},{y}" for x, y in (sidecar(n) for n in ROUTE))
    ex, ey = sidecar(ROUTE[-1])
    svg.add(
        f'<g class="motion"><circle r="4" fill="{t["active"]}">'
        f'<animateMotion dur="7s" repeatCount="indefinite" path="{path}" '
        f'keyPoints="0;1;1" keyTimes="0;0.4;1" calcMode="linear"/>'
        f'<animate attributeName="opacity" dur="7s" repeatCount="indefinite" '
        f'values="1;1;0;0" keyTimes="0;0.4;0.41;1"/></circle>'
        f'<circle cx="{ex}" cy="{ey}" fill="none" stroke="{t["active"]}" stroke-width="1.5" opacity="0">'
        f'<animate attributeName="r" dur="7s" repeatCount="indefinite" values="4;4;17;17" keyTimes="0;0.4;0.62;1"/>'
        f'<animate attributeName="opacity" dur="7s" repeatCount="indefinite" values="0;0;.9;0;0" '
        f'keyTimes="0;0.399;0.4;0.62;1"/></circle></g>'
    )
    svg.extra_css = "@media (prefers-reduced-motion:reduce){.motion{display:none}}"
    return svg.render()


# ---------------------------------------------------------------- project panels
PAD = 28
LEFT_W = 500
RIGHT_X = 588
RIGHT_W = W - RIGHT_X - PAD


def chips(svg: Svg, items: list[str], x0: float, y0: float, max_w: float) -> float:
    """Draw stack chips; return the y below the last row."""
    t, x, y = svg.t, x0, y0
    for item in items:
        w = FONTS.width(item, "Plex", 400, 12.5) + 18
        if x + w > x0 + max_w:
            x, y = x0, y + 30
        svg.add(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="22" rx="4" fill="none" '
                f'stroke="{t["border"]}"/>')
        svg.text(x + 9, y + 15.5, item, size=12.5, fill="muted")
        x += w + 7
    return y + 22


def panel(p: dict, theme: str, track: list[dict], now: str, detail: str, footnote: str = "") -> str:
    t = THEMES[theme]
    desc = FONTS.wrap(p["description"], "Plex", 400, 15, LEFT_W)
    stack_rows = 1
    x = 0.0
    for item in p["stack"]:
        w = FONTS.width(item, "Plex", 400, 12.5) + 25
        if x + w > LEFT_W:
            stack_rows, x = stack_rows + 1, 0
        x += w
    h = PAD + 30 + 24 + len(desc) * 23 + 14 + stack_rows * 30 + PAD - 8
    h = max(h, 196)

    alt = f"{p['title']}, {p['kind']}. {p['description']} Status: {now}. {detail}"
    svg = Svg(W, int(h), theme, alt)
    svg.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="12" fill="{t["surface"]}" '
            f'stroke="{t["border"]}"/>')

    # left: what it is
    svg.text(PAD, PAD + 22, p["title"], fam="SG", wt=700, size=24)
    svg.text(PAD, PAD + 48, p["kind"], wt=500, size=14, fill="muted")
    y = PAD + 80
    for line in desc:
        svg.text(PAD, y, line, size=15)
        y += 23
    chips(svg, p["stack"], PAD, y - 2, LEFT_W)

    # right: where it is
    svg.add(f'<line x1="{RIGHT_X - 30}" y1="{PAD}" x2="{RIGHT_X - 30}" y2="{h - PAD}" stroke="{t["faint"]}"/>')
    if track and "stage" in track[0]:
        stage_list(svg, track, detail)
        if footnote:
            svg.text(W - PAD, h - PAD + 6, footnote, size=11.5, fill="muted", anchor="end")
        return svg.render()
    gap = 4
    seg_w = (RIGHT_W - gap * (len(track) - 1)) / len(track)
    ty = PAD + 12
    for i, seg in enumerate(track):
        sx = RIGHT_X + i * (seg_w + gap)
        svg.add(f'<rect x="{sx:.1f}" y="{ty}" width="{seg_w:.1f}" height="8" rx="2" fill="{t["faint"]}"/>')
        frac = seg["fill"]
        if frac > 0:
            # amber marks only the phase being worked on; closed work elsewhere is teal
            color = t["active"] if seg.get("current") else t["done"]
            svg.add(f'<rect x="{sx:.1f}" y="{ty}" width="{max(seg_w * frac, 3):.1f}" height="8" rx="2" '
                    f'fill="{color}"/>')
        if seg.get("label"):
            svg.text(sx + seg_w / 2, ty + 26, seg["label"], size=11,
                     fill="text" if seg.get("current") else "muted", anchor="middle",
                     wt=500 if seg.get("current") else 400)
    y = ty + (62 if any(s.get("label") for s in track) else 40)
    for line in FONTS.wrap(now, "Plex", 500, 15, RIGHT_W):
        svg.text(RIGHT_X, y, line, wt=500, size=15)
        y += 21
    for line in FONTS.wrap(detail, "Plex", 400, 14, RIGHT_W):
        svg.text(RIGHT_X, y + 2, line, size=14, fill="muted")
        y += 20
    if footnote:
        svg.text(W - PAD, h - PAD + 6, footnote, size=11.5, fill="muted", anchor="end")
    return svg.render()


def stage_list(svg: Svg, track: list[dict], note: str) -> None:
    """Vertical list of stages: done (check), current (ring with dot), upcoming (ring)."""
    t, y = svg.t, PAD + 14
    for seg in track:
        cx, cy = RIGHT_X + 8, y - 5
        if seg["state"] == "done":
            svg.add(f'<circle cx="{cx}" cy="{cy}" r="8" fill="{t["done"]}"/>'
                    f'<path d="M{cx - 3.6},{cy + .2} l2.4,2.5 l4.8,-5" fill="none" stroke="{t["node"]}" '
                    f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
            svg.text(RIGHT_X + 26, y, seg["stage"], size=15)
        elif seg["state"] == "current":
            svg.add(f'<circle cx="{cx}" cy="{cy}" r="7.2" fill="none" stroke="{t["active"]}" stroke-width="1.6"/>'
                    f'<circle cx="{cx}" cy="{cy}" r="3.2" fill="{t["active"]}"/>')
            svg.text(RIGHT_X + 26, y, seg["stage"], wt=500, size=15)
        else:
            svg.add(f'<circle cx="{cx}" cy="{cy}" r="7.2" fill="none" stroke="{t["edge"]}" stroke-width="1.6"/>')
            svg.text(RIGHT_X + 26, y, seg["stage"], size=15, fill="muted")
        y += 27
    for line in FONTS.wrap(note, "Plex", 400, 14, RIGHT_W):
        svg.text(RIGHT_X, y + 8, line, size=14, fill="muted")
        y += 20


def thesis_track(p: dict) -> tuple[list[dict], str, str]:
    stages, cur = p["stages"], p["stages"].index(p["current"])
    track = [{"stage": s, "state": "done" if i < cur else ("current" if i == cur else "next")}
             for i, s in enumerate(stages)]
    return track, f"Now: {stages[cur]}", p.get("note", "")


def github(url: str) -> list:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def sotp_track(p: dict) -> tuple[list[dict], str, str]:
    api = f"https://api.github.com/repos/{p['repo']}"
    milestones = sorted(github(f"{api}/milestones?state=all&per_page=100"), key=lambda m: m["number"])
    track, current = [], None
    for m in milestones:
        issues = [i for i in github(f"{api}/issues?milestone={m['number']}&state=all&per_page=100")
                  if "pull_request" not in i]
        total = len(issues)
        closed = sum(i["state"] == "closed" for i in issues)
        code, _, name = m["title"].partition(" · ")
        done = total > 0 and closed == total
        seg = {"label": code, "fill": 1 if done else (closed / total if total else 0)}
        if current is None and total and not done:
            current = (code, name, closed, total)
            seg["current"] = True
            seg["fill"] = max(seg["fill"], 0.08)
        track.append(seg)
    if current is None:
        return track, "All phases complete", ""
    code, name, closed, total = current
    return track, f"Now in {code}: {name}", f"{closed} of {total} issues closed in this phase"


# ---------------------------------------------------------------- main
def write(name: str, content: str) -> None:
    path = OUT / name
    if not path.exists() or path.read_text() != content:
        path.write_text(content)
        print(f"updated {path.relative_to(HERE.parent)} ({len(content) // 1024} KB)")


def main() -> int:
    cfg = tomllib.loads((HERE / "config.toml").read_text())
    OUT.mkdir(exist_ok=True)

    thesis = thesis_track(cfg["thesis"])
    try:
        sotp = sotp_track(cfg["sotp"])
    except Exception as exc:  # keep the last good image if the API is unreachable
        print(f"warning: SOTP milestones unavailable ({exc}); keeping existing SOTP images", file=sys.stderr)
        sotp = None

    for theme in THEMES:
        write(f"header-{theme}.svg", header(cfg["header"], theme))
        write(f"thesis-{theme}.svg", panel(cfg["thesis"], theme, *thesis))
        if sotp:
            write(f"sotp-{theme}.svg", panel(cfg["sotp"], theme, *sotp, footnote="Progress synced from GitHub milestones"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
