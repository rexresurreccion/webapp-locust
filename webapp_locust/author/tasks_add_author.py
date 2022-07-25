__all__ = [
    "TasksAddAuthor",
]

from locust import task, tag, between, run_single_user
from locust.clients import ResponseContextManager

from webapp_locust.common.base_http_user import BaseHttpUser
from webapp_locust.security.security import SecurityToken
from webapp_locust.author.dataclass import AuthorData


security_token: SecurityToken = SecurityToken()


class TasksAddAuthor(BaseHttpUser):
    wait_time = between(1, 3)

    ADD_AUTHOR_URI: str = "/author"
    _headers: dict

    @staticmethod
    def _validate_response(response: ResponseContextManager) -> None:
        if response.status_code != 201:
            response.failure(f"Invalid response status code {response.status_code}")
        elif response.elapsed.total_seconds() > 0.5:
            response.failure(f"Request took too long {response.elapsed.total_seconds()}")
        else:
            response.success()

    def on_start(self) -> None:
        self._headers = {
            "Authorization": f"Bearer {security_token.generate_token()}"
        }

    @tag("default-test")
    @task
    def add_author(self) -> None:
        print(f"Task {TasksAddAuthor.add_author.__name__}")
        author_data = AuthorData(
            email="rex@example.com",
            name="Rex",
            admin=False,
        )
        with self.client.post(self.ADD_AUTHOR_URI, json=author_data.to_json(), headers=self._headers, catch_response=True) as response:
            self._validate_response(response)

    @task(2)
    def add_author_that_is_admin(self) -> None:
        print(f"Task {TasksAddAuthor.add_author_that_is_admin.__name__}")
        author_data = AuthorData(
            email="rex.admin@example.com",
            name="Rex Admin",
            admin=True,
        )
        with self.client.post(self.ADD_AUTHOR_URI, json=author_data.to_json(), headers=self._headers, catch_response=True) as response:
            self._validate_response(response)


if __name__ == "__main__":
    run_single_user(TasksAddAuthor)
