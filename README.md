notelendar
===

The goal of this project is to be able to add notes to calendar events.

These notes should be resilient to event changes and user owned, meaning other participants of the event won't have access to them.

Currently we plan on only supporting Google Calendar but this could change in the future.

You can find the frontend of the app [here](https://github.com/mario462/notelendar-frontend)

Technologies used
===

Backend of the app is built using [FastAPI](https://fastapi.tiangolo.com/).

Models are being managed using [SQLModel](https://github.com/tiangolo/sqlmodel)

Development dependencies are managed using [Poetry](https://python-poetry.org/).

Requirements
===

In order to be able to run the authentication flow, there must be a `api_credentials.json` file under `app/authentication`. You can obtain this file by setting up a project and enabling the API as instructed [here](https://developers.google.com/workspace/guides/create-project)
