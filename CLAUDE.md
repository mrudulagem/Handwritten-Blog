# Project Memory — Marathi Handwritten Blog Platform

> This file is automatically read by Claude Code at the start of every session.
> It is also meant to be shared with Claude in claude.ai chat to keep both in sync.
> **Keep this file CURRENT, not historical.** For history of what happened in each milestone, see `Documents/milestone-log.md`.

---

## What This Project Is

A personal web app that takes photographed handwritten Marathi articles, digitizes them via OCR, lets the author review/edit the text side-by-side with the original image, and publishes them as blog posts with an English translation toggle. Single author, no multi-user support.

Full requirements live in `PRD.md` — always check it for the authoritative requirement list and priorities.

---

## Current State (update this section every session)

**Last updated:** 2026-06-19
**Current milestone:** M2 (React Frontend Scaffold) — not started
**Next milestone:** M3 (OCR Pipeline)

### Milestone Status
| Milestone | Status |
|---|---|
| M0 — Repo Cleanup | ✅ Done — audited and verified 2026-06-19 |
| M1 — Foundation (Supabase, DB schema, auth) | ✅ Done — all M1 scope requirements verified 2026-06-19 |
| M2 — React Frontend Scaffold | 🔴 Not started |
| M3 — OCR Pipeline | 🔴 Not started |
| M4 — Publishing | 🔴 Not started |
| M5 — Translation | 🔴 Not started |
| M6 — Polish | 🔴 Not started |
| M7 — Accuracy Loop | 🔴 Not started |

### Test Coverage
- **`tests/test_app.py`** — 10 tests, code-reviewer approved 2026-06-19:
  - Auth suite (8 tests): login success/failure, auth guards on `/`, `/admin`, `/upload`, logout session clearing, and AUTH-2 regression (permanent session cookie verified via `Set-Cookie` header)
  - Upload validation (2 tests): no file → 400, empty filename → 400
- **`conftest.py`** (repo root) — enables `import app` from `tests/` via sys.path
- Supabase and Google Cloud Vision fully mocked — no real API calls per test run

### Known Gaps / TODOs
- **AUTH-3** (forgot password): not in M1 scope; Supabase Auth supports reset flows natively when needed
- **AUTH-5** (public blog pages without login): M4 scope — no public routes until blog reader is built
- **OCR-5**: No `try/except` around the Vision API call in `app.py:94-100` — a Vision API timeout or quota error returns a 500 with no user-facing message. Rewrite and add regression test in M3 when the upload route is overhauled.
- `static/uploads/jeevan_marathi.jpg` tracked in git (pre-gitignore); deferred by user — `git rm --cached` to clean up
- `requirements.txt` clean install in fresh venv not formally tested — verify before first Render deployment
- No React frontend yet — current frontend is Flask + Jinja2 templates (M1 scaffolding, replaced in M2)

---

## Tech Stack (decided — don't relitigate without good reason)

| Layer | Choice |
|---|---|
| Backend | Python, Flask |
| Frontend | React (Vite) — chosen partly as a learning goal for the author |
| Database | PostgreSQL via Supabase |
| Storage | Supabase Storage |
| Auth | Supabase Auth (email/password, single author account, no self-registration) |
| OCR | Google Cloud Vision API, `text_detection` method — already validated as accurate for Devanagari handwriting |
| Translation | Google Cloud Translation API (planned, not yet implemented) |
| Hosting (planned) | Render (Flask API) + Vercel (React frontend) |

---

## Key Decisions & Why

- **Flask over Next.js for backend:** the author had already built a Flask prototype before formal planning began; kept it rather than rewriting.
- **React chosen for frontend:** author wants to learn React, and the editor/blog/toggle UI is naturally component-driven.
- **Google Cloud Vision over alternatives:** already proven in the v0 prototype to handle Marathi handwriting well. Not re-evaluating unless accuracy becomes a problem.
- **Single author, no multi-user:** intentionally out of scope for v1. Don't add registration flows.
- **Flask session auth is M1-only scaffolding:** Replace with JWT validation (`supabase.auth.get_user(token)`) in M2 — React authenticates directly with Supabase JS and sends Bearer tokens to Flask. Do not build M2 features on top of the Flask session approach.
- **Env var startup validation pattern:** All required env vars (`SECRET_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`) raise `RuntimeError` at startup if missing. Follow this pattern for any new required vars.

---

## Gotchas / Things Not To Repeat

