# Changelog

## 0.1.1

- New "Reply style" block in `SKILL.md`: the reply leads with the answer, with no greeting, announcement or recap; complete short sentences; negations, numbers and units are never shortened; warnings and questions to the user keep full wording. Text saved to files still follows the skill's own file rules.

## 0.1.0
- Hardening from review: CRLF line endings preserved in `AGENTS.md`/`.gitignore`/hubs, damaged markers left untouched, NUL-safe `git ls-files`, symlink guard, numbered index parts for wide repos, mtime+size incremental scan.
- First release: project detection (greenfield/brownfield), neutral bundled rules 01-14, legacy-convention drafting,
  user-standard override, managed `AGENTS.md` block, default git ignore, wikilink hubs with `--check`,
  incremental symbol index (`.agents/code-analysis/`).
