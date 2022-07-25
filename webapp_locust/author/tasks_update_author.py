__all__ = [
    "TasksUpdateAuthor",
]

from locust import task, tag, between, run_single_user

from webapp_locust.common.base_http_user import BaseHttpUser
from webapp_locust.security.security import SecurityToken
from webapp_locust.author.dataclass import AuthorData


security_token: SecurityToken = SecurityToken()


class TasksUpdateAuthor(BaseHttpUser):
    wait_time = between(1, 3)

    UPDATE_AUTHOR_URI: str = "/author"
    _headers: dict

    def on_start(self) -> None:
        self._headers = {
            "Authorization": f"Bearer {security_token.generate_token()}"
        }

    @tag("default-test")
    @task
    def update_author(self) -> None:
        print(f"Task {TasksUpdateAuthor.update_author.__name__}")
        author_data = AuthorData(
            email="hello.rex@example.com",
            name="Rex",
            admin=False,
            author_id=123,
        )
        with self.client.put(self.UPDATE_AUTHOR_URI, json=author_data.to_json(), headers=self._headers, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Invalid response status code {response.status_code}")
            elif response.elapsed.total_seconds() > 0.5:
                response.failure(f"Request took too long {response.elapsed.total_seconds()}")
            else:
                response.success()


if __name__ == "__main__":
    run_single_user(TasksUpdateAuthor)
