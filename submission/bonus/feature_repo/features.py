from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.types import Int64, String

# 1. Entity: The User
user = Entity(name="user", join_keys=["user_id"], value_type=ValueType.STRING)

# 2. Data Sources (Simulated with Parquet for POC)
profile_source = FileSource(
    path="data/user_profiles.parquet",
    timestamp_field="event_timestamp",
)

activity_source = FileSource(
    path="data/user_activity.parquet",
    timestamp_field="event_timestamp",
)

# 3. Feature View: User Stable Profile
user_profile_view = FeatureView(
    name="user_profile",
    entities=[user],
    ttl=timedelta(days=365),
    schema=[
        Field(name="language_preference", dtype=String),
        Field(name="reading_speed_wpm", dtype=Int64),
        Field(name="topic_affinity", dtype=String),
    ],
    online=True,
    source=profile_source,
)

# 4. Feature View: Recent Activity (Simulated)
user_activity_view = FeatureView(
    name="user_activity",
    entities=[user],
    ttl=timedelta(hours=1),
    schema=[
        Field(name="query_count_1h", dtype=Int64),
        Field(name="last_topic", dtype=String),
    ],
    online=True,
    source=activity_source,
)
