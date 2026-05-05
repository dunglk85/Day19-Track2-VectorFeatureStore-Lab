import os
from pathlib import Path
from typing import List, Optional

from fastembed import TextEmbedding
from feast import FeatureStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams, Filter, FieldCondition, MatchValue

# Constants
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
EMBED_DIM = 384
COLLECTION_NAME = "ai_memory"

class HybridMemoryAgent:
    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            base_dir = Path(__file__).parent
        
        self.base_dir = base_dir
        
        # 1. Initialize Vector Store (Qdrant)
        # Using local storage path set in setup_infra.py
        self.qdrant = QdrantClient(path=str(self.base_dir / "qdrant_storage"))
        
        # 2. Initialize Feature Store (Feast)
        # Point to the feature_repo directory
        self.fs = FeatureStore(repo_path=str(self.base_dir / "feature_repo"))
        
        # 3. Initialize Embedding Model
        self.embedder = TextEmbedding(model_name=EMBED_MODEL)

    def _chunk_text(self, text: str) -> List[str]:
        """Simple chunking by sentence or fixed length for POC.
        In a real app, we'd use 'underthesea' for Vietnamese segmentation.
        """
        # For POC, we split by common sentence enders
        import re
        sentences = re.split(r'(?<=[.!?]) +', text)
        return [s.strip() for s in sentences if s.strip()]

    def remember(self, text: str, user_id: str = "u_001") -> None:
        """Add a new piece of episodic memory for this user."""
        chunks = self._chunk_text(text)
        if not chunks:
            return

        # Generate embeddings
        vectors = list(self.embedder.embed(chunks))
        
        # Prepare points for Qdrant
        points = []
        import uuid
        for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector.tolist(),
                payload={
                    "user_id": user_id,
                    "text": chunk,
                    "timestamp": os.times()[4] # Placeholder for real timestamp
                }
            ))
        
        # Upsert to Qdrant
        self.qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print(f"--- [Memory] Added {len(chunks)} chunks for User {user_id}")

    def recall(self, query: str, user_id: str = "u_001") -> str:
        """Retrieve top-K memories + user profile features -> return assembled context."""
        
        # 1. Get User Profile + Recent Activity from Feast
        entity_rows = [{"user_id": user_id}]
        features = [
            "user_profile:language_preference",
            "user_profile:reading_speed_wpm",
            "user_profile:topic_affinity",
            "user_activity:query_count_1h",
            "user_activity:last_topic"
        ]
        
        online_features = self.fs.get_online_features(
            features=features,
            entity_rows=entity_rows
        ).to_dict()
        
        # Extract feature values (handling possible Nones)
        lang = online_features.get("language_preference", ["Unknown"])[0]
        speed = online_features.get("reading_speed_wpm", [0])[0]
        affinity = online_features.get("topic_affinity", ["General"])[0]
        q_count = online_features.get("query_count_1h", [0])[0]
        
        # 2. Search Qdrant filtered by user_id
        query_vector = next(self.embedder.embed([query]))
        
        search_results = self.qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(value=user_id)
                    )
                ]
            ),
            limit=3
        )
        
        memories = [res.payload["text"] for res in search_results.points]
        memories_str = "\n- ".join(memories) if memories else "Không có ký ức liên quan."

        # 3. Assemble Context String
        # (Personalization logic based on profile)
        context = f"""
[USER PROFILE]
- ID: {user_id}
- Ngôn ngữ ưu tiên: {lang}
- Tốc độ đọc: {speed} wpm
- Lĩnh vực quan tâm: {affinity}

[RECENT ACTIVITY]
- Số câu hỏi trong 1h qua: {q_count}

[RELEVANT MEMORIES]
- {memories_str}

[SYSTEM INSTRUCTION]
Người dùng này thích được phản hồi bằng {lang}. 
Dựa vào tốc độ đọc {speed} wpm, hãy đưa ra câu trả lời {'ngắn gọn' if speed > 220 else 'chi tiết'}.
Lưu ý sở thích về {affinity} khi đưa ra ví dụ.
"""
        return context

if __name__ == "__main__":
    import sys
    # Fix for Windows console encoding
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        
    # Quick internal test
    agent = HybridMemoryAgent()
    agent.remember("Tôi đang nghiên cứu về kiến trúc Microservices và gRPC.", "u_001")
    ctx = agent.recall("Tôi quan tâm đến công nghệ gì?", "u_001")
    print(ctx)
