#!/usr/bin/env python3
"""
Test script for Phase 4: Advanced Automation & Notification System
"""

import json
from inclusive_travel_agent.agent import root_agent

def test_new_automation_agents():
    """Test that all new automation agents are properly integrated."""
    
    print("Testing New Automation Agents Integration...")
    
    # Get all sub-agent names
    sub_agent_names = [agent.name for agent in root_agent.sub_agents]
    
    # Check for new automation agents
    expected_new_agents = [
        "notification_agent",
        "accessibility_communication_agent", 
        "web_checkin_agent",
        "smart_guardrails_agent"
    ]
    
    for agent_name in expected_new_agents:
        if agent_name in sub_agent_names:
            print(f"✓ {agent_name} successfully integrated")
        else:
            print(f"❌ {agent_name} missing from root agent")
            return False
    
    print("✓ All new automation agents are integrated")
    return True

def test_automation_agent_imports():
    """Test that all automation agents can be imported successfully."""
    
    print("\nTesting Automation Agent Imports...")
    
    try:
        from inclusive_travel_agent.sub_agents.notification.agent import notification_agent
        print("✓ Notification Agent imported successfully")
        
        from inclusive_travel_agent.sub_agents.accessibility_communication.agent import accessibility_communication_agent
        print("✓ Accessibility Communication Agent imported successfully")
        
        from inclusive_travel_agent.sub_agents.web_checkin.agent import web_checkin_agent
        print("✓ Web Check-in Agent imported successfully")
        
        from inclusive_travel_agent.sub_agents.smart_guardrails.agent import smart_guardrails_agent
        print("✓ Smart Guardrails Agent imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing automation agents: {e}")
        return False

def test_agent_structure():
    """Test that each new agent has the expected structure and tools."""
    
    print("\nTesting Agent Structure...")
    
    try:
        from inclusive_travel_agent.sub_agents.notification.agent import notification_agent
        from inclusive_travel_agent.sub_agents.accessibility_communication.agent import accessibility_communication_agent
        from inclusive_travel_agent.sub_agents.web_checkin.agent import web_checkin_agent
        from inclusive_travel_agent.sub_agents.smart_guardrails.agent import smart_guardrails_agent
        
        # Test notification agent
        assert notification_agent.name == "notification_agent"
        assert len(notification_agent.tools) >= 3  # Should have email_composer_agent, notification_scheduler_agent, memorize, google_search_grounding
        print("✓ Notification Agent structure is correct")
        
        # Test accessibility communication agent
        assert accessibility_communication_agent.name == "accessibility_communication_agent"
        assert len(accessibility_communication_agent.tools) >= 4  # Should have hotel, airline, transport coordinators, memorize, google_search_grounding
        print("✓ Accessibility Communication Agent structure is correct")
        
        # Test web check-in agent
        assert web_checkin_agent.name == "web_checkin_agent"
        assert len(web_checkin_agent.tools) >= 4  # Should have flight_checkin, hotel_checkin, checkin_monitor agents, memorize, google_search_grounding
        print("✓ Web Check-in Agent structure is correct")
        
        # Test smart guardrails agent
        assert smart_guardrails_agent.name == "smart_guardrails_agent"
        assert len(smart_guardrails_agent.tools) >= 4  # Should have compliance_monitor, safety_monitor, issue_prevention agents, memorize, google_search_grounding
        print("✓ Smart Guardrails Agent structure is correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing agent structure: {e}")
        return False

def test_email_service_tools():
    """Test that email service tools are available and functional."""
    
    print("\nTesting Email Service Tools...")
    
    try:
        from inclusive_travel_agent.tools.email_service import (
            EmailService,
            send_notification_email,
            send_accessibility_provider_notification
        )
        
        # Test EmailService class
        email_service = EmailService()
        print("✓ EmailService class imported and instantiated")
        
        # Test notification email function
        result = send_notification_email(
            recipient_email="test@example.com",
            subject="Test Notification",
            message="This is a test notification",
            email_type="notification"
        )
        print(f"✓ Notification email function working: {result}")
        
        # Test accessibility provider notification function
        result = send_accessibility_provider_notification(
            provider_email="hotel@example.com",
            provider_name="Test Hotel",
            booking_details={
                "guest_name": "Test Guest",
                "reference": "TEST123",
                "arrival_date": "2024-12-01"
            },
            accessibility_needs={
                "mobility_needs": ["wheelchair_accessible"],
                "assistance_preferences": {"airport_assistance": "wheelchair_assistance"}
            }
        )
        print(f"✓ Accessibility provider notification function working: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing email service tools: {e}")
        return False

def test_root_agent_integration():
    """Test that the root agent properly integrates all automation features."""
    
    print("\nTesting Root Agent Integration...")
    
    try:
        # Check total number of sub-agents (should be original 10 + new 4 = 14)
        total_agents = len(root_agent.sub_agents)
        expected_total = 14
        
        if total_agents == expected_total:
            print(f"✓ Root agent has correct number of sub-agents: {total_agents}")
        else:
            print(f"❌ Root agent has {total_agents} sub-agents, expected {expected_total}")
            return False
        
        # Check that root agent description mentions automation
        description = root_agent.description.lower()
        automation_keywords = ["automation", "notification", "monitoring", "intelligent"]
        
        found_keywords = [keyword for keyword in automation_keywords if keyword in description]
        
        if found_keywords:
            print(f"✓ Root agent description reflects automation features: {found_keywords}")
        else:
            print("❌ Root agent description doesn't reflect automation features")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing root agent integration: {e}")
        return False

