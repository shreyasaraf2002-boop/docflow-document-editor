# Architecture and Tradeoffs

**User workflow:** Create a document → format content → auto-save → import a supported text file or share the document → switch users → reopen and edit.

**Frontend:** Native HTML, CSS, JS. Rich text is stored as HTML from a `contenteditable` element. Debounced save calls the Flask API; document list clearly labels `Mine` or `Shared by Alex/Sam`.

**Backend:** Flask JSON API for document listing, retrieval, creation, modification, sharing, plus a multipart upload endpoint. File extension and UTF-8 validation occur server-side.

**Database:** SQLite with three tables: `users`, `documents` and `shares`. The `documents.owner_id` relationship identifies ownership. `shares` has a composite uniqueness constraint to avoid duplicate grants. Document access checks join the request user to ownership or grant records.

**Authorization note:** Seeded user selection is not secure authentication. It demonstrates access-control behavior only. A production build must authenticate each request and derive identity from a verified session.

**Tradeoffs:** Optimized for a coherent vertical slice rather than real-time collaboration, DOCX support, or enterprise security. Flask, SQLite, and native browser editing reduce setup complexity; those choices would be reviewed for a larger deployment.

**Testing:** Automated test covers document create, update, sharing, saved formatted content and ownership restrictions. Second test checks disallowed extensions.

**Deployment:** Gunicorn hosts Flask. Local SQLite is persistent across app restart on a stable local disk, but free-tier cloud filesystem may be ephemeral. Prefer Postgres or persistent storage in production.
