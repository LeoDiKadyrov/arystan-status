#!/usr/bin/env python3
"""generate.py — sanitized public context files for arystan-context repo.

Reads Obsidian vault (90_Meta, daily-briefing.md) + project-graph.md.
Outputs: status.json, projects.json, goals.json

Run after second_brain/briefing.py:
    py generate.py

Commit outputs to publish updated context for external agents.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VAULT = Path(r"D:\Obsidian\opacity")
META = VAULT / "90_Meta"
BRIEFING = VAULT / "daily-briefing.md"
PROJECT_GRAPH = META / "project-graph.md"
GOALS_FILE = META / "Goals.md"

OUTPUT = Path(__file__).parent

# NDA + private — never appear in public output
EXCLUDE_PROJECTS = {"DBO_Faktura_KB", "Digital_ruble", "Olga_reich", "intercept"}
EXCLUDE_DOMAINS = {"work"}

# Public GitHub repos (project name → URL)
REPOS: dict[str, str] = {
    "autorss_feed":       "https://github.com/LeoDiKadyrov/autorss-feed",
    "second_brain":       "https://github.com/LeoDiKadyrov/arystan-digital-twin",
    "korzina_weekly":     "https://github.com/LeoDiKadyrov/korzina-weekly",
    "health-agent-plugin":"https://github.com/LeoDiKadyrov/health-agent-plugin",
    "psyskills":          "https://github.com/LeoDiKadyrov/psycho-plugin",
    "wtp-plugin":         "https://github.com/LeoDiKadyrov/wtp-plugin",
    "arystan-context":    "https://github.com/LeoDiKadyrov/arystan-status",
}


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def load_projects() -> list[dict]:
    text = _read(PROJECT_GRAPH)
    projects = []
    current_domain: str | None = None

    for line in text.splitlines():
        m = re.match(r"^##\s+(\w+)\s*\(", line)
        if m:
            current_domain = m.group(1)
            continue

        m = re.match(r"^-\s+[▶💤📦🧪•]\s+\*\*(.+?)\*\*\s+—\s+(.+)", line)
        if m and current_domain:
            name = m.group(1).strip()
            desc = m.group(2).strip()
            if name in EXCLUDE_PROJECTS or current_domain in EXCLUDE_DOMAINS:
                continue
            entry: dict = {
                "name": name,
                "domain": current_domain,
                "description": desc[:300],
            }
            if name in REPOS:
                entry["repo"] = REPOS[name]
                entry["agents_file"] = REPOS[name] + "/blob/main/AGENTS.md"
            else:
                entry["private"] = True
                entry["note"] = "No public repo. Exists but not open for external contribution."
            projects.append(entry)

    return projects


def load_goals() -> dict:
    text = _read(GOALS_FILE)
    if not text:
        return {}

    out: dict = {}

    m = re.search(r"##\s+Миссия\s*\n+(.+?)(?=\n##|\Z)", text, re.DOTALL)
    if m:
        out["mission"] = m.group(1).strip()[:500]

    m = re.search(r"##\s+Идентичность через 3 года\s*\n+(.+?)(?=\n##|\Z)", text, re.DOTALL)
    if m:
        center = re.search(r"\*\*Центр:\*\*\s+(.+)", m.group(1))
        if center:
            out["identity_3yr"] = center.group(1).strip()

    m = re.search(r"##\s+Чекпоинты 2026\s*\n+(.+?)(?=\n##|\Z)", text, re.DOTALL)
    if m:
        out["checkpoints_2026"] = m.group(1).strip()[:600]

    m = re.search(r"##\s+Стратегия.+?\n+(.+?)(?=\n##|\Z)", text, re.DOTALL)
    if m:
        steps = re.findall(r"\d+\.\s+\*\*(.+?)\*\*\s+—\s+(.+)", m.group(1))
        out["strategy_steps"] = [f"{k}: {v.strip()}" for k, v in steps]

    m = re.search(r"##\s+Антицели\s*\n+(.+?)(?=\n##|\Z)", text, re.DOTALL)
    if m:
        lines = [l.strip().lstrip("- ") for l in m.group(1).splitlines() if l.strip().startswith("-")]
        out["anti_goals"] = lines[:6]

    return out


def load_active_threads() -> list[str]:
    text = _read(BRIEFING)
    threads = []
    in_active = False

    for line in text.splitlines():
        if "## 🔥 Активные задачи" in line:
            in_active = True
            continue
        if in_active and line.startswith("## "):
            break
        if in_active:
            m = re.match(r"^-\s+\*\*(.+?)\*\*", line)
            if m:
                threads.append(m.group(1).strip())

    return threads[:8]


def generate() -> None:
    today = date.today().isoformat()

    projects = load_projects()
    goals = load_goals()
    threads = load_active_threads()

    status = {
        "as_of": today,
        "person": "Arystan Kadyrov",
        "github": "arystan-context",
        "location": "Karaganda, Kazakhstan (GMT+5)",
        "prime_time_gmt5": "19:00-21:00",
        "active_project_count": len(projects),
        "active_threads": threads,
        "mission_short": (goals.get("mission", "") or "")[:200],
        "identity_3yr": goals.get("identity_3yr", ""),
        "how_to_collaborate": (
            "Check projects.json for active side projects. "
            "Check goals.json for priorities and anti-goals. "
            "Best contact window: 19-21 GMT+5 weekdays."
        ),
        "generated_by": "arystan-context/generate.py",
    }

    outputs = {
        "status.json": status,
        "projects.json": projects,
        "goals.json": goals,
    }

    for filename, data in outputs.items():
        path = OUTPUT / filename
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        size = len(data) if isinstance(data, list) else len(data)
        print(f"✓ {filename} ({size} items)" if isinstance(data, list) else f"✓ {filename}")

    print(f"\nPublished context for {today}: {len(projects)} projects, {len(threads)} active threads.")


if __name__ == "__main__":
    generate()
