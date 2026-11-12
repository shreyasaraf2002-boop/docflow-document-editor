# DocFlow Submission

**Source code:** https://github.com/shreyasaraf2002-boop/docflow-document-editor

**Live application:** [Render URL — fill after deploy, then open `/health`]

**Walkthrough video (3–5 minutes):** [Loom, unlisted YouTube, or Drive video URL — record from the live site using `WALKTHROUGH_SCRIPT.md`]

**Test users:** Alex and Sam. Select the user using the menu in the application header. No password is needed because this demo uses mock identities.

**Local setup:** See `README.md`.

**Architecture:** See `ARCHITECTURE.md`.

**AI workflow:** See `AI_WORKFLOW.md`.

**Automated tests (local, 12 Nov 2026):** `python -m pytest -q` — 2 passed.

**Feature status:**

Working locally and verified in the browser:

- Create, rename, type, bold, save, and reopen a document after refresh.
- Import a UTF-8 `.txt` file (`sample-import.txt`) as an editable document.
- Owner (Alex) can share with Sam. Sam sees it as “Shared by Alex” and can open the saved formatting.
- `/health` returns `{"status":"ok"}`.
- Disallowed upload extensions are rejected (covered by pytest).

Incomplete:

- No recorded walkthrough video yet.
- No public URL until Render deploy finishes.
- No real authentication. Anyone who can set `X-User-Id` can act as Alex or Sam.
- Editor HTML is not sanitized on the server.
- Shared users can edit. There is no read-only role.
- No DOCX, Markdown rendering, version history, export, or delete.
- SQLite on Render’s filesystem can disappear when the free instance sleeps or redeploys. Do not claim durable cloud storage.

**Next 2–4 hours:** Put the database on persistent disk or Postgres, add server-side HTML sanitization, and record the 3–5 minute walkthrough against the live URL.

## Paste into the assessment Submission field

```markdown
# DocFlow submission
- Source and documentation: [GitHub repository](https://github.com/shreyasaraf2002-boop/docflow-document-editor)
- Live app: [DocFlow](REPLACE_WITH_REAL_URL)
- Walkthrough video: [3–5 minute demo](REPLACE_WITH_REAL_VIDEO_URL)
- Demo accounts: select Alex or Sam using the user switcher; no password.
- Run locally: `pip install -r requirements.txt` then `python app.py`; open http://localhost:5000.
- Automated tests: `python -m pytest -q` — 2 passed locally on 12 Nov 2026.
- Working: create, rename, rich-text save/reopen, .txt import, share from Alex to Sam, health check.
- Incomplete: no real authentication, no HTML sanitization, no read-only share role, and SQLite on Render free tier is not durable across restarts.
- Next 2–4 hours: persistent database, stronger authentication, HTML sanitization, better editor.
```
