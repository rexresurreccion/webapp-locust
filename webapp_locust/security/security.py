import requests
from requests import Response

from webapp_locust.config import BASE_URL
from webapp_locust.security.dataclass import AuthData


class SecurityToken:
    GENERATE_TOKEN_URI: str = "/generate-token"

    def auth_data(self) -> dict:
        return AuthData(client_id="ExampleClient", client_secret="ExampleSecret").to_dict()

    def generate_token(self) -> str:
        response: Response = requests.post(
            f"{BASE_URL}{SecurityToken.GENERATE_TOKEN_URI}",
            data=self.auth_data(),
        )
        response.raise_for_status()
        generated_token: dict = response.json()
        return generated_token.get("token")

