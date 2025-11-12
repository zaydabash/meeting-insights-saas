from celery import Celery
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.meeting import Meeting, MeetingStatus
from app.models.insight import Insight, InsightType
from app.models.task import Task, TaskStatus, TaskSource
from app.models.speaker import Speaker
from app.services.nlp_provider import get_provider
from app.services.redaction import redaction_service
from app.services.usage import usage_meter_service
from thefuzz import fuzz
from datetime import datetime
import json

celery_app = Celery(
    "meeting_insights",
    broker=settings.redis_url,
    backend=settings.redis_url,
)


@celery_app.task(name="process_meeting")
def process_meeting_task(meeting_id: int):
    """Process a meeting: transcribe, extract insights, create tasks"""
    db = SessionLocal()
    
    try:
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            return {"error": "Meeting not found"}
        
        meeting.status = MeetingStatus.PROCESSING
        db.commit()
        
        # Get transcript (if not already set, would transcribe audio here)
        transcript = meeting.transcript_text
        if not transcript:
            # In production, would use Whisper or other ASR here
            transcript = "Sample transcript for meeting processing."
            meeting.transcript_text = transcript
        
        # Redact PII if enabled
        redacted_transcript, vault_tokens = redaction_service.redact(transcript)
        
        # Extract insights using LLM provider
        provider = get_provider()
        import asyncio
        import time
        
        start_time = time.time()
        result = asyncio.run(provider.extract_insights(transcript))
        latency_ms = (time.time() - start_time) * 1000
        
        # Record provider event
        from app.core.config import settings
        cost = provider.get_cost_estimate(result["tokens_in"], result["tokens_out"])
        usage_meter_service.record_provider_event(
            db,
            meeting.org_id,
            settings.llm_provider,
            "default",
            latency_ms,
            result["tokens_in"],
            result["tokens_out"],
            cost,
        )
        
        # Create speakers (stub - would use diarization)
        speaker = Speaker(meeting_id=meeting.id, label="SPEAKER_00", name=None)
        db.add(speaker)
        db.flush()
        
        # Create insights
        for item in result.get("action_items", []):
            insight = Insight(
                meeting_id=meeting.id,
                type=InsightType.ACTION_ITEM,
                text=item.get("text", ""),
                owner_user_id=None,  # Would resolve from owner_candidate
                due_date=item.get("due_date_candidate"),
                confidence=item.get("confidence"),
                extra=json.dumps(item),
            )
            db.add(insight)
            
            # Auto-create task from action item
            task = Task(
                org_id=meeting.org_id,
                meeting_id=meeting.id,
                title=item.get("text", "")[:255],
                owner_user_id=meeting.created_by,  # Default to meeting creator
                status=TaskStatus.OPEN,
                due_date=item.get("due_date_candidate"),
                source=TaskSource.INTERNAL,
            )
            db.add(task)
        
        for decision in result.get("decisions", []):
            insight = Insight(
                meeting_id=meeting.id,
                type=InsightType.DECISION,
                text=decision.get("text", ""),
                confidence=decision.get("confidence"),
                extra=json.dumps(decision),
            )
            db.add(insight)
        
        # Create summary insight
        if result.get("summary"):
            insight = Insight(
                meeting_id=meeting.id,
                type=InsightType.SUMMARY,
                text=result["summary"],
                confidence=0.9,
            )
            db.add(insight)
        
        # Create sentiment insight
        if result.get("sentiment") is not None:
            insight = Insight(
                meeting_id=meeting.id,
                type=InsightType.SENTIMENT,
                text=str(result["sentiment"]),
                confidence=0.8,
                extra=json.dumps({"sentiment": result["sentiment"]}),
            )
            db.add(insight)
        
        # Update meeting status
        meeting.status = MeetingStatus.PROCESSED
        db.commit()
        
        # Update usage meter
        period_month = datetime.utcnow().strftime("%Y-%m")
        usage_meter_service.update_monthly_usage(
            db,
            meeting.org_id,
            period_month,
            tokens_in=result["tokens_in"],
            tokens_out=result["tokens_out"],
            cost_estimate=cost,
        )
        
        return {"status": "processed", "meeting_id": meeting_id}
        
    except Exception as e:
        if meeting:
            meeting.status = MeetingStatus.FAILED
            db.commit()
        return {"error": str(e)}
    finally:
        db.close()

