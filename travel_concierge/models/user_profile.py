"""User profile models for the Inclusive Travel Agent."""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class TravelStyle(str, Enum):
    """Travel style preferences."""
    CULTURAL = "cultural"
    ADVENTURE = "adventure"
    RELAXATION = "relaxation"
    BUSINESS = "business"
    FAMILY = "family"
    SOLO = "solo"
    ACCESSIBLE = "accessible"


class BudgetRange(str, Enum):
    """Budget range preferences."""
    BUDGET = "budget"
    MID_RANGE = "mid-range"
    LUXURY = "luxury"
    FLEXIBLE = "flexible"


class CommunicationStyle(str, Enum):
    """Communication style preferences."""
    BRIEF = "brief"
    DETAILED = "detailed"
    CONVERSATIONAL = "conversational"
    PROFESSIONAL = "professional"


class RiskTolerance(str, Enum):
    """Risk tolerance levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class BasicInfo(BaseModel):
    """Basic user information."""
    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")
    age: Optional[int] = Field(None, description="User's age")
    nationality: str = Field(..., description="User's nationality/passport country")
    home_location: str = Field(..., description="User's home city/location")
    phone: Optional[str] = Field(None, description="User's phone number")
    emergency_contact: Optional[Dict[str, str]] = Field(None, description="Emergency contact information")


class TravelInterests(BaseModel):
    """User's travel interests and preferences."""
    preferred_destinations: List[str] = Field(default_factory=list, description="Preferred destination types or regions")
    travel_style: List[TravelStyle] = Field(default_factory=list, description="Preferred travel styles")
    budget_range: BudgetRange = Field(BudgetRange.MID_RANGE, description="Preferred budget range")
    group_size_preference: str = Field("flexible", description="Preferred group size (solo, couple, family, etc.)")
    accommodation_preferences: List[str] = Field(default_factory=list, description="Hotel, Airbnb, accessible, etc.")
    activity_interests: List[str] = Field(default_factory=list, description="Museums, outdoor, food, etc.")
    transportation_preferences: List[str] = Field(default_factory=list, description="Flight, train, accessible transport")


class AccessibilityProfile(BaseModel):
    """Comprehensive accessibility profile."""
    mobility_needs: List[str] = Field(default_factory=list, description="Wheelchair accessible, step-free access, etc.")
    sensory_needs: List[str] = Field(default_factory=list, description="Hearing assistance, visual assistance, etc.")
    cognitive_needs: List[str] = Field(default_factory=list, description="Clear signage, quiet spaces, etc.")
    
    assistance_preferences: Dict[str, str] = Field(default_factory=dict, description="Assistance preferences by context")
    mobility_aids: List[str] = Field(default_factory=list, description="Wheelchair, walker, cane, etc.")
    medical_conditions: List[str] = Field(default_factory=list, description="Relevant medical conditions")
    
    dietary_restrictions: List[str] = Field(default_factory=list, description="Food allergies, dietary needs")
    medication_requirements: List[str] = Field(default_factory=list, description="Travel medication needs")
    
    accessibility_priorities: List[str] = Field(default_factory=list, description="Most important accessibility features")
    barrier_concerns: List[str] = Field(default_factory=list, description="Specific barriers to avoid")
    
    service_animal: Optional[Dict[str, str]] = Field(None, description="Service animal information")
    communication_needs: List[str] = Field(default_factory=list, description="Sign language, written communication, etc.")


class UserPreferences(BaseModel):
    """User's general preferences and settings."""
    communication_style: CommunicationStyle = Field(CommunicationStyle.DETAILED, description="Preferred communication style")
    risk_tolerance: RiskTolerance = Field(RiskTolerance.MEDIUM, description="Risk tolerance for travel")
    planning_horizon: str = Field("1_month", description="How far in advance to plan")
    
    notification_preferences: Dict[str, bool] = Field(default_factory=dict, description="Notification settings")
    privacy_settings: Dict[str, bool] = Field(default_factory=dict, description="Privacy preferences")
    
    language_preferences: List[str] = Field(default_factory=list, description="Preferred languages")
    currency_preference: str = Field("USD", description="Preferred currency")
    timezone: str = Field("UTC", description="User's timezone")


class UserProfile(BaseModel):
    """Complete user profile."""
    user_id: str = Field(..., description="Unique user identifier")
    basic_info: BasicInfo
    travel_interests: TravelInterests
    accessibility_profile: AccessibilityProfile
    preferences: UserPreferences
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: Optional[datetime] = Field(None, description="Last activity timestamp")
    
    # Profile completeness and validation
    profile_complete: bool = Field(False, description="Whether profile is complete")
    onboarding_completed: bool = Field(False, description="Whether onboarding is finished")
    
    # Travel history and preferences learned from interactions
    travel_history: List[Dict[str, Any]] = Field(default_factory=list, description="Past trips and experiences")
    learned_preferences: Dict[str, Any] = Field(default_factory=dict, description="Preferences learned from conversations")


class CreateUserProfileRequest(BaseModel):
    """Request model for creating a user profile."""
    basic_info: BasicInfo
    travel_interests: Optional[TravelInterests] = None
    accessibility_profile: Optional[AccessibilityProfile] = None
    preferences: Optional[UserPreferences] = None


class UpdateUserProfileRequest(BaseModel):
    """Request model for updating a user profile."""
    basic_info: Optional[BasicInfo] = None
    travel_interests: Optional[TravelInterests] = None
    accessibility_profile: Optional[AccessibilityProfile] = None
    preferences: Optional[UserPreferences] = None


class UserProfileResponse(BaseModel):
    """Response model for user profile operations."""
    user_id: str
    profile: UserProfile
    message: str = "Success"


class UserProfileSummary(BaseModel):
    """Summary of user profile for listings."""
    user_id: str
    name: str
    email: str
    created_at: datetime
    last_active: Optional[datetime]
    profile_complete: bool
    accessibility_needs_count: int
    travel_interests_count: int