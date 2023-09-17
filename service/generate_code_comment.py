import os

from dto.github_event import ProcessEvent
from git_providers.github import GitHubProvider
from llm_provider.code_comment_processor import CodeCommentProcessor
from rest_clients.github_rest_client import GithubRestClient
from utilities.diff_file_util import DiffFileUtil


class CodeCommentBotService:
    def __init__(self):
        pass

    @staticmethod
    async def generate_code_comment(process_event: ProcessEvent):
        github = GitHubProvider()

        process_event.token = await GithubRestClient.generate_key(process_event.install_id)

        directory_path = DiffFileUtil.split_diffs_to_files(
            await github.get_diff_content_from_pull_request(process_event), process_event)
        try:
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)

                # Check if the path is a file (this will exclude subdirectories)
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as file:
                        file_contents = file.read()
                        code_comment_metadata = DiffFileUtil.extract_file_info_from_diff(file_contents)

                        language = DiffFileUtil.language_from_diff_file(file_contents)
                        if language is None:
                            continue

                        code_comment_list = CodeCommentProcessor.generate_comments(file_contents, language)
                        for code_comment in code_comment_list.codeReviewCommentItems:
                            await github.post_comment(process_event, code_comment, code_comment_metadata)

        finally:
            DiffFileUtil.delete_directory(directory_path)
