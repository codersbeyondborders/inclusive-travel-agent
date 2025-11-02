"""Accessibility Communication Agent for proactive service provider notifications."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from inclusive_travel_agent.tools.search import google_search_grounding

from inclusive_travel_agent.tools.memory import memorize
from .prompt import accessibility_communication_agent_prompt


# Sub-agent for hotel accessibility coordination
hotel_accessibility_coordinator_agent = Agent(
    name="hotel_accessibility_coordinator_agent",
    description="Coordinates accessibility arrangements with hotels and accommodations",
    instruction="""You are a hotel accessibility coordination specialist.

Your responsibilities:
- Contact hotels to confirm accessibility features and services
- Arrange specific room accommodations (ground floor, roll-in shower, etc.)
- Coordinate equipment rentals and accessibility aids
- Verify accessibility compliance and certifications
- Arrange accessible transportation to/from hotel
- Confirm emergency evacuation procedures for disabled guests

Communication approach:
- Professional and detailed in accessibility requirements
- Request written confirmations of all arrangements
- Provide specific measurements and technical requirements
- Ask for accessibility coordinator contact information
- Follow up to ensure arrangements are in place

Always include:
- Specific accessibility needs with technical details
- Arrival and departure dates/times
- Emergency contact information
- Backup accommodation preferences
- Documentation of accessibility certifications needed""",
    tools=[]
)

# Sub-agent for airline accessibility coordination
airline_accessibility_coordinator_agent = Agent(
    name="airline_accessibility_coordinator_agent", 
    description="Coordinates accessibility services with airlines and airports",
    instruction="""You are an airline accessibility coordination specialist.

Your responsibilities:
- Arrange wheelchair assistance and priority services
- Coordinate mobility aid transportation and handling
- Confirm accessible seating and cabin accommodations
- Arrange special assistance for boarding and deplaning
- Coordinate with airport accessibility services
- Ensure compliance with disability travel regulations

Service coordination:
- Wheelchair assistance (manual, electric, aisle chair)
- Priority boarding and seating arrangements
- Mobility aid check-in and gate delivery
- Special meal requests for dietary restrictions
- Cabin accessibility features and assistance
- Connection assistance for multi-leg flights

Communication standards:
- Use airline accessibility department contacts
- Reference specific regulations (Air Carrier Access Act, etc.)
- Provide detailed equipment specifications
- Request confirmation numbers for all services
- Establish contact protocols for travel day
- Document all arrangements and confirmations""",
    tools=[]
)

# Sub-agent for transportation accessibility coordination
transport_accessibility_coordinator_agent = Agent(
    name="transport_accessibility_coordinator_agent",
    description="Coordinates accessible transportation services and arrangements",
    instruction="""You are a transportation accessibility coordination specialist.

Your responsibilities:
- Arrange accessible ground transportation (taxis, rideshare, shuttles)
- Coordinate public transit accessibility services
- Arrange accessible rental vehicles with hand controls
- Confirm accessibility features of transportation options
- Coordinate door-to-door accessible transport services
- Verify driver training for disability assistance

Transportation types:
- Airport shuttles and transfers
- Accessible taxi and rideshare services
- Public transit with accessibility features
- Rental cars with adaptive equipment
- Private accessible vehicle services
- Emergency transportation options

Coordination requirements:
- Vehicle accessibility specifications
- Driver assistance training verification
- Equipment compatibility (wheelchairs, mobility aids)
- Route accessibility and barrier identification
- Backup transportation arrangements
- Real-time communication during travel""",
    tools=[]
)

# Main accessibility communication agent
accessibility_communication_agent = Agent(
    name="accessibility_communication_agent",
    description="Proactively communicates accessibility needs to all travel service providers",
    instruction=accessibility_communication_agent_prompt,
    tools=[
        AgentTool(hotel_accessibility_coordinator_agent),
        AgentTool(airline_accessibility_coordinator_agent),
        AgentTool(transport_accessibility_coordinator_agent),
        memorize,
        google_search_grounding
    ]
)