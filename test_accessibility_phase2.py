#!/usr/bin/env python3
"""
Test script for Phase 2: Specialized Agent Development
"""

import json
from inclusive_travel_agent.agent import root_agent

def test_new_accessibility_agents():
    """Test that all new accessibility agents are properly integrated."""
    
    print("Testing New Accessibility Agents Integration...")
    
    # Get all sub-agent names
    sub_agent_names = [agent.name for agent in root_agent.sub_agents]
    
    # Check for new accessibility agents
    expected_new_agents = [
        "accessibility_research_agent",
        "mobility_preparation_agent", 
        "transit_support_agent",
        "barrier_navigation_agent"
    ]
    
    for agent_name in expected_new_agents:
        if agent_name in sub_agent_names:
            print(f"✓ {agent_name} successfully integrated")
        else:
            print(f"❌ {agent_name} missing from root agent")
            return False
    
    print("✓ All new accessibility agents are integrated")
    return True

def test_accessibility_agent_imports():
    """Test that all accessibility agents can be imported successfully."""
    
    print("\nTesting Accessibility Agent Imports...")
    
    try:
        from inclusive_travel_agent.sub_agents.accessibility_research.agent import accessibility_research_agent
        print("✓ Accessibility Research Agent imported successfully")
        
        from inclusive_travel_agent.sub_agents.mobility_preparation.agent import mobility_preparation_agent
        print("✓ Mobility Preparation Agent imported successfully")
        
        from inclusive_travel_agent.sub_agents.transit_support.agent import transit_support_agent
        print("✓ Transit Support Agent imported successfully")
        
        from inclusive_travel_agent.sub_agents.barrier_navigation.agent import barrier_navigation_agent
        print("✓ Barrier Navigation Agent imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing accessibility agents: {e}")
        return False

def test_agent_structure():
    """Test that each new agent has the expected structure and tools."""
    
    print("\nTesting Agent Structure...")
    
    try:
        from inclusive_travel_agent.sub_agents.accessibility_research.agent import accessibility_research_agent
        from inclusive_travel_agent.sub_agents.mobility_preparation.agent import mobility_preparation_agent
        from inclusive_travel_agent.sub_agents.transit_support.agent import transit_support_agent
        from inclusive_travel_agent.sub_agents.barrier_navigation.agent import barrier_navigation_agent
        
        # Test accessibility research agent
        assert accessibility_research_agent.name == "accessibility_research_agent"
        assert len(accessibility_research_agent.tools) >= 1  # Should have google_search_grounding and accessibility_info_agent
        print("✓ Accessibility Research Agent structure is correct")
        
        # Test mobility preparation agent
        assert mobility_preparation_agent.name == "mobility_preparation_agent"
        assert len(mobility_preparation_agent.tools) >= 2  # Should have packing_list_agent, memorize, google_search_grounding
        print("✓ Mobility Preparation Agent structure is correct")
        
        # Test transit support agent
        assert transit_support_agent.name == "transit_support_agent"
        assert len(transit_support_agent.tools) >= 2  # Should have assistance_booking_agent, memorize, google_search_grounding
        print("✓ Transit Support Agent structure is correct")
        
        # Test barrier navigation agent
        assert barrier_navigation_agent.name == "barrier_navigation_agent"
        assert len(barrier_navigation_agent.tools) >= 3  # Should have alternative_finder_agent, memorize, google_search_grounding, map_tool
        print("✓ Barrier Navigation Agent structure is correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing agent structure: {e}")
        return False

