import abc
from datetime import datetime
from typing import List


class Story(abc.ABC):
    name: str
    created: datetime
    updated: datetime
    owners: List[int]
    state: str
    type: str
    url: str
    deployed: bool
    deployed_today: bool
    updated_today: bool


class Label(abc.ABC):
    name: str
    created: datetime
    updated: datetime


class Person(abc.ABC):
    identifier: int
    initials: str
