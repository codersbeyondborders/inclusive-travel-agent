# Google AI Studio Prompt: Inclusive Travel Agent Frontend

## Project Overview

Create a **fully accessible, elegant, and highly engaging React TypeScript frontend application** for the Inclusive Travel Agent - an AI-powered travel assistant specializing in accessible travel planning for disabled travelers. The app must integrate seamlessly with the existing backend API and provide both text and speech input/output capabilities.

## 🎯 Core Requirements

### Application Purpose
Build a comprehensive frontend that enables disabled travelers to:
1. **Sign up and create detailed accessibility profiles** during onboarding
2. **Save and manage their travel preferences and accessibility needs**
3. **Chat with AI agents** using both text and speech for input and output
4. **Receive personalized, accessibility-focused travel recommendations**

### Technical Stack
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS with accessibility-first design
- **Speech**: Web Speech API for speech-to-text and text-to-speech
- **State Management**: React Context API or Zustand
- **HTTP Client**: Axios or Fetch API
- **Accessibility**: WCAG 2.1 AA compliance
- **Build Tool**: Vite or Create React App

## 🏗️ Application Architecture

### Page Structure
```
/
├── Landing Page (/)
├── Sign Up (/signup)
├── Profile Setup (/onboarding)
│   ├── Basic Information
│   ├── Travel Interests  
│   ├── Accessibility Profile
│   └── Preferences
├── Dashboard (/dashboard)
├── Chat Interface (/chat)
├── Profile Management (/profile)
└── Settings (/settings)
```

## 🔌 Backend Integration

### API Base URL
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';
```

### Key API Endpoints to Integrate

#### User Profile Management
```typescript
// Create user profile
POST /users
Content-Type: application/json
Body: CreateUserProfileRequest

// Get user profile  
GET /users/{user_id}

// Update user profile
PUT /users/{user_id}
Body: UpdateUserProfileRequest

// Delete user profile
DELETE /users/{user_id}
```

#### Context-Aware Chat
```typescript
// Chat with personalization
POST /chat
Content-Type: application/json
Body: {
  message: string,
  session_id: string,
  user_id?: string  // Include for personalized responses
}

