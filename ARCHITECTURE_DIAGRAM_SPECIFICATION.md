# Inclusive Travel Agent Architecture Diagram Specification

## Overview
This document specifies the visual architecture diagram for the Inclusive Travel Agent system with 14 specialized agents, user profile management, and comprehensive automation features.

## Diagram Layout

### Main Components (Top to Bottom)

#### 1. User Interface Layer (Top)
```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                        │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   Frontend App  │   ADK Web UI    │   Production API Server     │
│   (React/Vue)   │   (Development) │   (FastAPI - Port 8080)     │
│                 │                 │                             │
│ • User Profiles │ • Agent Testing │ • /users (CRUD)             │
│ • Chat Interface│ • Direct Chat   │ • /chat (Context-Aware)     │
│ • Onboarding    │ • State Viewer  │ • /health, /docs            │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

#### 2. Core System Layer (Middle)
```
┌─────────────────────────────────────────────────────────────────┐
│                      CORE SYSTEM LAYER                         │
├─────────────────┬─────────────────┬─────────────────────────────┤
│  User Profile   │   Context       │    Session Management       │
│    System       │   Service       │                             │
│                 │                 │                             │
│ • Profile CRUD  │ • Context       │ • ADK Sessions              │
│ • Accessibility │   Injection     │ • State Management          │
│   Needs         │ • Personalized │ • Memory Persistence        │
│ • Preferences   │   Instructions  │ • Event Handling            │
│ • Storage       │ • User Context  │                             │
│   (Firestore)   │   Retrieval     │                             │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

#### 3. Agent Architecture (Main Section)
```
┌─────────────────────────────────────────────────────────────────┐
│                    ROOT AGENT (Orchestrator)                   │
│              "Comprehensive Accessibility Support"              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
┌─────────┐    ┌─────────────┐    ┌─────────────┐
│ CORE    │    │ACCESSIBILITY│    │ AUTOMATION  │
│ TRAVEL  │    │  FOCUSED    │    │& NOTIFICATION│
│ AGENTS  │    │   AGENTS    │    │   AGENTS    │
│   (6)   │    │     (4)     │    │     (4)     │
└─────────┘    └─────────────┘    └─────────────┘
```

#### 4. Detailed Agent Breakdown
```
┌─────────────────────────────────────────────────────────────────┐
│                     CORE TRAVEL AGENTS (6)                     │
├─────────────────────────────────────────────────────────────────┤
│ inspiration_agent    │ planning_agent      │ booking_agent      │
│ • Accessible         │ • Accessible        │ • Accessibility    │
│   destinations       │   flights & hotels  │   accommodations   │
│ • Disability-        │ • Seat selection    │ • Special requests │
│   friendly options   │ • Accessibility     │ • Payment          │
│                      │   features          │   processing       │
├─────────────────────────────────────────────────────────────────┤
│ pre_trip_agent      │ in_trip_agent       │ post_trip_agent    │
│ • Travel prep       │ • Real-time support │ • Feedback         │
│ • Documentation     │ • Barrier navigation│   collection       │
│ • Medical clearance │ • Emergency assist  │ • Experience       │
│                     │                     │   sharing          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                 ACCESSIBILITY-FOCUSED AGENTS (4)               │
├─────────────────────────────────────────────────────────────────┤
│accessibility_research│ mobility_preparation│ transit_support   │
│ • Venue accessibility│ • Equipment prep    │ • Airport assist  │
│ • Disabled reviews   │ • Medical docs      │ • Priority services│
│ • Barrier assessment │ • Mobility aids     │ • Transportation   │
│                      │                     │   coordination     │
├─────────────────────────────────────────────────────────────────┤
│           barrier_navigation_agent                              │
│           • Real-time barrier solutions                        │
│           • Alternative accessible options                     │
│           • Emergency accessibility assistance                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│               AUTOMATION & NOTIFICATION AGENTS (4)             │
├─────────────────────────────────────────────────────────────────┤
│ notification_agent   │accessibility_comm   │ web_checkin_agent │
│ • Email confirmations│ • Provider          │ • Auto check-in   │
│ • Travel reminders   │   notifications     │ • Seat selection  │
│ • Emergency alerts   │ • Accessibility     │ • Boarding passes │
│                      │   coordination      │                   │
├─────────────────────────────────────────────────────────────────┤
│              smart_guardrails_agent                             │
│              • Safety monitoring & compliance                  │
│              • Proactive issue prevention                      │
│              • Risk assessment & mitigation                    │
└─────────────────────────────────────────────────────────────────┘
```

#### 5. External Integrations (Bottom)
```
┌─────────────────────────────────────────────────────────────────┐
│                   EXTERNAL INTEGRATIONS                        │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   AI Services   │  Accessibility  │    Communication            │
│                 │     APIs        │      Services               │
│ • Google AI API │ • Wheelmap.org  │ • Email (SMTP)              │
│   (ML Dev)      │ • Airport       │ • SMS (Future)              │
│ • Google Places │   Accessibility │ • Push Notifications        │
│   API           │   Database      │   (Future)                  │
│ • Google Search │ • AccessibleGO  │                             │
│   Grounding     │   API           │                             │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

#### 6. Data Flow Arrows
```
User Input → Frontend → API Server → Root Agent → Specialized Agents
                                                      ↓
External APIs ← Tools ← Sub-Agents ← Agent Tools ← Agents
                                                      ↓
Email Service ← Notification Agent ← Context Service ← User Profile
```

## Visual Design Guidelines

### Colors
- **Core Travel Agents**: Blue tones (#0ea5e9, #0284c7)
- **Accessibility Agents**: Green tones (#059669, #16a34a)  
- **Automation Agents**: Purple tones (#7c3aed, #8b5cf6)
- **Infrastructure**: Gray tones (#6b7280, #374151)
- **External APIs**: Orange tones (#ea580c, #dc2626)

### Icons
- **Core Travel**: ✈️ 🏨 🎯
- **Accessibility**: ♿ 🦽 🦯
- **Automation**: 🤖 📧 ⚡
- **Infrastructure**: 🔧 💾 🔄
- **External**: 🌐 📡 🔌

### Layout Style
- Clean, modern design with rounded corners
- Clear hierarchical structure from top to bottom
- Connecting lines showing data flow
- Consistent spacing and typography
- Professional color scheme suitable for technical documentation

### Dimensions
- **Width**: 1200px
- **Height**: 1000px
- **Format**: PNG with transparent background
- **Resolution**: 300 DPI for high-quality printing

## Key Messages to Convey

1. **Comprehensive System**: 14 specialized agents working together
2. **Accessibility-First**: Every component considers disability needs
3. **Automation Excellence**: Proactive notifications and check-ins
4. **Production-Ready**: Full API with user profile management
5. **Scalable Architecture**: Clean separation of concerns
6. **External Integration**: Real-world API connections

## Usage Context

This diagram will be used in:
- README.md documentation
- Technical presentations
- Architecture reviews
- Developer onboarding materials
- Marketing and demo materials

The diagram should clearly communicate the system's sophistication while remaining accessible to both technical and non-technical audiences.