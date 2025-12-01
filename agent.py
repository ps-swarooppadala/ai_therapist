"""
Personal Psychologist AI Agent
A simple multi-agent system with:
- Main orchestrator that delegates to specialized agents
- Therapeutic support agent for emotional help
- Task management agent for todos/reminders/scheduling  
- Wellness check-in flow (sequential) for structured assessments

Built with Google ADK (Agent Development Kit)

Restructured into modular components:
- config.py: Configuration settings
- tools/: Memory and task management tools
- agents/: Specialized and root orchestrator agents
"""

import logging
import os

# ============================================================
# LOGGING CONFIGURATION
# ============================================================

# Clean up any previous logs
for log_file in ["logger.log", "web.log", "tunnel.log"]:
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"🧹 Cleaned up {log_file}")

# Configure logging with DEBUG log level
logging.basicConfig(
    filename="logger.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(levelname)s: %(message)s",
)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)

print("✅ Logging configured - logs will be written to logger.log")
logging.info("Personal Psychologist Agent logging initialized")

from google.adk.apps import App, ResumabilityConfig
from google.adk.sessions import InMemorySessionService
from .agents.root_agent import root_agent


# ============================================================
# SERVICE CONFIGURATION
# ============================================================

session_service = InMemorySessionService()


# ============================================================
# APP CONFIGURATION
# ============================================================

app = App(
    name="personal_psychologist",
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)


# ============================================================
# MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":
    logging.info("Starting Personal Psychologist Agent initialization")    
    logging.info(f"Agent initialized with root: {root_agent.name}")
    logging.debug(f"Session service type: {type(session_service).__name__}")
    logging.debug(f"App name: {app.name}")
