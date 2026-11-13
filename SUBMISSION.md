# DocFlow Submission

**Source code:** https://github.com/shreyasaraf2002-boop/docflow-document-editor

**Live application:** https://docflow-0eo0.onrender.com (also check https://docflow-0eo0.onrender.com/health)

**Walkthrough video (3–5 minutes):** https://www.loom.com/share/afb134255b86418786e65157bebb157a

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

