import os
import typing as t
from dataclasses import dataclass

import requests

from . import json_support


@dataclass
class FreePlayPromptTemplate:
    name: str
    content: str


@dataclass
class FreePlayProjectSession:
    session_id: str
    prompt_templates: t.List[FreePlayPromptTemplate]

    def __all_names(self) -> t.List[str]:
        return [t.name for t in self.prompt_templates]

    def get_template(self, template_name: str) -> str:
        for t in self.prompt_templates:
            if t.name == template_name:
                return t.content

        raise Exception(f'Template with name {template_name} not found. Available names are: {self.__all_names()}')


class FreePlay:
    def __init__(self, api_key: str, api_url: t.Optional[str] = None) -> None:
        self.api_key = api_key
        self.api_url = api_url or self.__get_default_url()

    @staticmethod
    def __get_default_url() -> str:
        return os.environ.get('FREEPLAY_API_URL', 'https://review.freeplay.ai/api')

    def new_project_session(self, project_id: str, tag: str = 'latest') -> FreePlayProjectSession:
        create_session_url = f'{self.api_url}/projects/{project_id}/sessions/tag/{tag}'
        response = requests.post(
            url=create_session_url,
            headers={'Authorization': f'Bearer {self.api_key}'}
        )

        if response.status_code != 201:
            raise Exception(
                f'Unexpected status code while starting new project session at {create_session_url}, '
                f'got {response.status_code}'
            )

        maybe_project_session = json_support.try_decode(FreePlayProjectSession, response.content)
        if maybe_project_session is None:
            raise Exception(f'Failed to parse session for project with id {project_id}')

        return maybe_project_session
