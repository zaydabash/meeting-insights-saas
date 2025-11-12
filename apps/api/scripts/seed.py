#!/usr/bin/env python3
"""Seed database with demo data"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.organization import Organization
from app.models.user import User, UserRole
from app.models.meeting import Meeting, MeetingStatus
from app.models.insight import Insight, InsightType
from app.models.task import Task, TaskStatus, TaskSource
from app.models.speaker import Speaker
from datetime import datetime, timedelta

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Create demo organization
    org = Organization(name="Demo Corp", domain="demo.com")
    db.add(org)
    db.flush()
    
    # Create admin user
    admin_user = User(
        org_id=org.id,
        email="admin@demo.com",
        hashed_password=get_password_hash("demo123"),
        role=UserRole.ADMIN,
    )
    db.add(admin_user)
    db.flush()
    
    # Create member user
    member_user = User(
        org_id=org.id,
        email="member@demo.com",
        hashed_password=get_password_hash("demo123"),
        role=UserRole.MEMBER,
    )
    db.add(member_user)
    db.flush()
    
    # Create sample meetings
    meeting1 = Meeting(
        org_id=org.id,
        title="Q4 Planning Meeting",
        occurred_at=datetime.utcnow() - timedelta(days=2),
        language="en",
        duration_sec=3600,
        transcript_text="We discussed the Q4 goals. John needs to prepare the budget by next week. We agreed to increase marketing spend by 20%. The team is excited about the new product launch.",
        status=MeetingStatus.PROCESSED,
        created_by=admin_user.id,
    )
    db.add(meeting1)
    db.flush()
    
    # Create speakers
    speaker1 = Speaker(meeting_id=meeting1.id, label="SPEAKER_00", name="John")
    speaker2 = Speaker(meeting_id=meeting1.id, label="SPEAKER_01", name="Sarah")
    db.add(speaker1)
    db.add(speaker2)
    db.flush()
    
    # Create insights
    insight1 = Insight(
        meeting_id=meeting1.id,
        type=InsightType.ACTION_ITEM,
        text="Prepare Q4 budget",
        owner_user_id=admin_user.id,
        due_date=datetime.utcnow() + timedelta(days=7),
        confidence=0.9,
    )
    insight2 = Insight(
        meeting_id=meeting1.id,
        type=InsightType.DECISION,
        text="Increase marketing spend by 20%",
        confidence=0.85,
    )
    insight3 = Insight(
        meeting_id=meeting1.id,
        type=InsightType.SUMMARY,
        text="Q4 planning meeting covered budget preparation, marketing spend increase, and product launch timeline.",
        confidence=0.9,
    )
    insight4 = Insight(
        meeting_id=meeting1.id,
        type=InsightType.SENTIMENT,
        text="0.7",
        confidence=0.8,
        extra='{"sentiment": 0.7}',
    )
    db.add(insight1)
    db.add(insight2)
    db.add(insight3)
    db.add(insight4)
    db.flush()
    
    # Create tasks
    task1 = Task(
        org_id=org.id,
        meeting_id=meeting1.id,
        title="Prepare Q4 budget",
        owner_user_id=admin_user.id,
        status=TaskStatus.OPEN,
        due_date=datetime.utcnow() + timedelta(days=7),
        source=TaskSource.INTERNAL,
    )
    db.add(task1)
    
    meeting2 = Meeting(
        org_id=org.id,
        title="Team Standup",
        occurred_at=datetime.utcnow() - timedelta(days=1),
        language="en",
        duration_sec=1800,
        transcript_text="Quick standup. Everyone is on track. No blockers.",
        status=MeetingStatus.PROCESSED,
        created_by=member_user.id,
    )
    db.add(meeting2)
    
    db.commit()
    
    print("Database seeded successfully!")
    print(f"   Organization: {org.name}")
    print(f"   Admin user: admin@demo.com / demo123")
    print(f"   Member user: member@demo.com / demo123")
    print(f"   Created {2} meetings with insights and tasks")
    
except Exception as e:
    db.rollback()
    print(f"Error seeding database: {e}")
    raise
finally:
    db.close()

