

"""Common data schema and types for inclusive travel agent."""

from typing import Optional, Union, List, Dict

from google.genai import types
from pydantic import BaseModel, Field


# Convenient declaration for controlled generation.
json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)


# Accessibility-related data models (defined first for forward references)
class AccessibilityReview(BaseModel):
    """A review from a disabled traveler about accessibility."""
    reviewer_disability_type: str = Field(description="Type of disability of the reviewer")
    rating: float = Field(description="Accessibility rating from 1-5")
    review_text: str = Field(description="Detailed review text")
    helpful_tips: Optional[str] = Field(description="Specific accessibility tips")
    date: Optional[str] = Field(description="Review date")


class AccessibilityInfo(BaseModel):
    """Accessibility information for venues, transport, or activities."""
    wheelchair_accessible: bool = Field(description="Wheelchair accessibility available")
    hearing_assistance: bool = Field(description="Hearing assistance/loop systems available")
    visual_assistance: bool = Field(description="Visual assistance/braille/audio guides available")
    mobility_aid_friendly: bool = Field(description="Friendly to mobility aids (walkers, canes, etc.)")
    accessible_parking: bool = Field(description="Accessible parking available")
    accessible_restrooms: bool = Field(description="Accessible restroom facilities")
    elevator_access: bool = Field(description="Elevator access available")
    step_free_access: bool = Field(description="Step-free access available")
    accessibility_rating: float = Field(description="Overall accessibility rating 1-5")
    accessibility_notes: Optional[str] = Field(description="Additional accessibility notes")
    user_reviews: List[AccessibilityReview] = Field(default=[], description="Reviews from disabled travelers")


class DisabilityExpense(BaseModel):
    """Additional expenses related to disability needs."""
    expense_type: str = Field(description="Type of expense (assistance, equipment, etc.)")
    amount_usd: float = Field(description="Cost in USD")
    description: str = Field(description="Description of the expense")
    is_mandatory: bool = Field(description="Whether this expense is mandatory or optional")


class Room(BaseModel):
    """A room for selection."""
    is_available: bool = Field(
        description="Whether the room type is available for selection."
    )
    price_in_usd: int = Field(description="The cost of the room selection.")
    room_type: str = Field(
        description="Type of room, e.g. Twin with Balcon, King with Ocean View... etc."
    )


class RoomsSelection(BaseModel):
    """A list of rooms for selection."""
    rooms: list[Room]


class Hotel(BaseModel):
    """A hotel from the search."""
    name: str = Field(description="Name of the hotel")
    address: str = Field(description="Full address of the Hotel")
    check_in_time: str = Field(description="Time in HH:MM format, e.g. 16:00")
    check_out_time: str = Field(description="Time in HH:MM format, e.g. 15:30")
    thumbnail: str = Field(description="Hotel logo location")
    price: int = Field(description="Price of the room per night")
    accessibility_info: Optional[AccessibilityInfo] = Field(description="Hotel accessibility information")
    accessible_rooms_available: bool = Field(default=False, description="Accessible rooms available")
    accessibility_services: List[str] = Field(default=[], description="Available accessibility services")
    disability_additional_costs: List[DisabilityExpense] = Field(default=[], description="Additional costs for disability needs")


class HotelsSelection(BaseModel):
    """A list of hotels from the search."""
    hotels: list[Hotel]


class Seat(BaseModel):
    """A Seat from the search."""
    is_available: bool = Field(
        description="Whether the seat is available for selection."
    )
    price_in_usd: int = Field(description="The cost of the seat selection.")
    seat_number: str = Field(description="Seat number, e.g. 22A, 34F... etc.")


class SeatsSelection(BaseModel):
    """A list of seats from the search."""
    seats: list[list[Seat]]


class AirportEvent(BaseModel):
    """An Airport event."""
    city_name: str = Field(description="Name of the departure city")
    airport_code: str = Field(description="IATA code of the departure airport")
    timestamp: str = Field(description="ISO 8601 departure or arrival date and time")


