import uvicorn

from app import APP, gcal_api
from app.authentication import authenticator


@APP.get("/")
def get_events(day: str) -> list[object]:
    credentials = authenticator.authenticate()
    gcal_service = gcal_api.build_service(credentials)
    return gcal_api.get_events(gcal_service, day=day)


if __name__ == "__main__":
    uvicorn.run(APP, host="0.0.0.0", port=8000)
