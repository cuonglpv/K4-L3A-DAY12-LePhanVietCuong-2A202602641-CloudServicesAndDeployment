# Ghi nhận deploy

- Họ tên: Lê Phan Việt Cường
- Mã học viên: 2A202602641
- Nền tảng: Railway, dùng Dockerfile và Redis quản lý sẵn
- Public URL: https://k4-l3a-day12-lephanvietcuong-2a202602641-cloudse-production.up.railway.app

## Biến môi trường

Trên Railway đã đặt `AGENT_API_KEY`, `REDIS_URL`, `RATE_LIMIT_PER_MINUTE`,
`MONTHLY_BUDGET_USD` và `LOG_LEVEL`. Giá trị secret không xuất hiện trong repo.

## Kiểm tra

Ngày 29-09-2026, tôi build Docker image thành công. Trên Railway, service app
và Redis đều ở trạng thái Online.

- `GET https://k4-l3a-day12-lephanvietcuong-2a202602641-cloudse-production.up.railway.app/health`
  trả HTTP 200 với `{"status":"ok","service":"day12-agent","version":"1.0.0"}`.
- `/ask` yêu cầu header `X-API-Key`. Tôi không ghi giá trị key vào tài liệu hay repo.

## Ảnh kiểm tra

Thư mục `screenshots/` có các ảnh sau:

- `health.jpg`: `/health` trả HTTP 200.
- `ready.jpg`: `/ready` cho biết Redis sẵn sàng.
- `ask-401.jpg`: gọi `/ask` không có API key nhận HTTP 401.
- `ask-success.jpg`: gọi `/ask` có API key nhận HTTP 200; key không hiện trên ảnh.
- `docker-compose.jpg`: kiểm tra local trước khi deploy, cả `agent` và `redis` đều healthy.
