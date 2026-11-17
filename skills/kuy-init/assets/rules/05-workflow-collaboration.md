# Workflow & Collaboration

- **Scope discipline**: do what was asked. Anything else you notice is reported, not done.
- **Branches**: work on a branch, never directly on the default branch. Name it `<type>/<ticket-or-slug>`.
- **Commits**: small, one concern each, Conventional Commit messages (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`).
- **Review**: every change is reviewed by someone other than its author; check it against these rules and the tests.
- **Checks before handing over**: format, lint, typecheck (when the language has one) and the relevant tests pass. A failure that existed before your change is reported, not hidden.
- **Destructive actions** (database resets, deleting data, force-push, `reset --hard`) need explicit approval each time, plus a backup offer first.
- **Secrets** never enter the repository, logs, plans or chat.
