"""Context service for injecting user profile data into AI agents."""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from google.adk.sessions import Session
from travel_concierge.models.user_profile import UserProfile
from travel_concierge.services.user_profile_service import user_profile_service


logger = logging.getLogger(__name__)


class ContextService:
    """Service for managing user context in AI agent sessions."""
    
    def __init__(self):
        """Initialize the context service."""
        self.user_profile_service = user_profile_service
    
    async def inject_user_context(self, session: Session, user_id: str) -> bool:
        """
        Inject user profile context into an agent session.
        
        Args:
            session: ADK session to inject context into
            user_id: User ID to get profile for
            
        Returns:
            True if context was injected successfully
        """
        try:
            # Get user profile
            user_profile = await self.user_profile_service.get_user_profile(user_id)
            if not user_profile:
                logger.warning(f"No user profile found for user_id: {user_id}")
                return False
            
            # Update user's last active timestamp
            await self.user_profile_service.update_last_active(user_id)
            
            # Inject profile into session state
            session.state["user_profile"] = user_profile.model_dump()
            session.state["user_id"] = user_id
            session.state["context_injected"] = True
            session.state["context_timestamp"] = datetime.utcnow().isoformat()
            
            # Create personalized context for agents
            personalized_context = self._create_personalized_context(user_profile)
            session.state["personalized_context"] = personalized_context
            
            logger.info(f"Injected user context for user_id: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error injecting user context for {user_id}: {e}")
            return False
    
    def _create_personalized_context(self, profile: UserProfile) -> Dict[str, Any]:
        """
        Create personalized context data for agents.
        
        Args:
            profile: User profile
            
        Returns:
            Personalized context dictionary
        """
        context = {
            "user_info": {
                "name": profile.basic_info.name,
                "age": profile.basic_info.age,
                "nationality": profile.basic_info.nationality,
                "home_location": profile.basic_info.home_location,
            },
            "accessibility_summary": self._create_accessibility_summary(profile),
            "travel_preferences": self._create_travel_preferences_summary(profile),
            "communication_style": profile.preferences.communication_style,
            "personalized_instructions": self._generate_personalized_instructions(profile),
        }
        
        return context
    
    def _create_accessibility_summary(self, profile: UserProfile) -> Dict[str, Any]:
        """Create accessibility summary for agents."""
        accessibility = profile.accessibility_profile
        
        return {
            "has_mobility_needs": bool(accessibility.mobility_needs),
            "has_sensory_needs": bool(accessibility.sensory_needs),
            "has_cognitive_needs": bool(accessibility.cognitive_needs),
            "mobility_needs": accessibility.mobility_needs,
            "sensory_needs": accessibility.sensory_needs,
            "cognitive_needs": accessibility.cognitive_needs,
            "assistance_preferences": accessibility.assistance_preferences,
            "mobility_aids": accessibility.mobility_aids,
            "accessibility_priorities": accessibility.accessibility_priorities,
            "barrier_concerns": accessibility.barrier_concerns,
            "dietary_restrictions": accessibility.dietary_restrictions,
            "service_animal": accessibility.service_animal,
            "communication_needs": accessibility.communication_needs,
        }
    
    def _create_travel_preferences_summary(self, profile: UserProfile) -> Dict[str, Any]:
        """Create travel preferences summary for agents."""
        interests = profile.travel_interests
        
        return {
            "preferred_destinations": interests.preferred_destinations,
            "travel_styles": interests.travel_style,
            "budget_range": interests.budget_range,
            "group_size_preference": interests.group_size_preference,
            "accommodation_preferences": interests.accommodation_preferences,
            "activity_interests": interests.activity_interests,
            "transportation_preferences": interests.transportation_preferences,
        }
    
    def _generate_personalized_instructions(self, profile: UserProfile) -> Dict[str, str]:
        """
        Generate personalized instructions for each agent type.
        
        Args:
            profile: User profile
            
        Returns:
            Dictionary of agent-specific personalized instructions
        """
        user_info = profile.basic_info
        accessibility = profile.accessibility_profile
        interests = profile.travel_interests
        preferences = profile.preferences
        
        # Base context for all agents
        base_context = f"""
You are helping {user_info.name}, a {user_info.age or 'adult'} traveler from {user_info.home_location}, {user_info.nationality}.

COMMUNICATION STYLE: {preferences.communication_style.value} - Adapt your responses accordingly.
RISK TOLERANCE: {preferences.risk_tolerance.value} - Consider this in recommendations.
"""
        
        # Accessibility context
        accessibility_context = ""
        if accessibility.mobility_needs or accessibility.sensory_needs or accessibility.cognitive_needs:
            accessibility_context = f"""
ACCESSIBILITY NEEDS:
- Mobility: {', '.join(accessibility.mobility_needs) if accessibility.mobility_needs else 'None specified'}
- Sensory: {', '.join(accessibility.sensory_needs) if accessibility.sensory_needs else 'None specified'}
- Cognitive: {', '.join(accessibility.cognitive_needs) if accessibility.cognitive_needs else 'None specified'}
- Mobility Aids: {', '.join(accessibility.mobility_aids) if accessibility.mobility_aids else 'None'}
- Priority Concerns: {', '.join(accessibility.barrier_concerns) if accessibility.barrier_concerns else 'None specified'}

ASSISTANCE PREFERENCES: {accessibility.assistance_preferences}
"""
        
        # Travel preferences context
        travel_context = f"""
TRAVEL PREFERENCES:
- Destinations: {', '.join(interests.preferred_destinations) if interests.preferred_destinations else 'Open to suggestions'}
- Travel Style: {', '.join([style.value for style in interests.travel_style]) if interests.travel_style else 'Flexible'}
- Budget: {interests.budget_range.value}
- Group Size: {interests.group_size_preference}
- Activities: {', '.join(interests.activity_interests) if interests.activity_interests else 'Open to suggestions'}
"""
        
        full_context = base_context + accessibility_context + travel_context
        
        # Agent-specific instructions
        instructions = {
            "root_agent": full_context + """
Route requests to the most appropriate specialized agent based on the user's accessibility needs and travel preferences.
Always prioritize accessibility considerations in your routing decisions.
""",
            
            "inspiration_agent": full_context + """
Focus on destinations and experiences that match both the user's interests and accessibility needs.
Highlight accessibility features and disabled traveler reviews when available.
""",
            
            "planning_agent": full_context + """
Prioritize accessible flights, hotels, and transportation options.
Always consider the user's mobility aids and assistance needs when making recommendations.
Include accessibility features and costs in all suggestions.
""",
            
            "booking_agent": full_context + """
Automatically include all necessary accessibility accommodations in bookings.
Communicate the user's specific needs to service providers.
Ensure all accessibility services are confirmed and documented.
""",
            
            "accessibility_research_agent": full_context + """
Focus your research on the user's specific accessibility needs and concerns.
Prioritize information about barriers they've identified as concerning.
Look for reviews from travelers with similar accessibility profiles.
""",
            
            "mobility_preparation_agent": full_context + """
Focus on the user's specific mobility aids and medical requirements.
Provide detailed guidance for their particular equipment and documentation needs.
Consider their travel style and destinations when making preparation recommendations.
""",
            
            "transit_support_agent": full_context + """
Arrange assistance services that match the user's specific preferences and needs.
Focus on their preferred assistance types and communication methods.
Ensure all arrangements accommodate their mobility aids and requirements.
""",
            
            "barrier_navigation_agent": full_context + """
Prioritize solutions for the barriers the user has identified as most concerning.
Provide alternatives that match their accessibility needs and travel preferences.
Consider their risk tolerance when suggesting workarounds.
""",
        }
        
        return instructions
    
    def get_user_context_from_session(self, session: Session) -> Optional[Dict[str, Any]]:
        """
        Get user context from session state.
        
        Args:
            session: ADK session
            
        Returns:
            User context dictionary or None
        """
        try:
            if session.state.get("context_injected"):
                return {
                    "user_profile": session.state.get("user_profile"),
                    "user_id": session.state.get("user_id"),
                    "personalized_context": session.state.get("personalized_context"),
                    "context_timestamp": session.state.get("context_timestamp"),
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting user context from session: {e}")
            return None
    
    def update_learned_preferences(self, session: Session, preferences: Dict[str, Any]) -> bool:
        """
        Update learned preferences from conversation.
        
        Args:
            session: ADK session
            preferences: New preferences learned from conversation
            
        Returns:
            True if updated successfully
        """
        try:
            user_id = session.state.get("user_id")
            if not user_id:
                return False
            
            # Get current learned preferences
            current_learned = session.state.get("learned_preferences", {})
            current_learned.update(preferences)
            
            # Update session state
            session.state["learned_preferences"] = current_learned
            
            # TODO: Persist to database in background
            logger.info(f"Updated learned preferences for user {user_id}: {preferences}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating learned preferences: {e}")
            return False


# Global service instance
context_service = ContextService()