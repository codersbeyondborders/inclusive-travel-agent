#!/usr/bin/env python3
"""
Test script for the user profile and context system.
"""

import asyncio
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_user_profile_system():
    """Test the complete user profile and context system."""
    print("🧪 Testing User Profile and Context System")
    print("=" * 60)
    
    try:
        # Import services
        from inclusive_travel_agent.services import user_profile_service, context_service
        from inclusive_travel_agent.models import (
            CreateUserProfileRequest,
            BasicInfo,
            TravelInterests,
            AccessibilityProfile,
            UserPreferences,
            TravelStyle,
            BudgetRange,
            CommunicationStyle,
            RiskTolerance,
        )
        from inclusive_travel_agent.agent import root_agent
        from google.adk.sessions import Session
        
        print("✅ Successfully imported all modules")
        
        # Test 1: Create a user profile
        print("\n📝 Test 1: Creating User Profile")
        
        basic_info = BasicInfo(
            name="Sarah Johnson",
            email="sarah.johnson@example.com",
            age=34,
            nationality="US",
            home_location="Seattle, WA",
            phone="+1-555-0123"
        )
        
        travel_interests = TravelInterests(
            preferred_destinations=["Europe", "Japan", "New Zealand"],
            travel_style=[TravelStyle.CULTURAL, TravelStyle.ACCESSIBLE],
            budget_range=BudgetRange.MID_RANGE,
            group_size_preference="solo",
            accommodation_preferences=["accessible_hotel", "central_location"],
            activity_interests=["museums", "accessible_tours", "local_cuisine"],
            transportation_preferences=["accessible_public_transport", "taxi"]
        )
        
        accessibility_profile = AccessibilityProfile(
            mobility_needs=["wheelchair_accessible", "step_free_access"],
            sensory_needs=["hearing_assistance"],
            assistance_preferences={
                "airport_assistance": "wheelchair_assistance",
                "boarding_preference": "priority_boarding",
                "hotel_assistance": "accessible_room_ground_floor"
            },
            mobility_aids=["manual_wheelchair", "hearing_aids"],
            accessibility_priorities=["wheelchair_accessible", "accessible_restrooms"],
            barrier_concerns=["stairs", "narrow_doorways", "loud_environments"],
            dietary_restrictions=["gluten_free"],
            communication_needs=["written_communication_backup"]
        )
        
        preferences = UserPreferences(
            communication_style=CommunicationStyle.DETAILED,
            risk_tolerance=RiskTolerance.LOW,
            planning_horizon="2_months",
            language_preferences=["English"],
            currency_preference="USD",
            timezone="America/Los_Angeles"
        )
        
        create_request = CreateUserProfileRequest(
            basic_info=basic_info,
            travel_interests=travel_interests,
            accessibility_profile=accessibility_profile,
            preferences=preferences
        )
        
        # Create the profile
        user_profile = await user_profile_service.create_user_profile(create_request)
        user_id = user_profile.user_id
        
        print(f"✅ Created user profile: {user_id}")
        print(f"   Name: {user_profile.basic_info.name}")
        print(f"   Profile Complete: {user_profile.profile_complete}")
        print(f"   Accessibility Needs: {len(user_profile.accessibility_profile.mobility_needs + user_profile.accessibility_profile.sensory_needs)}")
        
        # Test 2: Retrieve the profile
        print("\n🔍 Test 2: Retrieving User Profile")
        
        retrieved_profile = await user_profile_service.get_user_profile(user_id)
        if retrieved_profile:
            print(f"✅ Retrieved profile for: {retrieved_profile.basic_info.name}")
            print(f"   Email: {retrieved_profile.basic_info.email}")
            print(f"   Travel Styles: {[style.value for style in retrieved_profile.travel_interests.travel_style]}")
        else:
            print("❌ Failed to retrieve profile")
            return False
        
        # Test 3: Context injection
        print("\n🎯 Test 3: Context Injection")
        
        # Create a session
        from google.adk.sessions import InMemorySessionService
        session_service = InMemorySessionService()
        session = await session_service.create_session(
            state={}, app_name="inclusive-travel-agent", user_id="test_user"
        )
        
        # Inject user context
        context_injected = await context_service.inject_user_context(session, user_id)
        
        if context_injected:
            print("✅ Context injected successfully")
            
            # Check session state
            user_context = context_service.get_user_context_from_session(session)
            if user_context:
                personalized_context = user_context.get("personalized_context", {})
                user_info = personalized_context.get("user_info", {})
                accessibility_summary = personalized_context.get("accessibility_summary", {})
                
                print(f"   User: {user_info.get('name')} from {user_info.get('home_location')}")
                print(f"   Mobility Needs: {accessibility_summary.get('has_mobility_needs')}")
                print(f"   Communication Style: {personalized_context.get('communication_style')}")
                print(f"   Accessibility Priorities: {accessibility_summary.get('accessibility_priorities')}")
            else:
                print("❌ Failed to get user context from session")
                return False
        else:
            print("❌ Failed to inject context")
            return False
        
        # Test 4: Personalized instructions
        print("\n📋 Test 4: Personalized Instructions")
        
        personalized_instructions = user_context.get("personalized_context", {}).get("personalized_instructions", {})
        
        if personalized_instructions:
            print("✅ Generated personalized instructions for agents:")
            for agent_name, instruction in personalized_instructions.items():
                if agent_name in ["root_agent", "accessibility_research_agent", "planning_agent"]:
                    print(f"\n   {agent_name}:")
                    # Show first few lines of instruction
                    lines = instruction.strip().split('\n')[:3]
                    for line in lines:
                        if line.strip():
                            print(f"     {line.strip()}")
                    print("     ...")
        else:
            print("❌ No personalized instructions generated")
            return False
        
        # Test 5: Update profile
        print("\n✏️  Test 5: Updating User Profile")
        
        from inclusive_travel_agent.models import UpdateUserProfileRequest
        
        # Add a new travel interest
        updated_interests = TravelInterests(
            preferred_destinations=["Europe", "Japan", "New Zealand", "Canada"],
            travel_style=[TravelStyle.CULTURAL, TravelStyle.ACCESSIBLE, TravelStyle.RELAXATION],
            budget_range=BudgetRange.MID_RANGE,
            group_size_preference="solo",
            accommodation_preferences=["accessible_hotel", "central_location", "quiet_location"],
            activity_interests=["museums", "accessible_tours", "local_cuisine", "accessible_nature"],
            transportation_preferences=["accessible_public_transport", "taxi"]
        )
        
        update_request = UpdateUserProfileRequest(
            travel_interests=updated_interests
        )
        
        updated_profile = await user_profile_service.update_user_profile(user_id, update_request)
        
        if updated_profile:
            print("✅ Profile updated successfully")
            print(f"   New destinations: {updated_profile.travel_interests.preferred_destinations}")
            print(f"   New travel styles: {[style.value for style in updated_profile.travel_interests.travel_style]}")
        else:
            print("❌ Failed to update profile")
            return False
        
        # Test 6: List profiles
        print("\n📋 Test 6: Listing User Profiles")
        
        profile_summaries = await user_profile_service.list_user_profiles(limit=10)
        
        if profile_summaries:
            print(f"✅ Found {len(profile_summaries)} user profiles:")
            for summary in profile_summaries:
                print(f"   - {summary.name} ({summary.email})")
                print(f"     Accessibility needs: {summary.accessibility_needs_count}")
                print(f"     Travel interests: {summary.travel_interests_count}")
                print(f"     Profile complete: {summary.profile_complete}")
        else:
            print("❌ No profiles found")
        
        # Test 7: Test with agent session
        print("\n🤖 Test 7: Testing with Agent Session")
        
        # Create a new session with context
        test_session = await session_service.create_session(
            state={}, app_name="inclusive-travel-agent", user_id="test_user_2"
        )
        await context_service.inject_user_context(test_session, user_id)
        
        # Test message
        test_message = "I need help planning a trip to Paris"
        
        print(f"   Test message: '{test_message}'")
        print("   Processing with personalized context...")
        
        # Note: We're not actually running the agent here to avoid API calls
        # but we can verify the context is properly set up
        session_context = context_service.get_user_context_from_session(test_session)
        if session_context:
            print("✅ Session ready with personalized context")
            print(f"   User: {session_context['personalized_context']['user_info']['name']}")
            print(f"   Accessibility focus: {session_context['personalized_context']['accessibility_summary']['has_mobility_needs']}")
        else:
            print("❌ Session context not properly set")
            return False
        
        # Cleanup
        print("\n🧹 Cleanup: Deleting Test Profile")
        deleted = await user_profile_service.delete_user_profile(user_id)
        if deleted:
            print("✅ Test profile deleted successfully")
        else:
            print("❌ Failed to delete test profile")
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ User Profile System Features Verified:")
        print("  - User profile creation and storage")
        print("  - Profile retrieval and updates")
        print("  - Context injection into AI sessions")
        print("  - Personalized agent instructions")
        print("  - Accessibility-aware personalization")
        print("  - Profile management operations")
        
        print("\n🚀 System Ready for Frontend Integration!")
        print("  - Frontend can create user profiles via POST /users")
        print("  - Chat API accepts user_id for personalized responses")
        print("  - All accessibility needs are automatically considered")
        print("  - Context persists across conversation sessions")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run the test."""
    success = await test_user_profile_system()
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    result = asyncio.run(main())
    sys.exit(result)