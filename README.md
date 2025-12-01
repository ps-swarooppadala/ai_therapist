# Personal Psychologist AI Agent

A sophisticated multi-agent system built with Google ADK that provides empathetic personal assistance through therapeutic support, task management, and intelligent scheduling.

## 🌟 Features

### Core Capabilities
- **Memory Management**: Remembers user information, preferences, and conversation history
- **Therapeutic Support**: Provides empathetic emotional support with evidence-based coping strategies
- **Task Management**: Manages todos and reminders with automatic date/time awareness
- **Goal Setting**: Creates actionable goals with routines and tracks progress
- **Web Search**: Searches for evidence-based information and research
- **Pattern Learning**: Learns what works for each user through feedback

### Agent Architecture

#### 1. **Root Orchestrator Agent** (`root_agent`)
Routes user requests to specialized agents based on intent:
- Emotional/therapeutic requests → Therapeutic Support Agent
- Task/reminder management → Task Manager Agent
- Goal setting and tracking → Goal Refinement Agent
- Information/research queries → Search Agent

#### 2. **Therapeutic Support Agent** (`therapeutic_agent`)
Provides empathetic emotional support with:
- Loads user memory to personalize responses
- Evidence-based coping strategies for stress, anxiety, sadness, overwhelm
- Learning system that remembers helpful responses
- Brief, conversational support style

#### 3. **Task Manager Agent** (`task_agent`)
Manages tasks and reminders with:
- **Automatic date/time awareness** - uses `get_current_datetime()` tool
- **Smart date parsing** - understands "tomorrow", "next week", etc.
- **Clear task vs reminder distinction**:
  - Tasks = Todo items (optional due dates)
  - Reminders = Time-specific events (meetings, appointments)
- Tools for creating, listing, and managing items

#### 4. **Goal Refinement Agent** (`goal_refinement_agent`)
Fast, action-oriented goal creation:
- Creates goals with specific routines and schedules
- Minimal questions (1-2 max) before creating goal
- Approval workflow before finalizing
- Goal tracking and status updates

#### 5. **Search Agent** (`search_agent`)
Web search for information:
- Uses Google Search integration
- Focuses on evidence-based, reputable sources
- Synthesizes findings into accessible summaries
- Ideal for research questions and psychoeducation

### Session State Management
- Uses InMemorySessionService to maintain state during sessions
- Stores user memories, tasks, reminders, goals, and therapeutic patterns
- Persists learning across conversations within the same session

## 📁 Project Structure

```
ai_therapist/
├── agent.py                        # Main application setup
├── config.py                       # Retry configuration
├── adk.yaml                        # ADK configuration
├── __init__.py                     # Package initialization
├── .env                            # Environment configuration (API keys)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore patterns
├── ai_assistant_agent.ipynb        # Testing/getting started notebook (optional)
├── agents/
│   ├── root_agent.py              # Main orchestrator
│   ├── specialized_agents.py     # Therapeutic & task agents
│   ├── goal_refinement_agent.py  # Goal setting agent
│   ├── search_agent.py            # Web search agent
│   ├── sequential_agent.py       # Sequential agent pattern (unused)
│   └── __init__.py
└── tools/
    ├── memory_tools.py            # Memory management
    ├── task_tools.py              # Task & reminder management
    ├── goal_tools.py              # Goal and routine management
    ├── datetime_tools.py          # Current date/time tools
    └── __init__.py
```

**Note**: The `ai_assistant_agent.ipynb` notebook was used for initial testing and getting started with the ADK framework. It's not required for running the agent but can be useful for learning and experimentation.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Update the `.env` file with your Google API key:

```bash
GOOGLE_API_KEY=your_api_key_here
```

Get your API key from: https://aistudio.google.com/app/apikey

### 3. Run the Agent

#### Interactive Web UI (Recommended)

```bash
cd ai_therapist
adk web
```

This will start a web interface at `http://localhost:8000` where you can interact with the agent.

#### Command Line Interface

```bash
adk run ai_therapist
```

#### Programmatic Usage

```python
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from ai_therapist import root_agent
from google.genai import types

# Create runner
runner = Runner(
    app_name="personal_psychologist_app",
    agent=root_agent,
    session_service=InMemorySessionService()
)

# Run query
async def chat(message):
    content = types.Content(role='user', parts=[types.Part(text=message)])
    async for event in runner.run_async(
        user_id="user123",
        session_id="session456",
        new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"[{event.author}]: {part.text}")

# Example usage
import asyncio
asyncio.run(chat("Hi! My name is Alice and I'm interested in mindfulness."))
```

## 🤖 Agent Architecture

### Root Agent: Personal Assistant
- Coordinates all specialized agents based on user intent
- Routes requests to appropriate agent (therapeutic, task, goal, search)
- Maintains conversation flow and context
- Uses `gemini-2.5-flash-lite` model for fast responses

