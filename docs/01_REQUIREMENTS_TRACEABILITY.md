# Requirements-to-implementation matrix
Source: the six screenshots of the AI-Native Full Stack assessment. This matrix is a verification plan, **not** a claim that the deployment works.

| Requirement | Implementation | Verification |
|---|---|---|
| Create a document | New document button; POST /api/documents | Create as Alex; document appears |
| Rename | Title input; PUT /api/documents/:id | Rename; save; reopen |
| Browser editing | contenteditable editor | Type several paragraphs |
| Save/reopen | PUT/GET endpoints, SQLite | Save; refresh; reopen |
| Bold/italic/underline | Toolbar commands | Format selections; refresh |
| Headings/text variation | H2 and paragraph | Apply heading |
| Bulleted/numbered lists | Toolbar commands | Create both list types |
| Upload at least one file | POST /api/upload | Import UTF-8 .txt file |
| Owner and grant access | owners, shares tables | Alex shares to Sam |
| Owned/shared distinction | Sidebar Mine / Shared by Alex | Switch users |
| Persistence | SQLite | Refresh/reopen; note deployment disk caveat |
| Setup instructions | README and runbook | Follow on clean machine |
| Working deployment | Render service | Open public URL and health route |
| Validation/error handling | File extension/size, access checks | Run tests; try .exe |
| At least one automated test | tests/test_app.py | pytest -q |
| Architecture note | ARCHITECTURE.md and docs | Review tradeoffs |
| AI workflow note | AI_WORKFLOW.md | Fill honestly with actual work |
| 3–5 minute walkthrough | WALKTHROUGH_SCRIPT.md | Record live demonstration |
| Google Drive folder | Submission checklist | Set link sharing appropriately |
| SUBMISSION.md | SUBMISSION.md | Add actual URLs |
| Video link | Submission form | Paste real public video URL |

## Optional, deliberately excluded
Real-time collaboration, comments, version history, PDF export, role-based permissions, DOCX parsing. Do not prioritize these over core requirements.
