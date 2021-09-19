from datetime import datetime
from typing import List, Optional

from pydantic import HttpUrl
from sqlmodel import Field, SQLModel


class BaseGoogleModel(SQLModel, table=False):
    class Config:
        allow_population_by_field_name = True


class Attendee(BaseGoogleModel):
    email: Optional[str]
    organizer: Optional[bool]
    is_self: Optional[bool] = Field(alias="self")
    response_status: Optional[str] = Field(alias="responseStatus")


class DateTimeField(BaseGoogleModel):
    date_time: datetime = Field(alias="dateTime")


class Event(BaseGoogleModel):
    event_id: str = Field(default=None, primary_key=True, alias="id")
    status: str
    google_calendar_link: HttpUrl = Field(alias="htmlLink")
    created: datetime
    updated: datetime
    summary: str
    creator: Attendee
    organizer: Attendee
    start: DateTimeField
    end: DateTimeField
    attendees: List[Attendee]
    google_meet_link: Optional[HttpUrl] = Field(alias="hangoutLink")
