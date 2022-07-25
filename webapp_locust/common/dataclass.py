import json

from dataclasses import dataclass, asdict


@dataclass
class BaseData:
    def to_json(self) -> str:
        return json.dumps(asdict(self))

    def to_dict(self) -> dict:
        asdict(self)
