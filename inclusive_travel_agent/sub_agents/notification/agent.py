"""Notification Agent for email alerts and confirmations."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from inclusive_travel_agent.tools.search import google_search_grounding

from inclusive_travel_agent.tools.memory import memorize
from inclusive_travel_agent.tools.email_service import send_notification_email, send_accessibility_provider_notification
from .prompt import notification_agent_prompt


# Sub-agent for email composition and sending
email_composer_agent = Agent(
    name="email_composer_agent",
    description="Composes professional emails for travel confirmations and accessibility notifications",
    instruction="""You are an expert email composer specializing in travel and accessibility communications.

Your responsibilities:
- Compose professional, clear emails for travel confirmations
- Create accessibility notification emails for hotels and airlines
- Draft confirmation requests and follow-up messages
- Ensure all accessibility needs are clearly communicated
- Use appropriate tone for different recipients (formal for businesses, friendly for personal)

Email types you handle:
1. Booking confirmations to user
2. Accessibility needs notifications to hotels/airlines
3. Check-in reminders and instructions
4. Travel document reminders
5. Emergency contact notifications
6. Itinerary updates and changes

Always include:
- Clear subject lines
- Professional greeting and closing
- Specific accessibility requirements
- Contact information for follow-up
- Relevant booking references and dates

Format emails in a structured way with clear sections and bullet points for accessibility needs.""",
    tools=[]
)

# Sub-agent for notification scheduling and management
notification_scheduler_agent = Agent(
    name="notification_scheduler_agent", 
    description="Schedules and manages travel notifications and reminders",
    instruction="""You are a notification scheduling specialist for accessible travel.

Your responsibilities:
- Schedule email notifications at optimal times
- Manage notification preferences and timing
- Track notification delivery and responses
- Set up reminder sequences for important tasks
- Coordinate multiple notification channels

Notification types you manage:
1. Pre-travel reminders (documents, packing, accessibility prep)
2. Booking confirmations and updates
3. Check-in reminders (24-48 hours before)
4. Accessibility service confirmations
5. Emergency contact notifications
6. Post-travel feedback requests

Timing guidelines:
- Accessibility notifications: 7-14 days before travel
- Check-in reminders: 24-48 hours before departure
- Document reminders: 1 week before travel
- Packing reminders: 2-3 days before travel
- Emergency notifications: Immediate

Always consider user preferences, time zones, and urgency levels.""",
    tools=[]
)

# Main notification agent
notification_agent = Agent(
    name="notification_agent",
    description="Manages all travel notifications, confirmations, and email communications",
    instruction=notification_agent_prompt,
    tools=[
        AgentTool(email_composer_agent),
        AgentTool(notification_scheduler_agent),
        memorize,
        google_search_grounding,
        send_notification_email,
        send_accessibility_provider_notification
    ]
)