# Evidence
One proof for each requirement. Commands assume the server is running at http://127.0.0.1:8000.
## 1. Ingestion (pasted Markdown and URL)
```powershell
$body = @{ title = "Why idempotency matters"; body_markdown = "Retries are a fact of life. A publish system that posts twice loses trust. Use idempotency keys so one action stays one action." } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/posts -ContentType "application/json" -Body $body
```
Result: the post is stored and returned with `id: 1`. `POST /posts/from-url` stores a fetched page with `source_url` set.
## 2. Constraint profiles are enforced by code
```powershell
$bad = @{ post_id = 2; platform = "x"; text = ("a" * 300) } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/variants -ContentType "application/json" -Body $bad
```
Result (HTTP 422, nothing stored):{“detail”:[“max_length: 300 chars exceeds the 280 limit for x”]}
`GET /variants` afterwards still lists only the 3 valid drafts, so a rule-breaking variant never reaches review.
## 3. Generation makes one variant per platform, without duplicates
`POST /posts/2/variants` creates x, telegram and linkedin variants (all `draft`). Calling it a second time creates nothing: `GET /variants` still returns exactly 3.
