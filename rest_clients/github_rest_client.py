import httpx
from fastapi import HTTPException

from constants.constants import GITHUB_API_URL
from dto.action import Action
from dto.github_event import ProcessEvent
from git_providers.git_provider_strategy import CodeCommentMetadata
from llm_provider.output_parser.code_review_comment import CodeReviewComment
from utilities.github_jwt_generator import JwtGenerator


class GithubRestClient:

    def __init__(self):
        pass

    @staticmethod
    async def get_diff_data_from_pull_request(github_event: ProcessEvent) -> str:
        if github_event.action is Action.opened:
            url = GITHUB_API_URL + f"/repos/{github_event.org_name}/{github_event.repo_name}/pulls/{github_event.pr_id}"
        else:
            url = GITHUB_API_URL + f"/repos/{github_event.org_name}/{github_event.repo_name}/commits/{github_event.commit_id}"

        headers = {"Authorization": f"Bearer {github_event.token}", "Accept": "application/vnd.github.v3.diff",
                   "X-GitHub-Api-Version": "2022-11-28"}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.text

    @staticmethod
    async def create_comment(github_event: ProcessEvent, code_review_comment: CodeReviewComment,
                             code_comment_metadata: CodeCommentMetadata):

        url = GITHUB_API_URL + f"/repos/{github_event.org_name}/{github_event.repo_name}/pulls/{github_event.pr_id}/comments"

        headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {github_event.token}",
                   "X-GitHub-Api-Version": "2022-11-28"}

        data = {"body": code_review_comment.comment, "commit_id": github_event.commit_id,
                "path": code_comment_metadata.path, "start_line": code_review_comment.startLine, "start_side": "RIGHT"}

        if code_review_comment.endLine == code_review_comment.startLine:
            data["line"] = code_review_comment.endLine + 1
        else:
            data["line"] = code_review_comment.endLine

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)

        if response.status_code not in (
                200, 201):  # 200 OK or 201 Created are the expected responses for successful comment creation
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()

    @staticmethod
    async def generate_key(install_id: int) -> str:
        url = f"{GITHUB_API_URL}/app/installations/{install_id}/access_tokens"
        headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {JwtGenerator.generate_jwt()}",
                   "X-GitHub-Api-Version": "2022-11-28"}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers)

        if response.status_code not in (201, 200):
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()["token"]
