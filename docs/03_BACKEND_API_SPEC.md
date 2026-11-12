# Backend API specification
Flask serves both the UI and JSON API. Demo identity is selected by `X-User-Id: 1` (Alex) or `X-User-Id: 2` (Sam). **This header is not secure authentication.**

| Method | Route | Purpose | Example |
|---|---|---|---|
| GET | / | UI | browser |
| GET | /health | service health | `{ "status": "ok" }` |
| GET | /api/users | demo users | array of users |
| GET | /api/documents | owned/shared list | header X-User-Id |
| POST | /api/documents | create | `{ "title": "Notes", "content": "" }` |
| GET | /api/documents/:id | retrieve if allowed | header X-User-Id |
| PUT | /api/documents/:id | edit title/HTML | `{ "title": "Notes", "content": "<p>Hi</p>" }` |
| POST | /api/documents/:id/share | grant access; owner only | `{ "user_id": 2 }` |
| POST | /api/upload | upload file and create doc | multipart field `file` |

## Validation
- Invalid user -> 401; inaccessible doc -> 404; non-owner sharing -> 403.
- Empty title on update -> 400; upload extension limited to .txt/.md; UTF-8; 1MB.
- HTML editor content has a 2-million-character application limit.
- Errors are JSON with `error` field.

## Example curl
```bash
curl -H 'X-User-Id: 1' http://localhost:5000/api/documents
curl -X POST http://localhost:5000/api/documents -H 'X-User-Id: 1' -H 'Content-Type: application/json' -d '{"title":"Test","content":"<p>Hello</p>"}'
```

## Security warning
This is a demo. Do not put private documents into it or expose it as a real authenticated service. User IDs can be spoofed and stored editor HTML is not sanitized.
