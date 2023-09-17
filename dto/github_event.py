from typing import Optional

from pydantic import BaseModel

from dto.action import Action


class ProcessEvent(BaseModel):
    action: Action
    pr_id: int
    repo_name: str
    org_name: str
    commit_id: str
    token: Optional[str] = None
    install_id: Optional[int] = None
