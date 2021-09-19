from typing import Optional

from sqlalchemy.future import Engine
from sqlmodel import Session, select

from app import ENGINE, LOGGER
from app.models.note import Note
from sqlalchemy.exc import NoResultFound


class DuplicatedNoteException(Exception):
    error_code = '0f7ff30f-d3be-4bb5-9f8e-6ef840fb181d'

    def __init__(self, event_id: str):
        self.event_id = event_id

    def error_message(self):
        return f"There's already a note for event with ID '{self.event_id}' in the DB"


class NoteNotFoundException(Exception):
    error_code = 'fb911e30-45ce-4d51-add5-6802f1b22d58'

    def __init__(self, event_id: str):
        self.event_id = event_id

    def error_message(self):
        return f"Could not find a note for event with ID '{self.event_id}' in the DB"


class NoteService:
    def __init__(self, engine: Engine = ENGINE, session: Optional[Session] = None):
        self.engine = engine
        self.session = session if session else Session(self.engine)

    def get(self, event_id: str, strict: bool = False) -> Optional[Note]:
        q = select(Note).where(Note.event_id == event_id)
        results = self.session.exec(q)
        if strict:
            try:
                return results.one()
            except NoResultFound:
                exception = NoteNotFoundException(event_id=event_id)
                LOGGER.error(exception.error_message())
                raise exception
        return results.first()

    def create_note(self, note: Note) -> Note:
        if self.get(event_id=note.event_id):
            exception = DuplicatedNoteException(event_id=note.event_id)
            LOGGER.error(exception.error_message())
            raise exception
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note

    def get_or_create_note(self, event_id: str) -> Note:
        return self.get(event_id=event_id) or self.create_note(Note(event_id=event_id))

    def update_note(self, note: Note) -> Note:
        existing_note = self.get(event_id=note.event_id, strict=True)
        existing_note.content = note.content
        existing_note.updated_at = note.updated_at
        self.session.add(existing_note)
        self.session.commit()
        self.session.refresh(existing_note)
        return existing_note

    def delete_note(self, event_id: str):
        note = self.get(event_id=event_id, strict=True)
        self.session.delete(note)
        self.session.commit()
