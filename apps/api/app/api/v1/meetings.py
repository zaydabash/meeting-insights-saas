from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.models.meeting import Meeting, MeetingStatus
from app.schemas.meeting import MeetingCreate, MeetingResponse, MeetingDetailResponse, MeetingListResponse
from app.services.storage import storage_service
from app.services.usage import usage_meter_service

router = APIRouter()


@router.post("/upload", response_model=MeetingResponse)
async def upload_meeting(
    file: UploadFile = File(...),
    title: str = Form(...),
    occurred_at: str = Form(...),
    language: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # Upload audio to S3
    audio_key = storage_service.upload_audio(file.file, file.filename)
    audio_url = storage_service.get_audio_url(audio_key)
    
    # Parse occurred_at
    occurred_at_dt = datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))
    
    # Create meeting
    meeting = Meeting(
        org_id=current_user.org_id,
        title=title,
        occurred_at=occurred_at_dt,
        language=language,
        audio_url=audio_url,
        status=MeetingStatus.PENDING,
        created_by=current_user.id,
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    
    # Record usage (approximate duration from file size - rough estimate)
    # In production, would get actual duration from audio metadata
    file.file.seek(0, 2)  # Seek to end
    file_size_mb = file.file.tell() / (1024 * 1024)
    estimated_minutes = file_size_mb * 2  # Rough estimate: 1MB ≈ 2 minutes
    
    period_month = datetime.utcnow().strftime("%Y-%m")
    usage_meter_service.update_monthly_usage(
        db,
        current_user.org_id,
        period_month,
        audio_minutes=estimated_minutes,
        storage_mb=file_size_mb,
    )
    
    return MeetingResponse.model_validate(meeting)


@router.post("/text", response_model=MeetingResponse)
async def create_meeting_from_text(
    request: MeetingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    meeting = Meeting(
        org_id=current_user.org_id,
        title=request.title,
        occurred_at=request.occurred_at,
        language=request.language,
        transcript_text=request.transcript_text,
        status=MeetingStatus.PENDING,
        created_by=current_user.id,
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    
    return MeetingResponse.model_validate(meeting)


@router.get("", response_model=MeetingListResponse)
async def list_meetings(
    q: Optional[str] = Query(None),
    status: Optional[MeetingStatus] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    query = db.query(Meeting).filter(Meeting.org_id == current_user.org_id)
    
    if q:
        query = query.filter(Meeting.title.ilike(f"%{q}%"))
    
    if status:
        query = query.filter(Meeting.status == status)
    
    if date_from:
        date_from_dt = datetime.fromisoformat(date_from)
        query = query.filter(Meeting.occurred_at >= date_from_dt)
    
    if date_to:
        date_to_dt = datetime.fromisoformat(date_to)
        query = query.filter(Meeting.occurred_at <= date_to_dt)
    
    total = query.count()
    items = query.order_by(Meeting.occurred_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return MeetingListResponse(
        items=[MeetingResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{meeting_id}", response_model=MeetingDetailResponse)
async def get_meeting(
    meeting_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    meeting = db.query(Meeting).filter(
        Meeting.id == meeting_id,
        Meeting.org_id == current_user.org_id,
    ).first()
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )
    
    return MeetingDetailResponse.model_validate(meeting)


@router.post("/{meeting_id}/process")
async def process_meeting(
    meeting_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    meeting = db.query(Meeting).filter(
        Meeting.id == meeting_id,
        Meeting.org_id == current_user.org_id,
    ).first()
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )
    
    # Update status and enqueue processing job
    meeting.status = MeetingStatus.PROCESSING
    db.commit()
    
    # In production, would enqueue Celery task here
    # For now, process synchronously (move to worker later)
    from app.workers.meeting_processor import process_meeting_task
    process_meeting_task.delay(meeting_id)
    
    return {"status": "queued"}

