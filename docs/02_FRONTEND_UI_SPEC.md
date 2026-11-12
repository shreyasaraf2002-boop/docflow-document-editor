# Frontend/UI specification
## Screens
1. Workspace with header (DocFlow brand, demo user selector), left sidebar (new document, import, document list), main area (empty state or editor).
2. Editor header: editable title, save status, Save and Share actions.
3. Toolbar: Bold, Italic, Underline, Heading 2, Paragraph, Bulleted list, Numbered list.
4. Share dialog: choose another seeded user, confirm or cancel.
5. Toast messages for success/errors.

## User journeys
- Create: click New document -> type title and body -> Save -> see document in sidebar.
- Edit: click document -> change title/body -> Save -> refresh -> reopen and verify HTML formatting.
- Import: choose .txt/.md UTF-8 file up to 1MB -> new editable document appears.
- Share: as Alex open owned document -> Share to Sam -> switch to Sam -> see Shared by Alex -> open and edit.

## Accessibility/UX acceptance checks
- Controls have readable labels/titles; keyboard users can tab to primary actions.
- Save status should visibly change on edits; error messages should appear on failed requests.
- Narrow browser widths should not hide critical actions (check manually).
- Treat this as a scoped demo, not a fully audited accessible editor.

## File mapping
- templates/index.html: markup and UI controls
- static/style.css: layout and styling
- static/app.js: event handlers, API calls, autosave, document list

## Limitations
The rich text editor uses native contenteditable and deprecated execCommand; it is a rapid prototype, not a production-grade collaborative editor. Content is stored as HTML; server-side sanitization is not implemented.
