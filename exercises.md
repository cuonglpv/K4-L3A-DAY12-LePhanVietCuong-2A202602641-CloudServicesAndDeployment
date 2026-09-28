# Phiếu phản ánh: K4 Level 3A, Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code, không sao chép đáp án của người khác.
>
> Cách trả lời: ghi câu trả lời ngay bên dưới từng câu hỏi.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Lê Phan Việt Cường  Mã học viên: 2A202602641

---

### Câu 1: Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> Khi đưa app lên Railway, nếu quên `AGENT_API_KEY` mà code âm thầm dùng
> `changeme`, endpoint `/ask` vẫn chạy nhưng ai đoán được giá trị đó đều gọi
> được API. Với fail fast, container không trở thành Online; log deployment
> chỉ ngay biến thiếu để tôi bổ sung secret trước khi có traffic thật.

---

### Câu 2: Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

> Một log tôi dùng có dạng `{"timestamp":"2026-09-29T10:15:02Z","level":"info","event":"ask_completed","user_id":"demo-01","cost_usd":0.002}`.
> Tôi có thể lọc tất cả request lỗi hoặc chậm của riêng `demo-01`, và cộng
> `cost_usd` theo ngày để phát hiện chi phí bất thường. Chuỗi `print` tự do
> không có trường cố định nên rất khó lọc, thống kê hoặc đặt cảnh báo.

---

### Câu 3: Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản thử) | 189.1 MB |
| Multi-stage | 192.1 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

> Lần đo này multi-stage lại lớn hơn khoảng 3 MB. Bản một-stage dùng trực tiếp
> package cài vào Python base image; bản multi-stage có thêm một virtualenv
> riêng. Vì dependencies của lab đều có wheel và pip dùng `--no-cache-dir`,
> builder không để lại nhiều file thừa để cắt giảm. Multi-stage vẫn hữu ích khi
> phải cài compiler hoặc công cụ build, vì những thứ đó không cần ở image chạy.

---

### Câu 4: Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

> Sửa `app/main.py` chỉ làm Docker chạy lại `COPY app ./app` và các layer sau
> nó; layer cài dependencies vẫn lấy từ cache vì `requirements.txt` chưa đổi.
> Nếu `COPY . .` đứng trước `RUN pip install`, mọi sửa đổi source làm checksum
> của layer COPY đổi và buộc pip cài lại toàn bộ dependency, dù requirements
> giống hệt.

---

### Câu 5: Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

> Một lỗ hổng RCE có thể cho kẻ tấn công chạy lệnh trong container. Nếu process
> là root, họ đọc/ghi được mọi file mà root trong container thấy và có thêm cơ
> hội khai thác cấu hình Docker hoặc kernel để leo ra host. `USER appuser`
> không xóa RCE, nhưng hạ quyền của process xuống UID 10001: các file hệ thống
> và thao tác đặc quyền bị từ chối, giảm đáng kể tác động nếu bị xâm nhập.

---

### Câu 6: Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

> Họ có thể gửi 10 request ở giây 59 của một phút và thêm 10 request ở giây 00
> của phút kế tiếp: tổng 20 request trong khoảng 2 giây. Sliding window giữ
> toàn bộ request 60 giây gần nhất nên sau 10 request đầu, 10 request sau vẫn
> bị tính vào cùng hạn mức và bị chặn.

---

### Câu 7: Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

> Rate limit đo nhịp gửi request trong một cửa sổ ngắn; cost guard đo tổng tiền
> đã tiêu theo user trong kỳ ngân sách. Một user còn dưới 10 request/phút nhưng
> đã dùng hết ngân sách tháng sẽ qua rate limit và bị cost guard trả 402. Ngược
> lại, user mới còn toàn bộ ngân sách nhưng bấm gửi liên tục 11 lần/phút sẽ bị
> rate limit trả 429 trước khi chi phí trở thành vấn đề.

---

### Câu 8: /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

> Nếu `/health` kiểm tra Redis, lúc Redis mất 30 giây cả ba container lần lượt
> bị orchestrator coi là chết, bị rút khỏi load balancer và có thể bị restart.
> Các restart đồng thời lại làm Redis vừa hồi phục phải nhận nhiều kết nối. Với
> `/health` nông, process vẫn sống; `/ready` mới trả 503 để load balancer tạm
> ngừng gửi request phụ thuộc Redis, nên tránh restart dây chuyền.

---

### Câu 9: Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

> Với Redis, dù request vào replica nào thì `history_length` của cùng user vẫn
> tăng liên tục vì lịch sử ở shared store. Nếu dùng dict Python, mỗi replica có
> một bản riêng: request luân phiên sẽ cho các chuỗi như 1, 1, 2, 1 thay vì
> 1, 2, 3, 4; restart replica còn làm mất hẳn phần lịch sử của nó.

---

### Câu 10: Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

> Lần đầu phần CP5 chỉ có `http://localhost:18080`, nên đây không phải public
> HTTPS URL để trình chấm truy cập. Tôi kiểm tra yêu cầu CP5, vào Railway >
> Settings > Networking và dùng **Generate Domain**. Sau khi service và Redis
> Online, URL `https://k4-l3a-day12-lephanvietcuong-2a202602641-cloudse-production.up.railway.app/health`
> trả HTTP 200; URL này đã được ghi vào `DEPLOYMENT.md` mà không ghi API key.
