# Deployment record

- Họ tên: Lê Phan Việt Cường
- Mã học viên: 2A202602641
- Nền tảng: Railway (Dockerfile + managed Redis)
- Public URL: https://k4-l3a-day12-lephanvietcuong-2a202602641-cloudse-production.up.railway.app

## Environment variables configured

`AGENT_API_KEY`, `REDIS_URL`, `RATE_LIMIT_PER_MINUTE`,
`MONTHLY_BUDGET_USD`, and `LOG_LEVEL` are configured in Railway. Secret
values are not recorded here.

## Verification

The Docker production image built successfully on 2026-09-29. Railway shows
the application service and managed Redis service as Online.

- `GET https://k4-l3a-day12-lephanvietcuong-2a202602641-cloudse-production.up.railway.app/health`
  returned HTTP 200 and `{"status":"ok","service":"day12-agent","version":"1.0.0"}`.
- The deployed service is protected by `X-API-Key`; no key value is included
  in this document or the repository.

## Evidence

The following evidence files are included in `screenshots/`:

- `health.jpg` — liveness response HTTP 200.
- `ready.jpg` — readiness response HTTP 200 with Redis ready.
- `ask-401.jpg` — `/ask` without an API key returns HTTP 401.
- `ask-success.jpg` — `/ask` with an API key returns HTTP 200; the key is
  loaded through a variable and is not visible in the screenshot.
- `docker-compose.jpg` — both `agent` and `redis` containers are healthy in
  the local production-equivalent check before the Railway deployment.
