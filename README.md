# kuy-init

An Agent Skill that prepares a project for AI coding agents in one run: it installs a rules folder, registers it in
`AGENTS.md`, keeps every agent document wikilinked, and builds a compact symbol index so agents can find code without
reading whole files.

*Kuy* is Indonesian slang for "let's go".

It is a plain `SKILL.md` folder (plus scripts that need only Python 3), so it works with any agent that supports Agent Skills.

```
/kuy-init                         detect, preview, ask once, install
/kuy-init --standard=<text|file>  use your own standard instead of the default
/kuy-init --dry-run               preview only, write nothing
/kuy-init --yes                   skip the confirmation question
/kuy-init --local                 ignore via .git/info/exclude instead of .gitignore
/kuy-init --code-analysis=auto|force|skip
```

## Where the rules come from

| Project | Rules |
|---|---|
| New, no instruction | A neutral bundled standard (14 short rules: stack, coding, architecture, folders, workflow, testing, performance, documentation, exceptions, security and data, tracking, UI best practices, code analysis, wikilinks). Stack and layout are filled from what is detected. |
| New, you give a standard | Your wording wins; the bundled rules only fill the topics you did not cover. |
| Existing (brownfield) | The project's own conventions, read from its configs, CI, contribution guide and commit history, written as descriptive rules. Only process rules (documentation, exceptions, tracking, code analysis, wikilinks) come from the template. |

All rules are plain Markdown owned by you after install; edit them freely. Re-running the skill never overwrites a file
you edited (a hash manifest in `.agents/.kuy-init.json` tells it apart).

## What it writes

- `.agents/rules/*.md`, `.agents/scripts/{wikilinks,code-index}.py`, `.agents/code-analysis/`, `.agents/.kuy-init.json`
- `AGENTS.md`: created, or extended with a managed block; your existing text is untouched
- `.gitignore`: `.agents/` and `AGENTS.md` appended (skipped for anything git already tracks)

It never changes your source, configs or lockfiles, and never commits or deletes. Because `.agents/` is ignored by
default, teammates do not receive the rules unless they run the skill too or you remove the lines from `.gitignore`.

## Wikilinks

Every `.md` under `.agents/` must be reachable from its folder hub, and hubs from `AGENTS.md`.
`python3 .agents/scripts/wikilinks.py` regenerates the hubs; `--check` exits 1 when anything is orphaned or stale.

## Code analysis

`python3 .agents/scripts/code-index.py` writes one line per function, method, class, type, enum and constant:
`name | kind | path:line | signature | doc`, split per directory, incremental by file hash.
Search it with `grep -n -i "<name>" .agents/code-analysis/*.md`. Python is parsed exactly; TypeScript/JavaScript, PHP, Go,
Java, Kotlin, C#, Rust, Ruby and Swift use best-effort patterns. When graphify is installed with a graph, the index is
skipped unless you pass `--force`.

## Tests

`evals/triggers-kuy-init.json` holds trigger queries; run `python3 evals/run-triggers.py evals/triggers-kuy-init.json`
(drives the `claude` CLI; billed sessions). `evals/fixtures/` holds a small mixed-language project for the scripts.

MIT licensed.
