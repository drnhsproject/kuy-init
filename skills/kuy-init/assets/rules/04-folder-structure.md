# Folder Structure

- Follow the structure the project already has; the layout recorded below is the source of truth for new files.
- Group by feature or module first, by technical kind second, unless the project already does the opposite.
- One public entry point per module (index, `__init__`, `mod`, or the language equivalent).
- Tests live where the project's test runner finds them and mirror the source path.
- Generated output, caches, secrets and local data never go in source folders; keep them ignored.
- New top-level folders need a reason in the change that adds them.

## Recorded layout

{{LAYOUT}}
