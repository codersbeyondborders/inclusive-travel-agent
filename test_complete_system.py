#!/usr/bin/env python3
"""
Complete system test for the Inclusive Travel Agent.
Tests all three phases of development.
"""

import os
import sys
from pathlib import Path


def test_phase1_accessibility_integration():
    """Test Phase 1: Core Accessibility Integration."""
    print("🔍 Testing Phase 1: Core Accessibility Integration")
    
    try:
        # Test accessibility data models
        from travel_concierge.shared_libraries.types import (
            AccessibilityInfo, AccessibilityNeeds, AccessibleUserProfile,
            Destination, POI, Hotel, Flight, DisabilityExpense
        )
        
        # Test enhanced models work
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
            accessibility_notes="Excellent accessibility features"
        )
        
        destination = Destination(
            name="San Francisco",
            country="United States", 
            image="https://example.com/sf.jpg",
            highlights="Accessible city with great public transport",
            rating="4.5",
            accessibility_info=accessibility_info,
            disability_friendly_score=4.8,
            accessible_attractions=["Golden Gate Bridge accessible areas"]
        )
        
        print("  ✅ Accessibility data models working")
        
        # Test accessible profile loading
        profile_path = Path("travel_concierge/profiles/itinerary_accessible_default.json")
        if profile_path.exists():
            print("  ✅ Accessible user profile exists")
        else:
            print("  ❌ Accessible user profile missing")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Phase 1 test failed: {e}")
        return False


def test_phase2_specialized_agents():
    """Test Phase 2: Specialized Agent Development."""
    print("\n🤖 Testing Phase 2: Specialized Agent Development")
    
    try:
        # Test new specialized agents
        from travel_concierge.sub_agents.accessibility_research.agent import accessibility_research_agent
        from travel_concierge.sub_agents.mobility_preparation.agent import mobility_preparation_agent
        from travel_concierge.sub_agents.transit_support.agent import transit_support_agent
        from travel_concierge.sub_agents.barrier_navigation.agent import barrier_navigation_agent
        
        agents = [
            accessibility_research_agent,
            mobility_preparation_agent,
            transit_support_agent,
            barrier_navigation_agent
        ]
        
        for agent in agents:
            if agent and agent.name and len(agent.tools) > 0:
                print(f"  ✅ {agent.name} working with {len(agent.tools)} tools")
            else:
                print(f"  ❌ {agent.name if agent else 'Unknown'} not working properly")
                return False
        
        # Test root agent integration
        from travel_concierge.agent import root_agent
        
        if len(root_agent.sub_agents) == 10:
            print("  ✅ All 10 agents integrated in root agent")
        else:
            print(f"  ❌ Expected 10 agents, found {len(root_agent.sub_agents)}")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Phase 2 test failed: {e}")
        return False


def test_phase3_cloud_deployment():
    """Test Phase 3: External API Integration & Cloud Run Deployment."""
    print("\n☁️  Testing Phase 3: External API Integration & Cloud Run Deployment")
    
    try:
        # Test ML Dev configuration
        with open(".env.example", "r") as f:
            env_content = f.read()
        
        if "GOOGLE_GENAI_USE_VERTEXAI=0" in env_content:
            print("  ✅ ML Dev backend configured")
        else:
            print("  ❌ ML Dev backend not configured")
            return False
        
        # Test accessibility APIs
        from travel_concierge.tools.accessibility_apis import AccessibilityAPIService
        
        api_service = AccessibilityAPIService()
        airport_info = api_service.get_airport_accessibility_info("LAX")
        
        if airport_info and "name" in airport_info:
            print("  ✅ Accessibility APIs working")
        else:
            print("  ❌ Accessibility APIs not working")
            return False
        
        # Test FastAPI application
        from travel_concierge.main import app
        
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/health", "/chat", "/agent/info"]
        
        if all(route in routes for route in expected_routes):
            print("  ✅ FastAPI application ready")
        else:
            print("  ❌ FastAPI application missing routes")
            return False
        
        # Test deployment files
        deployment_files = [
            "Dockerfile",
            "cloudbuild.yaml",
            "deploy/deploy_cloud_run.py"
        ]
        
        missing_files = [f for f in deployment_files if not Path(f).exists()]
        
        if not missing_files:
            print("  ✅ All deployment files present")
        else:
            print(f"  ❌ Missing deployment files: {missing_files}")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Phase 3 test failed: {e}")
        return False


def test_system_integration():
    """Test complete system integration."""
    print("\n🔗 Testing Complete System Integration")
    
    try:
        # Set ML Dev backend
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"
        
        # Test complete system loading
        from travel_concierge.agent import root_agent
        
        # Verify all components
        if not root_agent:
            print("  ❌ Root agent not loaded")
            return False
        
        if len(root_agent.sub_agents) != 10:
            print(f"  ❌ Expected 10 sub-agents, found {len(root_agent.sub_agents)}")
            return False
        
        # Test agent names and descriptions
        agent_names = [agent.name for agent in root_agent.sub_agents]
        expected_agents = [
            "inspiration_agent",
            "planning_agent", 
            "booking_agent",
            "pre_trip_agent",
            "in_trip_agent",
            "post_trip_agent",
            "accessibility_research_agent",
            "mobility_preparation_agent",
            "transit_support_agent",
            "barrier_navigation_agent"
        ]
        
        missing_agents = [name for name in expected_agents if name not in agent_names]
        
        if not missing_agents:
            print("  ✅ All expected agents present")
        else:
            print(f"  ❌ Missing agents: {missing_agents}")
            return False
        
        # Test accessibility focus
        if "inclusive" in root_agent.description.lower():
            print("  ✅ System focused on inclusive travel")
        else:
            print("  ❌ System not focused on inclusive travel")
            return False
        
        print("  ✅ Complete system integration successful")
        return True
        
    except Exception as e:
        print(f"  ❌ System integration test failed: {e}")
        return False


