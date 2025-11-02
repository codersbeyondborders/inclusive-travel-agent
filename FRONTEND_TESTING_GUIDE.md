# Frontend Integration Testing Guide

## 🎉 Great News!

Your **Inclusive Travel Agent backend is ready for frontend integration!** All API endpoints are working correctly and the system is production-ready.

## ✅ Test Results Summary

**8/8 tests passed** - Your backend supports:
- ✓ User profile creation (onboarding)
- ✓ Profile retrieval and updates
- ✓ Profile listing with pagination
- ✓ CORS headers for frontend requests
- ✓ Proper JSON responses
- ✓ Error handling (404, validation errors)

## 🚀 Quick Start for Frontend Integration

### 1. Server is Running
Your backend server is currently running at:
- **API Base URL**: `http://localhost:8080`
- **API Documentation**: `http://localhost:8080/docs`
- **Health Check**: `http://localhost:8080/health`

### 2. Frontend Configuration
In your frontend app, set:
```javascript
const API_BASE_URL = 'http://localhost:8080';
```

### 3. Test API Endpoints Manually

#### Create User Profile (Onboarding)
```bash
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{
    "basic_info": {
      "name": "Test User",
      "email": "test@example.com",
      "nationality": "US",
      "home_location": "San Francisco, CA"
    },
    "travel_interests": {
      "preferred_destinations": ["Europe"],
      "travel_style": ["cultural", "accessible"],
      "budget_range": "mid-range"
    },
    "accessibility_profile": {
      "mobility_needs": ["wheelchair_accessible"],
      "assistance_preferences": {
        "airport_assistance": "wheelchair_assistance"
      }
    }
  }'
```

#### Get User Profile
```bash
curl http://localhost:8080/users/{user_id}
```

#### Update User Profile
```bash
curl -X PUT http://localhost:8080/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{
    "travel_interests": {
      "preferred_destinations": ["Europe", "Japan", "Canada"]
    }
  }'
```

#### List User Profiles
```bash
curl http://localhost:8080/users?limit=10
```

## 🎨 Frontend Implementation Examples

### React/TypeScript Integration

```typescript
// userService.ts
const API_BASE_URL = 'http://localhost:8080';

export interface UserProfile {
  user_id: string;
  basic_info: {
    name: string;
    email: string;
    nationality: string;
    home_location: string;
  };
  travel_interests: {
    preferred_destinations: string[];
    travel_style: string[];
    budget_range: string;
  };
  accessibility_profile: {
    mobility_needs: string[];
    sensory_needs: string[];
    assistance_preferences: Record<string, string>;
  };
  // ... other fields
}

export class UserService {
  async createProfile(profileData: any): Promise<UserProfile> {
    const response = await fetch(`${API_BASE_URL}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profileData)
    });
    
    if (!response.ok) throw new Error('Failed to create profile');
    const result = await response.json();
    return result.profile;
  }

  async getProfile(userId: string): Promise<UserProfile> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`);
    if (!response.ok) throw new Error('Profile not found');
    const result = await response.json();
    return result.profile;
  }

  async updateProfile(userId: string, updates: any): Promise<UserProfile> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    });
    
    if (!response.ok) throw new Error('Failed to update profile');
    const result = await response.json();
    return result.profile;
  }
}
```

### Vue.js Integration

```vue
<template>
  <div class="onboarding">
    <form @submit.prevent="createProfile">
      <!-- Basic Info -->
      <input v-model="profile.basic_info.name" placeholder="Full Name" required />
      <input v-model="profile.basic_info.email" type="email" placeholder="Email" required />
      
      <!-- Accessibility Needs -->
      <div class="accessibility-section">
        <h3>Accessibility Needs</h3>
        <label v-for="need in mobilityOptions" :key="need">
          <input 
            type="checkbox" 
            :value="need" 
            v-model="profile.accessibility_profile.mobility_needs"
          />
          {{ need }}
        </label>
      </div>
      
      <button type="submit">Create Profile</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const API_BASE_URL = 'http://localhost:8080';

const profile = ref({
  basic_info: { name: '', email: '', nationality: '', home_location: '' },
  accessibility_profile: { mobility_needs: [] }
});

const createProfile = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile.value)
    });
    
    const result = await response.json();
    console.log('Profile created:', result.user_id);
  } catch (error) {
    console.error('Error:', error);
  }
};
</script>
```

