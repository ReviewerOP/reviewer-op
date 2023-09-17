import time

import jwt

from config import config


class JwtGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_jwt() -> str:
        # Open PEM
        with open(config.pem, 'rb') as pem_file:
            signing_key = jwt.jwk_from_pem(pem_file.read())

        payload = {  # Issued at time
            'iat': int(time.time()), 'exp': int(time.time()) + 600, 'iss': config.app_id}

        # Create JWT
        jwt_instance = jwt.JWT()
        encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')

        return encoded_jwt
