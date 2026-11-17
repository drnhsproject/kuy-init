# Performance

- Measure before optimizing; record the number you improved.
- Avoid queries or requests inside loops; batch or cache instead. Watch for N+1 access.
- Do heavy work off the hot path (background job, lazy load, pagination, streaming).
- Bound everything that grows: page sizes, cache sizes, retries, timeouts.
- Keep payloads and bundles small; load code and assets only when needed.
- A change that slows a measured path needs an explicit note and approval.
