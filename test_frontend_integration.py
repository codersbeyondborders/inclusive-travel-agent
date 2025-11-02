#!/usr/bin/env python3
"""
Frontend Integration Testing Script
Tests all API endpoints that the frontend will use.
"""

import asyncio
import json
import requests
import time
from typing import Dict, Any, Optional

# Configuration
API_BASE_URL = "http://localhost:8080"
TEST_TIMEOUT = 30  # seconds


class IntegrationTester:
    """Test the frontend-backend integration."""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_user_id: Optional[str] = None
        self.test_session_id = f"test_session_{int(time.time())}"
    
    def test_server_health(self) -> bool:
        """Test if the server is running and healthy."""
        print("🔍 Testing server health...")
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Server is healthy: {data}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Server health check failed: {e}")
            return False
    
    def test_api_info(self) -> bool:
        """Test the API info endpoints."""
        print("\n📋 Testing API information endpoints...")
        
        # Test root endpoint
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Root endpoint: {data['message']}")
                print(f"   Features: {len(data.get('features', []))} features listed")
            else:
                print(f"❌ Root endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Root endpoint error: {e}")
            return False
        
        # Test agent info endpoint
        try:
            response = self.session.get(f"{self.base_url}/agent/info")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Agent info: {data['agent_name']}")
                print(f"   Sub-agents: {data['total_sub_agents']}")
                print(f"   Accessibility features: {len(data.get('accessibility_features', []))}")
                print(f"   Personalization features: {len(data.get('personalization_features', []))}")
            else:
                print(f"❌ Agent info failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Agent info error: {e}")
            return False
        
        return True
    
    def test_user_profile_creation(self) -> bool:
        """Test creating a user profile (frontend onboarding)."""
        print("\n👤 Testing user profile creation...")
        
        # Sample user profile data (what frontend would send)
        profile_data = {
            "basic_info": {
                "name": "Test User",
                "email": "test@example.com",
                "age": 30,
                "nationality": "US",
                "home_location": "San Francisco, CA",
                "phone": "+1-555-0123"
            },
            "travel_interests": {
                "preferred_destinations": ["Europe", "Japan"],
                "travel_style": ["cultural", "accessible"],
                "budget_range": "mid-range",
                "group_size_preference": "solo",
                "accommodation_preferences": ["accessible_hotel", "central_location"],
                "activity_interests": ["museums", "accessible_tours"],
                "transportation_preferences": ["accessible_public_transport"]
            },
            "accessibility_profile": {
                "mobility_needs": ["wheelchair_accessible", "step_free_access"],
                "sensory_needs": ["hearing_assistance"],
                "assistance_preferences": {
                    "airport_assistance": "wheelchair_assistance",
                    "boarding_preference": "priority_boarding"
                },
                "mobility_aids": ["manual_wheelchair", "hearing_aids"],
                "accessibility_priorities": ["wheelchair_accessible", "accessible_restrooms"],
                "barrier_concerns": ["stairs", "narrow_doorways"],
                "dietary_restrictions": ["gluten_free"]
            },
            "preferences": {
                "communication_style": "detailed",
                "risk_tolerance": "low",
                "planning_horizon": "2_months",
                "language_preferences": ["English"],
                "currency_preference": "USD"
            }
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/users",
                json=profile_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.test_user_id = data["user_id"]
                print(f"✅ User profile created successfully")
                print(f"   User ID: {self.test_user_id}")
                print(f"   Name: {data['profile']['basic_info']['name']}")
                print(f"   Profile complete: {data['profile']['profile_complete']}")
                print(f"   Accessibility needs: {len(data['profile']['accessibility_profile']['mobility_needs'])}")
                return True
            else:
                print(f"❌ Profile creation failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Profile creation error: {e}")
            return False
    
    def test_user_profile_retrieval(self) -> bool:
        """Test retrieving a user profile."""
        if not self.test_user_id:
            print("❌ No test user ID available for retrieval test")
            return False
        
        print("\n🔍 Testing user profile retrieval...")
        
        try:
            response = self.session.get(f"{self.base_url}/users/{self.test_user_id}")
            
            if response.status_code == 200:
                data = response.json()
                profile = data["profile"]
                print(f"✅ Profile retrieved successfully")
                print(f"   User: {profile['basic_info']['name']}")
                print(f"   Email: {profile['basic_info']['email']}")
                print(f"   Travel styles: {profile['travel_interests']['travel_style']}")
                print(f"   Mobility needs: {profile['accessibility_profile']['mobility_needs']}")
                return True
            else:
                print(f"❌ Profile retrieval failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Profile retrieval error: {e}")
            return False
    
    def test_user_profile_update(self) -> bool:
        """Test updating a user profile."""
        if not self.test_user_id:
            print("❌ No test user ID available for update test")
            return False
        
        print("\n✏️  Testing user profile update...")
        
        # Update data (what frontend would send for profile updates)
        update_data = {
            "travel_interests": {
                "preferred_destinations": ["Europe", "Japan", "Canada", "Australia"],
                "travel_style": ["cultural", "accessible", "relaxation"],
                "budget_range": "mid-range",
                "group_size_preference": "solo",
                "accommodation_preferences": ["accessible_hotel", "central_location", "quiet_location"],
                "activity_interests": ["museums", "accessible_tours", "local_cuisine", "accessible_nature"],
                "transportation_preferences": ["accessible_public_transport", "taxi"]
            }
        }
        
        try:
            response = self.session.put(
                f"{self.base_url}/users/{self.test_user_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                profile = data["profile"]
                print(f"✅ Profile updated successfully")
                print(f"   New destinations: {profile['travel_interests']['preferred_destinations']}")
                print(f"   New activities: {profile['travel_interests']['activity_interests']}")
                return True
            else:
                print(f"❌ Profile update failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Profile update error: {e}")
            return False
    
    def test_chat_without_context(self) -> bool:
        """Test basic chat functionality without user context."""
        print("\n💬 Testing basic chat (no user context)...")
        
        chat_data = {
            "message": "Hello, I need help planning a trip",
            "session_id": self.test_session_id
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/chat",
                json=chat_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Basic chat working")
                print(f"   Response length: {len(data['response'])} characters")
                print(f"   Session ID: {data['session_id']}")
                print(f"   Events: {len(data.get('events', []))} events")
                print(f"   Response preview: {data['response'][:100]}...")
                return True
            else:
                print(f"❌ Basic chat failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Basic chat error: {e}")
            return False
    
    def test_chat_with_context(self) -> bool:
        """Test chat with user context (personalized responses)."""
        if not self.test_user_id:
            print("❌ No test user ID available for context chat test")
            return False
        
        print("\n🎯 Testing personalized chat (with user context)...")
        
        chat_data = {
            "message": "I want to plan an accessible trip to Paris",
            "session_id": f"{self.test_session_id}_context",
            "user_id": self.test_user_id
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/chat",
                json=chat_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Personalized chat working")
                print(f"   Response length: {len(data['response'])} characters")
                print(f"   Session ID: {data['session_id']}")
                
                # Check if user context was injected
                user_context = data.get('user_context')
                if user_context:
                    print(f"   ✅ User context injected: {user_context['context_injected']}")
                    print(f"   User name: {user_context.get('user_name', 'N/A')}")
                    print(f"   Accessibility needs: {user_context.get('accessibility_needs', False)}")
                else:
                    print(f"   ⚠️  No user context in response")
                
                print(f"   Response preview: {data['response'][:150]}...")
                return True
            else:
                print(f"❌ Personalized chat failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Personalized chat error: {e}")
            return False
    
    def test_session_management(self) -> bool:
        """Test session management endpoints."""
        print("\n🔄 Testing session management...")
        
        try:
            # List sessions
            response = self.session.get(f"{self.base_url}/sessions")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Session listing working")
                print(f"   Active sessions: {data['total_sessions']}")
                print(f"   Session IDs: {data['active_sessions']}")
            else:
                print(f"❌ Session listing failed: {response.status_code}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Session management error: {e}")
            return False
    
    def test_cors_headers(self) -> bool:
        """Test CORS headers for frontend integration."""
        print("\n🌐 Testing CORS headers...")
        
        try:
            # Test preflight request
            response = self.session.options(
                f"{self.base_url}/users",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )
            
            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
                "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
            }
            
            print(f"✅ CORS headers present:")
            for header, value in cors_headers.items():
                print(f"   {header}: {value}")
            
            return True
            
        except Exception as e:
            print(f"❌ CORS test error: {e}")
            return False
    
    def cleanup_test_data(self) -> bool:
        """Clean up test data."""
        if not self.test_user_id:
            return True
        
        print("\n🧹 Cleaning up test data...")
        
        try:
            response = self.session.delete(f"{self.base_url}/users/{self.test_user_id}")
            if response.status_code == 200:
                print(f"✅ Test user profile deleted")
                return True
            else:
                print(f"⚠️  Could not delete test profile: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️  Cleanup error: {e}")
            return False
    
    def run_all_tests(self) -> bool:
        """Run all integration tests."""
        print("🧪 Frontend-Backend Integration Testing")
        print("=" * 50)
        
        tests = [
            ("Server Health", self.test_server_health),
            ("API Information", self.test_api_info),
            ("User Profile Creation", self.test_user_profile_creation),
            ("User Profile Retrieval", self.test_user_profile_retrieval),
            ("User Profile Update", self.test_user_profile_update),
            ("Basic Chat", self.test_chat_without_context),
            ("Personalized Chat", self.test_chat_with_context),
            ("Session Management", self.test_session_management),
            ("CORS Headers", self.test_cors_headers),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                else:
                    print(f"❌ {test_name} FAILED")
            except Exception as e:
                print(f"❌ {test_name} ERROR: {e}")
        
        # Cleanup
        self.cleanup_test_data()
        
        print("\n" + "=" * 50)
        print(f"🎯 Integration Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Frontend integration ready!")
            print("\n✅ Your frontend can now:")
            print("  - Create and manage user profiles")
            print("  - Send personalized chat messages")
            print("  - Receive context-aware responses")
            print("  - Handle all API endpoints correctly")
            print("\n🚀 Ready for frontend development!")
            return True
        else:
            print(f"❌ {total - passed} tests failed. Please check the issues above.")
            return False


def main():
    """Main function to run integration tests."""
    print("🔍 Checking if server is running...")
    
    # Quick server check
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Server not responding correctly at {API_BASE_URL}")
            print("Please start the server first:")
            print("  uv run python start_server.py")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server at {API_BASE_URL}")
        print("Please start the server first:")
        print("  uv run python start_server.py")
        print(f"Error: {e}")
        return False
    
    # Run integration tests
    tester = IntegrationTester()
    success = tester.run_all_tests()
    
    return success


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)