Response: {
  response: string,
  session_id: string,
  events: Array<any>,
  user_context?: {
    user_id: string,
    context_injected: boolean,
    user_name: string,
    accessibility_needs: boolean
  }
}
```

### User Profile Schema
```typescript
interface UserProfile {
  user_id: string;
  basic_info: {
    name: string;
    email: string;
    age?: number;
    nationality: string;
    home_location: string;
    phone?: string;
    emergency_contact?: {
      name: string;
      phone: string;
      relationship: string;
    };
  };
  travel_interests: {
    preferred_destinations: string[];
    travel_style: ('cultural' | 'adventure' | 'relaxation' | 'business' | 'family' | 'solo' | 'accessible')[];
    budget_range: 'budget' | 'mid-range' | 'luxury' | 'flexible';
    group_size_preference: string;
    accommodation_preferences: string[];
    activity_interests: string[];
    transportation_preferences: string[];
  };
  accessibility_profile: {
    mobility_needs: string[];
    sensory_needs: string[];
    cognitive_needs: string[];
    assistance_preferences: Record<string, string>;
    mobility_aids: string[];
    medical_conditions: string[];
    accessibility_priorities: string[];
    barrier_concerns: string[];
    dietary_restrictions: string[];
    medication_requirements: string[];
    service_animal?: {
      type: string;
      name: string;
      documentation: boolean;
    };
    communication_needs: string[];
  };
  preferences: {
    communication_style: 'brief' | 'detailed' | 'conversational' | 'professional';
    risk_tolerance: 'low' | 'medium' | 'high';
    planning_horizon: string;
    language_preferences: string[];
    currency_preference: string;
    timezone: string;
  };
  created_at: string;
  updated_at: string;
  profile_complete: boolean;
  onboarding_completed: boolean;
}
```

## 🎨 UI/UX Design Requirements

### Accessibility-First Design Principles

#### Visual Accessibility
- **High Contrast**: Minimum 4.5:1 contrast ratio for normal text, 3:1 for large text
- **Color Independence**: Never rely solely on color to convey information
- **Focus Indicators**: Clear, visible focus indicators for all interactive elements
- **Text Scaling**: Support up to 200% zoom without horizontal scrolling
- **Font Choices**: Use accessible fonts like Inter, Open Sans, or system fonts

#### Motor Accessibility
- **Large Touch Targets**: Minimum 44px × 44px for touch targets
- **Keyboard Navigation**: Full keyboard accessibility with logical tab order
- **Click Alternatives**: Support for various input methods
- **Timeout Extensions**: Allow users to extend or disable timeouts

#### Cognitive Accessibility
- **Clear Navigation**: Consistent, predictable navigation patterns
- **Simple Language**: Use plain language and avoid jargon
- **Error Prevention**: Clear validation and helpful error messages
- **Progress Indicators**: Show progress through multi-step processes

#### Screen Reader Support
- **Semantic HTML**: Use proper heading hierarchy (h1, h2, h3, etc.)
- **ARIA Labels**: Comprehensive ARIA labels and descriptions
- **Live Regions**: Use aria-live for dynamic content updates
- **Skip Links**: Provide skip navigation links

### Design System

#### Color Palette
```css
:root {
  /* Primary Colors - High contrast, accessibility-friendly */
  --primary-50: #f0f9ff;
  --primary-500: #0ea5e9;
  --primary-600: #0284c7;
  --primary-700: #0369a1;
  
  /* Accessibility Colors */
  --success: #059669;
  --warning: #d97706;
  --error: #dc2626;
  --info: #0284c7;
  
  /* Neutral Colors */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-500: #6b7280;
  --gray-900: #111827;
  
  /* Text Colors */
  --text-primary: #111827;
  --text-secondary: #374151;
  --text-muted: #6b7280;
}
```

#### Typography Scale
```css
.text-xs { font-size: 0.75rem; line-height: 1rem; }
.text-sm { font-size: 0.875rem; line-height: 1.25rem; }
.text-base { font-size: 1rem; line-height: 1.5rem; }
.text-lg { font-size: 1.125rem; line-height: 1.75rem; }
.text-xl { font-size: 1.25rem; line-height: 1.75rem; }
.text-2xl { font-size: 1.5rem; line-height: 2rem; }
.text-3xl { font-size: 1.875rem; line-height: 2.25rem; }
```

## 📱 Component Specifications

### 1. Landing Page Component
```typescript
interface LandingPageProps {}

// Features to include:
// - Hero section with accessibility messaging
// - Feature highlights (10 specialized agents, personalized responses)
// - Accessibility testimonials
// - Clear call-to-action to sign up
// - Skip to main content link
// - High contrast mode toggle
```

### 2. Sign Up Component
```typescript
interface SignUpFormData {
  email: string;
  password: string;
  confirmPassword: string;
  agreeToTerms: boolean;
  accessibilityPreferences?: {
    highContrast: boolean;
    largeText: boolean;
    screenReader: boolean;
  };
}

// Features to include:
// - Email/password registration
// - Password strength indicator
// - Accessibility preference quick setup
// - Clear error messages with ARIA live regions
// - Keyboard navigation support
// - Screen reader announcements
```

### 3. Onboarding Flow Components

#### Basic Information Step
```typescript
interface BasicInfoStepProps {
  data: Partial<UserProfile['basic_info']>;
  onUpdate: (data: Partial<UserProfile['basic_info']>) => void;
  onNext: () => void;
  onBack: () => void;
}

// Form fields:
// - Full name (required)
// - Email (required, validated)
// - Age (optional, number input with +/- buttons)
// - Nationality (required, searchable dropdown)
// - Home location (required, with autocomplete)
// - Phone (optional, with country code)
// - Emergency contact (optional, expandable section)
```

#### Travel Interests Step
```typescript
interface TravelInterestsStepProps {
  data: Partial<UserProfile['travel_interests']>;
  onUpdate: (data: Partial<UserProfile['travel_interests']>) => void;
  onNext: () => void;
  onBack: () => void;
}

