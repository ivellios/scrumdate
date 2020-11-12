from datetime import datetime
from typing import Optional

from pivotal.abstract import Story, Label, Person


class DictDataAdapter:

    def __init__(self, data: dict):
        self.data = data

    @property
    def name(self):
        return self.data["name"]


class TimestampedAdapter(DictDataAdapter):

    @classmethod
    def _str_to_datetime(cls, timestring):
        return datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%SZ")

    @property
    def created(self):
        return self._str_to_datetime(self.data["created_at"])

    @property
    def updated(self):
        return self._str_to_datetime(self.data["updated_at"])


class LabelAdapter(TimestampedAdapter, Label):
    pass


class StoryAdapter(TimestampedAdapter, Story):

    @property
    def owners(self):
        return self.data["owner_ids"]

    @property
    def state(self):
        return self.data["current_state"]

    @property
    def type(self) -> str:
        return self.data["story_type"]

    @property
    def labels(self):
        return [LabelAdapter(label_data) for label_data in self.data["labels"]]

    @property
    def url(self):
        return self.data["url"]

    def _get_deployed_label(self) -> Optional[LabelAdapter]:
        try:
            return list(filter(lambda label: label.name == "deployed", self.labels))[0]
        except IndexError:
            return None

    @property
    def deployed(self) -> bool:
        return self._get_deployed_label() is not None

    @property
    def deployed_today(self) -> bool:
        label = self._get_deployed_label()
        if not label:
            return False
        return label.created.date() == datetime.today().date()

    @property
    def updated_today(self):
        return self.updated.date() == datetime.today().date()


class PersonAdapter(DictDataAdapter, Person):

    @property
    def identifier(self):
        return self.data["id"]

    @property
    def initials(self):
        return self.data["initials"]
