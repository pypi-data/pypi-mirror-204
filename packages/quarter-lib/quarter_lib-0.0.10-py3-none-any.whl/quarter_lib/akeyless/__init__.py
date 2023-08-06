import os
from ..logging import setup_logging

import requests
from dotenv import load_dotenv

logger = setup_logging(__file__)
values_loaded = load_dotenv("cred.env")
logger.info("credentials loaded from env: " + values_loaded)

AUTH_URL = "https://api.akeyless.io/auth"
SECRET_URL = "https://api.akeyless.io/get-secret-value"
TARGET_URL = "https://api.akeyless.io/get-target-details"

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json"
}


def __get_token():
    token_response = requests.post(AUTH_URL, json={
        "access-type": "access_key",
        "access-id": os.getenv('access_id'),
        "access-key": os.getenv('access_key'),
    }, headers=HEADERS).json()
    return token_response['token']


def get_secrets(secrets: list):
    payload = {
        "accessibility": "regular",
        "names": secrets,
        "pretty-print": True,
        "token": __get_token()
    }
    response = requests.post(SECRET_URL, json=payload, headers=HEADERS).json()
    if len(secrets) == 1:
        return response[secrets[0]]
    return [response[secret] for secret in secrets]


def get_target(name: str):
    payload = {
        "show-versions": False,
        "name": name,
        "token": __get_token()
    }
    response = requests.post(TARGET_URL, json=payload, headers=HEADERS).json()
    return response['value']['db_target_details'].values()