// Interactive elements:
// - Destination preferences (multi-select chips)
// - Travel style checkboxes with icons
// - Budget range slider with labels
// - Activity interests (visual grid selection)
// - Transportation preferences (accessible icons)
```

#### Accessibility Profile Step
```typescript
interface AccessibilityProfileStepProps {
  data: Partial<UserProfile['accessibility_profile']>;
  onUpdate: (data: Partial<UserProfile['accessibility_profile']>) => void;
  onNext: () => void;
  onBack: () => void;
}

// Comprehensive accessibility form:
// - Mobility needs (wheelchair, walker, cane, etc.)
// - Sensory needs (hearing, visual assistance)
// - Cognitive needs (clear signage, quiet spaces)
// - Assistance preferences (airport, hotel, transport)
// - Mobility aids (detailed equipment info)
// - Medical conditions (relevant to travel)
// - Dietary restrictions and allergies
// - Service animal information
// - Communication preferences
```

### 4. Chat Interface Component
```typescript
interface ChatInterfaceProps {
  userId: string;
  sessionId: string;
}

interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'agent';
  timestamp: Date;
  isTyping?: boolean;
  accessibility_context?: {
    user_name: string;
    accessibility_needs: boolean;
  };
}

// Features to implement:
// - Text input with send button
// - Speech-to-text button with visual feedback
// - Text-to-speech for agent responses
// - Message history with proper ARIA labels
// - Typing indicators
// - Error handling and retry mechanisms
// - Keyboard shortcuts (Enter to send, Escape to stop speech)
// - Voice activity detection
// - Speech rate and voice selection controls
```

### 5. Speech Integration Components

#### Speech-to-Text Component
```typescript
interface SpeechToTextProps {
  onTranscript: (text: string) => void;
  onError: (error: string) => void;
  isListening: boolean;
  language?: string;
}

// Implementation requirements:
// - Use Web Speech API (SpeechRecognition)
// - Visual feedback for listening state
// - Interim results display
// - Confidence threshold handling
// - Noise cancellation indicators
// - Manual start/stop controls
// - Accessibility announcements
```

#### Text-to-Speech Component
```typescript
interface TextToSpeechProps {
  text: string;
  autoPlay?: boolean;
  voice?: SpeechSynthesisVoice;
  rate?: number;
  pitch?: number;
  onStart?: () => void;
  onEnd?: () => void;
  onError?: (error: string) => void;
}

// Implementation requirements:
// - Use Web Speech API (SpeechSynthesis)
// - Voice selection dropdown
// - Speed control slider
// - Play/pause/stop controls
// - Progress indicator
// - Queue management for multiple messages
// - Interrupt capability
// - Accessibility announcements
```

## 🎤 Speech Implementation Details

### Speech-to-Text Setup
```typescript
class SpeechToTextService {
  private recognition: SpeechRecognition | null = null;
  
  constructor() {
    if ('webkitSpeechRecognition' in window) {
      this.recognition = new webkitSpeechRecognition();
    } else if ('SpeechRecognition' in window) {
      this.recognition = new SpeechRecognition();
    }
    
    if (this.recognition) {
      this.recognition.continuous = true;
      this.recognition.interimResults = true;
      this.recognition.lang = 'en-US';
    }
  }
  
  startListening(onResult: (text: string) => void, onError: (error: string) => void) {
    // Implementation with error handling and accessibility announcements
  }
  
  stopListening() {
    // Clean stop with user feedback
  }
}
```

### Text-to-Speech Setup
```typescript
class TextToSpeechService {
  private synth: SpeechSynthesis;
  private currentUtterance: SpeechSynthesisUtterance | null = null;
  
  constructor() {
    this.synth = window.speechSynthesis;
  }
  
  speak(text: string, options: TTSOptions = {}) {
    // Implementation with voice selection, rate control, and interruption handling
  }
  
  stop() {
    // Immediate stop with cleanup
  }
  
