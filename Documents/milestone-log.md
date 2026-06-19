# Milestone Log

> Historical record of what was actually done, milestone by milestone.
> Written by the `documentarian` subagent. Append-only — do not edit past entries, add corrections as new entries instead.
> For current project state, see `CLAUDE.md`. For requirements, see `PRD.md`. For test evidence, see `qa-log.md`.

---

## M0 — Repo Cleanup — 2026-05-27

**Requirement(s) addressed:** Repo hygiene — foundational cleanup before development begins (no formal PRD IDs)

**What was built:**
- Removed hardcoded Windows-path Google Cloud credentials from `app.py`; replaced with `python-dotenv` loading from `.env`
- Created `requirements.txt` with: flask, google-cloud-vision, werkzeug, python-dotenv
- Created `.gitignore` excluding `.env`, `*.json` credentials, `static/uploads/`, `.vscode/`, `__pycache__/`
- Rewrote `README.md` with project description, architecture diagram, prerequisites, setup steps, usage walkthrough, roadmap, and tech stack table
- Removed leftover stray files: `app - Copy.py`, `readme.txt`, `templates/index - Copy.html`, and an accidental `less` pager output file

**Key decisions:**
- Kept existing Flask backend rather than rewriting — working prototype already existed; avoided throwing away validated work
- Chose `python-dotenv` over alternatives — simplest option for a Flask project this size

**Verified by QA:** Formally verified 2026-06-19 (see `qa-log.md`): app starts cleanly with `.env` credentials, no hardcoded paths in committed code, startup validation works correctly.

**Reviewed by Code Reviewer:** Full git history scan on 2026-06-19 — no credentials or secrets ever committed. Clean.

**Known gaps / deferred:**
- `.env.example` was referenced in M0 README but NOT committed to git until 2026-06-19 — added as a correction during M1 audit
- `static/uploads/jeevan_marathi.jpg` was committed in the initial commit (before .gitignore existed) and remains tracked; not a security risk (test handwriting image), deferred by user — `git rm --cached static/uploads/jeevan_marathi.jpg` would remove it
- No automated tests exist for any part of the project

---

## M1 — Foundation — 2026-06-19

**Requirement(s) addressed:** AUTH-1, AUTH-2, AUTH-4 (all verified ✅); ADMIN-1, ADMIN-2 (verified ✅); DB schema — PRD section 6 (verified ✅); AUTH-3 and AUTH-5 explicitly out of M1 scope

**What was built:**
- `app.py` — Supabase client setup via env vars; `login_required` decorator; `/login` POST route using `supabase.auth.sign_in_with_password` with `session.permanent = True`; `/logout` clearing session; `/admin` querying `supabase.table('posts').select('*')`; `/`, `/admin`, `/upload` all protected by `login_required`
- `supabase/schema.sql` — `post_status` enum (`draft`, `published`); `posts` table (id, title_marathi, title_english, body_marathi, body_english, slug, status, published_at, created_at, updated_at); `post_images` table (id, post_id FK with CASCADE, storage_url, page_order, ocr_raw_text, ocr_confidence, created_at); `set_updated_at` trigger on `posts`
- `templates/login.html` — Styled login form with Noto Sans Devanagari + Inter fonts, flash error message support
- `templates/admin.html` — Post list table (title, status badge, date), empty state, user email display, sign out link

**Hardening applied during 2026-06-19 audit (findings from PM, Principal Engineer, Code Reviewer):**
- `SECRET_KEY` startup guard: replaced silent `'dev-secret-key'` fallback with `RuntimeError` if var is missing (`app.py:13–16`)
- Supabase env var startup guard: `RuntimeError` if `SUPABASE_URL` or `SUPABASE_SERVICE_ROLE_KEY` are missing (`app.py:22–26`)
- `session.permanent = True` added at login so sessions survive browser close (`app.py:51`)
- `debug=True` replaced with `os.getenv('FLASK_DEBUG', 'false').lower() == 'true'` to prevent Werkzeug debugger exposure in production (`app.py:109`)
- `login_required` comment added marking it as M1-only scaffolding to be replaced with JWT validation in M2
- `.env.example` committed with all 4 required vars (also corrects the M0 gap above)
- PRD section 5.8: ADMIN-1 and ADMIN-2 status updated to ✅ Done
- README updated: current status, Supabase env vars in setup section, project structure, roadmap row
- `CLAUDE.md` moved from `.claude/agents/` to repo root for automatic Claude Code pickup

**Key decisions:**
- Flask server-side sessions used instead of JWT — intentional M1 scaffolding for the Jinja2 phase; **will be replaced in M2** with `supabase.auth.get_user(token)` JWT validation once React authenticates directly via Supabase JS
- Supabase Auth (`sign_in_with_password`) used rather than a custom auth table — handles password hashing and future reset flows without additional code
- Supabase service role key (not anon key) — bypasses RLS; correct for a single-author admin app with no public routes; revisit for M4 when public blog routes are added
- Schema uses `TIMESTAMPTZ` (not `TIMESTAMP`) — timezone-aware, matches Supabase defaults
- `body_marathi` defaults to `''` (not NULL) — allows creating a post shell before OCR runs

**Verified by QA:** Full automated + manual test run on 2026-06-19 (see `qa-log.md`):
- AUTH-1 ✅ Login confirmed working end-to-end
- AUTH-2 ✅ Session cookie `Expires` confirmed ~30 days out via browser DevTools (manual, by user)
- AUTH-4 ✅ All three protected routes (`/`, `/admin`, `/upload`) redirect to `/login` when unauthenticated
- DB schema ✅ `posts` table live in Supabase — `/admin` returned HTTP 200
- Logout ✅ Session cleared, redirects to `/login`
- Admin dashboard shell ✅ Renders post list from DB

