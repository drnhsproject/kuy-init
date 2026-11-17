# UI Best Practices

Applies only when the project has a user interface. Use the project's design system and tokens when one exists.

- **Design tokens**: colors, spacing, type sizes and radii come from tokens or shared constants, not new literals. Prefer relative units (`rem`/`em`) for type and spacing.
- **Responsive**: design mobile-first, test at phone, tablet and desktop widths, never rely on hover alone, keep tap targets at least 44x44 CSS px.
- **Accessibility**: semantic elements before ARIA; every control reachable and operable by keyboard with a visible focus state; text contrast at least 4.5:1; images have text alternatives; form inputs have labels and error text tied to them; when the focused element disappears, move focus somewhere sensible.
- **Loading, empty and error states** are designed for every data-driven view: skeletons or spinners follow the real in-flight state (including stale data shown while refreshing), empty states say what to do next, errors say what failed and offer retry.
- **Feedback**: interactive elements show hover, focus, pressed and disabled states; respect `prefers-reduced-motion`; keep animation short and purposeful.
- **Stable rendering**: no layout shift while loading (reserve space); keep object and callback identity stable when passing them to memoized children.
- **Fidelity**: when a design or screenshot is given, match it and verify visually in a real browser at more than one width; do not invent content the design does not show.
- **Components**: small, single-purpose, presentation only; data and business logic live outside them (see [[rules/03-architecture]]).
