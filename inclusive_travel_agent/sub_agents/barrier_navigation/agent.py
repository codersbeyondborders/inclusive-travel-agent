

"""Barrier Navigation Agent - Provides real-time accessibility solutions and backup options."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from inclusive_travel_agent.sub_agents.barrier_navigation import prompt
from inclusive_travel_agent.tools.memory import memorize
from inclusive_travel_agent.tools.search import google_search_grounding
from inclusive_travel_agent.tools.places import map_tool
from inclusive_travel_agent.tools.accessibility_apis import search_accessible_venues, search_accessible_routes


alternative_finder_agent = Agent(
    model="gemini-2.5-flash",
    name="alternative_finder_agent",
    instruction=prompt.ALTERNATIVE_FINDER_AGENT_INSTR,
    description="Finds accessible alternatives when barriers are encountered",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

barrier_navigation_agent = Agent(
    model="gemini-2.5-flash",
    name="barrier_navigation_agent",
    description="Provides real-time accessibility solutions and backup options for barriers",
    instruction=prompt.BARRIER_NAVIGATION_AGENT_INSTR,
    tools=[
        AgentTool(agent=alternative_finder_agent), 
        memorize, 
        google_search_grounding, 
        map_tool,
        search_accessible_venues,
        search_accessible_routes
    ],
)