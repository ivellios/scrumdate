from datetime import datetime
from typing import List, Optional
from urllib.parse import urlencode

import requests

from .abstract import Story
from .adapters import StoryAdapter, PersonAdapter
from .formatters import UpdateFormatter


class UpdatesManager:

    def __init__(self, token, project_id):
        self.token = token
        self.project_id = project_id

    def call_api(self, endpoint, **kwargs):
        args = urlencode(kwargs)
        url = f"https://www.pivotaltracker.com/services/v5{endpoint}?{args}"
        response = requests.get(
            url=url,
            headers={
                "x-trackertoken": self.token
            }
        )
        return response

    def pull_me(self):
        response = self.call_api("/me")
        return response.json()

    def pull_memberships(self):
        response = self.call_api(f"/projects/{self.project_id}/memberships")
        data = response.json()
        return [
            PersonAdapter(membership["person"])
            for membership in data
        ]

    def get_user_id(self, initials) -> Optional[int]:
        persons = self.pull_memberships()
        for person in persons:
            if person.initials == initials:
                return person.identifier

    def search_stories(self, query) -> List[Story]:
        response = self.call_api(f"/projects/{self.project_id}/search", query=query)
        data = response.json()
        return [StoryAdapter(story_data) for story_data in data["stories"]["stories"]]

    def pull_my_work_stories(self, initials) -> List[Story]:
        return self.search_stories(f'mywork:"{initials}"')

    def pull_my_accepted_today(self, initials) -> List[Story]:
        today = datetime.today().strftime("%m/%d/%Y")
        return self.search_stories(f'owner:"{initials}" accepted_on:"{today}"')

    def pull_my_stories(self, initials) -> List[Story]:
        return self.pull_my_work_stories(initials) + self.pull_my_accepted_today(initials)

    def get_worked_on(self, stories, identifier):
        def is_active(story: Story):
            """
            Stories I was working on are:
            - not a release
            - started, finished, delivered, rejected -- they are basically active for the user
            - or accepted, but deployed today
            - or chore/bug that was updated today and accepted (not necessarily deployed) -- possible false positives here as any comment may also change updated time!
            """
            return (
                story.type not in ["release"]
                and identifier in story.owners
                and story.state in ["started", "finished", "delivered", "rejected"]
                or (story.deployed_today and story.state in ["accepted"])
                or (story.updated_today and story.type in ["chore", "bug"] and story.state in ["accepted"]))

        return [story for story in stories if is_active(story)]

    def get_deployed(self, stories, identifier):
        def was_deployed(story: Story):
            """
            Story with label deployed created today
            """
            return (story.state in ["finished", "delivered", "accepted", "rejected"]
                    and story.deployed_today
                    and identifier in story.owners)

        return [story for story in stories if was_deployed(story)]

    def get_next(self, stories, identifier) -> Optional[Story]:
        unstarted = [
            story for story in stories
            if (story.state == "unstarted"
                and identifier in story.owners
                and story.type != "release")
        ]
        if len(unstarted):
            return unstarted[0]

        # in case of no unstarted next work, we can repeat last worked on
        workerd_on = self.get_worked_on(stories, identifier)
        if len(workerd_on):
            return workerd_on[-1]

    def pull_daily_stories(self, initials: str = None) -> str:
        """
        Warning: initals are case sensitive, pivotal can set for the user either lowercase or upparcase
        When using this method, you should know your initials exact case. Simply go to your story and click initials
        to see the search bar filled with proper value.
        """
        if not initials:
            me = self.pull_me()
            initials = me.get("initials")

        identifier = self.get_user_id(initials)

        stories = self.pull_my_stories(initials)

        formatter = UpdateFormatter(
            self.get_deployed(stories, identifier),
            self.get_worked_on(stories, identifier),
            self.get_next(stories, identifier)
        )

        return formatter.get_message()
