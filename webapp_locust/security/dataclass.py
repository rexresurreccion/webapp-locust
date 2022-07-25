from dataclasses import dataclass

from webapp_locust.common.dataclass import BaseData


@dataclass
class AuthData(BaseData):
    client_id: str
    client_secret: str
