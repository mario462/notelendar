notelendar
===

The goal of this project is to be able to add notes to calendar events.

These notes should be resilient to event changes and user owned, meaning other participants of the event won't have access to them.

Currently we plan on only supporting Google Calendar but this could change in the future.

Technologies used
===

Backend of the app is written in [FastAPI](https://fastapi.tiangolo.com/) and frontend will be written in [VueJS](https://vuejs.org/).

Development dependencies are managed using [Poetry](https://python-poetry.org/).

Requirements
===

In order to be able to run the authentication flow, there must be a `api_credentials.json` file under `app/authentication`. You can obtain this file by setting up a project and enabling the API as instructed [here](https://developers.google.com/workspace/guides/create-project)