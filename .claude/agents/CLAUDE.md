# Project Memory — Marathi Handwritten Blog Platform

> This file is automatically read by Claude Code at the start of every session.
> It is also meant to be shared with Claude in claude.ai chat to keep both in sync.
> **Keep this file CURRENT, not historical.** For history of what happened in each milestone, see `docs/milestone-log.md`.

---

## What This Project Is

A personal web app that takes photographed handwritten Marathi articles, digitizes them via OCR, lets the author review/edit the text side-by-side with the original image, and publishes them as blog posts with an English translation toggle. Single author, no multi-user support.

Full requirements live in `PRD.md` — always check it for the authoritative requirement list and priorities.

---

## Current State (update this section every session)

**Last updated:** 2026-06-19
**Current milestone:** M1 (Foundation) — partially verified, see gaps below
**Next milestone:** M2 (React Frontend Scaffold)

### Milestone Status
| Milestone | Status |
|---|---|
| M0 — Repo Cleanup | ✅ Done |
| M1 — Foundation (Supabase, DB schema, auth) | 🟡 Partial — AUTH-1, AUTH-4, DB schema verified; AUTH-2/3/5 not done |
| M2 — React Frontend Scaffold | 🔴 Not started |
| M3 — OCR Pipeline | 🔴 Not started |
| M4 — Publishing | 🔴 Not started |
| M5 — Translation | 🔴 Not started |
| M6 — Polish | 🔴 Not started |
| M7 — Accuracy Loop | 🔴 Not started |

### Known Gaps / TODOs
- **AUTH-2** (session persists across browser close): `session.permanent = True` never set in `app.py`. Flask sessions die when browser closes. One-line fix.
- **AUTH-3** (forgot password / reset via email): No route, no template, no Supabase reset call. Not in M1 scope per PRD.
- **AUTH-5** (public blog pages without login): No public routes exist. `/` is admin-only. Blocked on M4 (blog reader).
- No React frontend exists yet — current frontend is Flask + Jinja2 templates only

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

---

## Gotchas / Things Not To Repeat

- **Never hardcode credentials.** The original prototype had a hardcoded Windows path to GCP credentials in `app.py`. Fixed in M0 via `python-dotenv` + `.env`. Always use environment variables for secrets.
- **`.gitignore` must always exclude:** `.env`, `*.json` (GCP credentials), `static/uploads/`, `.vscode/`, `__pycache__/`.
- Watch for stray files from terminal sessions accidentally being saved into the repo root (happened once with a `less` pager dump) — if you see an unfamiliar file with a command-like name, it's probably terminal output, not a real project file.

---

## How This Project Is Managed

- **PRD.md** — authoritative source of requirements, priorities, and milestone scope. Update its status table when a milestone completes.
- **`.claude/agents/`** — structured subagents (PM, Principal Engineer, QA, Code Reviewer, and a Documentarian) for working on this project inside Claude Code. Use them via `@agent-name`.
- **`docs/milestone-log.md`** — historical log of what was actually done in each milestone, written by the Documentarian subagent. Read this for "how did we solve X" — don't put this detail here in CLAUDE.md.

---

## Instructions for Claude Code (this means you)

- At the **start** of a session, read this file plus `PRD.md` before doing anything else.
- At the **end** of a session (or after completing a meaningful chunk of work), update the "Current State" section above — milestone status, next steps, known gaps. Keep it current, overwrite stale info rather than appending.
- Do NOT duplicate detailed change history here — that belongs in `docs/milestone-log.md` via the Documentarian subagent.
- If you make a new architecture decision not listed above, add it to "Key Decisions & Why" so future sessions (and the user's Claude.ai chat) know about it.
