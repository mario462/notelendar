from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel


class Attendee(SQLModel, table=False):
    email: Optional[str]
    organizer: Optional[bool]
    self: Optional[bool]
    responseStatus: Optional[str]


class Date(SQLModel, table=False):
    dateTime: datetime


class Event(SQLModel, table=False):
    id: str = Field(default=None, primary_key=True)
    status: str
    htmlLink: str
    created: datetime
    updated: datetime
    summary: str
    creator: Attendee
    organizer: Attendee
    start: Date
    end: Date
    attendees: List[Attendee]
    hangoutLink: Optional[str]
