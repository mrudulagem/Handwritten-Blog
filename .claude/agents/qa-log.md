# QA Log

> Test evidence for the Marathi Handwritten Blog Platform.
> Written by the `qa` subagent. Append-only — do not edit past entries.
> For requirements, see `PRD.md`. For milestone history, see `milestone-log.md`.

---

## M0 + M1 Auth Flow — 2026-06-19

**Requirements tested:** M0 startup hygiene, AUTH-1, AUTH-2, AUTH-4
**Tested by:** QA subagent (automated) + user (manual AUTH-2 step)
**App version:** commit `ba69285` (Harden Supabase env var startup check)

### Automated tests (curl against running Flask app)

| # | What was tested | Result |
|---|---|---|
| 1 | App starts cleanly from `.env` — no hardcoded paths, no import errors | ✅ Pass |
| 2 | Startup with `SECRET_KEY=""` → `RuntimeError` at `app.py:15` | ✅ Pass |
| 3 | Startup with `SUPABASE_URL=""` → `RuntimeError` at `app.py:25` | ✅ Pass |
| 4 | Startup with `SUPABASE_SERVICE_ROLE_KEY=""` → `RuntimeError` at `app.py:25` | ✅ Pass |
| 5 | `GET /admin` logged out → `302 Location: /login` | ✅ Pass |
| 6 | `GET /` logged out → `302 Location: /login` | ✅ Pass |
| 7 | `POST /upload` logged out → `302` | ✅ Pass |
| 8 | `POST /login` wrong credentials → `200` with `"Invalid email or password."`, no 500 | ✅ Pass |
| 9 | `POST /login` empty email + empty password → `200` with error message, no crash | ✅ Pass |
| 10 | `GET /logout` while already logged out → `302 Location: /login`, no crash | ✅ Pass |

### Manual test (AUTH-2 — session persistence across browser close)

**Steps:**
1. Started app via `.venv\Scripts\python app.py`
2. Logged in at `http://127.0.0.1:5000/login` with valid Supabase credentials
3. Opened DevTools → Application → Cookies → `http://127.0.0.1:5000`
4. Inspected `session` cookie `Expires` field
5. Closed browser entirely, reopened, navigated to `/admin`

**Result:** ✅ Pass — `session` cookie `Expires` showed a date ~30 days from now (not "Session"). Browser close + reopen landed on `/admin` without redirecting to login.

### Findings

- Failed login correctly clears session cookie (`Set-Cookie: session=; Max-Age=0`) after flash message is consumed. Expected behaviour.
- `requirements.txt` not tested in a clean venv — `.venv` proves packages work but a fresh `pip install` was not run. Do this before first Render deployment.

### Verdict

**✅ PASS** — AUTH-1, AUTH-2, AUTH-4 and all M0 startup checks confirmed working.

**Known not tested:**
- AUTH-3 (forgot password) — not implemented, deferred
- AUTH-5 (public blog without login) — not implemented, M4 scope
- `requirements.txt` clean install in fresh venv — defer to pre-Render deploy

---
