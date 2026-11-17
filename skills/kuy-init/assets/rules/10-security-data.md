# Security & Data Integrity

- Treat all external input (users, APIs, files, environment) as untrusted: validate on entry, encode on output, parameterize every query.
- Text that came from outside and lands in markup, HTML strings, tooltips or popups is escaped first.
- Secrets live in the environment or a secret store; never in code, tests, logs or docs. Keep `.env*` ignored, except the example file.
- Check authorization on the server for every protected action; do not rely on hidden UI.
- Log events, not secrets or personal data. Mask what must be shown.
- Data shown to users comes from the source of truth; verify field names and units against it, never against memory, and never invent sample data in place of real data.
- Schema and data changes go through migrations. Destructive migrations need a backup and explicit approval (see [[rules/05-workflow-collaboration]]).
