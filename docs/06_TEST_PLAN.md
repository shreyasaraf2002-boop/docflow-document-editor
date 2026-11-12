# QA plan and evidence collection
## Automated
Run `python -m pytest -q`. The existing tests cover creating/editing/sharing, access restrictions, and rejecting invalid upload extensions. A passing run is required before describing tests as passed.

## Manual scenarios
| ID | Steps | Expected |
|---|---|---|
| T01 | Create document | New document opens |
| T02 | Rename and save | Title persists after refresh |
| T03 | Bold, italic, underline | Formatting persists after refresh |
| T04 | Heading and two list styles | Formatting remains visible |
| T05 | Upload UTF-8 .txt | New editable document appears |
| T06 | Upload .exe | Clear error shown |
| T07 | Share Alex document to Sam | Sam sees Shared by Alex |
| T08 | Sam edits shared document | Alex sees change on reopen |
| T09 | Sam tries to share Alex's document | Access denied |
| T10 | Restart local server without deleting DB | Data remains |
| T11 | Open live URL on another browser | App loads and basic actions work |

## Screenshot evidence
Save optional screenshots in `evidence/` named `01-home.png`, `02-editing.png`, `03-upload.png`, `04-sharing.png`, `05-tests.png`, `06-deployment.png`.
Do not manufacture screenshots or claim scenarios passed without checking.

## Defect log
Record issue, reproduction steps, expected/actual behavior, fix, retest result. Report unresolved issues honestly in submission.
