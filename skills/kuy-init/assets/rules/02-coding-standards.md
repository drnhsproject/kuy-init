# Coding Standards

- **Small units**: one responsibility per function, class and file. Split before a unit needs a section comment to be readable.
- **Naming**: names describe the business meaning, never `a`, `tmp`, `data2`. Follow the language's own casing convention (see the formatter or linter config) and keep one convention per project.
- **Types**: use the strongest typing the language offers. No untyped escape hatches (`any`, unchecked casts, untyped dicts) at module boundaries; validate data that comes from outside.
- **Control flow**: prefer guard clauses and early returns to deep nesting; replace long `if/else` chains on a variant with a lookup table or a polymorphic structure.
- **DRY with judgment**: extract on the third repetition, not the first; reuse existing helpers before writing new ones (search the code index first, see [[rules/13-code-analysis]]).
- **Errors**: handle errors where there is enough context to act; never swallow them silently; surface a useful message and keep the original cause.
- **Comments** explain why, not what. Remove commented-out code.
- **Imports** grouped: standard library, third-party, local. Remove unused ones.
- **Formatting** belongs to the project's formatter and linter; do not hand-format against them.
