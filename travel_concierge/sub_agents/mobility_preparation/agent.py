

"""Mobility Aid Preparation Agent - Handles equipment, medical docs, and assistive tech preparation."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from travel_concierge.shared_libraries.types import PackingList, json_response_config
from travel_concierge.sub_agents.mobility_preparation import prompt
from travel_concierge.tools.memory import memorize
from travel_concierge.tools.search import google_search_grounding


packing_list_agent = Agent(
    model="gemini-2.5-flash",
    name="packing_list_agent",
    instruction=prompt.PACKING_LIST_AGENT_INSTR,
    description="Creates comprehensive packing lists for disabled travelers including mobility aids and medical supplies",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=PackingList,
    output_key="packing_list",
    generate_content_config=json_response_config,
)

mobility_preparation_agent = Agent(
    model="gemini-2.5-flash",
    name="mobility_preparation_agent",
    description="Helps prepare mobility aids, medical documentation, and assistive equipment for travel",
    instruction=prompt.MOBILITY_PREPARATION_AGENT_INSTR,
    tools=[AgentTool(agent=packing_list_agent), memorize, google_search_grounding],
)