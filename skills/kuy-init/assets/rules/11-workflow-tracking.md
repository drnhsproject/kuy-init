# Workflow & Progress Tracking

Lightweight paper trail under `.agents/` so work survives a session ending. All files follow [[rules/14-wikilinks]].

- **Plans** (`plans/YYYY/MM/DD/<date>-<slug>.md`): goal, findings with `file:line`, tasks as a checklist, execution log. One plan per piece of work.
- **Fix history** (`changelog/CHANGELOG_FIXES.md`): after a bug fix is verified, add an entry at the top: symptom, root cause, fix, verification with real numbers, lesson. Search it with `grep -n -i "<symptom>"` before fixing a bug; never read it whole.
- **Handoffs** (`handoffs/<topic>.md`): only for work that will cross a session. Status, what is done, next steps, traps found. Delete it when the work is verified done.
- **Analyses** (`analysis/YYYY/MM/DD/<date>-<slug>.md`): finished knowledge that is not a fix.
- Tick a task only after its own check ran and passed.