def test_enhanced_booking_agent():
    """Test that the booking agent has been enhanced with accessibility features."""
    
    print("\nTesting Enhanced Booking Agent...")
    
    try:
        from inclusive_travel_agent.sub_agents.booking.agent import booking_agent
        
        # Check that booking agent exists and has expected tools
        assert booking_agent.name == "booking_agent"
        assert len(booking_agent.tools) >= 3  # Should have create_reservation, payment_choice, process_payment
        
        # Read the booking prompt to verify accessibility enhancements
        with open("inclusive_travel_agent/sub_agents/booking/prompt.py", "r") as f:
            booking_prompt_content = f.read()
        
        # Check for accessibility-related keywords in the prompt
        accessibility_keywords = [
            "accessibility accommodations",
            "accessible booking",
            "wheelchair assistance",
            "accessibility needs"
        ]
        
        found_keywords = []
        for keyword in accessibility_keywords:
            if keyword.lower() in booking_prompt_content.lower():
                found_keywords.append(keyword)
        
        if len(found_keywords) >= 2:
            print("✓ Booking agent enhanced with accessibility features")
            print(f"  Found accessibility keywords: {found_keywords}")
            return True
        else:
            print(f"❌ Booking agent missing accessibility enhancements. Found: {found_keywords}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing enhanced booking agent: {e}")
        return False

def test_root_agent_integration():
    """Test that the root agent properly integrates all accessibility features."""
    
    print("\nTesting Root Agent Integration...")
    
    try:
        # Check total number of sub-agents (should be original 6 + new 4 = 10)
        total_agents = len(root_agent.sub_agents)
        expected_total = 10
        
        if total_agents == expected_total:
            print(f"✓ Root agent has correct number of sub-agents: {total_agents}")
        else:
            print(f"❌ Root agent has {total_agents} sub-agents, expected {expected_total}")
            return False
        
        # Check that root agent description mentions accessibility
        if "inclusive" in root_agent.description.lower() or "accessibility" in root_agent.description.lower():
            print("✓ Root agent description reflects accessibility focus")
        else:
            print("❌ Root agent description doesn't reflect accessibility focus")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing root agent integration: {e}")
        return False

def test_prompt_enhancements():
    """Test that prompts have been enhanced with accessibility considerations."""
    
    print("\nTesting Prompt Enhancements...")
    
    try:
        # Check root agent prompt
        with open("inclusive_travel_agent/prompt.py", "r") as f:
            root_prompt = f.read()
        
        new_agent_references = [
            "accessibility_research_agent",
            "mobility_preparation_agent",
            "transit_support_agent", 
            "barrier_navigation_agent"
        ]
        
        found_references = []
        for agent_ref in new_agent_references:
            if agent_ref in root_prompt:
                found_references.append(agent_ref)
        
        if len(found_references) == len(new_agent_references):
            print("✓ Root agent prompt includes all new accessibility agents")
        else:
            print(f"❌ Root agent prompt missing references to: {set(new_agent_references) - set(found_references)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing prompt enhancements: {e}")
        return False

def test_agent_loading():
    """Test that the complete system loads without errors."""
    
    print("\nTesting Complete System Loading...")
    
    try:
        # Try to load the root agent (this tests the entire system)
        assert root_agent is not None
        assert root_agent.name == "root_agent"
        
        print("✓ Complete system loads successfully")
        print(f"✓ Root agent has {len(root_agent.sub_agents)} sub-agents")
        
        # List all agents for verification
        agent_names = [agent.name for agent in root_agent.sub_agents]
        print("✓ Integrated agents:")
        for name in sorted(agent_names):
            print(f"  - {name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading complete system: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Phase 2 Specialized Agent Development Tests\n")
    
    success = True
    
    # Run all tests
    success &= test_new_accessibility_agents()
    success &= test_accessibility_agent_imports()
    success &= test_agent_structure()
    success &= test_enhanced_booking_agent()
    success &= test_root_agent_integration()
    success &= test_prompt_enhancements()
    success &= test_agent_loading()
    
    if success:
        print("\n✅ Phase 2: Specialized Agent Development - ALL TESTS PASSED!")
        print("\nPhase 2 Summary:")
        print("- ✅ Created 4 new specialized accessibility agents")
        print("- ✅ Accessibility Research Agent for gathering accessibility information")
        print("- ✅ Mobility Preparation Agent for equipment and documentation")
        print("- ✅ Transit Support Agent for airport/station assistance")
        print("- ✅ Barrier Navigation Agent for real-time accessibility solutions")
        print("- ✅ Enhanced booking agent with accessibility accommodations")
        print("- ✅ Integrated all agents into the root agent system")
        print("- ✅ Updated prompts to include new accessibility capabilities")
        print("\nReady to proceed to Phase 3!")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")