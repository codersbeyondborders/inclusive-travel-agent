#!/bin/bash

# Frontend-Backend Integration Test Script
echo "🚀 Inclusive Travel Agent - Frontend Integration Testing"
echo "======================================================="

# Check if server is already running
echo "🔍 Checking if server is already running..."
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Server is already running at http://localhost:8080"
    echo ""
    echo "🧪 Running integration tests..."
    uv run python test_frontend_integration.py
else
    echo "⚠️  Server not running. Starting server..."
    echo ""
    echo "🚀 Starting backend server..."
    echo "   Server URL: http://localhost:8080"
    echo "   API Docs: http://localhost:8080/docs"
    echo ""
    echo "⏳ Please wait for server to start, then run integration tests..."
    echo ""
    echo "In another terminal, run:"
    echo "   uv run python test_frontend_integration.py"
    echo ""
    echo "Or visit http://localhost:8080/docs to test the API manually"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    # Start the server
    uv run python start_server.py
fi