### Specialized Agents:

#### Therapeutic Support Agent
- **Purpose**: Emotional support and coping strategies
- **Model**: `gemini-2.5-flash-lite`
- **Tools**: `load_memory`, `save_therapeutic_pattern`
- **Approach**: Brief, warm responses with evidence-based techniques
- **Coping strategies**: Breathing exercises, grounding, reframing, self-compassion

#### Task Manager Agent  
- **Purpose**: Task and reminder management
- **Model**: `gemini-2.5-flash-lite`
- **Tools**: `get_current_datetime`, `create_task`, `get_tasks`, `schedule_reminder`, `get_reminders`, `get_all_items`
- **Features**: Auto date parsing, clear task/reminder distinction, organized list views

#### Goal Refinement Agent
- **Purpose**: Fast goal creation with routines
- **Model**: `gemini-2.0-flash`
- **Tools**: `get_current_datetime`, `create_goal_with_routine`, `approve_goal`, `get_goal`, `list_goals`, `update_goal_status`
- **Workflow**: 1-2 questions max → create goal → get approval
- **Features**: Routine scheduling, progress tracking, status updates

#### Search Agent
- **Purpose**: Web search for evidence-based information
- **Model**: `gemini-2.5-flash-lite`
- **Tools**: `google_search`
- **Focus**: Reputable sources, research institutions, medical sites
- **Output**: Clear, accessible summaries of findings

### Tools Available:

**Memory Tools** (`memory_tools.py`):
- `save_to_memory`: Store user information
- `load_memory`: Retrieve user information
- `save_therapeutic_pattern`: Record feedback on therapeutic responses

**Task Tools** (`task_tools.py`):
- `create_task`: Create todo items
- `get_tasks`: List all tasks
- `schedule_reminder`: Create time-specific reminders
- `get_reminders`: List all reminders
- `get_all_items`: View tasks and reminders together

**Goal Tools** (`goal_tools.py`):
- `create_goal_with_routine`: Create goal with routine details
- `approve_goal`: Finalize and activate a goal
- `get_goal`: Retrieve specific goal details
- `list_goals`: View all user goals
- `update_goal_status`: Mark goals as completed/paused

**DateTime Tools** (`datetime_tools.py`):
- `get_current_datetime`: Get current date/time for automatic calculations

## 💬 Example Interactions

### Emotional Support
```
User: I'm feeling really stressed about work
Agent: I hear you - work stress is tough. Try this: Take 3 slow, deep 
breaths right now. Count to 4 on the inhale, hold for 4, exhale for 4. 
It helps calm your nervous system instantly. What's one small thing you 
could do in the next 5 minutes to feel more in control?
```

### Task Management
```
User: Add "buy groceries" to my todo list
Agent: ✅ Created task: "buy groceries"

User: Remind me to call mom tomorrow at 2pm
Agent: ✅ Scheduled reminder: "call mom" for 2025-12-02 at 14:00

User: Show me what I have to do
Agent: Here's what you have:

📋 Tasks:
• buy groceries

⏰ Reminders:
• call mom - 2025-12-02 at 14:00
```

### Goal Setting
```
User: I want to exercise more
Agent: Great! Let me create a goal for you. Should we start tomorrow 
or this Monday?

User: Tomorrow
Agent: Perfect! Here's your goal:

**Morning Fitness Habit**
Goal: Exercise regularly to build strength and energy
Routine: 
- 15 min workout each morning
- Start with stretches
- Do bodyweight exercises (squats, pushups, planks)
Frequency: 3x per week (Mon/Wed/Fri)
Duration: 30 days
Start: 2025-12-02

Ready to approve this goal?

User: Yes
Agent: 🎯 Goal approved and activated! I'll help you track your progress.
```

### Web Search
```
User: What does research say about meditation for anxiety?
Agent: [Searches for evidence-based information]

Research shows meditation can significantly help with anxiety:
- Multiple studies find 8 weeks of mindfulness meditation reduces anxiety 
  symptoms by 30-40%
- Works by training attention away from worry and toward present moment
- Brain scans show decreased activity in anxiety-related regions
- Most effective when practiced daily for 10-20 minutes

Sources from NIH, Harvard Medical School, and peer-reviewed journals.
```

### Learning from Feedback
```
User: I'm overwhelmed with everything
Agent: I hear you. When everything feels like too much, try this: 
Write down just ONE thing you'll do in the next hour. Not the whole 
list, just one thing. Finishing something small helps break the paralysis.

User: That really helps, thanks
Agent: I'm glad! I'll remember this approach works well for you when 
you're feeling overwhelmed.
```

## 🔧 Technical Details

### State Management

