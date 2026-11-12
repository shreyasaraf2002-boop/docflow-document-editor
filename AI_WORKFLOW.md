# AI-Native Workflow Note

This note describes the work done in this workspace on 12 Nov 2026. It does not claim a public deployment or a recorded walkthrough until those links are filled in `SUBMISSION.md`.

## Tools used

I used Cursor’s coding agent in this project folder. The agent installed the Python dependencies, started the Flask app, ran pytest, and exercised the browser UI. The application source (`app.py`, `templates/index.html`, `static/app.js`, `static/style.css`, and `tests/test_app.py`) was already in the starter folder and was not rewritten.

## Where AI accelerated the work

The starter already contained the document API, SQLite schema, editor, and tests. AI was used to get that project running on this machine, confirm the required flows, and prepare the deployment and submission notes from those results.

## What I changed or rejected

I kept the existing Flask, SQLite, and contenteditable design. I did not add real-time collaboration, DOCX import, authentication, or a different editor. Deployment files were added only so Render can start the same app with Gunicorn and one worker, which is safer for SQLite than multiple workers writing one file.

## How I verified correctness and UX

Local checks on 12 Nov 2026:

- `python -m pytest -q` — 2 passed (create/edit/share/persist, and rejection of a `.exe` upload).
- `GET /health` returned `{"status":"ok"}`.
- In the browser at http://127.0.0.1:5000, as Alex: created a document, renamed it to “Project notes”, typed body text, applied bold, and saved. The sidebar showed it as Mine.
- Refreshed and reopened the document. Title and bold HTML were still there.
- Shared the document with Sam. Switched the header user to Sam. The document appeared as “Shared by Alex” and opened with the same bold text.
- Imported `sample-import.txt`. It became a document titled “sample-import” with the file text in the editor.
- After a full page reload as Alex, both “sample-import” and “Project notes” were still listed as Mine.

No product defects showed up in those flows. The live URL still needs the same checks after deploy, because Render’s filesystem can drop the SQLite file on restart.

## Reliability and scope

The project is a deliberately scoped demo using seeded user identities. The user switcher is not secure authentication. Editor HTML is stored without server-side sanitization. On a free Render instance, SQLite is not durable across restarts or redeploys.
