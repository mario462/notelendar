import datetime
import logging

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build


def build_service(credentials: Credentials) -> Resource:
    return build('calendar', 'v3', credentials=credentials)


def get_events(calendar_service: Resource, max_results: int = 10) -> list[object]:
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # gets the next max_results events
    events_result = (
        calendar_service.events()
        .list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime',
        )
        .execute()
    )
    events = events_result.get('items', [])

    logging.debug(f'Fetched {len(events)} events.', data=events)
    return events
