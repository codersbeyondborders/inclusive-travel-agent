#!/usr/bin/env python3
"""Start the Inclusive Travel Agent API server for local testing."""

import uvicorn
from inclusive_travel_agent.main import app

if __name__ == "__main__":
    print("🚀 Starting Inclusive Travel Agent API server...")
    print("📍 Server URL: http://localhost:8080")
    print("📚 API Documentation: http://localhost:8080/docs")
    print("🔍 Health Check: http://localhost:8080/health")
    print("👤 User Management: http://localhost:8080/users")
    print("💬 Chat Endpoint: http://localhost:8080/chat")
    print("\n⚡ Server starting... Press Ctrl+C to stop")
    
    uvicorn.run(
        "inclusive_travel_agent.main:app", 
        host="0.0.0.0", 
        port=8080, 
        reload=True,
        log_level="info"
    )