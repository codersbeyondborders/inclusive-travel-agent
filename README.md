# Inclusive Travel Agent

An AI-powered travel agent specializing in accessible travel planning, built with Google's Agent Development Kit (ADK). This system provides comprehensive support for disabled travelers throughout their entire journey, from inspiration to post-trip feedback.

## 🌟 Key Features

- **14 Specialized AI Agents** covering all aspects of accessible travel with comprehensive automation
- **Personalized User Profiles** with detailed accessibility needs and travel preferences
- **Automated Notifications & Communications** with email confirmations and provider coordination
- **Proactive Accessibility Communication** to hotels, airlines, and transportation providers
- **Automated Web Check-in** for flights and hotels with accessibility optimization
- **Smart Safety Monitoring** with compliance verification and issue prevention
- **Real-time Accessibility Information** from external APIs and databases
- **Barrier Navigation Support** with immediate solutions and alternatives
- **Mobility Aid Preparation** assistance for equipment and documentation
- **Transit Support Coordination** for airports, stations, and transportation
- **Inclusive Booking Process** with accessibility accommodations
- **Cloud-Ready Deployment** on Google Cloud Run with production-ready API

## 🎯 Mission

Making travel accessible for everyone by providing AI-powered assistance that understands and addresses the unique needs of disabled travelers. Our system covers the complete travel journey:

### 🔍 **Plan & Research**
- Choose accessible destinations with verified accessibility information
- Review experiences from other disabled travelers
- Research accessibility features and potential barriers

### 💰 **Budget & Route Decisions**
- Compare cost vs accessibility of routes, transport, and accommodation
- Calculate disability-related expenses transparently
- Find the best value for accessible options

### 📋 **Book & Notify**
- Book flights, trains, hotels with accessibility accommodations
- Request special assistance services automatically
- Communicate accessibility needs to service providers
- Send automated email confirmations with accessibility details
- Proactively notify providers 7-14 days before arrival

### 🧳 **Prepare & Pack**
- Arrange mobility aids and assistive equipment for travel
- Organize medical documents and prescriptions
- Plan accessible routes and backup options

### ✈️ **Travel & Transit Support**
- Coordinate assistance at airports and stations
- Automated web check-in 24 hours before departure with optimal accessible seating
- Manage priority check-in, security, and boarding
- Provide real-time support during travel
- Smart safety monitoring with compliance verification

### 🏨 **Stay & Explore**
- Confirm hotel accessibility and room features
- Plan accessible activities and dining options
- Navigate barriers with immediate alternatives

### 🔄 **Return & Review**
- Automated return journey check-in and assistance coordination
- Collect accessibility feedback for future travelers
- Share experiences to help the community
- Post-trip email follow-ups and satisfaction surveys


## Agent Details
The key features of the Inclusive Travel Agent include:

| Feature | Description |
| --- | --- |
| **Interaction Type:** | Conversational |
| **Complexity:**  | Advanced |
| **Agent Type:**  | Multi Agent |
| **Components:**  | Tools, AgentTools, Memory |
| **Vertical:**  | Travel |

