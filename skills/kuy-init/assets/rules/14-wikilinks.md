# Wikilinks for `.agents/` documents

**Invariant**: every Markdown document under `.agents/` is reachable by wikilink from its folder's hub, and every folder hub is reachable from `AGENTS.md`.

- New document → add it to the hub of its folder, or just run `python3 .agents/scripts/wikilinks.py`, which regenerates hubs.
- Link between documents with `[[folder/file]]` or `[[folder/file|label]]` (path relative to `.agents/`, no `.md`).
- Generated hubs (`00-<folder>.md` and the `wikilink-index` block in `AGENTS.md`) are never edited by hand; put your own text outside the generated markers.
- Verify with `python3 .agents/scripts/wikilinks.py --check`: exit 0 means no orphans.
- When deleting or renaming a document, run the script again so no link dangles.