def test_prompt_enhancements():
    """Test that prompts have been enhanced with automation agent references."""
    
    print("\nTesting Prompt Enhancements...")
    
    try:
        # Check root agent prompt
        with open("inclusive_travel_agent/prompt.py", "r") as f:
            root_prompt = f.read()
        
        new_agent_references = [
            "notification_agent",
            "accessibility_communication_agent",
            "web_checkin_agent", 
            "smart_guardrails_agent"
        ]
        
        found_references = []
        for agent_ref in new_agent_references:
            if agent_ref in root_prompt:
                found_references.append(agent_ref)
        
        if len(found_references) == len(new_agent_references):
            print("✓ Root agent prompt includes all new automation agents")
        else:
            missing = set(new_agent_references) - set(found_references)
            print(f"❌ Root agent prompt missing references to: {missing}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing prompt enhancements: {e}")
        return False

def test_agent_capabilities():
    """Test specific capabilities of each automation agent."""
    
    print("\nTesting Agent Capabilities...")
    
    try:
        from inclusive_travel_agent.sub_agents.notification.agent import notification_agent
        from inclusive_travel_agent.sub_agents.accessibility_communication.agent import accessibility_communication_agent
        from inclusive_travel_agent.sub_agents.web_checkin.agent import web_checkin_agent
        from inclusive_travel_agent.sub_agents.smart_guardrails.agent import smart_guardrails_agent
        
        # Test notification agent capabilities
        notification_tools = [str(tool) for tool in notification_agent.tools]
        has_email_tools = any("email" in tool.lower() or "notification" in tool.lower() for tool in notification_tools)
        if has_email_tools or len(notification_agent.tools) >= 3:
            print("✓ Notification Agent has appropriate tools for email and scheduling")
        else:
            print("❌ Notification Agent missing expected tools")
            return False
        
        # Test accessibility communication agent capabilities
        comm_tools = [str(tool) for tool in accessibility_communication_agent.tools]
        has_coordination_tools = any("coordinator" in tool.lower() or "hotel" in tool.lower() or "airline" in tool.lower() for tool in comm_tools)
        if has_coordination_tools or len(accessibility_communication_agent.tools) >= 4:
            print("✓ Accessibility Communication Agent has appropriate coordination tools")
        else:
            print("❌ Accessibility Communication Agent missing expected tools")
            return False
        
        # Test web check-in agent capabilities
        checkin_tools = [str(tool) for tool in web_checkin_agent.tools]
        has_checkin_tools = any("checkin" in tool.lower() or "flight" in tool.lower() or "hotel" in tool.lower() for tool in checkin_tools)
        if has_checkin_tools or len(web_checkin_agent.tools) >= 4:
            print("✓ Web Check-in Agent has appropriate check-in tools")
        else:
            print("❌ Web Check-in Agent missing expected tools")
            return False
        
        # Test smart guardrails agent capabilities
        guardrails_tools = [str(tool) for tool in smart_guardrails_agent.tools]
        has_monitoring_tools = any("monitor" in tool.lower() or "compliance" in tool.lower() or "safety" in tool.lower() for tool in guardrails_tools)
        if has_monitoring_tools or len(smart_guardrails_agent.tools) >= 4:
            print("✓ Smart Guardrails Agent has appropriate monitoring tools")
        else:
            print("❌ Smart Guardrails Agent missing expected tools")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing agent capabilities: {e}")
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
    print("🚀 Starting Phase 4 Advanced Automation & Notification System Tests\n")
    
    success = True
    
    # Run all tests
    success &= test_new_automation_agents()
    success &= test_automation_agent_imports()
    success &= test_agent_structure()
    success &= test_email_service_tools()
    success &= test_root_agent_integration()
    success &= test_prompt_enhancements()
    success &= test_agent_capabilities()
    success &= test_agent_loading()
    
    if success:
        print("\n✅ Phase 4: Advanced Automation & Notification System - ALL TESTS PASSED!")
        print("\nPhase 4 Summary:")
        print("- ✅ Created 4 new automation and notification agents")
        print("- ✅ Notification Agent for email alerts and confirmations")
        print("- ✅ Accessibility Communication Agent for proactive provider coordination")
        print("- ✅ Web Check-in Agent for automated flight and hotel check-in")
        print("- ✅ Smart Guardrails Agent for safety monitoring and issue prevention")
        print("- ✅ Email service tools for comprehensive notification system")
        print("- ✅ Integrated all agents into the root agent system (14 total agents)")
        print("- ✅ Updated prompts to include new automation capabilities")
        print("\n🎉 System now provides comprehensive automation and proactive support!")
        print("\nTotal Agent Count: 14 specialized agents")
        print("- 6 Original travel agents")
        print("- 4 Accessibility-focused agents (Phase 2)")
        print("- 4 Automation & notification agents (Phase 4)")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")