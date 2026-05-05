import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "feature_repo" / "data"
DATA_DIR.mkdir(exist_ok=True)

def setup_feast_data():
    print("--- Setting up Feast Sample Data ---")
    
    # 1. User Profiles
    profile_df = pd.DataFrame({
        "user_id": ["u_001", "u_002"],
        "language_preference": ["vi", "en"],
        "reading_speed_wpm": [200, 250],
        "topic_affinity": ["AI & Machine Learning", "Cloud Infrastructure"],
        "event_timestamp": [datetime.now()] * 2,
        "created": [datetime.now()] * 2
    })
    profile_df.to_parquet(DATA_DIR / "user_profiles.parquet")
    print(f"Created {DATA_DIR / 'user_profiles.parquet'}")

    # 2. User Activity
    activity_df = pd.DataFrame({
        "user_id": ["u_001", "u_002"],
        "query_count_1h": [12, 5],
        "last_topic": ["FastAPI", "Kubernetes"],
        "event_timestamp": [datetime.now()] * 2,
        "created": [datetime.now()] * 2
    })
    activity_df.to_parquet(DATA_DIR / "user_activity.parquet")
    print(f"Created {DATA_DIR / 'user_activity.parquet'}")

def setup_qdrant():
    print("\n--- Setting up Qdrant Collection ---")
    # Using in-memory for POC simplicity or local server if preferred.
    # To keep it consistent with the lab, we'll use a local file-based qdrant or memory.
    client = QdrantClient(path=str(BASE_DIR / "qdrant_storage"))
    
    COLLECTION_NAME = "ai_memory"
    
    # Recreate collection
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    print(f"Collection '{COLLECTION_NAME}' created at {BASE_DIR / 'qdrant_storage'}")

if __name__ == "__main__":
    setup_feast_data()
    setup_qdrant()
    print("\nInfrastructure setup complete.")
