# Deployment record

- Họ tên: Lê Phan Việt Cường
- Mã học viên: 2A202602641
- Nền tảng: local fallback (Docker Compose)
- Public URL: Local fallback — `http://localhost:18080` (cổng 8000 và 8001
  đã được dịch vụ khác trên máy sử dụng khi kiểm tra).

## Environment variables configured

`AGENT_API_KEY`, `REDIS_URL`, `RATE_LIMIT_PER_MINUTE`,
`MONTHLY_BUDGET_USD`, `HISTORY_MAX_MESSAGES`, `HISTORY_TTL_SECONDS`, and
`LOG_LEVEL` are configured locally. Secret values are not recorded here.

## Verification

The Docker production image built successfully on 2026-09-29. The local
fallback stack was started with `$env:PORT='18080'; docker compose up -d`; Redis was
healthy and the agent container was running.

- `GET /health` returned HTTP 200 and `{"status":"ok"}`.
- `GET /ready` returned HTTP 200 and `{"status":"ready","redis":true}`.
- `POST /ask` without `X-API-Key` returned HTTP 401.

## Evidence

The following evidence files are included in `screenshots/`:

- `health.jpg` — liveness response HTTP 200.
- `ready.jpg` — readiness response HTTP 200 with Redis ready.
- `ask-401.jpg` — `/ask` without an API key returns HTTP 401.
- `ask-success.jpg` — `/ask` with an API key returns HTTP 200; the key is
  loaded through a variable and is not visible in the screenshot.
- `docker-compose.jpg` — both `agent` and `redis` containers are healthy.

Local fallback was selected because no Railway/Render account credentials are
stored in this repository; this fallback is worth at most 9/15 for CP5.
