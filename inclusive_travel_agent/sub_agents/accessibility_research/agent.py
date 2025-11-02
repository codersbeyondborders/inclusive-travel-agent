"""Accessibility Research Agent - Gathers accessibility information and reviews."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from inclusive_travel_agent.shared_libraries.types import AccessibilityInfo, json_response_config
from inclusive_travel_agent.sub_agents.accessibility_research import prompt
from inclusive_travel_agent.tools.search import google_search_grounding
from inclusive_travel_agent.tools.accessibility_apis import search_accessible_venues, get_airport_accessibility


accessibility_info_agent = Agent(
    model="gemini-2.5-flash",
    name="accessibility_info_agent",
    instruction=prompt.ACCESSIBILITY_INFO_AGENT_INSTR,
    description="Gathers detailed accessibility information for venues, transport, and activities",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=AccessibilityInfo,
    output_key="accessibility_info",
    generate_content_config=json_response_config,
)

accessibility_research_agent = Agent(
    model="gemini-2.5-flash",
    name="accessibility_research_agent",
    description="Researches accessibility information, disabled traveler reviews, and barrier assessments",
    instruction=prompt.ACCESSIBILITY_RESEARCH_AGENT_INSTR,
    tools=[
        AgentTool(agent=accessibility_info_agent), 
        google_search_grounding,
        search_accessible_venues,
        get_airport_accessibility
    ],
)