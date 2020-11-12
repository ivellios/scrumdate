from typing import List, Optional

from .abstract import Story


class UpdateFormatter:

    def __init__(self,
                 deployed: List[Story],
                 worked_on: List[Story],
                 next: Optional[Story] = None
                 ):
        self.deployed = deployed
        self.worked_on = worked_on
        self.next = [next] if next else None

    @staticmethod
    def _format_story(story):
        return f"- *[{story.type.capitalize()}]* _{story.name}_ -- {story.url}\n"

    @staticmethod
    def _format_extra(extra):
        return f"- _{extra}_\n"

    @classmethod
    def _format_block(cls, header, stories, empty_message="", extras: Optional[list] = None):
        text = f"""
*{header}:* """

        if extras:
            text += "\n" + "".join([cls._format_extra(extra) for extra in extras])

        if stories:
            if not extras:
                text += "\n"
            text += "".join([cls._format_story(story) for story in stories])
        elif not extras:
            text += empty_message + "\n"

        return text

    def get_deployed(self):
        return self._format_block("Deployed", self.deployed, "nothing")

    def get_worked_on(self):
        return self._format_block("Worked on", self.worked_on, "nothing", ["code reviews", "teamwork"])

    def get_next(self):
        return self._format_block("Next", self.next, "nothing")

    def get_blockers(self):
        return self._format_block("Blockers", None, "none")

    def get_message(self):
        return f"""{self.get_deployed()}{self.get_worked_on()}{self.get_next()}{self.get_blockers()}"""
