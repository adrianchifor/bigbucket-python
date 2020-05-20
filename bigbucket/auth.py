import requests
import base64
import time
import json

from functools import wraps


def authenticate(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.gcp_auth:
            self.headers, self.jwt = _get_gcp_auth_header(
                self.jwt, self.address)
        return func(self, *args, **kwargs)
    return wrapper


def _get_gcp_auth_header(jwt: str, address: str) -> (dict, str):
    """
    Constructs the auth header and returns it with a refreshed jwt token
    """
    if _jwt_expired(jwt):
        jwt = _get_gcp_auth_token(address)

    return {"Authorization": f"bearer {jwt}"}, jwt


def _get_gcp_auth_token(receiving_service_url: str) -> str:
    token_request_url = ("http://metadata/computeMetadata/v1/instance/service-accounts"
                         f"/default/identity?audience={receiving_service_url}")
    token_response = requests.get(token_request_url,
                                  headers={"Metadata-Flavor": "Google"})
    return token_response.content.decode("utf-8")


def _jwt_expired(jwt: str) -> bool:
    if not jwt:
        return True

    jwt_arr = jwt.split(".")
    jwt_payload = base64.b64decode(f"{jwt_arr[1]}==").decode()
    expiry = int(json.loads(jwt_payload)["exp"])
    # Add 30 seconds to allow time for requests
    now = int(time.time()) + 30

    return expiry <= now
