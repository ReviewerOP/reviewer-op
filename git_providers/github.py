from dto.code_comment_meta import CodeCommentMetadata
from dto.github_event import ProcessEvent
from git_providers.git_provider_strategy import GitProviderStrategy
from llm_provider.output_parser.code_review_comment import CodeReviewComment
from rest_clients.github_rest_client import GithubRestClient


class GitHubProvider(GitProviderStrategy):

    def __init__(self):
        pass

    async def get_diff_content_from_pull_request(self, github_event: ProcessEvent) -> str:
        return await GithubRestClient.get_diff_data_from_pull_request(github_event)

    async def post_comment(self, github_event: ProcessEvent, code_review_comment: CodeReviewComment,
                           code_comment_metadata: CodeCommentMetadata):
        return await GithubRestClient.create_comment(github_event, code_review_comment, code_comment_metadata)