class Flight(BaseModel):
    """A Flight search result."""
    flight_number: str = Field(
        description="Unique identifier for the flight, like BA123, AA31, etc."
    )
    departure: AirportEvent
    arrival: AirportEvent
    airlines: list[str] = Field(
        description="Airline names, e.g., American Airlines, Emirates"
    )
    airline_logo: str = Field(description="Airline logo location")
    price_in_usd: int = Field(description="Flight price in US dollars")
    number_of_stops: int = Field(description="Number of stops during the flight")
    accessibility_services: List[str] = Field(default=[], description="Available accessibility services")
    wheelchair_assistance: bool = Field(default=False, description="Wheelchair assistance available")
    priority_boarding: bool = Field(default=False, description="Priority boarding for disabled passengers")
    accessible_seating: bool = Field(default=False, description="Accessible seating options available")
    disability_additional_costs: List[DisabilityExpense] = Field(default=[], description="Additional costs for disability services")


class FlightsSelection(BaseModel):
    """A list of flights from the search."""
    flights: list[Flight]


class Destination(BaseModel):
    """A destination recommendation."""
    name: str = Field(description="A Destination's Name")
    country: str = Field(description="The Destination's Country Name")
    image: str = Field(description="verified URL to an image of the destination")
    highlights: str = Field(description="Short description highlighting key features")
    rating: str = Field(description="Numerical rating (e.g., 4.5)")
    accessibility_info: Optional[AccessibilityInfo] = Field(description="Accessibility information for the destination")
    disability_friendly_score: Optional[float] = Field(description="Overall disability-friendly score 1-5")
    accessible_attractions: List[str] = Field(default=[], description="List of accessible attractions")


class DestinationIdeas(BaseModel):
    """Destinations recommendation."""
    places: list[Destination]


class POI(BaseModel):
    """A Point Of Interest suggested by the agent."""
    place_name: str = Field(description="Name of the attraction")
    address: str = Field(
        description="An address or sufficient information to geocode for a Lat/Lon"
    )
    lat: str = Field(
        description="Numerical representation of Latitude of the location (e.g., 20.6843)"
    )
    long: str = Field(
        description="Numerical representation of Longitude of the location (e.g., -88.5678)"
    )
    review_ratings: str = Field(
        description="Numerical representation of rating (e.g. 4.8 , 3.0 , 1.0 etc)"
    )
    highlights: str = Field(description="Short description highlighting key features")
    image_url: str = Field(description="verified URL to an image of the destination")
    map_url: Optional[str] = Field(description="Verified URL to Google Map")
    place_id: Optional[str] = Field(description="Google Map place_id")
    accessibility_info: Optional[AccessibilityInfo] = Field(description="Accessibility information for this POI")
    accessibility_features: List[str] = Field(default=[], description="Specific accessibility features available")
    barrier_warnings: List[str] = Field(default=[], description="Potential accessibility barriers to be aware of")


class POISuggestions(BaseModel):
    """Points of interest recommendation."""
    places: list[POI]


class AttractionEvent(BaseModel):
    """An Attraction."""
    event_type: str = Field(default="visit")
    description: str = Field(
        description="A title or description of the activity or the attraction visit"
    )
    address: str = Field(description="Full address of the attraction")
    start_time: str = Field(description="Time in HH:MM format, e.g. 16:00")
    end_time: str = Field(description="Time in HH:MM format, e.g. 16:00")
    booking_required: bool = Field(default=False)
    price: Optional[str] = Field(description="Some events may cost money")


class FlightEvent(BaseModel):
    """A Flight Segment in the itinerary."""
    event_type: str = Field(default="flight")
    description: str = Field(description="A title or description of the Flight")
    booking_required: bool = Field(default=True)
    departure_airport: str = Field(description="Airport code, i.e. SEA")
    arrival_airport: str = Field(description="Airport code, i.e. SAN")
    flight_number: str = Field(description="Flight number, e.g. UA5678")
    boarding_time: str = Field(description="Time in HH:MM format, e.g. 15:30")
    seat_number: str = Field(description="Seat Row and Position, e.g. 32A")
    departure_time: str = Field(description="Time in HH:MM format, e.g. 16:00")
    arrival_time: str = Field(description="Time in HH:MM format, e.g. 20:00")
    price: Optional[str] = Field(description="Total air fare")
    booking_id: Optional[str] = Field(
        description="Booking Reference ID, e.g LMN-012-STU"
    )


