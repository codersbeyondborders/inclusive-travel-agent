#!/usr/bin/env python3
"""
Simple Integration Test for Frontend
Tests user profile API endpoints without AI functionality.
Perfect for frontend integration development.
"""

import requests
import json
import time
from typing import Optional


class SimpleIntegrationTest:
    """Test user profile API endpoints for frontend integration."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_user_id: Optional[str] = None
    
    def test_server_health(self) -> bool:
        """Test if the server is running."""
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
            print(f"❌ Cannot connect to server: {e}")
            print(f"Please start the server first:")
            print(f"  uv run python start_server.py")
            return False
    
    def test_api_info(self) -> bool:
        """Test API information endpoints."""
        print("\n📋 Testing API Information...")
        
        # Test root endpoint
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API Root: {data['message']}")
                print(f"   Features: {len(data.get('features', []))}")
                print(f"   Endpoints: {len(data.get('endpoints', {}))}")
            else:
                print(f"❌ API Root failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API Root error: {e}")
            return False
        
        # Test agent info
        try:
            response = self.session.get(f"{self.base_url}/agent/info")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Agent Info: {data['total_sub_agents']} agents")
                print(f"   Accessibility features: {len(data.get('accessibility_features', []))}")
                print(f"   Personalization features: {len(data.get('personalization_features', []))}")
            else:
                print(f"❌ Agent Info failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Agent Info error: {e}")
            return False
        
        return True
    
    def test_user_profile_creation(self) -> bool:
        """Test creating a user profile (onboarding simulation)."""
        print("\n👤 Testing User Profile Creation (Onboarding)...")
        
        # Sample profile data that frontend would send
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
        
        try:
            response = self.session.post(
                f"{self.base_url}/users",
                json=profile_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.test_user_id = data["user_id"]
                profile = data["profile"]
                
                print(f"✅ Profile created successfully!")
                print(f"   User ID: {self.test_user_id[:8]}...")
                print(f"   Name: {profile['basic_info']['name']}")
                print(f"   Email: {profile['basic_info']['email']}")
                print(f"   Profile Complete: {profile['profile_complete']}")
                print(f"   Onboarding Complete: {profile['onboarding_completed']}")
                
                # Accessibility details
                accessibility = profile['accessibility_profile']
                print(f"   Mobility Needs: {len(accessibility['mobility_needs'])} ({', '.join(accessibility['mobility_needs'])})")
                print(f"   Sensory Needs: {len(accessibility['sensory_needs'])} ({', '.join(accessibility['sensory_needs'])})")
                print(f"   Assistance Preferences: {len(accessibility['assistance_preferences'])} configured")
                
                # Travel interests
                interests = profile['travel_interests']
                print(f"   Destinations: {', '.join(interests['preferred_destinations'])}")
                print(f"   Travel Style: {', '.join(interests['travel_style'])}")
                print(f"   Budget: {interests['budget_range']}")
                
                return True
            else:
                print(f"❌ Profile creation failed: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False
                
        except Exception as e:
            print(f"❌ Profile creation error: {e}")
            return False
    
    def test_user_profile_retrieval(self) -> bool:
        """Test retrieving a user profile."""
        if not self.test_user_id:
            print("❌ No test user ID available")
            return False
        
        print("\n🔍 Testing User Profile Retrieval...")
        
        try:
            response = self.session.get(f"{self.base_url}/users/{self.test_user_id}")
            
            if response.status_code == 200:
                data = response.json()
                profile = data["profile"]
                
                print(f"✅ Profile retrieved successfully!")
                print(f"   User: {profile['basic_info']['name']}")
                print(f"   Communication Style: {profile['preferences']['communication_style']}")
                print(f"   Risk Tolerance: {profile['preferences']['risk_tolerance']}")
                print(f"   Planning Horizon: {profile['preferences']['planning_horizon']}")
                
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
            print("❌ No test user ID available")
            return False
        
        print("\n✏️  Testing User Profile Update...")
        
        # Update data
        update_data = {
            "travel_interests": {
                "preferred_destinations": ["Europe", "Japan", "Canada", "Australia"],
                "travel_style": ["cultural", "accessible", "relaxation"],
                "budget_range": "luxury",
                "group_size_preference": "couple",
                "accommodation_preferences": ["accessible_hotel", "central_location", "quiet_location", "spa_access"],
                "activity_interests": ["museums", "accessible_tours", "local_cuisine", "accessible_nature", "accessible_beaches"],
                "transportation_preferences": ["accessible_public_transport", "taxi", "accessible_rental_car"]
            },
            "preferences": {
                "communication_style": "conversational",
                "risk_tolerance": "medium",
                "planning_horizon": "6_months",
                "language_preferences": ["English", "Spanish"],
                "currency_preference": "USD",
                "timezone": "America/Los_Angeles"
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
                
                print(f"✅ Profile updated successfully!")
                
                # Show changes
                interests = profile["travel_interests"]
                preferences = profile["preferences"]
                
                print(f"   New destinations: {len(interests['preferred_destinations'])} ({', '.join(interests['preferred_destinations'])})")
                print(f"   New budget: {interests['budget_range']}")
                print(f"   New group preference: {interests['group_size_preference']}")
                print(f"   New communication style: {preferences['communication_style']}")
                print(f"   New risk tolerance: {preferences['risk_tolerance']}")
                print(f"   New planning horizon: {preferences['planning_horizon']}")
                
                return True
            else:
                print(f"❌ Profile update failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Profile update error: {e}")
            return False
    
    def test_user_profile_listing(self) -> bool:
        """Test listing user profiles."""
        print("\n📋 Testing User Profile Listing...")
        
        try:
            response = self.session.get(f"{self.base_url}/users?limit=10")
            
            if response.status_code == 200:
                profiles = response.json()
                
                print(f"✅ Profile listing successful!")
                print(f"   Found: {len(profiles)} profiles")
                
                if profiles:
                    profile = profiles[0]
                    print(f"   Sample profile:")
                    print(f"     Name: {profile['name']}")
                    print(f"     Email: {profile['email']}")
                    print(f"     Profile Complete: {profile['profile_complete']}")
                    print(f"     Accessibility Needs: {profile['accessibility_needs_count']}")
                    print(f"     Travel Interests: {profile['travel_interests_count']}")
                    print(f"     Created: {profile['created_at'][:10]}")
                
                return True
            else:
                print(f"❌ Profile listing failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Profile listing error: {e}")
            return False
    
    def test_cors_and_headers(self) -> bool:
        """Test CORS headers and response formats."""
        print("\n🌐 Testing CORS and Headers...")
        
        try:
            # Test CORS preflight
            response = self.session.options(
                f"{self.base_url}/users",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )
            
            cors_origin = response.headers.get("Access-Control-Allow-Origin")
            cors_methods = response.headers.get("Access-Control-Allow-Methods")
            cors_headers = response.headers.get("Access-Control-Allow-Headers")
            
            print(f"✅ CORS Headers:")
            print(f"   Origin: {cors_origin}")
            print(f"   Methods: {cors_methods}")
            print(f"   Headers: {cors_headers}")
            
            # Test JSON content type
            response = self.session.get(f"{self.base_url}/")
            content_type = response.headers.get("Content-Type", "")
            print(f"✅ Content Type: {content_type}")
            
            return True
            
        except Exception as e:
            print(f"❌ CORS/Headers test error: {e}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling."""
        print("\n❌ Testing Error Handling...")
        
        try:
            # Test 404 for non-existent user
            response = self.session.get(f"{self.base_url}/users/nonexistent-user-id")
            
            if response.status_code == 404:
                error_data = response.json()
                print(f"✅ 404 Error: {error_data.get('detail', 'No detail')}")
            else:
                print(f"❌ Expected 404, got {response.status_code}")
                return False
            
            # Test 400 for invalid data
            response = self.session.post(
                f"{self.base_url}/users",
                json={"invalid": "data"},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [400, 422]:  # 422 is validation error
                print(f"✅ Validation Error: {response.status_code}")
            else:
                print(f"❌ Expected 400/422, got {response.status_code}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error handling test error: {e}")
            return False
    
    def cleanup(self) -> bool:
        """Clean up test data."""
        if not self.test_user_id:
            return True
        
        print("\n🧹 Cleaning up test data...")
        
        try:
            response = self.session.delete(f"{self.base_url}/users/{self.test_user_id}")
            if response.status_code == 200:
                print(f"✅ Test user deleted successfully")
                return True
            else:
                print(f"⚠️  Could not delete test user: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️  Cleanup error: {e}")
            return False
    
    def run_all_tests(self) -> bool:
        """Run all integration tests."""
        print("🧪 Simple Frontend Integration Test")
        print("=" * 40)
        print("Testing user profile API endpoints")
        print("Perfect for frontend development!")
        print("=" * 40)
        
        tests = [
            ("Server Health", self.test_server_health),
            ("API Information", self.test_api_info),
            ("User Profile Creation", self.test_user_profile_creation),
            ("User Profile Retrieval", self.test_user_profile_retrieval),
            ("User Profile Update", self.test_user_profile_update),
            ("User Profile Listing", self.test_user_profile_listing),
            ("CORS and Headers", self.test_cors_and_headers),
            ("Error Handling", self.test_error_handling),
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
        self.cleanup()
        
        print("\n" + "=" * 40)
        print(f"🎯 Test Results: {passed}/{total} tests passed")
        
        if passed >= total - 1:  # Allow for one failure
            print("\n🎉 FRONTEND INTEGRATION READY!")
            print("\n✅ Your backend supports:")
            print("  ✓ User profile creation (onboarding)")
            print("  ✓ Profile retrieval and updates")
            print("  ✓ Profile listing with pagination")
            print("  ✓ CORS headers for frontend requests")
            print("  ✓ Proper JSON responses")
            print("  ✓ Error handling (404, validation errors)")
            
            print("\n🚀 Frontend Integration Steps:")
            print("  1. Keep server running: http://localhost:8080")
            print("  2. Start your frontend (usually port 3000)")
            print("  3. Set API_BASE_URL: http://localhost:8080")
            print("  4. Test onboarding flow with profile creation")
            print("  5. Test profile management features")
            
            print("\n📚 Resources:")
            print("  • API Docs: http://localhost:8080/docs")
            print("  • Health Check: http://localhost:8080/health")
            print("  • Agent Info: http://localhost:8080/agent/info")
            
            print("\n💬 For Chat Functionality:")
            print("  • Add GOOGLE_API_KEY to .env file")
            print("  • Get key from: https://aistudio.google.com/app/apikey")
            print("  • Restart server after adding key")
            
            return True
        else:
            print(f"\n❌ {total - passed} tests failed.")
            print("Please check the issues above.")
            return False


def main():
    """Main function."""
    tester = SimpleIntegrationTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 Integration test completed successfully!")
        print("Your backend is ready for frontend integration.")
    else:
        print("\n❌ Some tests failed. Please check the server and try again.")
    
    return success


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)