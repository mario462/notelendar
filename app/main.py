import uvicorn
from fastapi.responses import JSONResponse

from app import APP, gcal_api
from app.authentication import authenticator
from app.models.google import Event
from app.models.note import Note
from app.services.note import DuplicatedNoteException, NoteNotFoundException, NoteService


@APP.exception_handler(DuplicatedNoteException)
async def unicorn_exception_handler(_, exc: DuplicatedNoteException):
    return JSONResponse(
        status_code=400,
        content={"error_code": exc.error_code, "error_message": exc.error_message()},
    )


@APP.exception_handler(NoteNotFoundException)
async def unicorn_exception_handler(_, exc: DuplicatedNoteException):
    return JSONResponse(
        status_code=404,
        content={"error_code": exc.error_code, "error_message": exc.error_message()},
    )


@APP.get("/", response_model=list[Event], response_model_by_alias=False)
def get_events(day: str):
    credentials = authenticator.authenticate()
    gcal_service = gcal_api.build_service(credentials)
    return gcal_api.get_events(gcal_service, day=day)


@APP.get("/{event_id}/notes", response_model=Note)
def get_or_create_note(event_id: str):
    return NoteService().get_or_create_note(event_id)


@APP.post("/notes", response_model=Note, status_code=201)
def create_note(note: Note):
    return NoteService().create_note(note)


@APP.put("/notes", response_model=Note)
def update_note(note: Note):
    return NoteService().update_note(note)


@APP.delete("/{event_id}/notes", status_code=204)
def delete_note(event_id: str):
    return NoteService().delete_note(event_id)


if __name__ == "__main__":
    uvicorn.run(APP, host="0.0.0.0", port=8000)
