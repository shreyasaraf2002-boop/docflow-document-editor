# DocFlow — Mini Document Workspace

A deliberately scoped document editor built as a full-stack coding assessment. Create, rename, edit, import, save, and share documents through a responsive browser interface.

## Features
- Create, rename, save, and reopen rich-text documents.
- Bold, italic, underline, headings, bulleted and numbered lists.
- Import UTF-8 `.txt` and `.md` files up to 1 MB as editable text. Markdown is imported as plain text; Markdown syntax is **not** rendered.
- Share a document with a second seeded user. Shared recipients can view and edit, but only the owner can grant access.
- SQLite persists documents (including HTML formatting) and sharing relationships.
- Basic error handling, tests, and health endpoint.

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000. Use the user selector at the top right to switch between **Alex** and **Sam**. Create a document as Alex, share it with Sam, then switch to Sam to verify it appears under Shared.

## Run automated tests

```bash
pytest -q
```

Local run on 12 Nov 2026: 2 passed. The same session created “Project notes” as Alex, saved bold text, refreshed, shared it with Sam, and imported `sample-import.txt`. Screenshots from that session are in `evidence/`.

## Deploy

1. Push the project files to a GitHub repository.
2. In Render, create a new **Web Service** and connect that repository.
3. Set **Build Command** to `pip install -r requirements.txt`.
4. Set **Start Command** to `gunicorn app:app --bind 0.0.0.0:$PORT`.
5. Choose an appropriate Python runtime and deploy.
6. Open the assigned URL and visit `/health` to verify the app is running.

**Storage caveat:** SQLite is stored on the app filesystem. On hosting platforms with ephemeral filesystems, data can disappear when an instance restarts/redeploys. To demonstrate durable persistence beyond restarts, attach a persistent disk and set `DATABASE_PATH` to a path on that disk, or migrate to managed PostgreSQL. Some free hosting tiers do not offer persistent disks. Do not claim production-grade persistence on ephemeral hosting.

## Implementation decisions

- **Flask over a split frontend/backend:** fewer configuration steps, simpler deployment, and familiar Python patterns.
- **SQLite:** relational document and access-grant storage suitable for a local demo.
- **Browser native `contenteditable`:** supports an approachable rich-text interface with minimal dependencies. `document.execCommand()` is deprecated and would be replaced by TipTap/ProseMirror in a production application.
- **Seeded users:** deliberately mock identity. The `X-User-Id` header is **not authentication** and must not be used in a real system.
- **Automatic save:** changes are debounced in the browser and saved by API.

## Known limitations

- Shared users can edit; no read-only permission setting.
- No user registration or secure authentication.
- Browser editing/HTML sanitization is not production-hardened. Imported text is escaped, but editor HTML is stored and returned as provided; a real service requires server-side sanitization and a hardened editor.
- No real-time simultaneous editing or conflict handling.
- No DOCX support or actual Markdown rendering.
- No version history, exporting, or deletion.
- SQLite on an ephemeral deployment is not durable across redeploys.

## Next improvements

Implement real authentication, stronger HTML sanitization, managed Postgres, editor collaboration/concurrency, and read-only roles.
