

"""Demonstration of Travel AI Conceirge using Agent Development Kit"""

from google.adk.agents import Agent

from travel_concierge import prompt

from travel_concierge.sub_agents.booking.agent import booking_agent
from travel_concierge.sub_agents.in_trip.agent import in_trip_agent
from travel_concierge.sub_agents.inspiration.agent import inspiration_agent
from travel_concierge.sub_agents.planning.agent import planning_agent
from travel_concierge.sub_agents.post_trip.agent import post_trip_agent
from travel_concierge.sub_agents.pre_trip.agent import pre_trip_agent

# New accessibility-focused agents
from travel_concierge.sub_agents.accessibility_research.agent import accessibility_research_agent
from travel_concierge.sub_agents.mobility_preparation.agent import mobility_preparation_agent
from travel_concierge.sub_agents.transit_support.agent import transit_support_agent
from travel_concierge.sub_agents.barrier_navigation.agent import barrier_navigation_agent

from travel_concierge.tools.memory import _load_precreated_itinerary


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="An Inclusive Travel Agent using specialized accessibility-focused sub-agents",
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
    ],
    before_agent_callback=_load_precreated_itinerary,
)
