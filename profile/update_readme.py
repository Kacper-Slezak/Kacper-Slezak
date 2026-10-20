"""Rewrite the auto-updated sections of README.md with live data from SOTP.

Sections are delimited by HTML comments, e.g.
    <!-- sotp_progress starts --> ... <!-- sotp_progress ends -->

Standard library only. Set GITHUB_TOKEN to raise the API rate limit.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

REPO = "Kacper-Slezak/SOTP"
API = f"https://api.github.com/repos/{REPO}"
README = Path(__file__).resolve().parent.parent / "README.md"


def get(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def clean(title: str) -> str:
    """'[P1][CI] Make tests a real gate' -> 'Make tests a real gate'"""
    title = re.sub(r"^(\[[^\]]*\]\s*)+", "", title)
    return re.sub(r"^[A-Za-z]+ - ", "", title).strip()  # 'Backend - Implement X' -> 'Implement X'


def progress() -> str:
    lines, current_found = [], False
    for m in sorted(get(f"{API}/milestones?state=all&per_page=100"), key=lambda m: m["number"]):
        issues = [i for i in get(f"{API}/issues?milestone={m['number']}&state=all&per_page=100")
                  if "pull_request" not in i]
        total, closed = len(issues), sum(i["state"] == "closed" for i in issues)
        code, _, name = m["title"].partition(" · ")
        line = f"[{code} {name}]({m['html_url']}): {closed}/{total}"
        if total and closed < total and not current_found:
            current_found = True
            line = f"**{line}** (current)"
        lines.append(line)
    return "\n\n".join(lines)


def recently_closed(n: int = 6) -> str:
    issues = [i for i in get(f"{API}/issues?state=closed&sort=updated&direction=desc&per_page=50")
              if "pull_request" not in i and i.get("state_reason") == "completed"]
    issues.sort(key=lambda i: i["closed_at"], reverse=True)
    return "\n\n".join(
        f"[#{i['number']} {clean(i['title'])}]({i['html_url']}) - {i['closed_at'][:10]}" for i in issues[:n]
    )


def replace(text: str, marker: str, content: str) -> str:
    pattern = re.compile(rf"(<!-- {marker} starts -->).*?(<!-- {marker} ends -->)", re.DOTALL)
    if not pattern.search(text):
        raise SystemExit(f"marker '{marker}' not found in README.md")
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(2)}", text)


def main() -> int:
    text = README.read_text()
    text = replace(text, "sotp_progress", progress())
    text = replace(text, "sotp_closed", recently_closed())
    README.write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
