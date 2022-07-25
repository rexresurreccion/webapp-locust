__all__ = [
    "TasksUpdatePost",
]

from locust import task, tag, between, run_single_user
from locust.clients import ResponseContextManager

from webapp_locust.common.base_http_user import BaseHttpUser
from webapp_locust.security.security import SecurityToken
from webapp_locust.post.dataclass import PostData


security_token: SecurityToken = SecurityToken()


class TasksUpdatePost(BaseHttpUser):
    wait_time = between(1, 3)

    UPDATE_POST_URI: str = "/post"
    _headers: dict

    @staticmethod
    def _validate_response(response: ResponseContextManager) -> None:
        if response.status_code != 200:
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
    def update_post(self) -> None:
        print(f"Task {TasksUpdatePost.update_post.__name__}")
        post_data = PostData(
            title="Some Example",
            content="Hi World!",
            author_id=123,
            post_id=123,
        )
        with self.client.put(self.UPDATE_POST_URI, json=post_data.to_json(), headers=self._headers, catch_response=True) as response:
            self._validate_response(response)


if __name__ == "__main__":
    run_single_user(TasksUpdatePost)