  pause() {
    // Pause with resume capability
  }
}
```

## 🔧 State Management

### User Context
```typescript
interface UserContextType {
  user: UserProfile | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  signUp: (userData: SignUpData) => Promise<void>;
  signIn: (credentials: SignInData) => Promise<void>;
  signOut: () => void;
  updateProfile: (updates: Partial<UserProfile>) => Promise<void>;
  deleteProfile: () => Promise<void>;
}
```

### Chat Context
```typescript
interface ChatContextType {
  messages: ChatMessage[];
  isTyping: boolean;
  sessionId: string;
  isListening: boolean;
  isSpeaking: boolean;
  
  // Actions
  sendMessage: (text: string) => Promise<void>;
  startListening: () => void;
  stopListening: () => void;
  speakMessage: (text: string) => void;
  stopSpeaking: () => void;
  clearChat: () => void;
}
```

### Accessibility Context
```typescript
interface AccessibilityContextType {
  preferences: {
    highContrast: boolean;
    largeText: boolean;
    reducedMotion: boolean;
    screenReaderMode: boolean;
    keyboardNavigation: boolean;
  };
  
  // Actions
  updatePreferences: (prefs: Partial<AccessibilityPreferences>) => void;
  announceToScreenReader: (message: string) => void;
  focusElement: (elementId: string) => void;
}
```

## 🎯 Key Features Implementation

### 1. Progressive Onboarding
- **Step-by-step wizard** with clear progress indicators
- **Save and resume** capability for incomplete profiles
- **Skip optional sections** with ability to complete later
- **Accessibility hints** and help text throughout
- **Validation feedback** with clear error messages

### 2. Intelligent Chat Interface
- **Context awareness** - shows when user profile is being used
- **Rich message formatting** for travel recommendations
- **Quick action buttons** for common requests
- **Message categories** (inspiration, planning, booking, etc.)
- **Conversation history** with search capability

### 3. Speech Integration Excellence
- **Ambient noise detection** with quality indicators
- **Multiple language support** for international users
- **Voice training** for better recognition accuracy
- **Speech shortcuts** for common travel queries
- **Offline fallback** when speech APIs unavailable

### 4. Accessibility Excellence
- **Screen reader optimization** with proper ARIA labels
- **Keyboard-only navigation** with visible focus indicators
- **High contrast mode** with user preference memory
- **Text scaling support** up to 200% without breaking layout
- **Motion reduction** respect for user preferences

## 📱 Responsive Design Requirements

### Mobile-First Approach
```css
/* Mobile (320px+) */
.container { padding: 1rem; }
.text-input { font-size: 16px; } /* Prevents zoom on iOS */

