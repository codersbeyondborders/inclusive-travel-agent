

"""FastAPI application for the Inclusive Travel Concierge."""

import os
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from inclusive_travel_agent.agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.genai import types
from inclusive_travel_agent.models import (
    CreateUserProfileRequest,
    UpdateUserProfileRequest,
    UserProfileResponse,
    UserProfileSummary,
    UserProfile,
)
from inclusive_travel_agent.services import user_profile_service, context_service


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    """Chat message model."""
    message: str
    session_id: str = "default"
    user_id: Optional[str] = None  # Optional user ID for personalized responses


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

# Initialize services
session_service = InMemorySessionService()
artifacts_service = InMemoryArtifactService()

# Initialize runner
runner = Runner(
    app_name="inclusive-travel-agent",
    agent=root_agent,
    artifact_service=artifacts_service,
    session_service=session_service,
)

# Store active sessions
sessions: Dict[str, Any] = {}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to the Inclusive Travel Agent API",
        "description": "An AI-powered travel agent specializing in accessible travel planning",
        "version": "1.0.0",
        "features": [
            "Personalized user profiles with accessibility needs",
            "Context-aware AI responses based on user preferences",
            "10 specialized accessibility-focused agents",
            "Real-time accessibility information integration"
        ],
        "endpoints": {
            "chat": "/chat - Chat with personalized context",
            "users": "/users - User profile management",
            "health": "/health - Service health check",
            "sessions": "/sessions - Session management",
            "agent_info": "/agent/info - Agent capabilities"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "inclusive-travel-agent"}


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Chat with the inclusive travel agent with optional user context.
    
    Args:
        message: Chat message containing user input, session ID, and optional user ID
        
    Returns:
        ChatResponse with agent response and events
    """
    try:
        # Get or create session
        if message.session_id not in sessions:
            sessions[message.session_id] = await session_service.create_session(
                state={}, app_name="inclusive-travel-agent", user_id=message.user_id or "anonymous"
            )
            logger.info(f"Created new session: {message.session_id}")
        
        session = sessions[message.session_id]
        
        # Inject user context if user_id is provided
        context_injected = False
        if message.user_id:
            context_injected = await context_service.inject_user_context(session, message.user_id)
            if context_injected:
                logger.info(f"Injected user context for user {message.user_id} in session {message.session_id}")
            else:
                logger.warning(f"Failed to inject user context for user {message.user_id}")
        
        # Process message with the agent
        logger.info(f"Processing message for session {message.session_id}: {message.message}")
        
        # Create content for the agent
        content = types.Content(role="user", parts=[types.Part(text=message.message)])
        
        # Run the agent
        events_async = runner.run_async(
            session_id=session.id, 
            user_id=message.user_id or "anonymous", 
            new_message=content
        )
        
        # Collect events and extract the final response
        events = []
        result = ""
        
        async for event in events_async:
            if not event.content:
                continue
            
            # Convert event to dict for frontend
            event_dict = {
                "author": event.author,
                "content": str(event.content) if event.content else None,
                "timestamp": str(event.timestamp) if hasattr(event, 'timestamp') else None
            }
            events.append(event_dict)
            
            # Extract text response
            if event.content.parts and event.content.parts[0].text:
                result = event.content.parts[0].text
        
        # Add context information to response
        response_data = {
            "response": result,
            "session_id": message.session_id,
            "events": events
        }
        
        # Include user context info if available
        if context_injected:
            user_context = context_service.get_user_context_from_session(session)
            if user_context:
                response_data["user_context"] = {
                    "user_id": message.user_id,
                    "context_injected": True,
                    "user_name": user_context.get("personalized_context", {}).get("user_info", {}).get("name"),
                    "accessibility_needs": bool(user_context.get("personalized_context", {}).get("accessibility_summary", {}).get("has_mobility_needs") or
                                                user_context.get("personalized_context", {}).get("accessibility_summary", {}).get("has_sensory_needs"))
                }
        
        response = ChatResponse(**response_data)
        
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


# User Profile Management Endpoints

@app.post("/users", response_model=UserProfileResponse)
async def create_user_profile(request: CreateUserProfileRequest):
    """
    Create a new user profile.
    
    Args:
        request: User profile creation request
        
    Returns:
        Created user profile
    """
    try:
        profile = await user_profile_service.create_user_profile(request)
        return UserProfileResponse(
            user_id=profile.user_id,
            profile=profile,
            message="User profile created successfully"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating user profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/users/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(user_id: str):
    """
    Get user profile by ID.
    
    Args:
        user_id: User ID
        
    Returns:
        User profile
    """
    try:
        profile = await user_profile_service.get_user_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        return UserProfileResponse(
            user_id=user_id,
            profile=profile,
            message="User profile retrieved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.put("/users/{user_id}", response_model=UserProfileResponse)
async def update_user_profile(user_id: str, request: UpdateUserProfileRequest):
    """
    Update user profile.
    
    Args:
        user_id: User ID
        request: Update request with partial data
        
    Returns:
        Updated user profile
    """
    try:
        profile = await user_profile_service.update_user_profile(user_id, request)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        return UserProfileResponse(
            user_id=user_id,
            profile=profile,
            message="User profile updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/users/{user_id}")
async def delete_user_profile(user_id: str):
    """
    Delete user profile.
    
    Args:
        user_id: User ID
        
    Returns:
        Deletion confirmation
    """
    try:
        deleted = await user_profile_service.delete_user_profile(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        return {"message": f"User profile {user_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user profile {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/users", response_model=List[UserProfileSummary])
async def list_user_profiles(
    limit: int = Query(50, ge=1, le=100, description="Maximum number of profiles to return"),
    offset: int = Query(0, ge=0, description="Number of profiles to skip")
):
    """
    List user profiles with pagination.
    
    Args:
        limit: Maximum number of profiles to return
        offset: Number of profiles to skip
        
    Returns:
        List of user profile summaries
    """
    try:
        profiles = await user_profile_service.list_user_profiles(limit=limit, offset=offset)
        return profiles
    except Exception as e:
        logger.error(f"Error listing user profiles: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


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
        ],
        "personalization_features": [
            "User profile-based context injection",
            "Accessibility needs-aware responses",
            "Travel preference personalization",
            "Communication style adaptation",
            "Learned preference tracking"
        ]
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(
        "inclusive_travel_agent.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )