"""User profile service for Firestore database operations."""

import os
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid

from google.cloud import firestore
from google.cloud.exceptions import NotFound

from inclusive_travel_agent.models.user_profile import (
    UserProfile,
    CreateUserProfileRequest,
    UpdateUserProfileRequest,
    UserProfileSummary,
    BasicInfo,
    TravelInterests,
    AccessibilityProfile,
    UserPreferences,
)


logger = logging.getLogger(__name__)


class UserProfileService:
    """Service for managing user profiles in Firestore."""
    
    def __init__(self):
        """Initialize the Firestore client."""
        self.collection_name = "user_profiles"
        self._memory_store: Dict[str, Dict] = {}
        
        try:
            # Initialize Firestore client
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            if project_id:
                self.db = firestore.Client(project=project_id)
            else:
                # Use default project from environment
                self.db = firestore.Client()
            
            # Test the connection with a simple operation
            # This will fail if Firestore API is not enabled
            test_collection = self.db.collection("_test_connection")
            # Just getting the collection reference doesn't make an API call
            # We'll test the actual connection on first use
            
            logger.info("UserProfileService initialized with Firestore")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firestore client: {e}")
            # Fallback to in-memory storage for development
            self.db = None
            logger.warning("Using in-memory storage as fallback")
    
    def _use_memory_store(self) -> bool:
        """Check if using in-memory storage."""
        return self.db is None
    
    async def create_user_profile(self, request: CreateUserProfileRequest) -> UserProfile:
        """
        Create a new user profile.
        
        Args:
            request: User profile creation request
            
        Returns:
            Created user profile
            
        Raises:
            ValueError: If user already exists or invalid data
        """
        try:
            # Generate unique user ID
            user_id = str(uuid.uuid4())
            
            # Create user profile with defaults
            now = datetime.utcnow()
            
            profile = UserProfile(
                user_id=user_id,
                basic_info=request.basic_info,
                travel_interests=request.travel_interests or TravelInterests(),
                accessibility_profile=request.accessibility_profile or AccessibilityProfile(),
                preferences=request.preferences or UserPreferences(),
                created_at=now,
                updated_at=now,
                profile_complete=self._is_profile_complete(request),
                onboarding_completed=False
            )
            
            # Store in database
            if self._use_memory_store():
                self._memory_store[user_id] = profile.model_dump()
            else:
                try:
                    doc_ref = self.db.collection(self.collection_name).document(user_id)
                    doc_ref.set(profile.model_dump())
                except Exception as firestore_error:
                    logger.warning(f"Firestore operation failed, falling back to memory store: {firestore_error}")
                    # Fall back to memory store
                    self.db = None
                    self._memory_store[user_id] = profile.model_dump()
            
            logger.info(f"Created user profile: {user_id}")
            return profile
            
        except Exception as e:
            logger.error(f"Error creating user profile: {e}")
            raise ValueError(f"Failed to create user profile: {str(e)}")
    
    async def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        Get user profile by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User profile or None if not found
        """
        try:
            if self._use_memory_store():
                profile_data = self._memory_store.get(user_id)
                if profile_data:
                    return UserProfile(**profile_data)
                return None
            else:
                doc_ref = self.db.collection(self.collection_name).document(user_id)
                doc = doc_ref.get()
                
                if doc.exists:
                    profile_data = doc.to_dict()
                    return UserProfile(**profile_data)
                return None
                
        except Exception as e:
            logger.error(f"Error getting user profile {user_id}: {e}")
            return None
    
    async def update_user_profile(self, user_id: str, request: UpdateUserProfileRequest) -> Optional[UserProfile]:
        """
        Update user profile.
        
        Args:
            user_id: User ID
            request: Update request with partial data
            
        Returns:
            Updated user profile or None if not found
        """
        try:
            # Get existing profile
            existing_profile = await self.get_user_profile(user_id)
            if not existing_profile:
                return None
            
            # Update fields that are provided
            update_data = {}
            if request.basic_info:
                update_data["basic_info"] = request.basic_info.model_dump()
            if request.travel_interests:
                update_data["travel_interests"] = request.travel_interests.model_dump()
            if request.accessibility_profile:
                update_data["accessibility_profile"] = request.accessibility_profile.model_dump()
            if request.preferences:
                update_data["preferences"] = request.preferences.model_dump()
            
            # Always update timestamp
            update_data["updated_at"] = datetime.utcnow()
            
            # Check if profile is now complete
            if any([request.basic_info, request.travel_interests, request.accessibility_profile]):
                # Reconstruct profile to check completeness
                updated_profile_data = existing_profile.model_dump()
                updated_profile_data.update(update_data)
                temp_profile = UserProfile(**updated_profile_data)
                update_data["profile_complete"] = self._is_profile_complete_from_profile(temp_profile)
            
            # Update in database
            if self._use_memory_store():
                if user_id in self._memory_store:
                    self._memory_store[user_id].update(update_data)
                    return UserProfile(**self._memory_store[user_id])
            else:
                doc_ref = self.db.collection(self.collection_name).document(user_id)
                doc_ref.update(update_data)
                
                # Get updated profile
                return await self.get_user_profile(user_id)
                
        except Exception as e:
            logger.error(f"Error updating user profile {user_id}: {e}")
            return None
    
    async def delete_user_profile(self, user_id: str) -> bool:
        """
        Delete user profile.
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            if self._use_memory_store():
                if user_id in self._memory_store:
                    del self._memory_store[user_id]
                    logger.info(f"Deleted user profile: {user_id}")
                    return True
                return False
            else:
                doc_ref = self.db.collection(self.collection_name).document(user_id)
                doc = doc_ref.get()
                
                if doc.exists:
                    doc_ref.delete()
                    logger.info(f"Deleted user profile: {user_id}")
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Error deleting user profile {user_id}: {e}")
            return False
    
    async def list_user_profiles(self, limit: int = 50, offset: int = 0) -> List[UserProfileSummary]:
        """
        List user profiles with pagination.
        
        Args:
            limit: Maximum number of profiles to return
            offset: Number of profiles to skip
            
        Returns:
            List of user profile summaries
        """
        try:
            profiles = []
            
            if self._use_memory_store():
                all_profiles = list(self._memory_store.values())
                paginated_profiles = all_profiles[offset:offset + limit]
                
                for profile_data in paginated_profiles:
                    profile = UserProfile(**profile_data)
                    summary = self._create_profile_summary(profile)
                    profiles.append(summary)
            else:
                query = self.db.collection(self.collection_name).order_by("created_at").offset(offset).limit(limit)
                docs = query.stream()
                
                for doc in docs:
                    profile_data = doc.to_dict()
                    profile = UserProfile(**profile_data)
                    summary = self._create_profile_summary(profile)
                    profiles.append(summary)
            
            return profiles
            
        except Exception as e:
            logger.error(f"Error listing user profiles: {e}")
            return []
    
    async def update_last_active(self, user_id: str) -> bool:
        """
        Update user's last active timestamp.
        
        Args:
            user_id: User ID
            
        Returns:
            True if updated successfully
        """
        try:
            update_data = {"last_active": datetime.utcnow()}
            
            if self._use_memory_store():
                if user_id in self._memory_store:
                    self._memory_store[user_id].update(update_data)
                    return True
                return False
            else:
                doc_ref = self.db.collection(self.collection_name).document(user_id)
                doc_ref.update(update_data)
                return True
                
        except Exception as e:
            logger.error(f"Error updating last active for {user_id}: {e}")
            return False
    
    def _is_profile_complete(self, request: CreateUserProfileRequest) -> bool:
        """Check if profile creation request has minimum required fields."""
        if not request.basic_info:
            return False
        
        # Basic info is required
        basic_complete = bool(
            request.basic_info.name and 
            request.basic_info.email and 
            request.basic_info.nationality and 
            request.basic_info.home_location
        )
        
        # At least some travel interests or accessibility info
        interests_complete = bool(
            request.travel_interests and 
            (request.travel_interests.preferred_destinations or 
             request.travel_interests.travel_style or
             request.travel_interests.activity_interests)
        )
        
        accessibility_complete = bool(
            request.accessibility_profile and
            (request.accessibility_profile.mobility_needs or
             request.accessibility_profile.sensory_needs or
             request.accessibility_profile.assistance_preferences)
        )
        
        return basic_complete and (interests_complete or accessibility_complete)
    
    def _is_profile_complete_from_profile(self, profile: UserProfile) -> bool:
        """Check if existing profile is complete."""
        # Basic info is required
        basic_complete = bool(
            profile.basic_info.name and 
            profile.basic_info.email and 
            profile.basic_info.nationality and 
            profile.basic_info.home_location
        )
        
        # At least some travel interests or accessibility info
        interests_complete = bool(
            profile.travel_interests.preferred_destinations or 
            profile.travel_interests.travel_style or
            profile.travel_interests.activity_interests
        )
        
        accessibility_complete = bool(
            profile.accessibility_profile.mobility_needs or
            profile.accessibility_profile.sensory_needs or
            profile.accessibility_profile.assistance_preferences
        )
        
        return basic_complete and (interests_complete or accessibility_complete)
    
    def _create_profile_summary(self, profile: UserProfile) -> UserProfileSummary:
        """Create a summary of the user profile."""
        return UserProfileSummary(
            user_id=profile.user_id,
            name=profile.basic_info.name,
            email=profile.basic_info.email,
            created_at=profile.created_at,
            last_active=profile.last_active,
            profile_complete=profile.profile_complete,
            accessibility_needs_count=len(
                profile.accessibility_profile.mobility_needs +
                profile.accessibility_profile.sensory_needs +
                profile.accessibility_profile.cognitive_needs
            ),
            travel_interests_count=len(
                profile.travel_interests.preferred_destinations +
                profile.travel_interests.activity_interests +
                profile.travel_interests.accommodation_preferences
            )
        )


# Global service instance
user_profile_service = UserProfileService()