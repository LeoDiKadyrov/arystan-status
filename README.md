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

## Example: tell your agent about Arystan

```
Fetch https://raw.githubusercontent.com/<username>/arystan-context/main/status.json
to understand what Arystan is currently focused on before suggesting collaboration.
```

Or load all three files and ask:
> "Based on Arystan's current projects and goals, where could I help?"

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
