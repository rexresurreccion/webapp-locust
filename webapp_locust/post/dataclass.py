from typing import Optional
from dataclasses import dataclass

from webapp_locust.common.dataclass import BaseData


@dataclass
class PostData(BaseData):
    title: str
    content: str
    author_id: int
    post_id: Optional[int] = None
