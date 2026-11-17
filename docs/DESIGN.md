# Design: Social Media Studio
## 1. Constraint profiles
| Platform | Max length | Tone | Max hashtags |
|---|---|---|---|
| telegram | 4096 | conversational | 3 |
| x | 280 | punchy, casual | 2 |
| linkedin | 3000 | professional | 5 |
Each variant is validated against its profile before it can reach review.
## 2. Data model
**posts** (the single source of truth)
- id, title, source_url (nullable), body_markdown, created_at
**variants**
- id, post_id, platform, text, status, created_at, updated_at
- status: draft | approved | rejected | published
**slots** (a variant scheduled at a time)
- id, variant_id, scheduled_at, status (pending | done), idempotency_key (UNIQUE)
- idempotency_key = variant_id + scheduled_at, so the same variant in the same slot can only exist once
**publish_attempts** (the visible history)
- id, slot_id, result (success | failed), external_url (nullable), error (nullable), attempted_at
## 3. API surface
| Method | Path | Purpose |
|---|---|---|
| POST | /posts | Ingest a post (URL or pasted Markdown) |
| POST | /posts/{id}/variants | Generate variants for configured platforms |
| GET | /variants | List variants (filter by status) |
| PATCH | /variants/{id} | Edit variant text (re-validated) |
| POST | /variants/{id}/approve | draft -> approved |
| POST | /variants/{id}/reject | draft -> rejected |
| POST | /variants/{id}/schedule | Schedule an approved variant (4xx if not approved) |
| GET | /history | Publish attempts and their results |
## 4. Non-goal
No image generation, analytics, or real Instagram/X/LinkedIn accounts. Mock adapters plus one real platform (Telegram) prove the architecture.
