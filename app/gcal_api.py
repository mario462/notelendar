from typing import Optional

import arrow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build
from pydantic import parse_obj_as

from app.models.google import Event


def build_service(credentials: Credentials) -> Resource:
    return build('calendar', 'v3', credentials=credentials)


def get_events(calendar_service: Resource, *, day: Optional[str]) -> list[Event]:
    time_min: Optional[str] = None
    time_max: Optional[str] = None
    if day:
        time_min = arrow.get(day).isoformat()
        time_max = arrow.get(day).shift(days=+1).isoformat()
    if not time_min or not time_max:
        raise ValueError(
            "Couldn't figure a minimum or maximum time with the supplied params to fetch the events"
        )
    events_result = (
        calendar_service.events()
        .list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime',
        )
        .execute()
    )
    events = parse_obj_as(list[Event], events_result.get('items', []))
    return events