**Reviewed by Code Reviewer:** Full review on 2026-06-19:
- Full git history scan: no secrets or credentials ever committed ✅
- No hardcoded credentials in any file ✅
- All blocking findings fixed (see Hardening above) ✅

**Known gaps / deferred:**
- `translated_text` variable name in `result.html:11` is misleading (it holds OCR output, not a translation); deferred — M2 replaces this template entirely
- `static/uploads/jeevan_marathi.jpg` remains tracked in git; deferred by user
- AUTH-3 (forgot password): not in M1 scope; Supabase Auth supports reset flows natively when needed
- AUTH-5 (public blog without login): not in M1 scope; M4 work
- `requirements.txt` clean install in fresh venv not formally tested — verify before first Render deployment in M2

---

## Deferred to M3 — OCR-5 error handling — 2026-06-19

**Tagged against:** OCR-5 (If OCR fails, author is notified with retry option — Must Have)

**Gap:** `/upload` in `app.py:98-101` has no `try/except` around the Google Cloud Vision API call. A timeout, quota error, or network failure causes an unhandled exception and a generic 500 response. There is no user-facing error message and no retry option.

**Action for M3:** Wrap `client.text_detection(image=image)` in try/except, render a meaningful error to the author, and provide a retry option (OCR-5). Add a regression test at that point using a mocked Vision API failure.

---

## M1 — Test Coverage — 2026-06-19

**Requirement(s) addressed:** AUTH-1, AUTH-2 (regression), AUTH-4; upload route input validation (UPLOAD-1 partial); OCR-5 gap documented

**What was built:**
- `conftest.py` (repo root) — empty file whose presence causes pytest to add the repo root to `sys.path`, allowing `import app` from `tests/`
- `tests/test_app.py` — 10 tests covering the full M1 auth flow and upload input validation:
  - `test_login_success_redirects_to_admin` — POST /login with valid credentials → 302 to /admin
  - `test_login_failure_shows_error` — POST /login with wrong credentials → 200 with "Invalid email or password" flash
  - `test_admin_route_blocked_when_logged_out` — GET /admin without session → 302 to /login
  - `test_root_route_blocked_when_logged_out` — GET / without session → 302 to /login
  - `test_upload_route_blocked_when_logged_out` — POST /upload without session → 302 to /login
  - `test_admin_accessible_when_logged_in` — GET /admin with session set → 200
  - `test_session_is_permanent_after_login` — AUTH-2 regression: asserts login response is 302 AND Set-Cookie contains `Expires` or `Max-Age` (permanent session cookie)
  - `test_logout_clears_session` — GET /logout clears `user_id` from session
  - `test_upload_with_no_file_returns_400` — POST /upload with no file key → 400 "No file uploaded"
  - `test_upload_with_empty_filename_returns_400` — POST /upload with empty filename → 400 "No file selected"
- `tests/test_logout_only.py` — standalone single test for logout behaviour, written as an isolated demonstration; covers the same case as `test_logout_clears_session` in `test_app.py`

**Key decisions:**
- Patched `supabase.create_client` (not `app.supabase` directly) — intercepts the Supabase client at import time so the app module initialises without real credentials; side effect is that `app.supabase` is a single shared mock across all tests due to Python module caching
- Supabase and Google Cloud Vision mocked entirely — no real API calls, no cost per run; upload 400 tests don't reach the Vision API so no Vision mock was needed there
- `session.permanent = True` regression test checks `Set-Cookie` response header (not `sess.permanent` via `session_transaction`) — the session transaction approach returned a fresh empty session object that didn't preserve the `permanent` flag; checking the header is the correct observable behaviour
- Auth tests inject session state directly via `session_transaction()` rather than going through the login flow — keeps tests independent and fast

**Verified by QA:** All 10 tests pass (`pytest tests/test_app.py -v`). Run confirmed at commit `6872a6f`.

**Reviewed by Code Reviewer:** Yes — review on 2026-06-19 found three issues, all fixed before push:
1. AUTH-2 test was a false positive: `side_effect = Exception` from `test_login_failure_shows_error` leaked into `test_session_is_permanent_after_login` via the shared mock; failed login produced a `Set-Cookie: Max-Age=0` header that satisfied the assertion. Fixed by (a) adding `assert response.status_code == 302` before the cookie check and (b) clearing `side_effect` explicitly at the start of the test.
2. `from io import BytesIO` was inside a test function body — moved to top-level imports.
3. `WTF_CSRF_ENABLED` config was set in the fixture but Flask-WTF is not a dependency — removed.

**Known gaps / deferred:**
- `tests/test_logout_only.py` duplicates `test_logout_clears_session` in `test_app.py`; can be deleted or kept as an isolated smoke test — no action required now
- Shared mock object (`app.supabase`) across all tests: any test that sets `side_effect` must clear it before the next test that uses the mock differently. Current workaround is explicit `side_effect = None` in affected tests. Could be fixed in M2 by patching `app.supabase` directly so each fixture gets a fresh mock.
- No tests for the Vision API happy path or error path in `/upload` — intentionally deferred to M3 when the route is rewritten (Supabase Storage, DB persistence). OCR-5 error handling test also deferred to M3 (see entry above).

---
