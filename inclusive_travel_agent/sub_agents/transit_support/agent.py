

"""Transit Support Agent - Manages airport/station assistance and priority services."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from inclusive_travel_agent.sub_agents.transit_support import prompt
from inclusive_travel_agent.tools.memory import memorize
from inclusive_travel_agent.tools.search import google_search_grounding


assistance_booking_agent = Agent(
    model="gemini-2.5-flash",
    name="assistance_booking_agent",
    instruction=prompt.ASSISTANCE_BOOKING_AGENT_INSTR,
    description="Books and coordinates accessibility assistance services for airports, stations, and transport",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

transit_support_agent = Agent(
    model="gemini-2.5-flash",
    name="transit_support_agent",
    description="Manages accessibility assistance at airports, train stations, and during transit",
    instruction=prompt.TRANSIT_SUPPORT_AGENT_INSTR,
    tools=[AgentTool(agent=assistance_booking_agent), memorize, google_search_grounding],
)