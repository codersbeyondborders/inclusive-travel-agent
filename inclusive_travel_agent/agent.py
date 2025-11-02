

"""Demonstration of Travel AI Conceirge using Agent Development Kit"""

from google.adk.agents import Agent

from inclusive_travel_agent import prompt

from inclusive_travel_agent.sub_agents.booking.agent import booking_agent
from inclusive_travel_agent.sub_agents.in_trip.agent import in_trip_agent
from inclusive_travel_agent.sub_agents.inspiration.agent import inspiration_agent
from inclusive_travel_agent.sub_agents.planning.agent import planning_agent
from inclusive_travel_agent.sub_agents.post_trip.agent import post_trip_agent
from inclusive_travel_agent.sub_agents.pre_trip.agent import pre_trip_agent

# New accessibility-focused agents
from inclusive_travel_agent.sub_agents.accessibility_research.agent import accessibility_research_agent
from inclusive_travel_agent.sub_agents.mobility_preparation.agent import mobility_preparation_agent
from inclusive_travel_agent.sub_agents.transit_support.agent import transit_support_agent
from inclusive_travel_agent.sub_agents.barrier_navigation.agent import barrier_navigation_agent

# New automation and notification agents
from inclusive_travel_agent.sub_agents.notification.agent import notification_agent
from inclusive_travel_agent.sub_agents.accessibility_communication.agent import accessibility_communication_agent
from inclusive_travel_agent.sub_agents.web_checkin.agent import web_checkin_agent
from inclusive_travel_agent.sub_agents.smart_guardrails.agent import smart_guardrails_agent

from inclusive_travel_agent.tools.memory import _load_precreated_itinerary


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="An Inclusive Travel Agent with comprehensive accessibility support, automated notifications, and intelligent safety monitoring",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        inspiration_agent,
        planning_agent,
        booking_agent,
        pre_trip_agent,
        in_trip_agent,
        post_trip_agent,
        # New accessibility-focused agents
        accessibility_research_agent,
        mobility_preparation_agent,
        transit_support_agent,
        barrier_navigation_agent,
        # New automation and notification agents
        notification_agent,
        accessibility_communication_agent,
        web_checkin_agent,
        smart_guardrails_agent,
    ],
    before_agent_callback=_load_precreated_itinerary,
)