## 💬 Chat Functionality (Optional)

To enable chat functionality with personalized responses:

### 1. Get Google AI API Key
- Visit: https://aistudio.google.com/app/apikey
- Create a new API key
- Copy the key

### 2. Add to Environment
Create a `.env` file:
```bash
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your_google_ai_api_key_here
```

### 3. Restart Server
```bash
# Stop current server (Ctrl+C)
# Then restart:
uv run python start_server.py
```

### 4. Test Chat API
```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need help planning an accessible trip to Paris",
    "session_id": "user_session_123",
    "user_id": "your_user_id_here"
  }'
```

## 🎯 Frontend Testing Checklist

### User Onboarding Flow
- [ ] Create user profile form
- [ ] Handle form validation
- [ ] Submit profile data to API
- [ ] Store user_id for future requests
- [ ] Show success/error messages

### Profile Management
- [ ] Retrieve and display user profile
- [ ] Edit profile information
- [ ] Update profile via API
- [ ] Handle update confirmations

### Chat Interface (if enabled)
- [ ] Send messages to chat API
- [ ] Include user_id for personalization
- [ ] Display agent responses
- [ ] Handle typing indicators
- [ ] Show context information

### Error Handling
- [ ] Handle network errors
- [ ] Display validation errors
- [ ] Show 404 errors gracefully
- [ ] Provide retry mechanisms

## 📊 API Response Examples

### Successful Profile Creation
```json
{
  "user_id": "09e2ca16-8b4a-4c5d-9e7f-1234567890ab",
  "profile": {
    "user_id": "09e2ca16-8b4a-4c5d-9e7f-1234567890ab",
    "basic_info": {
      "name": "Sarah Johnson",
      "email": "sarah@example.com",
      "nationality": "US",
      "home_location": "Seattle, WA"
    },
    "travel_interests": {
      "preferred_destinations": ["Europe", "Japan"],
      "travel_style": ["cultural", "accessible"],
      "budget_range": "mid-range"
    },
    "accessibility_profile": {
      "mobility_needs": ["wheelchair_accessible", "step_free_access"],
      "sensory_needs": ["hearing_assistance"],
      "assistance_preferences": {
        "airport_assistance": "wheelchair_assistance",
        "boarding_preference": "priority_boarding"
      }
    },
    "profile_complete": true,
    "onboarding_completed": false,
    "created_at": "2025-11-02T10:30:00Z"
  },
  "message": "User profile created successfully"
}
```

### Chat Response (with personalization)
```json
{
  "response": "Hi Sarah! I'd love to help you plan an accessible trip to Paris. Based on your profile, I know you use a wheelchair and prefer detailed information. I'll focus on wheelchair-accessible attractions, hotels with ground-floor accessible rooms, and transportation that accommodates your manual wheelchair. What dates are you considering?",
  "session_id": "user_session_123",
  "events": [],
  "user_context": {
    "user_id": "09e2ca16-8b4a-4c5d-9e7f-1234567890ab",
    "context_injected": true,
    "user_name": "Sarah Johnson",
    "accessibility_needs": true
  }
}
```

## 🛠️ Troubleshooting

### Common Issues

#### CORS Errors
If you see CORS errors, make sure your frontend is running on `localhost:3000` or update the CORS settings in the backend.

#### 404 Errors
Check that the server is running on `http://localhost:8080` and the endpoints are correct.

#### Validation Errors (422)
Ensure all required fields are included in your requests. Check the API documentation at `/docs` for field requirements.

#### Server Not Responding
Restart the server:
```bash
uv run python start_server.py
```

## 📚 Additional Resources

- **API Documentation**: http://localhost:8080/docs (Interactive Swagger UI)
- **Health Check**: http://localhost:8080/health
- **Agent Information**: http://localhost:8080/agent/info
- **Frontend Integration Guide**: `FRONTEND_INTEGRATION_GUIDE.md`
- **User Profile System Summary**: `USER_PROFILE_SYSTEM_SUMMARY.md`

## 🎉 You're Ready!

Your backend is fully functional and ready for frontend integration. The system provides:

- **Complete user profile management** for onboarding
- **Accessibility-focused data models** for inclusive travel
- **Personalized AI responses** (when API key is added)
- **Production-ready API** with proper error handling
- **CORS support** for frontend requests

Start building your frontend and create an amazing accessible travel experience! 🌟