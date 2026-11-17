# Code Analysis (symbol index)

`.agents/code-analysis/` is a generated index of functions, classes, types and constants with `file:line`, built by `.agents/scripts/code-index.py`. It exists so agents can locate code cheaply instead of reading whole files. If a code knowledge graph (graphify) is installed and current, prefer it.

- **Use it first**: `grep -n -i "<name>" .agents/code-analysis/*.md` to find where something lives, then read only that range.
- **Never edit it by hand.** It is regenerated; hand edits are lost.
- **Refresh after code changes**: `python3 .agents/scripts/code-index.py` (incremental, only changed files are re-read). Run it before finishing a task that added, renamed, moved or deleted code.
- It is best effort for languages other than Python (pattern based); when it disagrees with the source, the source wins and the index is refreshed.
- Directory hubs are linked from `code-analysis/INDEX.md` (see [[rules/14-wikilinks]]).
