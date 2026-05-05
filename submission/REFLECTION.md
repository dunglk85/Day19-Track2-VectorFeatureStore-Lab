# Reflection — Lab 19

**Tên:** _DungLK_2A202600100
**Cohort:** _A20-K2_
**Path đã chạy:** _lite_

---

## Câu hỏi (≤ 200 chữ)

> Trên golden set 50 queries, mode nào thắng ở loại query nào (`exact` /
> `paraphrase` / `mixed`), và tại sao? Khi nào bạn **không** dùng hybrid
> (i.e. khi nào pure BM25 hoặc pure vector là lựa chọn đúng)?

- **Exact:** BM25 thường thắng do khả năng khớp chính xác các từ khóa kỹ thuật (ví dụ: gRPC, IAM).
- **Paraphrase:** Vector Search thắng vượt trội nhờ hiểu được ngữ nghĩa và các từ đồng nghĩa (ví dụ: "tự động mở rộng" vs "auto-scaling").
- **Mixed:** Hybrid (RRF) là lựa chọn tối ưu nhất vì nó kết hợp được sự chính xác của BM25 và độ phủ của Vector.

**Khi nào không dùng Hybrid:**
- Dùng **Pure BM25** khi dữ liệu là các mã định danh, ID hoặc thuật ngữ cực kỳ đặc thù mà không có biến thể ngữ nghĩa.
- Dùng **Pure Vector** khi query có độ nhiễu cao, sai chính tả nhiều hoặc khi cần tìm kiếm xuyên ngôn ngữ (cross-lingual) mà từ khóa không khớp nhau.

---

## Điều ngạc nhiên nhất khi làm lab này

Sự kết hợp giữa Feast và Qdrant giúp Agent có một "trí nhớ" cực kỳ sống động, không chỉ nhớ nội dung mà còn biết cách điều chỉnh tông giọng dựa trên hồ sơ người dùng.

---

## Bonus challenge

- [x] Đã làm bonus (xem `submission/bonus/`)
- [ ] Pair work với: _None_
