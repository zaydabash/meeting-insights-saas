from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User, UserRole
from app.models.usage_meter import UsageMeter
from app.models.provider_event import ProviderEvent
from app.schemas.user import UserResponse
from datetime import datetime
from typing import List, Dict, Any

router = APIRouter()


@router.get("/org/users", response_model=List[UserResponse])
async def list_org_users(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    users = db.query(User).filter(User.org_id == current_user.org_id).all()
    return [UserResponse.model_validate(user) for user in users]


@router.post("/org/users")
async def invite_user(
    email: str,
    role: UserRole = UserRole.MEMBER,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    # Stub - would send invitation email in production
    return {"message": f"Invitation sent to {email}", "status": "pending"}


@router.get("/usage")
async def get_usage(
    period_month: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    if not period_month:
        period_month = datetime.utcnow().strftime("%Y-%m")
    
    meter = db.query(UsageMeter).filter(
        UsageMeter.org_id == current_user.org_id,
        UsageMeter.period_month == period_month,
    ).first()
    
    if not meter:
        return {
            "period_month": period_month,
            "audio_minutes": 0.0,
            "tokens_in": 0,
            "tokens_out": 0,
            "storage_mb": 0.0,
            "cost_estimate": 0.0,
        }
    
    return {
        "period_month": meter.period_month,
        "audio_minutes": meter.audio_minutes,
        "tokens_in": meter.tokens_in,
        "tokens_out": meter.tokens_out,
        "storage_mb": meter.storage_mb,
        "cost_estimate": meter.cost_estimate,
    }


@router.get("/costs")
async def get_costs(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    # Get provider events for last 30 days
    from datetime import timedelta
    cutoff = datetime.utcnow() - timedelta(days=30)
    
    events = db.query(ProviderEvent).filter(
        ProviderEvent.org_id == current_user.org_id,
        ProviderEvent.created_at >= cutoff,
    ).all()
    
    total_cost = sum(e.cost_usd for e in events)
    by_provider = {}
    
    for event in events:
        if event.provider not in by_provider:
            by_provider[event.provider] = {
                "cost": 0.0,
                "requests": 0,
                "tokens_in": 0,
                "tokens_out": 0,
            }
        by_provider[event.provider]["cost"] += event.cost_usd
        by_provider[event.provider]["requests"] += 1
        by_provider[event.provider]["tokens_in"] += event.tokens_in
        by_provider[event.provider]["tokens_out"] += event.tokens_out
    
    return {
        "total_cost_usd": total_cost,
        "by_provider": by_provider,
        "period_days": 30,
    }

