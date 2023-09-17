import uvicorn
from fastapi import FastAPI

from dto.action import Action
from dto.github import WebhookPayload
from dto.github_event import ProcessEvent
from service.generate_code_comment import CodeCommentBotService
from utilities.git_url_util import GitUrlUtil

app = FastAPI()


@app.post("/webhook")
async def github_webhook(payload: WebhookPayload):
    if payload.action != Action.opened and payload.action != Action.synchronize:
        return

    metaData = GitUrlUtil.get_organization_and_repository_name_from_url(payload.pull_request.url)

    github_event: ProcessEvent = ProcessEvent(action=payload.action, pr_id=payload.number, repo_name=metaData[1],
                                              org_name=metaData[0], commit_id=payload.pull_request.head.sha,
                                              install_id=payload.installation.id)

    await CodeCommentBotService.generate_code_comment(github_event)


if __name__ == "__main__":
    uvicorn.run(app)
