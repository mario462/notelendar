import uvicorn

from app import APP, gcal_api
from app.authentication import authenticator
from app.models.google import Event


@APP.get("/", response_model=list[Event], response_model_by_alias=False)
def get_events(day: str):
    credentials = authenticator.authenticate()
    gcal_service = gcal_api.build_service(credentials)
    return gcal_api.get_events(gcal_service, day=day)


if __name__ == "__main__":
    uvicorn.run(APP, host="0.0.0.0", port=8000)
