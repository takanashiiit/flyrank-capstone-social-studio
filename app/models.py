from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
def utcnow() -> datetime:
    return datetime.now(timezone.utc)
class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    source_url: Optional[str] = None
    body_markdown: str
    created_at: datetime = Field(default_factory=utcnow)
class Variant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    platform: str
    text: str
    status: str = "draft"  # draft | approved | rejected | published
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
class Slot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    variant_id: int = Field(foreign_key="variant.id")
    scheduled_at: datetime
    status: str = "pending"  # pending | done
    idempotency_key: str = Field(unique=True, index=True)
class PublishAttempt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slot_id: int = Field(foreign_key="slot.id")
    result: str  # success | failed
    external_url: Optional[str] = None
    error: Optional[str] = None
    attempted_at: datetime = Field(default_factory=utcnow)
