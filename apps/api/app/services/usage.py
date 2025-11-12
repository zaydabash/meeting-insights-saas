from sqlalchemy.orm import Session
from datetime import datetime
from app.models.usage_meter import UsageMeter
from app.models.provider_event import ProviderEvent
from typing import Optional


class UsageMeterService:
    @staticmethod
    def record_provider_event(
        db: Session,
        org_id: int,
        provider: str,
        model: str,
        latency_ms: float,
        tokens_in: int,
        tokens_out: int,
        cost_usd: float,
        success: bool = True,
    ):
        event = ProviderEvent(
            org_id=org_id,
            provider=provider,
            model=model,
            latency_ms=latency_ms,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=cost_usd,
            success=success,
        )
        db.add(event)
        db.commit()

    @staticmethod
    def get_monthly_usage(
        db: Session, org_id: int, period_month: str
    ) -> Optional[UsageMeter]:
        return (
            db.query(UsageMeter)
            .filter(
                UsageMeter.org_id == org_id,
                UsageMeter.period_month == period_month,
            )
            .first()
        )

    @staticmethod
    def update_monthly_usage(
        db: Session,
        org_id: int,
        period_month: str,
        audio_minutes: float = 0,
        tokens_in: int = 0,
        tokens_out: int = 0,
        storage_mb: float = 0,
        cost_estimate: float = 0,
    ):
        meter = UsageMeterService.get_monthly_usage(db, org_id, period_month)
        if meter:
            meter.audio_minutes += audio_minutes
            meter.tokens_in += tokens_in
            meter.tokens_out += tokens_out
            meter.storage_mb += storage_mb
            meter.cost_estimate += cost_estimate
        else:
            meter = UsageMeter(
                org_id=org_id,
                period_month=period_month,
                audio_minutes=audio_minutes,
                tokens_in=tokens_in,
                tokens_out=tokens_out,
                storage_mb=storage_mb,
                cost_estimate=cost_estimate,
            )
            db.add(meter)
        db.commit()
        return meter


usage_meter_service = UsageMeterService()

