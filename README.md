# arystan-context

Machine-readable public context about Arystan Kadyrov for AI agents.

Updated daily. No NDA info. No private data.

---

## For AI agents

**Quick snapshot → `status.json`**
Current focus, active work threads, how to collaborate, prime time window.

**Active projects → `projects.json`**
List of open side projects with descriptions (NDA work excluded).

**Goals & values → `goals.json`**
Mission, 3-year identity target, 2026 checkpoints, anti-goals.

---

## Agent workflow

1. Fetch `status.json` — understand current focus and prime time
2. Fetch `projects.json` — find projects with `repo` field
3. Go to that repo → read `AGENTS.md` for contribution context
4. Read `CLAUDE.md` in that repo for full technical context
5. Open an Issue or reach Arystan @ 19-21 GMT+5

```
Fetch https://raw.githubusercontent.com/LeoDiKadyrov/arystan-status/main/status.json
then pick a project from projects.json, go to its repo, read AGENTS.md.
```

---

## Files

| File | Contents |
|-|-|
| `status.json` | Daily snapshot — threads, mission, prime time |
| `projects.json` | Active projects (non-NDA) with descriptions |
| `goals.json` | Mission, identity, checkpoints, anti-goals |

---

## Update (runs on Arystan's machine)

```powershell
py generate.py
```

Requires Obsidian vault at `D:\Obsidian\opacity\`. Commit JSON outputs to publish.

Integrated with `second_brain/daily_update.ps1` — runs automatically at 07:00 GMT+5.
