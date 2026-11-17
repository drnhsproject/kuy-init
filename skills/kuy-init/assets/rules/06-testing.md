# Testing

- Every behaviour change ships with a test that fails on the old code.
- Pure logic gets unit tests; boundaries (database, HTTP, files) get integration tests against a fake or a disposable instance.
- Bug fixes start with a reproducing test.
- Tests are deterministic: no real network, real clock or shared mutable state unless the test is explicitly an end-to-end test.
- Test names state the behaviour, not the function name.
- Never weaken or delete a test to make a change pass; fix the cause or record the reason.
- Use the project's own test command (see [[rules/01-tech-stack]]); do not add a second runner.
