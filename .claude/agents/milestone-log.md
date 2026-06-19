# Milestone Log

> Historical record of what was actually done, milestone by milestone.
> Written by the `documentarian` subagent. Append-only — don't edit past entries, add corrections as new entries instead.
> For current project state, see `CLAUDE.md`. For requirements, see `PRD.md`.

---

## M0 — Repo Cleanup — 2026-05-27

**Requirement(s) addressed:** Repo hygiene (not a formal PRD requirement ID — foundational cleanup)

**What was built:**
- Removed hardcoded Windows-path Google Cloud credentials from `app.py`; replaced with `python-dotenv` loading from `.env`
- Created `requirements.txt` (flask, google-cloud-vision, werkzeug, python-dotenv)
- Created `.gitignore` excluding `.env`, `*.json` credentials, `static/uploads/`, `.vscode/`, `__pycache__/`
- Created `.env.example` as a safe-to-commit template
- Rewrote `README.md` with proper setup instructions, project structure, and roadmap table
- Removed leftover stray files: `app - Copy.py`, `readme.txt`, `templates/index - Copy.html`, and an accidental `less` pager output file

**Key decisions:**
- Kept existing Flask backend rather than rewriting in Next.js, since a working prototype already existed — avoided throwing away validated work
- Chose `python-dotenv` over alternatives for env var loading — simplest option for a Flask project this size

**Verified by QA:** No formal QA pass — manually confirmed by user that `git status` showed expected changes and push succeeded
**Reviewed by Code Reviewer:** No formal review (subagent didn't exist yet at this point) — manually checked for credentials before push

**Known gaps / deferred:**
- No automated tests exist yet for any part of the project

---

## M1 — Foundation (Supabase, DB Schema, Auth, Admin Dashboard Shell) — 2026-06-19

**Requirement(s) addressed:** AUTH-1, AUTH-4 (verified); AUTH-2 (gap identified); AUTH-3, AUTH-5 (out of M1 scope); DB schema (PRD section 6)

**What was built:**
- `app.py` — Flask application with Supabase client setup (service role key via `python-dotenv`); `login_required` decorator (lines 24–29); `/login` route using `supabase.auth.sign_in_with_password` (lines 33–49); `/logout` route calling `session.clear()` and redirecting to `/login` (lines 53–55); `/admin` route querying `supabase.table('posts')` (line 59, protected by `login_required`); `/` root route redirecting to `/admin` (line 66, protected by `login_required`); `/upload` route stub (line 71, protected by `login_required`)
- `supabase/schema.sql` — Full DB schema: `post_status` enum (`draft`, `published`), `posts` table (id, title_marathi, title_english, body_marathi, body_english, slug, status, published_at, created_at, updated_at — timestamps as `TIMESTAMPTZ`), `post_images` table (id, post_id FK, storage_url, page_order, ocr_raw_text, ocr_confidence, created_at), `set_updated_at` trigger function applied to `posts`
- `templates/login.html` — Email/password login form with Noto Sans Devanagari + Inter fonts, error flash message support
- `templates/admin.html` — Admin dashboard: post list table with title, status badge (draft/published), created date; empty state for zero posts; user email display; sign out link

**Key decisions:**
- Used Supabase Auth (`sign_in_with_password`) rather than a custom auth table — Supabase handles password hashing, token management, and future reset flows without additional code
- Used Flask server-side sessions (not JWT) for auth state — no frontend JS required to manage auth state; simpler for a single-author app
- Used Supabase service role key (not anon key) — bypasses RLS since this is a single-author admin app; no RLS policies needed
- Schema uses `TIMESTAMPTZ` over `TIMESTAMP` — timezone-aware, matches Supabase defaults
- `body_marathi` defaults to empty string (not NULL) — allows creating a post shell before OCR runs

**Verified by QA:** Manual verification by user on 2026-06-19.
- AUTH-1 (login with email/password): confirmed working — user entered Supabase credentials on `/login`, was redirected to `/admin`
- AUTH-4 (unauthenticated access redirected to login): confirmed working — `login_required` decorator applied to `/`, `/admin`, `/upload`; unauthenticated requests redirect to `/login`
- `posts` table live in Supabase: confirmed — `/admin` route queried `supabase.table('posts')` and returned HTTP 200 with no error
- `post_images` table: schema file (`supabase/schema.sql`) confirmed correct and matches PRD section 6; table was not directly queried during verification
- Logout: confirmed implemented (`/logout` at app.py:53–55)
- Admin dashboard shell: confirmed implemented (`templates/admin.html` renders post list from DB)
- AUTH-2 (session persistence across browser close): NOT tested. `app.py` sets `session['user_id']` but never sets `session.permanent = True`. Sessions expire on browser close. Identified as a known gap from code review.

**Reviewed by Code Reviewer:** No formal review pass.

**Known gaps / deferred:**
- AUTH-2: `session.permanent = True` is never set in `app.py`. Flask sessions expire on browser close. Not an M1 blocker per PRD milestone scope; defer to a future hardening pass.
- AUTH-3 (forgot password / reset via email): No route, no template, no Supabase reset call exists. Not in M1 scope; Supabase Auth supports this natively when needed.
- AUTH-5 (public blog pages accessible without login): No public routes exist. The `/` route is admin-only. Public blog reader is M4 scope.

---
