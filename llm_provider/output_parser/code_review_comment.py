from pydantic.v1 import BaseModel, Field


class CodeReviewComment(BaseModel):
    startLine: int = Field(description="Start Line NUMBER of the Code Review Comment Scope")
    endLine: int = Field(description="End Line NUMBER of the Code Review Comment Scope")
    comment: str = Field(
        description="Comment on the Code Change you are recommending for the given scope between start line and end line")
