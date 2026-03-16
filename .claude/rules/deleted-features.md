---
globs: frontend/src/**
---

# Deleted Features — Do NOT Recreate

These pages were intentionally removed. Do not recreate routes, components, or navigation entries for them:
- `/contradictions`, `/dependencies`, `/influence-graph`, `/meeting-scores`
- `/resources`, `/risks`, `/scope`, `/topic-evolution`, `/workstreams`

These backend models/routers were also removed:
- `Workstream` model and `workstreams` router — replaced by the Project system (PR1-PR11)

If you encounter references to these in old code or comments, remove the references rather than recreating the features.
