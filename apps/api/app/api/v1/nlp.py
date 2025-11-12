from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.models.meeting import Meeting
from app.schemas.insight import InsightCreate, InsightResponse
from app.services.nlp_provider import get_provider
from app.services.redaction import redaction_service
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()


class ExtractRequest(BaseModel):
    meeting_id: int = None
    text: str = None


class RedactRequest(BaseModel):
    text: str


class RedactResponse(BaseModel):
    redacted_text: str
    tokens: List[Dict[str, str]]


@router.post("/extract")
async def extract_insights(
    request: ExtractRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if request.meeting_id:
        meeting = db.query(Meeting).filter(
            Meeting.id == request.meeting_id,
            Meeting.org_id == current_user.org_id,
        ).first()
        if not meeting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meeting not found",
            )
        text = meeting.transcript_text or ""
    elif request.text:
        text = request.text
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either meeting_id or text must be provided",
        )
    
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No text to process",
        )
    
    provider = get_provider()
    import time
    start_time = time.time()
    
    try:
        result = await provider.extract_insights(text)
        latency_ms = (time.time() - start_time) * 1000
        
        # Record provider event
        from app.services.usage import usage_meter_service
        from app.core.config import settings
        cost = provider.get_cost_estimate(result["tokens_in"], result["tokens_out"])
        usage_meter_service.record_provider_event(
            db,
            current_user.org_id,
            settings.llm_provider,
            "default",
            latency_ms,
            result["tokens_in"],
            result["tokens_out"],
            cost,
        )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction failed: {str(e)}",
        )


@router.post("/redact", response_model=RedactResponse)
async def redact_text(
    request: RedactRequest,
    current_user: User = Depends(get_current_active_user),
):
    redacted_text, tokens = redaction_service.redact(request.text)
    return RedactResponse(
        redacted_text=redacted_text,
        tokens=[{"token": t["token"], "kind": t["kind"]} for t in tokens],
    )


@router.get("/providers")
async def list_providers():
    from app.core.config import settings
    return {
        "current": settings.llm_provider,
        "available": ["mock", "openai", "anthropic"],
    }

