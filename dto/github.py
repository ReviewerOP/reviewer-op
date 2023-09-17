from typing import Optional

from pydantic import BaseModel

from dto.action import Action


class User(BaseModel):
    login: str
    id: int
    type: str


class Head(BaseModel):
    label: str
    ref: str
    sha: str


class PullRequest(BaseModel):
    url: str
    id: int
    state: str
    locked: bool
    title: str
    user: User
    head: Head


class Installation(BaseModel):
    id: int
    node_id: str


class WebhookPayload(BaseModel):
    action: Action
    number: int
    pull_request: PullRequest
    installation: Optional[Installation] = None
