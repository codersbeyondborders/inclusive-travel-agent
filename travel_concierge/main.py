

"""FastAPI application for the Inclusive Travel Concierge."""

import os
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from travel_concierge.agent import root_agent
from google.adk.sessions import Session


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    """Chat message model."""
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    session_id: str
    events: List[Dict[str, Any]] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting Inclusive Travel Agent API")
    yield
    logger.info("Shutting down Inclusive Travel Agent API")


# Create FastAPI app
app = FastAPI(
    title="Inclusive Travel Agent API",
    description="An AI-powered travel agent specializing in accessible travel planning",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active sessions
sessions: Dict[str, Session] = {}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to the Inclusive Travel Agent API",
        "description": "An AI-powered travel agent specializing in accessible travel planning",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "sessions": "/sessions"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "inclusive-travel-agent"}


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Chat with the inclusive travel agent.
    
    Args:
        message: Chat message containing user input and session ID
        
    Returns:
        ChatResponse with agent response and events
    """
    try:
        # Get or create session
        if message.session_id not in sessions:
            sessions[message.session_id] = Session(root_agent)
            logger.info(f"Created new session: {message.session_id}")
        
        session = sessions[message.session_id]
        
        # Process message with the agent
        logger.info(f"Processing message for session {message.session_id}: {message.message}")
        
        # Run the agent
        result = session.run(message.message)
        
        # Extract events for rich UI rendering
        events = []
        for event in session.get_events():
            if hasattr(event, 'to_dict'):
                events.append(event.to_dict())
            else:
                events.append({"type": "unknown", "data": str(event)})
        
        response = ChatResponse(
            response=result,
            session_id=message.session_id,
            events=events
        )
        
        logger.info(f"Generated response for session {message.session_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.get("/sessions")
async def list_sessions():
    """List active sessions."""
    return {
        "active_sessions": list(sessions.keys()),
        "total_sessions": len(sessions)
    }


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a specific session."""
    if session_id in sessions:
        del sessions[session_id]
        logger.info(f"Deleted session: {session_id}")
        return {"message": f"Session {session_id} deleted"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@app.get("/agent/info")
async def agent_info():
    """Get information about the agent and its capabilities."""
    sub_agents = [
        {
            "name": agent.name,
            "description": agent.description,
            "tools": len(agent.tools) if hasattr(agent, 'tools') else 0
        }
        for agent in root_agent.sub_agents
    ]
    
    return {
        "agent_name": root_agent.name,
        "agent_description": root_agent.description,
        "total_sub_agents": len(root_agent.sub_agents),
        "sub_agents": sub_agents,
        "accessibility_features": [
            "Comprehensive accessibility research",
            "Mobility aid preparation assistance", 
            "Transit support coordination",
            "Real-time barrier navigation",
            "Accessible venue recommendations",
            "Disability-friendly travel planning"
        ]
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(
        "travel_concierge.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )