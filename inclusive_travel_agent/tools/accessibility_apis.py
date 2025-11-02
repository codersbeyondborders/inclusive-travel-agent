

"""External API integrations for accessibility information."""

import os
import requests
from typing import Dict, List, Any, Optional
from google.adk.tools import ToolContext


class AccessibilityAPIService:
    """Service for integrating with accessibility-focused APIs."""

    def __init__(self):
        self.wheelmap_api_key = os.getenv("WHEELMAP_API_KEY")
        self.accessiblego_api_key = os.getenv("ACCESSIBLEGO_API_KEY")

    def search_wheelmap_accessibility(self, location: str, venue_type: str = "restaurant") -> Dict[str, Any]:
        """
        Search Wheelmap.org for accessibility information about venues.
        
        Args:
            location: Location to search (city, address, etc.)
            venue_type: Type of venue (restaurant, hotel, attraction, etc.)
            
        Returns:
            Dictionary with accessibility information
        """
        try:
            # Wheelmap API endpoint (using their public API)
            base_url = "https://wheelmap.org/api/nodes"
            
            params = {
                "api_key": self.wheelmap_api_key,
                "q": location,
                "category": venue_type,
                "wheelchair": "yes",  # Filter for wheelchair accessible venues
                "limit": 10
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = requests.get(base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "venues": self._format_wheelmap_results(data.get("nodes", [])),
                    "source": "Wheelmap.org"
                }
            else:
                return {
                    "success": False,
                    "error": f"Wheelmap API error: {response.status_code}",
                    "fallback_message": "Using general accessibility guidelines"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Wheelmap API connection error: {str(e)}",
                "fallback_message": "Using general accessibility guidelines"
            }

    def _format_wheelmap_results(self, nodes: List[Dict]) -> List[Dict]:
        """Format Wheelmap API results into our standard format."""
        formatted_venues = []
        
        for node in nodes:
            venue = {
                "name": node.get("name", "Unknown Venue"),
                "address": node.get("street", ""),
                "wheelchair_accessible": node.get("wheelchair") == "yes",
                "accessibility_rating": self._convert_wheelmap_rating(node.get("wheelchair")),
                "latitude": node.get("lat"),
                "longitude": node.get("lon"),
                "venue_type": node.get("category", {}).get("identifier", "unknown"),
                "accessibility_notes": self._get_wheelmap_notes(node.get("wheelchair")),
                "source": "Wheelmap.org",
                "last_updated": node.get("updated_at")
            }
            formatted_venues.append(venue)
            
        return formatted_venues

    def _convert_wheelmap_rating(self, wheelchair_status: str) -> float:
        """Convert Wheelmap wheelchair status to numerical rating."""
        rating_map = {
            "yes": 5.0,
            "limited": 3.0,
            "no": 1.0,
            "unknown": 2.5
        }
        return rating_map.get(wheelchair_status, 2.5)

    def _get_wheelmap_notes(self, wheelchair_status: str) -> str:
        """Get accessibility notes based on Wheelmap status."""
        notes_map = {
            "yes": "Fully wheelchair accessible entrance and facilities",
            "limited": "Limited wheelchair accessibility - may have some barriers",
            "no": "Not wheelchair accessible - significant barriers present",
            "unknown": "Accessibility status not verified - contact venue directly"
        }
        return notes_map.get(wheelchair_status, "Accessibility information not available")

    def get_airport_accessibility_info(self, airport_code: str) -> Dict[str, Any]:
        """
        Get accessibility information for airports.
        
        Args:
            airport_code: IATA airport code (e.g., 'LAX', 'JFK')
            
        Returns:
            Dictionary with airport accessibility information
        """
        # This would integrate with airport accessibility APIs or databases
        # For now, providing structured fallback information
        
        airport_accessibility_db = {
            "LAX": {
                "name": "Los Angeles International Airport",
                "wheelchair_accessible": True,
                "accessibility_services": [
                    "Wheelchair assistance available",
                    "Accessible restrooms throughout",
                    "TTY phones available",
                    "Service animal relief areas",
                    "Accessible parking spaces"
                ],
                "assistance_phone": "+1-855-463-5252",
                "accessibility_rating": 4.5,
                "notes": "Comprehensive accessibility services available 24/7"
            },
            "JFK": {
                "name": "John F. Kennedy International Airport",
                "wheelchair_accessible": True,
                "accessibility_services": [
                    "Wheelchair and mobility assistance",
                    "Accessible transportation between terminals",
                    "Braille and large print materials",
                    "Hearing loop systems",
                    "Accessible hotel shuttles"
                ],
                "assistance_phone": "+1-718-244-4444",
                "accessibility_rating": 4.3,
                "notes": "Full accessibility compliance with additional services"
            },
            "SFO": {
                "name": "San Francisco International Airport", 
                "wheelchair_accessible": True,
                "accessibility_services": [
                    "Comprehensive wheelchair assistance",
                    "Accessible BART connection",
                    "Audio announcements",
                    "Accessible rental car facilities",
                    "Service animal facilities"
                ],
                "assistance_phone": "+1-650-821-7014",
                "accessibility_rating": 4.7,
                "notes": "Award-winning accessibility program"
            }
        }
        
        return airport_accessibility_db.get(airport_code.upper(), {
            "name": f"Airport {airport_code}",
            "wheelchair_accessible": True,
            "accessibility_services": ["Standard accessibility services available"],
            "assistance_phone": "Contact airport directly",
            "accessibility_rating": 3.5,
            "notes": "Contact airport for specific accessibility information"
        })


# Tool functions for ADK integration
accessibility_api_service = AccessibilityAPIService()


def search_accessible_venues(location: str, venue_type: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Search for accessible venues in a specific location.
    
    Args:
        location: Location to search (city, address, etc.)
        venue_type: Type of venue (restaurant, hotel, attraction, etc.)
        tool_context: ADK tool context
        
    Returns:
        Dictionary with accessible venue information
    """
    result = accessibility_api_service.search_wheelmap_accessibility(location, venue_type)
    
    # Store results in session state for later use
    if result["success"]:
        key = f"accessible_venues_{location}_{venue_type}"
        tool_context.state[key] = result["venues"]
    
    return result


def get_airport_accessibility(airport_code: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Get accessibility information for a specific airport.
    
    Args:
        airport_code: IATA airport code (e.g., 'LAX', 'JFK')
        tool_context: ADK tool context
        
    Returns:
        Dictionary with airport accessibility information
    """
    result = accessibility_api_service.get_airport_accessibility_info(airport_code)
    
    # Store airport accessibility info in session state
    key = f"airport_accessibility_{airport_code}"
    tool_context.state[key] = result
    
    return result


def search_accessible_routes(origin: str, destination: str, transport_mode: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Search for accessible transportation routes between locations.
    
    Args:
        origin: Starting location
        destination: Destination location  
        transport_mode: Mode of transport (public_transit, walking, driving)
        tool_context: ADK tool context
        
    Returns:
        Dictionary with accessible route information
    """
    # This would integrate with accessible route planning APIs
    # For now, providing structured guidance
    
    route_guidance = {
        "public_transit": {
            "accessibility_features": [
                "Look for wheelchair accessible stations",
                "Check for elevator availability",
                "Verify accessible vehicle announcements",
                "Confirm priority seating availability"
            ],
            "recommended_apps": ["Citymapper", "Transit", "Google Maps"],
            "notes": "Contact local transit authority for real-time accessibility status"
        },
        "walking": {
            "accessibility_features": [
                "Identify step-free routes",
                "Check sidewalk conditions",
                "Locate accessible crossings",
                "Find rest areas and accessible restrooms"
            ],
            "recommended_apps": ["AccessMap", "Wheelmap", "Google Maps"],
            "notes": "Use accessibility-focused navigation apps for best routes"
        },
        "driving": {
            "accessibility_features": [
                "Locate accessible parking spaces",
                "Check for curb cuts and ramps",
                "Verify accessible building entrances",
                "Identify accessible gas stations"
            ],
            "recommended_apps": ["SpotHero", "ParkWhiz", "Wheelmap"],
            "notes": "Reserve accessible parking in advance when possible"
        }
    }
    
    result = {
        "origin": origin,
        "destination": destination,
        "transport_mode": transport_mode,
        "accessibility_guidance": route_guidance.get(transport_mode, route_guidance["walking"]),
        "general_tips": [
            "Allow extra time for accessibility needs",
            "Have backup transportation options",
            "Contact venues in advance to confirm accessibility",
            "Keep emergency contact information handy"
        ]
    }
    
    # Store route guidance in session state
    key = f"accessible_routes_{origin}_{destination}_{transport_mode}"
    tool_context.state[key] = result
    
    return result