All data is stored in `tool_context.state` with the following structure:

```python
{
    "user_memories": {
        "user_id": {
            "info_key": "value",
            "name": "Alice",
            "interests": ["mindfulness"]
        }
    },
    "tasks": [
        {
            "id": 1,
            "user_id": "...",
            "task": "buy groceries",
            "due_date": None,
            "completed": False,
            "created_at": "2025-12-01T10:00:00"
        }
    ],
    "reminders": [
        {
            "id": 1,
            "user_id": "...",
            "reminder": "call mom",
            "date": "2025-12-02",
            "time": "14:00",
            "created_at": "2025-12-01T10:00:00"
        }
    ],
    "goals": [
        {
            "id": 1,
            "user_id": "...",
            "title": "Morning Fitness Habit",
            "description": "Exercise regularly",
            "routine": "15 min workout...",
            "frequency": "3x per week",
            "duration": "30 days",
            "start_date": "2025-12-02",
            "status": "active",
            "created_at": "2025-12-01T10:00:00"
        }
    ],
    "therapeutic_patterns": {
        "user_id": {
            "pattern_key": {
                "helpful_responses": [...],
                "unhelpful_responses": [...]
            }
        }
    }
}
```

### Retry Configuration

Uses exponential backoff with jitter for API calls:
- Initial delay: 1 second
- Max delay: 60 seconds  
- Max retries: 5
- Strategy: Exponential with jitter

### Customization

#### Adding Custom Tools

Create a new tool in the appropriate `tools/` file:

```python
def my_custom_tool(param: str, tool_context: ToolContext) -> str:
    """Description of what the tool does."""
    user_id = tool_context.user_id
    # Your logic here
    return "Result"
```

Then import and add to the appropriate agent in `agents/`:

```python
from ..tools.my_tools import my_custom_tool

agent = LlmAgent(
    name="my_agent",
    tools=[my_custom_tool, ...],
    # ... other config
)
```

#### Adding New Agents

Create a new agent file in `agents/` or add to existing files:

```python
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from ..config import retry_config
from ..tools.my_tools import my_tool

my_new_agent = LlmAgent(
    name="my_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="What this agent does",
    instruction="Detailed instructions for the agent...",
    tools=[my_tool]
)
```

Then import in `root_agent.py` and add to the sub-agents list.

#### Changing Models

Update the model in any agent file:

```python
model=Gemini(
    model="gemini-2.5-flash-lite",  # Fastest, good for simple tasks
    # model="gemini-2.5-flash",     # Balanced speed/capability
    # model="gemini-2.0-flash",     # Latest features
    # model="gemini-2.0-pro",       # Most capable
    retry_options=retry_config
)
```

## 📊 Data Storage

The agent uses `InMemorySessionService` for storage during sessions:
- `user_memories`: User information and preferences
- `tasks`: Todo items with optional due dates
- `reminders`: Time-specific events
- `goals`: Goals with routines and progress tracking
- `therapeutic_patterns`: Learned therapeutic responses

**Note**: Data is lost when the agent restarts. For persistent storage, integrate a database service or implement custom session persistence.

## 🧪 Testing

```bash
# Run in debug mode
adk run ai_therapist --verbose

# Evaluate agent performance
adk eval ai_therapist path/to/evalset.json
```

## 🚢 Deployment

### Deploy to Google Cloud Run

```bash
adk deploy cloud-run ai_therapist \
  --project your-project-id \
  --region us-central1
```

### Deploy to Vertex AI Agent Engine

```bash
adk deploy agent-engine ai_therapist \
  --project your-project-id \
  --location us-central1 \
  --display-name "Personal Psychologist"
```

## 📝 License

This project is built with Google ADK and follows its licensing terms.

## 🤝 Contributing

Feel free to extend this agent with:
- Additional specialized agents for specific domains
- Integration with external services via MCP (Model Context Protocol)
- Enhanced memory with vector databases for semantic search
- Persistent storage backends (PostgreSQL, MongoDB, etc.)
- Custom evaluation metrics and test sets
- Voice interface integration
- Multi-modal capabilities (image understanding, audio)

## 📚 Resources

- [Google ADK Documentation](https://github.com/google/adk-python)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Model Context Protocol](https://github.com/anthropics/mcp)

## ⚠️ Important Notes

- **API Key Security**: Never commit your `.env` file with real API keys. Use environment variables in production.
- **Demo Purpose**: This is a demonstration agent - review and enhance security for production use
- **Medical Disclaimer**: Therapeutic features are for emotional support only, not professional medical advice or therapy
- **Data Persistence**: Data is stored in-memory and lost on restart. Implement persistent storage for production
- **Testing Notebook**: The `ai_assistant_agent.ipynb` notebook is for learning/testing only and not required to run the agent
