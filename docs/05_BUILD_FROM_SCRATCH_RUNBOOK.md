# End-to-end build/run instructions (Windows + Colab)
## Path A: VS Code (recommended)
1. Install Python 3.10+ and VS Code. Extract project ZIP into a folder.
2. Open that folder in VS Code -> Terminal -> New Terminal.
3. Run `py -m venv .venv` and `.venv\Scripts\Activate.ps1` (or `python -m venv .venv`). If activation is blocked, use `.venv\Scripts\python.exe` directly.
4. Run `python -m pip install -r requirements.txt`.
5. Run `python -m pytest -q` and address any failures.
6. Run `python app.py`; visit `http://127.0.0.1:5000`.
7. Create, edit, save, import, share, switch user; refresh to verify persistence.

## Path B: Google Colab (development/testing only)
1. Open https://colab.research.google.com/ and upload `DocFlow_Colab_Setup.ipynb`.
2. Run cells. When asked for a ZIP, upload `DocFlow_Assessment_Starter.zip` (available separately).
3. The notebook installs dependencies, runs tests and starts Flask with a notebook preview. Colab sessions are temporary; they are **not** a reliable live submission URL.
4. Export/download source files and upload to GitHub for deployment.

## GitHub
1. Create `docflow-document-editor` repository.
2. Upload `app.py`, `requirements.txt`, `Procfile`, `templates/`, `static/`, `tests/`, and docs. Do not upload `.venv/`, `docflow.db`, credentials or private files.
3. Commit.

## Render
1. New -> Web Service -> connect GitHub repo.
2. Build: `pip install -r requirements.txt`.
3. Start: `gunicorn app:app --bind 0.0.0.0:$PORT`.
4. Open the assigned URL and `/health`; manually test every feature.
5. For persistent database across redeploys/restarts, provision a persistent disk (if supported on your plan) and set `DATABASE_PATH` to the mounted path. Otherwise clearly disclose ephemeral storage and do not claim durable cloud persistence.

## Troubleshooting
- `ModuleNotFoundError: flask`: install requirements using the same Python interpreter running app.py.
- Port busy: set `PORT=5001` (PowerShell: `$env:PORT='5001'`) and rerun.
- `no such table`: check that DATABASE_PATH directory is writable and app initialization runs.
- Colab preview unavailable: use VS Code locally; do not use a temporary Colab URL as final deployment.
- Refresh loses data on Render: ephemeral filesystem; use persistent storage.
- Share not visible: share while Alex owns the document, then switch to Sam.
