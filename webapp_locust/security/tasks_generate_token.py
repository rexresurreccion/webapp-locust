__all__ = [
    "TasksGenerateToken",
]

from json import JSONDecodeError

from locust import task, tag, between, run_single_user

from webapp_locust.common.base_http_user import BaseHttpUser
from webapp_locust.security.security import SecurityToken


security_token: SecurityToken = SecurityToken()


class TasksGenerateToken(BaseHttpUser):
    wait_time = between(1, 3)

    @tag("default-test")
    @task
    def generate_token(self) -> None:
        print(f"Task {TasksGenerateToken.generate_token.__name__}")
        with self.client.post(security_token.GENERATE_TOKEN_URI, data=security_token.auth_data(), catch_response=True) as response:
            try:
                if response.status_code != 201:
                    response.failure(f"Invalid response status code {response.status_code}")
                elif response.elapsed.total_seconds() > 0.5:
                    response.failure(f"Request took too long {response.elapsed.total_seconds()}")
                elif not response.json()["token"]:
                    response.failure("token was empty")
                else:
                    response.success()
            except JSONDecodeError:
                response.failure("Response could not be decoded as JSON")
            except KeyError:
                response.failure("Response did not contain expected key 'token'")


if __name__ == "__main__":
    run_single_user(TasksGenerateToken)
