from pydantic import BaseModel


class CodeCommentMetadata(BaseModel):
    commit_id: str
    path: str
