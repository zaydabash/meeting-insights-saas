from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.models.meeting import Meeting
from app.models.task import Task, TaskSource
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()


class SlackPostRequest(BaseModel):
    meeting_id: int
    channel: str


class JiraCreateRequest(BaseModel):
    meeting_id: int
    project_key: str


@router.post("/slack/post")
async def post_to_slack(
    request: SlackPostRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if not settings.slack_bot_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Slack integration not configured",
        )
    
    meeting = db.query(Meeting).filter(
        Meeting.id == request.meeting_id,
        Meeting.org_id == current_user.org_id,
    ).first()
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )
    
    # Get summary and action items
    summary_insight = next(
        (i for i in meeting.insights if i.type == "summary"),
        None
    )
    action_items = [i for i in meeting.insights if i.type == "action_item"]
    
    # Format message
    message = f"*Meeting: {meeting.title}*\n\n"
    if summary_insight:
        message += f"*Summary:*\n{summary_insight.text}\n\n"
    
    if action_items:
        message += "*Action Items:*\n"
        for item in action_items:
            message += f"• {item.text}\n"
    
    # Post to Slack (stub - would use slack_sdk in production)
    try:
        import httpx
        response = httpx.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {settings.slack_bot_token}"},
            json={
                "channel": request.channel,
                "text": message,
            },
        )
        response.raise_for_status()
        return {"ok": True, "message": "Posted to Slack"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to post to Slack: {str(e)}",
        )


@router.post("/jira/create")
async def create_jira_issues(
    request: JiraCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if not settings.jira_base_url or not settings.jira_api_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Jira integration not configured",
        )
    
    meeting = db.query(Meeting).filter(
        Meeting.id == request.meeting_id,
        Meeting.org_id == current_user.org_id,
    ).first()
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )
    
    action_items = [i for i in meeting.insights if i.type == "action_item"]
    created_issues = []
    
    # Create Jira issues for each action item
    try:
        import httpx
        import base64
        
        auth = base64.b64encode(
            f"{settings.jira_email}:{settings.jira_api_token}".encode()
        ).decode()
        
        for item in action_items:
            issue_data = {
                "fields": {
                    "project": {"key": request.project_key},
                    "summary": item.text[:255],  # Jira summary limit
                    "description": f"From meeting: {meeting.title}\n\n{item.text}",
                    "issuetype": {"name": "Task"},
                }
            }
            
            response = httpx.post(
                f"{settings.jira_base_url}/rest/api/3/issue",
                headers={
                    "Authorization": f"Basic {auth}",
                    "Content-Type": "application/json",
                },
                json=issue_data,
            )
            response.raise_for_status()
            
            issue_key = response.json()["key"]
            created_issues.append(issue_key)
            
            # Create task linked to Jira
            task = Task(
                org_id=current_user.org_id,
                meeting_id=meeting.id,
                title=item.text,
                owner_user_id=item.owner_user_id or current_user.id,
                due_date=item.due_date,
                source=TaskSource.JIRA,
                external_id=issue_key,
            )
            db.add(task)
        
        db.commit()
        
        return {"created": created_issues}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create Jira issues: {str(e)}",
        )