class HotelEvent(BaseModel):
    """A Hotel Booking in the itinerary."""
    event_type: str = Field(default="hotel")
    description: str = Field(description="A name, title or a description of the hotel")
    address: str = Field(description="Full address of the attraction")
    check_in_time: str = Field(description="Time in HH:MM format, e.g. 16:00")
    check_out_time: str = Field(description="Time in HH:MM format, e.g. 15:30")
    room_selection: str = Field()
    booking_required: bool = Field(default=True)
    price: Optional[str] = Field(description="Total hotel price including all nights")
    booking_id: Optional[str] = Field(
        description="Booking Reference ID, e.g ABCD12345678"
    )


class ItineraryDay(BaseModel):
    """A single day of events in the itinerary."""
    day_number: int = Field(
        description="Identify which day of the trip this represents, e.g. 1, 2, 3... etc."
    )
    date: str = Field(description="The Date this day YYYY-MM-DD format")
    events: list[Union[FlightEvent, HotelEvent, AttractionEvent]] = Field(
        default=[], description="The list of events for the day"
    )


class Itinerary(BaseModel):
    """A multi-day itinerary."""
    trip_name: str = Field(
        description="Simple one liner to describe the trip. e.g. 'San Diego to Seattle Getaway'"
    )
    start_date: str = Field(description="Trip Start Date in YYYY-MM-DD format")
    end_date: str = Field(description="Trip End Date in YYYY-MM-DD format")
    origin: str = Field(description="Trip Origin, e.g. San Diego")
    destination: str = (Field(description="Trip Destination, e.g. Seattle"),)
    days: list[ItineraryDay] = Field(
        default_factory=list, description="The multi-days itinerary"
    )


class UserProfile(BaseModel):
    """An example user profile."""
    allergies: list[str] = Field(
        default=[], description="A list of food allergies to avoid"
    )
    diet_preference: list[str] = Field(
        default=[], description="Vegetarian, Vegan... etc."
    )
    passport_nationality: str = Field(
        description="Nationality of traveler, e.g. US Citizen"
    )
    home_address: str = Field(description="Home address of traveler")
    home_transit_preference: str = Field(
        description="Preferred mode of transport around home, e.g. drive"
    )


class AccessibilityNeeds(BaseModel):
    """User's specific accessibility requirements."""
    mobility_needs: List[str] = Field(default=[], description="Mobility requirements (wheelchair, walker, etc.)")
    sensory_needs: List[str] = Field(default=[], description="Sensory requirements (hearing, visual assistance)")
    cognitive_needs: List[str] = Field(default=[], description="Cognitive assistance needs")
    medical_needs: List[str] = Field(default=[], description="Medical requirements during travel")
    assistance_preferences: Dict[str, str] = Field(default={}, description="Preferred types of assistance")
    mobility_aids: List[str] = Field(default=[], description="Mobility aids used (wheelchair, cane, etc.)")


class AccessibleUserProfile(BaseModel):
    """Enhanced user profile with accessibility information."""
    allergies: List[str] = Field(default=[], description="A list of food allergies to avoid")
    diet_preference: List[str] = Field(default=[], description="Vegetarian, Vegan... etc.")
    passport_nationality: str = Field(description="Nationality of traveler, e.g. US Citizen")
    home_address: str = Field(description="Home address of traveler")
    home_transit_preference: str = Field(description="Preferred mode of transport around home, e.g. drive")
    accessibility_needs: AccessibilityNeeds = Field(default_factory=AccessibilityNeeds, description="Accessibility requirements")
    emergency_contacts: List[Dict[str, str]] = Field(default=[], description="Emergency contacts with accessibility awareness")
    medical_documents: List[str] = Field(default=[], description="Required medical documentation for travel")


class PackingList(BaseModel):
    """A list of things to pack for the trip."""
    items: list[str]