- **Never hardcode credentials.** The original prototype had a hardcoded Windows path to GCP credentials in `app.py`. Fixed in M0 via `python-dotenv` + `.env`. Always use environment variables for secrets.
- **`.gitignore` must always exclude:** `.env`, `*.json` (GCP credentials), `static/uploads/`, `.vscode/`, `__pycache__/`.
- Watch for stray files from terminal sessions accidentally being saved into the repo root (happened once with a `less` pager dump) — if you see an unfamiliar file with a command-like name, it's probably terminal output, not a real project file.

---

## How This Project Is Managed

- **PRD.md** — authoritative source of requirements, priorities, and milestone scope. Update its status table when a milestone completes.
- **`.claude/agents/`** — structured subagents (PM, Principal Engineer, QA, Code Reviewer, Documentarian, Test Writer) for working on this project inside Claude Code. Use them via `@agent-name`. They work alongside the **Superpowers** plugin (`superpowers@claude-plugins-official`, installed per user account, not stored in this repo), which handles planning and TDD implementation; plans are saved in `Documents/plans/`. See "Development Workflow" below for who does what.
- **`Documents/milestone-log.md`** — historical log of what was actually done in each milestone, written by the Documentarian subagent. Read this for "how did we solve X" — don't put this detail here in CLAUDE.md.
- **`Documents/qa-log.md`** — persistent QA findings log, appended by the QA subagent after each test run. Read this to see what has been manually verified.

---

## Development Workflow

Full workflow, in this exact order:

```
pm → principal-engineer → Superpowers writing-plans (save plans to Documents/plans/)
   → principal-engineer reviews the plan as judge (APPROVE/REVISE)
   → Superpowers subagent-driven-development with TDD
   → qa → test-writer (gap-filling only) → code-reviewer → documentarian
```

| Step | Owner | Output |
|---|---|---|
| 1. Scope | `pm` | What is in and out of scope, checked against the PRD |
| 2. Design | `principal-engineer` | Design recommendation |
| 3. Plan | Superpowers `writing-plans` | Plan saved in `Documents/plans/` |
| 4. Judge the plan | `principal-engineer` (Plan Review Mode) | APPROVE or REVISE. Max 2 revision rounds, then escalate to the author |
| 5. Build | Superpowers `subagent-driven-development` with TDD | Code plus unit tests |
| 6. Verify | `qa` | Findings in `Documents/qa-log.md` |
| 7. Fill test gaps | `test-writer` | Regression tests for QA's bugs and edge-case gaps only |
| 8. Final gate | `code-reviewer` | Sign-off before pushing, secrets checked first |
| 9. Record | `documentarian` | Entry in `Documents/milestone-log.md`, `CLAUDE.md` current state |

**Rules:**
- Use OUR agents for scoping, design, QA, code review, and documentation.
- Do NOT use Superpowers' brainstorming in place of `pm`/`principal-engineer`. `writing-plans` starts from their output.
- Do NOT use Superpowers' code review in place of our `code-reviewer` (ours checks for secrets first).
- Do not use git worktrees — work directly on the current branch. This is the author's standing consent for `subagent-driven-development` to run on the current branch.

**Where these rules override Superpowers' defaults:**
- `writing-plans`: save to `Documents/plans/YYYY-MM-DD-<feature-name>.md`, not `docs/superpowers/plans/`.
- `writing-plans`: when the plan is saved, go to the next step for this change size (step 4 for the full workflow, TDD implementation for a feature) instead of offering to start execution.
- `subagent-driven-development` setup: skip `using-git-worktrees`.
- `subagent-driven-development` Final Review: skip it. Report the "Rulings I made" list from its Finish section, then go to the next step for this change size (`qa` for the full workflow, `code-reviewer` for a feature), so our agents act as the final checks. Its per-task reviews may still run, but they never replace `code-reviewer`.
- `subagent-driven-development` Finish: do not run `finishing-a-development-branch`.

**Scale the workflow to the change size:**

| Change | Workflow |
|---|---|
| Small fix | `code-reviewer` only |
| Feature | `principal-engineer` → `writing-plans` → TDD implementation → `code-reviewer` (no plan judge for features) |
| Milestone, or anything auth/security-related | Full workflow |

---

## Instructions for Claude Code (this means you)

- At the **start** of a session, read this file plus `PRD.md` before doing anything else.
- At the **end** of a session (or after completing a meaningful chunk of work), update the "Current State" section above — milestone status, next steps, known gaps. Keep it current, overwrite stale info rather than appending.
- Do NOT duplicate detailed change history here — that belongs in `Documents/milestone-log.md` via the Documentarian subagent.
- If you make a new architecture decision not listed above, add it to "Key Decisions & Why" so future sessions (and the user's Claude.ai chat) know about it.
