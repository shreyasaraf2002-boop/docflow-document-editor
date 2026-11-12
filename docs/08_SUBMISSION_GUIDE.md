# Submission packaging instructions
## Required Google Drive folder contents
- `source-code/` with app.py, templates/, static/, tests/, requirements.txt, Procfile
- README.md
- ARCHITECTURE.md (or PDF)
- AI_WORKFLOW.md (or PDF), revised to reflect actual AI use
- SUBMISSION.md with real URLs and honest limitations
- WALKTHROUGH_SCRIPT.md (optional)
- `evidence/` screenshots if helpful
- `video-link.txt` with actual public 3–5 minute walkthrough URL

## Before submission
1. Verify live URL opens without login and `/health` returns OK.
2. Verify the document workflows on live URL, especially sharing.
3. Verify reviewers can view Google Drive folder and video.
4. Include seeded test users Alex and Sam (top-right selector).
5. Put the public video URL in the assessment's Video Submission Link field.
6. Put a concise Markdown summary in the assessment Submission field.
7. Disclose incomplete/partial features and what you'd do with 2–4 more hours.

## Submission field template (replace placeholders)
```markdown
# DocFlow submission
- Source and documentation: [Google Drive folder](REPLACE_WITH_REAL_LINK)
- Live app: [DocFlow](REPLACE_WITH_REAL_URL)
- Walkthrough video: [3–5 minute demo](REPLACE_WITH_REAL_VIDEO_URL)
- Demo accounts: select Alex or Sam using the user switcher; no password.
- Run locally: `pip install -r requirements.txt` then `python app.py`; open http://localhost:5000.
- Automated tests: `python -m pytest -q` (include actual result).
- Working: [list verified features]
- Incomplete: [list actual gaps, including any persistence limitation]
- Next 2–4 hours: persistent database, stronger authentication, HTML sanitization, better editor.
```