See section [MCP](#mcp) for an example using Airbnb's MCP search tool.

### Agent Architecture
Inclusive Travel Agent Architecture

<img src="inclusive-travel-agent-arch.png" alt="Inclusive Travel Agent's 14-Agent Architecture with Automation & Notifications" width="800"/>

### System Architecture Overview

The Inclusive Travel Agent features a comprehensive 14-agent architecture organized into three specialized tiers:

**🎯 Core Travel Agents (6)** - Handle the fundamental travel planning journey from inspiration to post-trip feedback

**♿ Accessibility-Focused Agents (4)** - Provide specialized accessibility research, mobility preparation, transit support, and barrier navigation

**🤖 Automation & Notification Agents (4)** - Deliver proactive communications, automated check-ins, and intelligent safety monitoring

**🔧 Supporting Infrastructure:**
- **User Profile System** with comprehensive accessibility needs tracking
- **Email Service Integration** for automated notifications and confirmations  
- **External API Connections** for real-time accessibility information
- **Production-Ready FastAPI** with full CRUD operations and chat endpoints

### Component Details

Expand on the "Key Components" from above.
*   **Core Travel Agents (6):**
    * `inspiration_agent` - Provides accessible destination suggestions and activity recommendations with disability-friendly options.
    * `planning_agent` - Helps select accessible flights, seats, and hotels with comprehensive accessibility features.
    * `booking_agent` - Processes bookings with automatic accessibility accommodation requests and confirmations.
    * `pre_trip_agent` - Fetches accessibility information, travel advisories, and preparation requirements.
    * `in_trip_agent` - Provides real-time travel support, accessibility assistance, and barrier navigation.
    * `post_trip_agent` - Collects accessibility feedback and learns preferences for future trips.

*   **Accessibility-Focused Agents (4):**
    * `accessibility_research_agent` - Gathers comprehensive accessibility information, reviews, and barrier assessments.
    * `mobility_preparation_agent` - Assists with mobility aid preparation, medical documentation, and equipment coordination.
    * `transit_support_agent` - Coordinates airport assistance, priority services, and accessible transportation.
    * `barrier_navigation_agent` - Provides real-time solutions for accessibility barriers and alternative options.

*   **Automation & Notification Agents (4):**
    * `notification_agent` - Manages email confirmations, travel reminders, and emergency notifications.
    * `accessibility_communication_agent` - Proactively communicates accessibility needs to service providers.
    * `web_checkin_agent` - Automates flight and hotel check-in with accessibility optimization.
    * `smart_guardrails_agent` - Monitors safety, compliance, and prevents accessibility issues proactively.
*   **Tools:**
    * `map_tool` - retrieves lat/long; geocoding an address with the Google Map API.
    * `memorize` - a function to memorize information from the dialog that are important to trip planning and to provide in-trip support.
*   **AgentTools:**  
    * `google_search_grounding` - used in the example for pre-trip information gather such as visa, medical, travel advisory...etc.
    * `what_to_pack` - suggests what to pack for the trip given the origin and destination.
    * `place_agent` - this recommends destinations.
    * `poi_agent` - this suggests activities given a destination.
    * `itinerary_agent` - called by the `planning_agent` to fully construct and represent an itinerary in JSON following a pydantic schema.
    * `day_of_agent` - called by the `in_trip_agent` to provide in_trip on the day and in the moment transit information, getting from A to B. Implemented using dynamic instructions.
    * `flight_search_agent` -  mocked flight search given origin, destination, outbound and return dates.
    * `flight_seat_selection_agent` -  mocked seat selection, some seats are not available.
    * `hotel_search_agent` - mocked hotel selection given destination, outbound and return dates.
    * `hotel_room_selection_agent` - mocked hotel room selection.
    * `confirm_reservation_agent` - mocked reservation.
    * `payment_choice` - mocked payment selection, Apple Pay will not succeed, Google Pay and Credit Card will.
    * `payment_agent` - mocked payment processing.
*   **Memory:** 
    * All agents and tools in this example use the Agent Development Kit's internal session state as memory.
    * The session state is used to store information such as the itinerary, and temporary AgentTools' responses.
    * There are a number of premade itineraries that can be loaded for test runs. See 'Running the Agent' below on how to run them.

## Setup and Installation

### Folder Structure
```
.
├── README.md
├── inclusive-travel-agent-arch.png
├── pyproject.toml
├── inclusive_travel_agent/
│   ├── shared_libraries/
│   ├── tools/
│   │   ├── email_service.py
│   │   ├── accessibility_apis.py
│   │   └── memory.py
│   ├── models/
│   │   └── user_profile.py
│   ├── services/
│   │   ├── user_profile_service.py
│   │   └── context_service.py
│   └── sub_agents/
│       ├── inspiration/
│       ├── planning/
│       ├── booking/
│       ├── pre_trip/
│       ├── in_trip/
│       ├── post_trip/
│       ├── accessibility_research/
│       ├── mobility_preparation/
│       ├── transit_support/
│       ├── barrier_navigation/
│       ├── notification/
│       ├── accessibility_communication/
│       ├── web_checkin/
│       └── smart_guardrails/
├── tests/
│   └── unit/
├── eval/
│   └── data/
└── deployment/
```

### Prerequisites

- Python 3.10+
- Google AI API Key (for ML Dev backend) or Google Cloud Project (for Vertex AI)
- API Key for [Google Maps Platform Places API](https://developers.google.com/maps/documentation/places/web-service/get-api-key)
- Email account for notifications (Gmail recommended)
- Google Agent Development Kit 1.0+
- uv: Install uv by following the instructions on the official uv [website](https://docs.astral.sh/uv/)
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/google/adk-samples.git
    cd adk-samples/python/agents/inclusive-travel-agent
    ```
    NOTE: From here on, all command-line instructions shall be executed under the directory  `inclusive-travel-agent/` unless otherwise stated.

2.  Install dependencies:

    ```bash
    uv sync
    ```

3.  Set up configuration:

    - At the top directory `inclusive-travel-agent/`, make a `.env` by copying `.env.example`
    - Set the following environment variables:
    ```bash
    # Choose Model Backend: 0 -> ML Dev (recommended), 1 -> Vertex AI
    GOOGLE_GENAI_USE_VERTEXAI=0
    
    # Google AI API Key (for ML Dev backend - get from https://aistudio.google.com/app/apikey)
    GOOGLE_API_KEY=YOUR_GOOGLE_AI_API_KEY_HERE
    
    # Google Cloud Project (optional for ML Dev, required for Vertex AI)
    GOOGLE_CLOUD_PROJECT=YOUR_CLOUD_PROJECT_ID_HERE
    GOOGLE_CLOUD_REGION=us-central1

    # Places API (required for location features)
    GOOGLE_PLACES_API_KEY=YOUR_PLACES_API_KEY_HERE

    # Email Service Configuration (for notifications)
    EMAIL_ADDRESS=your_email@gmail.com
    EMAIL_PASSWORD=your_app_password
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    EMAIL_USE_TLS=true

    # Accessibility APIs (optional)
    WHEELMAP_API_KEY=YOUR_WHEELMAP_API_KEY_HERE
    ACCESSIBLEGO_API_KEY=YOUR_ACCESSIBLEGO_API_KEY_HERE

    # Default user profile with accessibility needs
    INCLUSIVE_TRAVEL_AGENT_SCENARIO=inclusive_travel_agent/profiles/itinerary_accessible_default.json
    ```

4. (Optional) For Vertex AI backend, authenticate your GCloud account:
    ```bash
    gcloud auth application-default login
    ```

## 🤖 Automation Features

### Proactive Notifications
- **Email Confirmations**: Automated booking confirmations with accessibility details
- **Provider Communications**: Proactive emails to hotels and airlines about accessibility needs
- **Travel Reminders**: Automated reminders for documents, packing, and preparation
- **Emergency Alerts**: Immediate notifications to emergency contacts when needed

### Automated Check-in Services
- **Flight Check-in**: Automatic web check-in 24 hours before departure
- **Optimal Seating**: Intelligent accessible seat selection based on mobility needs
- **Hotel Coordination**: Early check-in arrangements for accessibility room preparation
- **Service Confirmation**: Verification of all special assistance services

### Smart Safety Monitoring
- **Compliance Verification**: Continuous monitoring of accessibility regulation compliance
- **Risk Assessment**: Proactive identification of safety risks for disabled travelers
- **Issue Prevention**: Early warning systems and preventive measures
- **Emergency Coordination**: Rapid response protocols for accessibility emergencies

### Accessibility Communication
- **7-14 Day Advance Notice**: Accessibility needs communicated well before travel
- **Written Confirmations**: All accessibility services confirmed in writing
- **Direct Coordinator Contact**: Relationships established with accessibility coordinators
- **Follow-up Protocols**: Systematic follow-up to ensure arrangements remain in place

## Running the Agent

### Using the Production API Server

The system includes a production-ready FastAPI server with comprehensive endpoints:

```bash
# Start the production server
uv run python start_server.py
```

This starts the server at `http://localhost:8080` with the following endpoints:
- **API Documentation**: `http://localhost:8080/docs`
- **Health Check**: `http://localhost:8080/health`
- **User Profiles**: `http://localhost:8080/users` (CRUD operations)
- **Chat with Context**: `http://localhost:8080/chat` (personalized responses)
- **Agent Information**: `http://localhost:8080/agent/info`

### Using `adk` (Development)

For development and testing, ADK provides convenient ways to interact with agents:

```bash
# CLI interface
adk run inclusive_travel_agent

# Web interface
adk web
```

Select "inclusive_travel_agent" in the top-left drop-down menu for the chatbot interface. 

The conversation is initially blank. For an outline on the concierge interaction, see the section [Sample Agent interaction](#sample-agent-interaction) 

Here are some things to try:
* **Inspiration**: "Need accessible destination ideas for Europe"
* **Planning**: "Help me plan an accessible trip to Tokyo with wheelchair accessibility"
* **Automation**: "Set up automated check-in and notify the hotel about my accessibility needs"
* **Notifications**: "Send me email confirmations and coordinate with the airline about my wheelchair assistance"
* **Safety**: "Monitor my trip for accessibility compliance and safety issues"


### Programmatic Access

Below is an example of interacting with the agent as a server using Python. 
Try it under the inclusive-travel-agent directory:

First, establish a quick development API server for the inclusive_travel_agent package.
```bash
adk api_server inclusive_travel_agent
```
This will start a fastapi server at http://127.0.0.1:8000.
You can access its API docs at http://127.0.0.1:8000/docs

Here is an example client that only call the server for two turns:
```bash
python tests/programmatic_example.py
```

You may notice that there are code to handle function responses. We will revisit this in the [GUI](#gui) section below.


### Sample Agent interaction

Two example sessions are provided to illustrate how the Inclusive Travel Agent operates.
- Trip planning from inspiration to finalized bookings for a trip to Peru ([`tests/pre_booking_sample.md`](tests/pre_booking_sample.md)).
- In-trip experience for a short get away to Seattle, simulating the passage of time using a tool ([`tests/post_booking_sample.md`](tests/post_booking_sample.md)).

### Worth Trying

Instead of interacting with the concierge one turn at time. Try giving it the entire instruction, including decision making criteria, and watch it work, e.g. 

  *"Find flights to London from JFK on April 20th for 4 days. Pick any flights and any seats; also Any hotels and room type. Make sure you pick seats for both flights. Go ahead and act on my behalf without my input, until you have selected everything, confirm with me before generating an itinerary."*

Without specifically optimizing for such usage, this cohort of agents seem to be able to operate by themselves on your behalf with very little input.


## Running Tests

To run the illustrative tests and evaluations, install the extra dependencies and run `pytest`:

```bash
uv sync --dev
uv run pytest
```

The different tests can also be run separately:

To run the unit tests, just checking all agents and tools responds:
```bash
uv run pytest tests
```

To run agent trajectory tests:
```bash
uv run pytest eval
```

## 👤 User Profile System

### Comprehensive Profile Management
The system includes a sophisticated user profile system that enables personalized, context-aware responses:

**Profile Components:**
- **Basic Information**: Name, email, nationality, home location, emergency contacts
- **Travel Interests**: Preferred destinations, travel styles, budget range, activity preferences
- **Accessibility Profile**: Mobility needs, sensory needs, assistance preferences, mobility aids
- **Communication Preferences**: Style, risk tolerance, language, currency preferences

### API Endpoints
- `POST /users` - Create user profile (onboarding)
- `GET /users/{user_id}` - Retrieve user profile
- `PUT /users/{user_id}` - Update user profile
- `DELETE /users/{user_id}` - Delete user profile
- `GET /users` - List user profiles (paginated)
- `POST /chat` - Context-aware chat with user_id parameter

### Personalization Benefits
- **Context-Aware Responses**: AI agents know your specific accessibility needs
- **Consistent Experience**: No need to re-explain requirements in each conversation
- **Tailored Recommendations**: Suggestions match your interests and accessibility requirements
- **Automated Accommodations**: Accessibility services automatically included in all bookings

### Storage Options
- **Production**: Google Cloud Firestore for scalable, real-time user profile storage
- **Development**: In-memory storage with automatic fallback when Firestore unavailable
- **Security**: Proper handling of sensitive accessibility and medical information

## Deploying the Agent

### Cloud Run Deployment (Recommended)

Deploy the complete system to Google Cloud Run for production use:

```bash
# One-command deployment
uv run python deploy/deploy_cloud_run.py --project-id YOUR_PROJECT_ID
```

This deploys:
- **FastAPI Application** with all endpoints
- **User Profile System** with Firestore integration
- **Email Notification Service** for automated communications
- **All 14 Specialized Agents** with full functionality
- **Auto-scaling Infrastructure** that handles variable loads

### Vertex AI Agent Engine (Alternative)

For Vertex AI deployment, run the following command:

```bash
uv sync --group deployment
uv run python deployment/deploy.py --create
```

This will return an AgentEngine resource ID for testing and management.

### Alternative: Using Agent Starter Pack

You can also use the [Agent Starter Pack](https://goo.gle/agent-starter-pack) to create a production-ready version of this agent with additional deployment options:

```bash
# Create and activate a virtual environment
python -m venv .venv && source .venv/bin/activate # On Windows: .venv\Scripts\activate

# Install the starter pack and create your project
pip install --upgrade agent-starter-pack
agent-starter-pack create my-inclusive-travel-agent -a adk@inclusive-travel-agent
```

<details>
<summary>⚡️ Alternative: Using uv</summary>

If you have [`uv`](https://github.com/astral-sh/uv) installed, you can create and set up your project with a single command:
```bash
uvx agent-starter-pack create my-inclusive-travel-agent -a adk@inclusive-travel-agent
```
This command handles creating the project without needing to pre-install the package into a virtual environment.

</details>

The starter pack will prompt you to select deployment options and provides additional production-ready features including automated CI/CD deployment scripts.

## Application Development

### Callbacks and initial State

The `root_agent` in this demo currently has a `before_agent_callback` registered to load an initial state, such as user preferences and itinerary, from a file into the session state for interaction. The primary reason for this is to reduce the amount of set up necessary, and this makes it easy to use the ADK UIs.

In a realistic application scenario, initial states can be included when a new `Session` is being created, there by satisfying use cases where user preferences and other pieces of information are most likely loaded from external databases.
 
### Memory vs States

In this example, we are using the session states as memory for the concierge, to store the itinerary, and intermediate agent / tools / user preference responses. In a realistic application scenario, the source for user profiles should be an external database, and the 
reciprocal writes to session states from tools should in addition be persisted, as a write-through, to external databases dedicated for user profiles and itineraries. 

### MCP

An example using Airbnb's MCP server is included. ADK supports MCP and provides several MCP tools.
This example attaches the Airbnb search and listing MCP tools to the `planning_agent`, and ask the concierge to simply find an airbnb given certain dates. The concierge will transfer the request to the planning agent which in turn will call the Airbnb search MCP tool.

To try the example, first set up nodejs and npx from Node.js [website](https://nodejs.org/en/download)

Making sure:
```
$ which node
/Users/USERNAME/.nvm/versions/node/v22.14.0/bin/node

$ which npx
/Users/USERNAME/.nvm/versions/node/v22.14.0/bin/npx
```

Then, under the `inclusive-travel-agent/` directory, run the test with:
```
python -m tests.mcp_abnb
```

You will see outputs on the console similar to the following:
```
[user]: Find me an airbnb in San Diego, April 9th, to april 13th, no flights nor itinerary needed. No need to confirm, simply return 5 choicess, remember to include urls.

( Setting up the agent and the tool ) 

Server started with options: ignore-robots-txt
Airbnb MCP Server running on stdio

Inserting Airbnb MCP tools into Inclusive Travel Agent...
...
FOUND planning_agent

( Execute: Runner.run_async() ) 

[root_agent]: transfer_to_agent( {"agent_name": "planning_agent"} )
...
[planning_agent]: airbnb_search( {"checkout": "2025-04-13", "location": "San Diego", "checkin": "2025-04-09"} )

[planning_agent]: airbnb_search responds -> {
  "searchUrl": "https://www.airbnb.com/s/San%20Diego/homes?checkin=2025-04-09&checkout=2025-04-13&adults=1&children=0&infants=0&pets=0",
  "searchResults": [
    {
      "url": "https://www.airbnb.com/rooms/24669593",
      "listing": {
        "id": "24669593",
        "title": "Room in San Diego",
        "coordinate": {
          "latitude": 32.82952,
          "longitude": -117.22201
        },
        "structuredContent": {
          "mapCategoryInfo": "Stay with Stacy, Hosting for 7 years"
        }
      },
      "avgRatingA11yLabel": "4.91 out of 5 average rating,  211 reviews",
      "listingParamOverrides": {
        "categoryTag": "Tag:8678",
        "photoId": "1626723618",
        "amenities": ""
      },
      "structuredDisplayPrice": {
        "primaryLine": {
          "accessibilityLabel": "$9,274 TWD for 4 nights"
        },
        "explanationData": {
          "title": "Price details",
          "priceDetails": "$2,319 TWD x 4 nights: $9,274 TWD"
        }
      }
    },
    ...
    ...
  ]
}

[planning_agent]: Here are 5 Airbnb options in San Diego for your trip from April 9th to April 13th, including the URLs:

1.  Room in San Diego: [https://www.airbnb.com/rooms/24669593](https://www.airbnb.com/rooms/24669593)
2.  Room in San Diego: [https://www.airbnb.com/rooms/5360158](https://www.airbnb.com/rooms/5360158)
3.  Room in San Diego: [https://www.airbnb.com/rooms/1374944285472373029](https://www.airbnb.com/rooms/1374944285472373029)
4.  Apartment in San Diego: [https://www.airbnb.com/rooms/808814447273523115](https://www.airbnb.com/rooms/808814447273523115)
5.  Room in San Diego: [https://www.airbnb.com/rooms/53010806](https://www.airbnb.com/rooms/53010806)
```

### GUI

A typical end-user will be interacting with agents via GUIs instead of pure text. The front-end concierge application will likely render several kinds of agent responses graphically and/or with rich media, for example:
- Destination ideas as a carousel of cards,
- Points of interest / Directions on a Map,
- Expandable videos, images, link outs.
- Selection of flights and hotels as lists with logos, 
- Selection of flight seats on a seating chart,
- Clickable templated responses.

Many of these can be achieved via ADK's Events. This is because:
- All function calls and function responses are reported as events by the session runner.
- In this inclusive travel agent example, several sub-agents and tools use an explicit pydantic schema and controlled generation to generate a JSON response. These agents are: place agent (for destinations), poi agent (for pois and activities), flights and hotels selection agents, seats and rooms selection agents, and itinerary.
- When a session runner service is wrapped as a server endpoint, the series of events carrying these JSON payloads can be streamed over to the application.
- When the application recognizes the payload schema by their source agent, it can therefore render the payload accordingly.

To see how to work with events, agents and tools responses, open the file [`tests/programmatic_example.py`](tests/programmatic_example.py).

Run the test client code with:
```
python tests/programmatic_example.py 
```

You will get outputs similar to this below:
```
[user]: "Inspire me about Maldives"

...

[root_agent]: transfer_to_agent( {"agent_name": "inspiration_agent"} )

...

[inspiration_agent]: place_agent responds -> {
  "id": "af-be786618-b60b-45ee-a801-c40fd6811e60",
  "name": "place_agent",
  "response": {
    "places": [
      {
        "name": "Malé",
        "country": "Maldives",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Male%2C_Maldives_panorama_2016.jpg/1280px-Male%2C_Maldives_panorama_2016.jpg",
        "highlights": "The vibrant capital city, offering bustling markets, historic mosques, and a glimpse into local Maldivian life.",
        "rating": "4.2"
      },
      {
        "name": "Baa Atoll",
        "country": "Maldives",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Baa_Atoll_Maldives.jpg/1280px-Baa_Atoll_Maldives.jpg",
        "highlights": "A UNESCO Biosphere Reserve, famed for its rich marine biodiversity, including manta rays and whale sharks, perfect for snorkeling and diving.",
        "rating": "4.8"
      },
      {
        "name": "Addu Atoll",
        "country": "Maldives",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Addu_Atoll_Maldives.jpg/1280px-Addu_Atoll_Maldives.jpg",
        "highlights": "The southernmost atoll, known for its unique equatorial vegetation, historic WWII sites, and excellent diving spots with diverse coral formations.",
        "rating": "4.5"
      }
    ]
  }
}

[app]: To render a carousel of destinations

[inspiration_agent]: Maldives is an amazing destination! I see three great options:

1.  **Malé:** The capital city, where you can experience local life, markets, and mosques.
2.  **Baa Atoll:** A UNESCO Biosphere Reserve, perfect for snorkeling and diving, with manta rays and whale sharks.
3.  **Addu Atoll:** The southernmost atoll, offering unique vegetation, WWII history, and diverse coral for diving.

Are any of these destinations sound interesting? I can provide you with some activities you can do in the destination you selected.

[user]: "Suggest some acitivities around Baa Atoll"

...

```

In an environment where the events are passed from the server running the agents to an application front-end, the application can use the method in this example to parse and identify which payload is being sent and choose the most appropriate payload renderer / handler.

## Customization

The following are some ideas how one can reuse the concierge and make it your own.

### User Profile System

The system now includes comprehensive user profile management:

- **Accessible Default Profile**: `inclusive_travel_agent/profiles/itinerary_accessible_default.json` includes sample accessibility needs
- **Profile API**: Full CRUD operations for user profiles via REST API
- **Context-Aware Responses**: Chat responses personalized based on user accessibility needs and preferences
- **Frontend Integration**: Ready for frontend onboarding applications

### Load Different Scenarios
- **Empty Profile**: `inclusive_travel_agent/profiles/itinerary_empty_default.json`
- **Seattle Example**: `inclusive_travel_agent/profiles/itinerary_seattle_example.json`
- **Accessible Profile**: `inclusive_travel_agent/profiles/itinerary_accessible_default.json` (default)

Set `INCLUSIVE_TRAVEL_AGENT_SCENARIO` in your `.env` file to change the default profile.


### Make your own premade itinerary for demos

- The Itinerary schema is defined in types.py
- Make a copy of `itinerary_seattle_example.json` and make your own `itinerary` following the schema.
- Use the above steps to load and test your new itinerary.
- For the `user_profile` dict:
  - `passport_nationality` and `home` are mandatory fields, modify only the `address` and `local_prefer_mode`.
  - You can modify / add additional profile fields to the 


### Integration with External APIs

The system includes several external API integrations:

**Current Integrations:**
- **Google AI API**: ML Dev backend for cost-effective AI processing
- **Google Places API**: Location and venue information
- **Wheelmap.org API**: Crowd-sourced accessibility information
- **Airport Accessibility Database**: Comprehensive airport accessibility data
- **Email Services**: SMTP integration for notifications and confirmations

**Enhancement Opportunities:**
- Real flight and hotel booking system integration
- Advanced accessibility databases and certification systems
- Real-time transportation accessibility APIs
- Medical facility accessibility verification services
- Emergency accessibility service coordination systems


### Refining Agents

The following are just the starting ideas:
- A more sophisticated itinerary and activity planning agent; For example, currently the agent does not handle flights with lay-over.
- Better accounting - accuracy in calculating costs on flights, hotels + others.
- A booking agent that is less mundane and more efficient
- For the pre-trip and in-trip agents, there are opportunities to dynamically adjusts the itinerary and resolves trip exceptions

## Troubleshoot

The following occasionally happens while interaction with the agent:
- "Malformed" function call or response, or pydantic errors - when this happens simply tell the agent to "try again". 
- If the agents tries to call a tool that doesn't exist, tell the agent that it is the "wrong tool, try again", the agent  is often able to self correct. 
- Similarly, if you have waited for a while and the agent has stopped in the middle of executing a series of actions, ask the agent "what's next" to nudge it forward.

These happens occasionally, it is likely due to variations in JSON responses that requires more rigorous experimentation on prompts and generation parameters to attain more stable results. Within an application, these retries can also be built into the application as part of exception handling.


## Disclaimer

This agent sample is provided for illustrative purposes only and is not intended for production use. It serves as a basic example of an agent and a foundational starting point for individuals or teams to develop their own agents.

This sample has not been rigorously tested, may contain bugs or limitations, and does not include features or optimizations typically required for a production environment (e.g., robust error handling, security measures, scalability, performance considerations, comprehensive logging, or advanced configuration options).

Users are solely responsible for any further development, testing, security hardening, and deployment of agents based on this sample. We recommend thorough review, testing, and the implementation of appropriate safeguards before using any derived agent in a live or critical system.