def test_accessibility_features():
    """Test specific accessibility features."""
    print("\n♿ Testing Accessibility Features")
    
    try:
        # Test accessibility data structures
        from travel_concierge.shared_libraries.types import AccessibilityInfo, AccessibilityNeeds
        
        # Create comprehensive accessibility info
        accessibility_info = AccessibilityInfo(
            wheelchair_accessible=True,
            hearing_assistance=True,
            visual_assistance=True,
            mobility_aid_friendly=True,
            accessible_parking=True,
            accessible_restrooms=True,
            elevator_access=True,
            step_free_access=True,
            accessibility_rating=5.0,
            accessibility_notes="Fully accessible venue with all accommodations"
        )
        
        accessibility_needs = AccessibilityNeeds(
            mobility_needs=["wheelchair_accessible", "step_free_access"],
            sensory_needs=["hearing_assistance", "visual_assistance"],
            assistance_preferences={
                "airport_assistance": "wheelchair_assistance",
                "boarding_preference": "priority_boarding"
            },
            mobility_aids=["manual_wheelchair", "hearing_aids"]
        )
        
        print("  ✅ Accessibility data structures comprehensive")
        
        # Test accessibility API tools
        from travel_concierge.tools.accessibility_apis import (
            search_accessible_venues,
            get_airport_accessibility,
            search_accessible_routes
        )
        
        print("  ✅ Accessibility API tools available")
        
        # Test agent accessibility integration
        from travel_concierge.sub_agents.accessibility_research.agent import accessibility_research_agent
        
        research_tools = [str(tool) for tool in accessibility_research_agent.tools]
        has_accessibility_tools = any("accessibility" in tool.lower() for tool in research_tools)
        
        if has_accessibility_tools:
            print("  ✅ Agents integrated with accessibility tools")
        else:
            print("  ❌ Agents missing accessibility tool integration")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Accessibility features test failed: {e}")
        return False


def generate_system_report():
    """Generate a comprehensive system report."""
    print("\n📊 System Report")
    
    try:
        from travel_concierge.agent import root_agent
        
        print(f"  🤖 Root Agent: {root_agent.name}")
        print(f"  📝 Description: {root_agent.description}")
        print(f"  🔢 Total Sub-Agents: {len(root_agent.sub_agents)}")
        
        print("\n  📋 Sub-Agents:")
        for i, agent in enumerate(root_agent.sub_agents, 1):
            tool_count = len(agent.tools) if hasattr(agent, 'tools') else 0
            print(f"    {i:2d}. {agent.name} ({tool_count} tools)")
        
        # Check accessibility features
        accessibility_agents = [
            agent for agent in root_agent.sub_agents 
            if "accessibility" in agent.name or "mobility" in agent.name or 
               "transit" in agent.name or "barrier" in agent.name
        ]
        
        print(f"\n  ♿ Accessibility-Focused Agents: {len(accessibility_agents)}")
        
        # Check deployment readiness
        deployment_files = [
            "Dockerfile",
            "cloudbuild.yaml", 
            "travel_concierge/main.py",
            "deploy/deploy_cloud_run.py"
        ]
        
        ready_files = [f for f in deployment_files if Path(f).exists()]
        print(f"\n  🚀 Deployment Readiness: {len(ready_files)}/{len(deployment_files)} files ready")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Report generation failed: {e}")
        return False


def main():
    """Run complete system tests."""
    print("🧪 Inclusive Travel Agent - Complete System Test")
    print("=" * 60)
    
    success = True
    
    # Run all test phases
    success &= test_phase1_accessibility_integration()
    success &= test_phase2_specialized_agents()
    success &= test_phase3_cloud_deployment()
    success &= test_system_integration()
    success &= test_accessibility_features()
    
    # Generate system report
    generate_system_report()
    
    print("\n" + "=" * 60)
    
    if success:
        print("🎉 ALL TESTS PASSED - SYSTEM READY FOR DEPLOYMENT!")
        print("\n✅ Phase 1: Core Accessibility Integration - Complete")
        print("✅ Phase 2: Specialized Agent Development - Complete") 
        print("✅ Phase 3: External API Integration & Cloud Run Deployment - Complete")
        print("\n🚀 The Inclusive Travel Agent is ready to help disabled travelers!")
        print("\n📋 Next Steps:")
        print("  1. Set up Google Cloud project and API keys")
        print("  2. Run: python deploy/deploy_cloud_run.py --project-id YOUR_PROJECT")
        print("  3. Test deployed service and configure monitoring")
        print("  4. Launch and start helping travelers! 🌟")
        
        return 0
    else:
        print("❌ SOME TESTS FAILED - PLEASE CHECK ERRORS ABOVE")
        return 1


if __name__ == "__main__":
    sys.exit(main())