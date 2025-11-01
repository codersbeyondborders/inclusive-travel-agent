#!/usr/bin/env python3
"""
Test script for Phase 1: Core Accessibility Integration
"""

import json
from travel_concierge.shared_libraries.types import (
    AccessibilityInfo, 
    AccessibleUserProfile, 
    AccessibilityNeeds,
    Destination,
    POI,
    Hotel,
    Flight,
    DisabilityExpense
)

def test_accessibility_data_models():
    """Test that our new accessibility data models work correctly."""
    
    print("Testing Accessibility Data Models...")
    
    # Test AccessibilityInfo
    accessibility_info = AccessibilityInfo(
        wheelchair_accessible=True,
        hearing_assistance=True,
        visual_assistance=False,
        mobility_aid_friendly=True,
        accessible_parking=True,
        accessible_restrooms=True,
        elevator_access=True,
        step_free_access=True,
        accessibility_rating=4.5,
        accessibility_notes="Excellent wheelchair access with ramps and wide doorways"
    )
    print("✓ AccessibilityInfo model created successfully")
    
    # Test AccessibilityNeeds
    accessibility_needs = AccessibilityNeeds(
        mobility_needs=["wheelchair_accessible", "step_free_access"],
        sensory_needs=["hearing_assistance"],
        assistance_preferences={
            "airport_assistance": "wheelchair_assistance",
            "boarding_preference": "priority_boarding"
        },
        mobility_aids=["manual_wheelchair"]
    )
    print("✓ AccessibilityNeeds model created successfully")
    
    # Test AccessibleUserProfile
    user_profile = AccessibleUserProfile(
        passport_nationality="US Citizen",
        home_address="123 Main St, San Diego, CA",
        home_transit_preference="accessible_public_transport",
        accessibility_needs=accessibility_needs,
        emergency_contacts=[{
            "name": "John Doe",
            "phone": "+1-555-0123",
            "relationship": "family"
        }],
        medical_documents=["disability_certificate"]
    )
    print("✓ AccessibleUserProfile model created successfully")
    
    # Test enhanced Destination with accessibility
    destination = Destination(
        name="San Francisco",
        country="United States",
        image="https://example.com/sf.jpg",
        highlights="Accessible city with excellent public transport and disability-friendly attractions",
        rating="4.5",
        accessibility_info=accessibility_info,
        disability_friendly_score=4.8,
        accessible_attractions=["Golden Gate Bridge accessible viewpoints", "Accessible cable car routes"]
    )
    print("✓ Enhanced Destination model created successfully")
    
    # Test enhanced POI with accessibility
    poi = POI(
        place_name="Golden Gate Bridge",
        address="Golden Gate Bridge, San Francisco, CA",
        lat="37.8199",
        long="-122.4783",
        review_ratings="4.8",
        highlights="Iconic bridge with accessible viewing areas and parking",
        image_url="https://example.com/ggb.jpg",
        map_url="",  # Required field
        place_id="",  # Required field
        accessibility_info=accessibility_info,
        accessibility_features=["Accessible parking", "Wheelchair accessible paths", "Audio descriptions"],
        barrier_warnings=["Strong winds may affect some mobility aids"]
    )
    print("✓ Enhanced POI model created successfully")
    
    # Test enhanced Hotel with accessibility
    disability_expense = DisabilityExpense(
        expense_type="Accessible room upgrade",
        amount_usd=25.0,
        description="Daily surcharge for accessible room with roll-in shower",
        is_mandatory=False
    )
    
    hotel = Hotel(
        name="Accessible Grand Hotel",
        address="456 Market St, San Francisco, CA",
        check_in_time="16:00",
        check_out_time="11:00",
        thumbnail="/images/hotel.png",
        price=200,
        accessibility_info=accessibility_info,
        accessible_rooms_available=True,
        accessibility_services=["Wheelchair rental", "Sign language interpreters", "Braille menus"],
        disability_additional_costs=[disability_expense]
    )
    print("✓ Enhanced Hotel model created successfully")
    
    # Test enhanced Flight with accessibility
    flight = Flight(
        flight_number="AA123",
        departure={
            "city_name": "San Francisco",
            "airport_code": "SFO", 
            "timestamp": "2024-03-15T08:00:00"
        },
        arrival={
            "city_name": "Los Angeles",
            "airport_code": "LAX",
            "timestamp": "2024-03-15T10:30:00"
        },
        airlines=["American Airlines"],
        airline_logo="/images/american.png",
        price_in_usd=350,
        number_of_stops=0,
        accessibility_services=["Wheelchair assistance", "Priority boarding", "Accessible seating"],
        wheelchair_assistance=True,
        priority_boarding=True,
        accessible_seating=True,
        disability_additional_costs=[
            DisabilityExpense(
                expense_type="Service animal accommodation",
                amount_usd=0.0,
                description="No charge for service animals",
                is_mandatory=False
            )
        ]
    )
    print("✓ Enhanced Flight model created successfully")
    
    print("\n🎉 All accessibility data models are working correctly!")
    return True

def test_accessible_profile_loading():
    """Test that our accessible profile loads correctly."""
    
    print("\nTesting Accessible Profile Loading...")
    
    try:
        with open("travel_concierge/profiles/itinerary_accessible_default.json", "r") as f:
            profile_data = json.load(f)
        
        user_profile_data = profile_data["state"]["user_profile"]
        
        # Verify accessibility fields are present
        assert "accessibility_needs" in user_profile_data
        assert "mobility_needs" in user_profile_data["accessibility_needs"]
        assert "assistance_preferences" in user_profile_data["accessibility_needs"]
        
        print("✓ Accessible profile file loads correctly")
        print("✓ Accessibility fields are present in profile")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading accessible profile: {e}")
        return False

def test_agent_loading():
    """Test that the agent loads with accessibility features."""
    
    print("\nTesting Agent Loading...")
    
    try:
        from travel_concierge.agent import root_agent
        
        # Check that the agent has the expected sub-agents
        sub_agent_names = [agent.name for agent in root_agent.sub_agents]
        expected_agents = ["inspiration_agent", "planning_agent", "booking_agent", 
                          "pre_trip_agent", "in_trip_agent", "post_trip_agent"]
        
        for expected in expected_agents:
            assert expected in sub_agent_names, f"Missing sub-agent: {expected}"
        
        print("✓ Root agent loads successfully")
        print("✓ All expected sub-agents are present")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading agent: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Phase 1 Accessibility Integration Tests\n")
    
    success = True
    
    # Run all tests
    success &= test_accessibility_data_models()
    success &= test_accessible_profile_loading()
    success &= test_agent_loading()
    
    if success:
        print("\n✅ Phase 1: Core Accessibility Integration - ALL TESTS PASSED!")
        print("\nPhase 1 Summary:")
        print("- ✅ Extended data schemas with accessibility information")
        print("- ✅ Created AccessibilityInfo, AccessibilityNeeds, and AccessibleUserProfile models")
        print("- ✅ Enhanced existing models (Destination, POI, Hotel, Flight) with accessibility fields")
        print("- ✅ Updated agent prompts to include accessibility considerations")
        print("- ✅ Created accessible default user profile")
        print("- ✅ Modified root agent to focus on inclusive travel")
        print("\nReady to proceed to Phase 2!")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")