# Hướng dẫn: AI Hybrid Memory (Bonus Challenge)

Hệ thống này là một Proof of Concept (POC) cho trợ lý ảo cá nhân có bộ nhớ, kết hợp giữa **Vector Store** (Qdrant) để lưu trữ ký ức hội thoại và **Feature Store** (Feast) để quản lý hồ sơ người dùng ổn định.

## 1. Yêu cầu hệ thống
- Python 3.9+
- Đã cài đặt các thư viện trong `requirements.txt` của lab chính.
- Môi trường ảo (Virtual Environment) `.venv` đã được khởi tạo.

## 2. Cấu trúc thư mục
```text
submission/bonus/
├── ARCHITECTURE.md    # Tài liệu thiết kế & Tradeoffs
├── README.md          # Tài liệu này
├── agent.py           # Logic chính của HybridMemoryAgent
├── demo.py            # Script chạy 5 kịch bản demo
├── setup_infra.py     # Script khởi tạo dữ liệu & Qdrant
└── feature_repo/      # Cấu hình Feast Feature Store
```

## 3. Các bước cài đặt và chạy

### Bước 1: Khởi tạo hạ tầng và dữ liệu mẫu
Script này sẽ tạo dữ liệu người dùng mẫu (Parquet) và khởi tạo collection trong Qdrant.
```powershell
.venv\Scripts\python submission/bonus/setup_infra.py
```

### Bước 2: Cấu hình Feature Store (Feast)
Chúng ta cần đăng ký các tính năng (apply) và đưa dữ liệu vào bộ nhớ online (materialize) để truy xuất nhanh.
```powershell
# Di chuyển vào repo của feast (nếu dùng terminal thủ công)
cd submission/bonus/feature_repo
..\..\..\.venv\Scripts\feast apply
..\..\..\.venv\Scripts\feast materialize-incremental 2027-01-01T00:00:00
cd ..\..\..
```

### Bước 3: Chạy Demo
Script này sẽ nạp một số ký ức vào hệ thống và thực hiện 5 kịch bản truy vấn khác nhau để kiểm tra sự kết hợp giữa Profile và Memory.
```powershell
.venv\Scripts\python submission/bonus/demo.py
```

## 4. Các Scenarios trong Demo
1. **Hỏi đơn giản:** Chỉ sử dụng Vector Search để tìm thông tin về Kubernetes.
2. **Cá nhân hóa:** Recommend nội dung dựa trên `topic_affinity` trong Feature Store.
3. **Hoạt động gần đây:** Nhận diện mức độ active của người dùng trong 1h qua.
4. **Diễn đạt khác:** Kiểm tra khả năng hiểu ngữ nghĩa (Semantic Search).
5. **Truy vấn hỗn hợp:** Kết hợp thông tin từ cả 2 kho dữ liệu để đưa ra lộ trình học cá nhân hóa.

---
*Lưu ý: POC này sử dụng Qdrant ở chế độ local storage (file-based) bên trong thư mục `submission/bonus/qdrant_storage`.*
