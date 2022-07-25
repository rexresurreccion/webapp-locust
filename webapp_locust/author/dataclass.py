from typing import Optional
from dataclasses import dataclass

from webapp_locust.common.dataclass import BaseData


@dataclass
class AuthorData(BaseData):
    email: str
    name: str
    admin: bool
    author_id: Optional[int] = None
