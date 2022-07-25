from locust import HttpUser

from webapp_locust.config import BASE_URL


class BaseHttpUser(HttpUser):
    abstract: bool = True
    host: str = BASE_URL
