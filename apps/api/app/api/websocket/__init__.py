from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.meeting import Meeting
import json

router = APIRouter()


@router.websocket("/meetings/{meeting_id}/stream")
async def stream_meeting_updates(
    websocket: WebSocket,
    meeting_id: int,
    db: Session = Depends(get_db),
):
    await websocket.accept()
    
    try:
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            await websocket.send_json({"error": "Meeting not found"})
            await websocket.close()
            return
        
        # In production, would subscribe to Redis pub/sub or use async DB listeners
        # For now, send periodic updates
        import asyncio
        
        while True:
            # Refresh meeting from DB
            db.refresh(meeting)
            
            # Send partial transcript if available
            if meeting.transcript_text:
                await websocket.send_json({
                    "type": "partial_transcript",
                    "text": meeting.transcript_text[-500:],  # Last 500 chars
                })
            
            # Send insights if available
            if meeting.insights:
                await websocket.send_json({
                    "type": "partial_insights",
                    "insights": [
                        {
                            "type": insight.type,
                            "text": insight.text,
                        }
                        for insight in meeting.insights[-5:]  # Last 5 insights
                    ],
                })
            
            # Send progress
            await websocket.send_json({
                "type": "progress",
                "status": meeting.status,
            })
            
            await asyncio.sleep(2)  # Poll every 2 seconds
            
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()

