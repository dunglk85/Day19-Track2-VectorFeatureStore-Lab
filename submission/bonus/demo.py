import sys
from pathlib import Path

# Fix for Windows console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from agent import HybridMemoryAgent

def run_demo():
    print("=== AI HYBRID MEMORY DEMO ===\n")
    agent = HybridMemoryAgent()

    # 1. Pre-populate Memory
    print("--- Step 1: Nạp ký ức (Remembering) ---")
    memories = [
        "Kubernetes là một nền tảng mã nguồn mở để tự động hóa việc triển khai, mở rộng và quản lý các ứng dụng container.",
        "Tôi đang học về Docker và cách đóng gói ứng dụng.",
        "Cloud Security yêu cầu hiểu rõ về Shared Responsibility Model, IAM và mã hóa dữ liệu.",
        "Tự động mở rộng (Auto-scaling) giúp hạ tầng đáp ứng linh hoạt theo lưu lượng truy cập thực tế.",
        "Lần cuối cùng tôi xem tài liệu về Terraform là tuần trước."
    ]
    
    for m in memories:
        agent.remember(m, user_id="u_001")
    print("Dữ liệu đã được nạp vào Qdrant.\n")

    # 2. Run 5 Scenarios
    scenarios = [
        ("Hỏi đơn giản (Vector hit)", "Tôi đã đọc gì về Kubernetes?"),
        ("Cần thông tin hồ sơ (Profile context)", "Recommend tôi nên đọc gì tiếp theo?"),
        ("Cần hoạt động gần đây (Fresh activity)", "Tôi đang quan tâm gì gần đây?"),
        ("Hỏi theo cách diễn đạt khác (Paraphrase)", "Tài liệu về tự động mở rộng hạ tầng?"),
        ("Hỏi hỗn hợp (Mixed Hybrid + Profile)", "Cho tôi summary về cloud security và lộ trình học phù hợp.")
    ]

    for title, query in scenarios:
        print(f"--- Scenario: {title} ---")
        print(f"Query: '{query}'")
        context = agent.recall(query, user_id="u_001")
        print(context)
        print("-" * 50 + "\n")

if __name__ == "__main__":
    run_demo()
