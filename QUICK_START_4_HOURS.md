# DocFlow 4-hour build and submission guide

## First: launch and verify

**VS Code (recommended):** Extract the project. In its folder run `python -m pip install -r requirements.txt`, then `python app.py`; visit http://127.0.0.1:5000.

**Google Colab (optional):** Open `DocFlow_Colab_Setup.ipynb` in https://colab.research.google.com/, upload the original ZIP when asked, run cells top to bottom, and open the preview window. Colab is a temporary test environment, not the final public deployed app.

## Core verification
1. Create a document as Alex and rename it.
2. Type text; apply bold, italic, underline, heading, bulleted and numbered formatting.
3. Click Save, refresh browser, reopen, verify content and formatting.
4. Upload sample-import.txt. Text should become an editable new document.
5. Share a document with Sam, switch accounts in top right; verify Shared by Alex appears.
6. Run `python -m pytest -q`.

## Deploy
1. Push extracted project files (not ZIP) to GitHub.
2. Render > New > Web Service > Connect repository.
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Test public URL and `/health`.

**Data caution:** Render Free uses ephemeral filesystem. It may lose SQLite documents when it sleeps/restarts; for reliable durable cloud persistence choose persistent storage (for example, a compatible paid service with disk, or refactor to Postgres). Document this limitation transparently if using the free tier.

## Prepare submission
- Edit README, ARCHITECTURE and AI_WORKFLOW to reflect what you actually built and tested.
- Record a real 3–5 minute demonstration of creating, formatting, uploading, sharing and refreshing. Discuss decisions, scope tradeoffs and actual AI tool usage.
- Upload source code, notes and demo materials to one Google Drive folder.
- Put live app URL, Drive folder link, video link, test accounts (Alex/Sam), local setup commands and honest limitations in the assessment form.
