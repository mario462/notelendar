import logging
from typing import Optional
import datetime
import arrow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build


def build_service(credentials: Credentials) -> Resource:
    return build('calendar', 'v3', credentials=credentials)


def get_events(calendar_service: Resource, *, day: Optional[str]) -> list[object]:
    time_min: Optional[str] = None
    time_max: Optional[str] = None
    if day:
        time_min = arrow.get(day).isoformat()
        time_max = arrow.get(day).shift(days=+1).isoformat()
    if not time_min or not time_max:
        raise ValueError("Couldn't figure a minimum or maximum time with the supplied params to fetch the events")
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
    events = events_result.get('items', [])

    logging.info(f'Fetched {len(events)} events.', data=events)
    return events
