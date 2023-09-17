import os
import time

import httpx
import jwt
from starlette import requests


class JwtGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_jwt() -> str:
        pem = os.environ.get("PEM_FILE_PATH")

        # Get the App ID
        app_id = os.environ.get("GITHUB_APP_ID")

        # Open PEM
        with open(pem, 'rb') as pem_file:
            signing_key = jwt.jwk_from_pem(pem_file.read())

        payload = {  # Issued at time
            'iat': int(time.time()), 'exp': int(time.time()) + 600, 'iss': app_id}

        # Create JWT
        jwt_instance = jwt.JWT()
        encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')

        return encoded_jwt