/* Tablet (768px+) */
@media (min-width: 768px) {
  .container { padding: 2rem; }
  .grid { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container { max-width: 1200px; margin: 0 auto; }
  .grid { grid-template-columns: repeat(3, 1fr); }
}
```

### Touch-Friendly Design
- **Minimum 44px touch targets** for all interactive elements
- **Adequate spacing** between clickable elements
- **Swipe gestures** for navigation where appropriate
- **Pull-to-refresh** for chat and profile updates

## 🔒 Security & Privacy

### Data Protection
```typescript
// Encrypt sensitive data before storage
const encryptSensitiveData = (data: any) => {
  // Implementation for client-side encryption
};

// Secure API communication
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Privacy Controls
- **Data usage transparency** - clear explanations of how data is used
- **Granular permissions** - users control what data is shared
- **Data export** - users can download their data
- **Data deletion** - complete profile removal option

## 🧪 Testing Requirements

### Accessibility Testing
```typescript
// Example accessibility tests
describe('Accessibility Tests', () => {
  test('should have proper heading hierarchy', () => {
    // Test h1, h2, h3 structure
  });
  
  test('should support keyboard navigation', () => {
    // Test tab order and keyboard interactions
  });
  
  test('should have sufficient color contrast', () => {
    // Test contrast ratios
  });
  
  test('should work with screen readers', () => {
    // Test ARIA labels and announcements
  });
});
```

### Speech Testing
```typescript
describe('Speech Integration Tests', () => {
  test('should handle speech recognition errors gracefully', () => {
    // Test error scenarios
  });
  
  test('should provide visual feedback during speech input', () => {
    // Test UI states
  });
  
  test('should allow interruption of speech output', () => {
    // Test stop/pause functionality
  });
});
```

## 🚀 Performance Requirements

### Loading Performance
- **Initial page load** under 3 seconds on 3G
- **Code splitting** for route-based loading
- **Image optimization** with WebP and lazy loading
- **Service worker** for offline capability

### Runtime Performance
- **Smooth animations** at 60fps
- **Efficient re-renders** with React.memo and useMemo
- **Memory management** for long chat sessions
- **Battery optimization** for mobile devices

## 📋 Implementation Checklist

### Phase 1: Core Setup
- [ ] Project setup with TypeScript and Tailwind CSS
- [ ] Accessibility-first design system
- [ ] Basic routing and navigation
- [ ] API integration layer
- [ ] User authentication flow

### Phase 2: Onboarding
- [ ] Multi-step onboarding wizard
- [ ] Form validation and error handling
- [ ] Progress saving and resumption
- [ ] Accessibility profile creation
- [ ] Profile completion tracking

### Phase 3: Chat Interface
- [ ] Basic text chat functionality
- [ ] Backend API integration
- [ ] Message history and persistence
- [ ] Typing indicators and loading states
- [ ] Error handling and retry logic

### Phase 4: Speech Integration
- [ ] Speech-to-text implementation
- [ ] Text-to-speech implementation
- [ ] Voice controls and settings
- [ ] Audio feedback and indicators
- [ ] Fallback for unsupported browsers

### Phase 5: Accessibility Excellence
- [ ] Screen reader optimization
- [ ] Keyboard navigation
- [ ] High contrast mode
- [ ] Focus management
- [ ] ARIA labels and live regions

### Phase 6: Polish & Testing
- [ ] Responsive design refinement
- [ ] Performance optimization
- [ ] Accessibility testing
- [ ] Cross-browser compatibility
- [ ] User acceptance testing

## 🎨 Visual Design Guidelines

### Component Examples

#### Accessible Button Component
```typescript
interface AccessibleButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  ariaLabel?: string;
  ariaDescribedBy?: string;
  loading?: boolean;
}

// Implementation with proper ARIA attributes, focus management, and loading states
```

#### Accessible Form Input Component
```typescript
interface AccessibleInputProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: 'text' | 'email' | 'tel' | 'password';
  required?: boolean;
  error?: string;
  helpText?: string;
  placeholder?: string;
  autoComplete?: string;
}

// Implementation with proper labeling, error handling, and validation feedback
```

## 🌟 Success Criteria

The frontend application will be considered successful when it achieves:

### Accessibility Metrics
- **WCAG 2.1 AA compliance** verified by automated and manual testing
- **Screen reader compatibility** with NVDA, JAWS, and VoiceOver
- **Keyboard navigation** for 100% of functionality
- **Color contrast ratios** meeting or exceeding 4.5:1 for normal text

### User Experience Metrics
- **Onboarding completion rate** above 80%
- **Chat engagement** with average session length over 5 minutes
- **Speech feature adoption** by at least 40% of users
- **User satisfaction score** above 4.5/5 for accessibility features

### Technical Metrics
- **Page load speed** under 3 seconds on 3G networks
- **Accessibility score** above 95 in Lighthouse audits
- **Cross-browser compatibility** in Chrome, Firefox, Safari, Edge
- **Mobile responsiveness** on devices from 320px to 1920px width

## 🎯 Final Notes

This frontend application should serve as a **gold standard for accessible web applications**, demonstrating that beautiful, engaging user interfaces can be fully inclusive. Every design decision should prioritize accessibility while maintaining visual appeal and user engagement.

The integration with the backend API should be seamless, providing users with personalized, context-aware responses that make travel planning more accessible and enjoyable for disabled travelers.

Remember: **Accessibility is not a feature to be added later - it's a fundamental requirement that should guide every design and development decision from the start.**

---

**Build an application that doesn't just serve disabled travelers - build one that sets the standard for how all web applications should be designed: accessible, inclusive, and empowering for everyone.**