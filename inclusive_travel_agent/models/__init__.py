"""Models package for the Inclusive Travel Agent."""

from .user_profile import (
    UserProfile,
    BasicInfo,
    TravelInterests,
    AccessibilityProfile,
    UserPreferences,
    CreateUserProfileRequest,
    UpdateUserProfileRequest,
    UserProfileResponse,
    UserProfileSummary,
    TravelStyle,
    BudgetRange,
    CommunicationStyle,
    RiskTolerance,
)

__all__ = [
    "UserProfile",
    "BasicInfo", 
    "TravelInterests",
    "AccessibilityProfile",
    "UserPreferences",
    "CreateUserProfileRequest",
    "UpdateUserProfileRequest",
    "UserProfileResponse",
    "UserProfileSummary",
    "TravelStyle",
    "BudgetRange",
    "CommunicationStyle",
    "RiskTolerance",
]