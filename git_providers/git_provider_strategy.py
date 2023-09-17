from abc import abstractmethod, ABC

from dto.code_comment_meta import CodeCommentMetadata
from dto.github_event import ProcessEvent
from llm_provider.output_parser.code_review_comment import CodeReviewComment


class GitProviderStrategy(ABC):

    @abstractmethod
    def get_diff_content_from_pull_request(self, process_event: ProcessEvent):
        pass

    @abstractmethod
    def post_comment(self, process_event: ProcessEvent, code_review_comment: CodeReviewComment,
                     code_comment_metadata: CodeCommentMetadata):
        pass
