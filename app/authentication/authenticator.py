from __future__ import print_function

import os.path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file user_token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# The api_credentials file stores the credentials/API key for the web application as configured in the google console
CREDENTIALS_FILE = 'api_credentials.json'
# The user_token file stores the user's access and refresh tokens
# and is created automatically when the authorization flow completes for the first time
TOKEN_FILE = 'user_token.json'


def _abs_path(filename: str) -> str:
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)


def save_credentials(credentials: Credentials, token_file: str = TOKEN_FILE):
    """Saves the user credentials to a JSON file"""
    with open(_abs_path(token_file), 'w') as token:
        token.write(credentials.to_json())


def load_credentials(token_file: str = TOKEN_FILE) -> Optional[Credentials]:
    """Load user credentials stored in a JSON file"""
    path = _abs_path(token_file)
    if os.path.exists(path):
        return Credentials.from_authorized_user_file(path, SCOPES)
    return None


def auth_flow(
    credentials: Optional[Credentials], api_credentials_file: str = CREDENTIALS_FILE
) -> Credentials:
    """Run the Authentication flow in case there are no valid credentials available"""
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        path = _abs_path(api_credentials_file)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Couldn't find API credentials file {path}"
            )
        flow = InstalledAppFlow.from_client_secrets_file(path, SCOPES)
        # the port on which to run is not configurable since is the callback URI specified in the google console
        credentials = flow.run_local_server(port=9090)
    return credentials


def authenticate() -> Credentials:
    """Returns valid credentials for the user"""
    credentials = load_credentials()
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        credentials = auth_flow(credentials)
        # Save the credentials for the next run
        save_credentials(credentials)
    return credentials
