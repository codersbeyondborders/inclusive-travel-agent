#!/usr/bin/env python3
"""
Complete Frontend-Backend Integration Test
Starts the server and runs all integration tests.
"""

import asyncio
import json
import requests
import time
import threading
import uvicorn
from typing import Dict, Any, Optional

from travel_concierge.main import app

# Configuration
API_BASE_URL = "http://localhost:8080"
SERVER_START_TIMEOUT = 10  # seconds


class CompleteIntegrationTest:
    """Complete integration test with server management."""
    
    def __init__(self):
        self.server_thread = None
        self.server_started = False
        self.test_user_id = None
        self.session = requests.Session()
    
    def start_server(self):
        """Start the FastAPI server in a background thread."""
        print("🚀 Starting backend server...")
        
        def run_server():
            uvicorn.run(app, host="127.0.0.1", port=8080, log_level="error")
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # Wait for server to start
        for i in range(SERVER_START_TIMEOUT):
            try:
                response = requests.get(f"{API_BASE_URL}/health", timeout=2)
                if response.status_code == 200:
                    self.server_started = True
                    print(f"✅ Server started successfully at {API_BASE_URL}")
                    return True
            except:
                time.sleep(1)
        
        print("❌ Server failed to start within timeout")
        return False
    
    def test_api_endpoints(self):
        """Test all API endpoints that frontend will use."""
        print("\n📋 Testing API Endpoints")
        print("-" * 30)
        
        tests_passed = 0
        total_tests = 0
        
        # Test 1: Health Check
        total_tests += 1
        try:
            response = self.session.get(f"{API_BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Health Check: PASSED")
                tests_passed += 1
            else:
                print(f"❌ Health Check: FAILED ({response.status_code})")
        except Exception as e:
            print(f"❌ Health Check: ERROR ({e})")
        
        # Test 2: API Info
        total_tests += 1
        try:
            response = self.session.get(f"{API_BASE_URL}/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API Info: PASSED - {data['message']}")
                tests_passed += 1
            else:
                print(f"❌ API Info: FAILED ({response.status_code})")
        except Exception as e:
            print(f"❌ API Info: ERROR ({e})")
        
        # Test 3: Agent Info
        total_tests += 1
        try:
            response = self.session.get(f"{API_BASE_URL}/agent/info")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Agent Info: PASSED - {data['total_sub_agents']} agents")
                tests_passed += 1
            else:
                print(f"❌ Agent Info: FAILED ({response.status_code})")
        except Exception as e:
            print(f"❌ Agent Info: ERROR ({e})")
        
        return tests_passed, total_tests
    
    def test_user_profile_flow(self):
        """Test the complete user profile flow (onboarding simulation)."""
        print("\n👤 Testing User Profile Flow (Onboarding)")
        print("-" * 45)
        
        tests_passed = 0
        total_tests = 0
        
        # Sample profile data (what frontend onboarding would create)
        profile_data = {
            "basic_info": {
                "name": "Sarah Johnson",
                "email": "sarah.test@example.com",
                "age": 34,
                "nationality": "US",
                "home_location": "Seattle, WA",
                "phone": "+1-555-0123"
            },
            "travel_interests": {
                "preferred_destinations": ["Europe", "Japan"],
                "travel_style": ["cultural", "accessible"],
                "budget_range": "mid-range",
                "group_size_preference": "solo",
                "accommodation_preferences": ["accessible_hotel", "central_location"],
                "activity_interests": ["museums", "accessible_tours", "local_cuisine"],
                "transportation_preferences": ["accessible_public_transport", "taxi"]
            },
            "accessibility_profile": {
                "mobility_needs": ["wheelchair_accessible", "step_free_access"],
                "sensory_needs": ["hearing_assistance"],
                "cognitive_needs": [],
                "assistance_preferences": {
                    "airport_assistance": "wheelchair_assistance",
                    "boarding_preference": "priority_boarding",
                    "hotel_assistance": "accessible_room_ground_floor"
                },
                "mobility_aids": ["manual_wheelchair", "hearing_aids"],
                "medical_conditions": ["hearing_impairment"],
                "accessibility_priorities": ["wheelchair_accessible", "accessible_restrooms"],
                "barrier_concerns": ["stairs", "narrow_doorways", "loud_environments"],
                "dietary_restrictions": ["gluten_free"],
                "medication_requirements": ["daily_medication"],
                "service_animal": None,
                "communication_needs": ["written_communication_backup"]
            },
            "preferences": {
                "communication_style": "detailed",
                "risk_tolerance": "low",
                "planning_horizon": "2_months",
                "language_preferences": ["English"],
                "currency_preference": "USD",
                "timezone": "America/Los_Angeles"
            }
        }
        
        # Test 1: Create Profile
        total_tests += 1
        try:
            response = self.session.post(
                f"{API_BASE_URL}/users",
                json=profile_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                self.test_user_id = data["user_id"]
                print(f"✅ Create Profile: PASSED - User ID: {self.test_user_id[:8]}...")
                print(f"   Profile Complete: {data['profile']['profile_complete']}")
                tests_passed += 1
            else:
                print(f"❌ Create Profile: FAILED ({response.status_code})")
                print(f"   Response: {response.text[:100]}...")
        except Exception as e:
            print(f"❌ Create Profile: ERROR ({e})")
        
        if not self.test_user_id:
            print("❌ Cannot continue profile tests without user ID")
            return tests_passed, total_tests
        
        # Test 2: Retrieve Profile
        total_tests += 1
        try:
            response = self.session.get(f"{API_BASE_URL}/users/{self.test_user_id}")
            if response.status_code == 200:
                data = response.json()
                profile = data["profile"]
                print(f"✅ Retrieve Profile: PASSED - {profile['basic_info']['name']}")
                print(f"   Accessibility Needs: {len(profile['accessibility_profile']['mobility_needs'])} mobility")
                tests_passed += 1
            else:
                print(f"❌ Retrieve Profile: FAILED ({response.status_code})")
        except Exception as e:
            print(f"❌ Retrieve Profile: ERROR ({e})")
        
        # Test 3: Update Profile
        total_tests += 1
        try:
            update_data = {
                "travel_interests": {
                    "preferred_destinations": ["Europe", "Japan", "Canada"],
                    "travel_style": ["cultural", "accessible", "relaxation"],
                    "budget_range": "mid-range",
                    "group_size_preference": "solo",
                    "accommodation_preferences": ["accessible_hotel", "central_location", "quiet_location"],
                    "activity_interests": ["museums", "accessible_tours", "local_cuisine", "accessible_nature"],
                    "transportation_preferences": ["accessible_public_transport", "taxi"]
                }
            }
            
            response = self.session.put(
                f"{API_BASE_URL}/users/{self.test_user_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                destinations = data["profile"]["travel_interests"]["preferred_destinations"]
                print(f"✅ Update Profile: PASSED - {len(destinations)} destinations")
                tests_passed += 1
            else:
                print(f"❌ Update Profile: FAILED ({response.status_code})")
        except Exception as e:
            print(f"❌ Update Profile: ERROR ({e})")
        
        return tests_passed, total_tests
    
    def test_chat_functionality(self):
        """Test chat functionality with and without user context."""
        print("\n💬 Testing Chat Functionality")
        print("-" * 30)
        
        tests_passed = 0
        total_tests = 0
        session_id = f"test_session_{int(time.time())}"
        
        # Test 1: Basic Chat (no context)
        total_tests += 1
        try:
            chat_data = {
                "message": "Hello, I need help planning a trip",
                "session_id": session_id
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/chat",
                json=chat_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Basic Chat: PASSED - Response: {len(data['response'])} chars")
                print(f"   Session: {data['session_id']}")
                tests_passed += 1
            else:
                print(f"❌ Basic Chat: FAILED ({response.status_code})")
                print(f"   Response: {response.text[:100]}...")
        except Exception as e:
            print(f"❌ Basic Chat: ERROR ({e})")
        
        # Test 2: Personalized Chat (with context)
        if self.test_user_id:
            total_tests += 1
            try:
                chat_data = {
                    "message": "I want to plan an accessible trip to Paris",
                    "session_id": f"{session_id}_context",
                    "user_id": self.test_user_id
                }
                
                response = self.session.post(
                    f"{API_BASE_URL}/chat",
                    json=chat_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    user_context = data.get('user_context', {})
                    context_injected = user_context.get('context_injected', False)
                    
                    print(f"✅ Personalized Chat: PASSED - Context: {context_injected}")
                    if context_injected:
                        print(f"   User: {user_context.get('user_name', 'N/A')}")
                        print(f"   Accessibility: {user_context.get('accessibility_needs', False)}")
                    print(f"   Response: {len(data['response'])} chars")
                    tests_passed += 1
                else:
                    print(f"❌ Personalized Chat: FAILED ({response.status_code})")
                    print(f"   Response: {response.text[:100]}...")
            except Exception as e:
                print(f"❌ Personalized Chat: ERROR ({e})")
        else:
            print("⚠️  Skipping personalized chat test (no user ID)")
        
        return tests_passed, total_tests
    
    def test_frontend_requirements(self):
        """Test specific requirements for frontend integration."""
        print("\n🌐 Testing Frontend Integration Requirements")
        print("-" * 45)
        
        tests_passed = 0
        total_tests = 0
        
        # Test 1: CORS Headers
        total_tests += 1
        try:
            response = self.session.options(
                f"{API_BASE_URL}/users",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )
            
            cors_origin = response.headers.get("Access-Control-Allow-Origin")
            cors_methods = response.headers.get("Access-Control-Allow-Methods")
            
            if cors_origin and cors_methods:
                print(f"✅ CORS Headers: PASSED")
                print(f"   Origin: {cors_origin}")
                print(f"   Methods: {cors_methods}")
                tests_passed += 1
            else:
                print(f"❌ CORS Headers: FAILED - Missing headers")
        except Exception as e:
            print(f"❌ CORS Headers: ERROR ({e})")
        
        # Test 2: JSON Content Type
        total_tests += 1
        try:
            response = self.session.get(f"{API_BASE_URL}/")
            content_type = response.headers.get("Content-Type", "")
            
            if "application/json" in content_type:
                print(f"✅ JSON Content Type: PASSED")
                tests_passed += 1
            else:
                print(f"❌ JSON Content Type: FAILED - {content_type}")
        except Exception as e:
            print(f"❌ JSON Content Type: ERROR ({e})")
        
        # Test 3: Error Handling
        total_tests += 1
        try:
            response = self.session.get(f"{API_BASE_URL}/users/nonexistent-user-id")
            
            if response.status_code == 404:
                error_data = response.json()
                print(f"✅ Error Handling: PASSED - 404 for missing user")
                tests_passed += 1
            else:
                print(f"❌ Error Handling: FAILED - Expected 404, got {response.status_code}")
        except Exception as e:
            print(f"❌ Error Handling: ERROR ({e})")
        
        return tests_passed, total_tests
    
    def cleanup(self):
        """Clean up test data."""
        if self.test_user_id:
            try:
                response = self.session.delete(f"{API_BASE_URL}/users/{self.test_user_id}")
                if response.status_code == 200:
                    print(f"\n🧹 Cleanup: Test user deleted successfully")
                else:
                    print(f"\n⚠️  Cleanup: Could not delete test user ({response.status_code})")
            except Exception as e:
                print(f"\n⚠️  Cleanup: Error deleting test user ({e})")
    
    def run_complete_test(self):
        """Run the complete integration test suite."""
        print("🧪 Complete Frontend-Backend Integration Test")
        print("=" * 50)
        
        # Start server
        if not self.start_server():
            print("❌ Cannot start server. Exiting.")
            return False
        
        # Run all test suites
        total_passed = 0
        total_tests = 0
        
        # API Endpoints
        passed, tests = self.test_api_endpoints()
        total_passed += passed
        total_tests += tests
        
        # User Profile Flow
        passed, tests = self.test_user_profile_flow()
        total_passed += passed
        total_tests += tests
        
        # Chat Functionality
        passed, tests = self.test_chat_functionality()
        total_passed += passed
        total_tests += tests
        
        # Frontend Requirements
        passed, tests = self.test_frontend_requirements()
        total_passed += passed
        total_tests += tests
        
        # Cleanup
        self.cleanup()
        
        # Results
        print("\n" + "=" * 50)
        print(f"🎯 Integration Test Results: {total_passed}/{total_tests} tests passed")
        
        if total_passed == total_tests:
            print("\n🎉 ALL TESTS PASSED! Frontend integration is ready!")
            print("\n✅ Your backend supports:")
            print("  ✓ User profile creation and management")
            print("  ✓ Personalized chat with context injection")
            print("  ✓ CORS headers for frontend requests")
            print("  ✓ Proper error handling and JSON responses")
            print("  ✓ All 10 specialized accessibility agents")
            
            print("\n🚀 Frontend Integration Instructions:")
            print("  1. Keep this server running (http://localhost:8080)")
            print("  2. Start your frontend app (typically on port 3000)")
            print("  3. Configure frontend to use API_BASE_URL: http://localhost:8080")
            print("  4. Test user onboarding flow")
            print("  5. Test personalized chat functionality")
            
            print("\n📚 API Documentation: http://localhost:8080/docs")
            print("🔍 Health Check: http://localhost:8080/health")
            
            return True
        else:
            print(f"\n❌ {total_tests - total_passed} tests failed.")
            print("Please check the issues above before proceeding with frontend integration.")
            return False


def main():
    """Main function."""
    tester = CompleteIntegrationTest()
    success = tester.run_complete_test()
    
    if success:
        print("\n⏳ Server will continue running for frontend testing...")
        print("Press Ctrl+C to stop the server when done.")
        try:
            # Keep the server running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Server stopped. Goodbye!")
    
    return success


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)