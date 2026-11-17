# Tech Stack

> Descriptive and binding: this file records the stack the project uses. Change it deliberately, and update the code to match.

{{STACK}}

- Add a dependency only when the standard library or an existing dependency cannot do the job; note why in the change that adds it.
- Pin versions through the project's lockfile. Never edit a lockfile by hand.
- Do not introduce a second tool for something the project already solves (second HTTP client, second test runner, second formatter).
