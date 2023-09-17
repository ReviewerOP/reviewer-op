from typing import List

from pydantic.v1 import BaseModel

from llm_provider.output_parser.code_review_comment import CodeReviewComment


class CodeReviewCommentList(BaseModel):
    codeReviewCommentItems: List[CodeReviewComment]
