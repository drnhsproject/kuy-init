# Architecture

- Keep business rules independent of frameworks, I/O and presentation. Dependencies point inward: presentation and infrastructure may know the domain, never the reverse.
- A typical layering (adapt to what the project already has): **domain** (entities, rules) → **application** (use cases, orchestration) → **infrastructure** (database, HTTP, files) → **presentation** (UI, controllers, CLI).
- No business logic in controllers, views or components; no I/O in domain code.
- External systems sit behind one adapter each, so they can be replaced or faked in tests.
- A module exposes a small public surface; other modules import only from it, not from its internals.
- Configuration comes from the environment or a config file, never from literals scattered in code.
- When a feature needs a structural change, write the decision down (short ADR in `docs/` or the plan) before coding.
