# Deployment and security decisions
## Deployment
- Development: Flask built-in server on localhost.
- Public demo: Gunicorn hosting Flask via Render (or equivalent).
- Readiness check: GET /health.
- DB: SQLite file. `DATABASE_PATH` can point to mounted persistent storage when available.

## Major limitations to disclose
1. Demo user switching via client-controlled header is **not** real authentication; do not store sensitive data.
2. Rich HTML from the editor is stored without server-side sanitization, creating a potential XSS risk. Production would sanitize HTML with an allowlist and enforce CSP.
3. Concurrent editing has no revision checks; last write wins.
4. SQLite on an ephemeral cloud filesystem is not durable across restarts.
5. Browser native editor uses deprecated execCommand.

## Production next steps
Use proper sessions/OAuth, server-side HTML sanitization, PostgreSQL, migrations, optimistic concurrency, robust editor (TipTap/ProseMirror), rate limits, audit logs, HTTPS security headers, and CI.

## Scope decision
The assessment allows mocked users and practical storage, so the starter demonstrates basic workflows while explicitly documenting what is not production-ready.
