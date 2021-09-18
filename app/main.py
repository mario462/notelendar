import uvicorn
from fastapi import FastAPI

from app import gcal_api
from app.authentication import authenticator

app = FastAPI()


@app.get("/")
def get_events() -> list[object]:
    credentials = authenticator.authenticate()
    gcal_service = gcal_api.build_service(credentials)
    return gcal_api.get_events(gcal_service)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
