from datetime import datetime

from sqlmodel import Field, SQLModel


class Note(SQLModel, table=True):
    event_id: str = Field(default=None, primary_key=True)
    content: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
