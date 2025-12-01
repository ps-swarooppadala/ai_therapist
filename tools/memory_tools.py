"""
Memory management tools for Personal Psychologist AI Agent
Handles user memory, preferences, and therapeutic patterns
"""

import logging
from datetime import datetime
from typing import Dict, Any
from google.adk.tools.tool_context import ToolContext

# Get logger for this module
logger = logging.getLogger(__name__)


def load_memory(tool_context: ToolContext) -> Dict[str, Any]:
    """Load comprehensive user memory including personal info, preferences, and therapeutic patterns.
    
    Returns:
        Complete user memory including:
        - personal_details: name, interests
        - preferences: communication style
        - therapeutic_patterns: what responses work/don't work
        - history: interaction log
    """
    user_id = tool_context.user_id
    logger.debug(f"Loading memory for user: {user_id}")
    
    if 'user_memories' not in tool_context.state:
        tool_context.state['user_memories'] = {}
        logger.debug("Initialized user_memories in state")
    
    if user_id not in tool_context.state['user_memories']:
        tool_context.state['user_memories'][user_id] = {
            "personal_details": {},
            "preferences": {},
            "therapeutic_patterns": {
                "triggers": {},  # Maps triggers to response history
                "preferred_styles": [],
                "avoided_styles": []
            },
            "history": [],
            "interests": []
        }
        logger.info(f"Created new memory structure for user: {user_id}")
    else:
        logger.debug(f"Memory found for user: {user_id}")
    
    result = {"user_id": user_id, "memory": tool_context.state['user_memories'][user_id]}
    logger.debug(f"Memory loaded with keys: {list(result['memory'].keys())}")
    return result


def save_to_memory(key: str, value: str, tool_context: ToolContext) -> str:
    """Save information to user memory.
    
    Args:
        key: Category (personal_details, preferences, history, interests, name)
        value: Value to store
    """
    user_id = tool_context.user_id
    logger.debug(f"Saving to memory - user: {user_id}, key: {key}, value: {value}")
    
    if 'user_memories' not in tool_context.state:
        tool_context.state['user_memories'] = {}
    
    if user_id not in tool_context.state['user_memories']:
        tool_context.state['user_memories'][user_id] = {
            "personal_details": {},
            "preferences": {},
            "therapeutic_patterns": {"triggers": {}, "preferred_styles": [], "avoided_styles": []},
            "history": [],
            "interests": []
        }
    
    memory = tool_context.state['user_memories'][user_id]
    
    if key == "name":
        memory["personal_details"]["name"] = value
    elif key == "interests":
        interests = memory["interests"]
        interests.append(value)
        memory["interests"] = interests
    elif key == "preferences":
        memory["preferences"]["general"] = value
    elif key == "history":
        history = memory["history"]
        history.append(value)
        memory["history"] = history
    else:
        memory[key] = value
    
    # Reassign to trigger state change
    tool_context.state['user_memories'][user_id] = memory
    
    logger.info(f"Successfully saved {key} to memory for user {user_id}")
    return f"✓ Saved {key} to memory"


def save_therapeutic_pattern(
    trigger: str,
    response: str,
    helpful: bool,
    tool_context: ToolContext
) -> str:
    """Save therapeutic response pattern - tracks what works/doesn't work.
    
    Args:
        trigger: Emotional trigger (e.g., "overwhelmed", "procrastinating")
        response: The response given
        helpful: True if user found it helpful, False otherwise
    """
    user_id = tool_context.user_id
    logger.debug(f"Saving therapeutic pattern - user: {user_id}, trigger: {trigger}, helpful: {helpful}")
    
    if 'user_memories' not in tool_context.state:
        tool_context.state['user_memories'] = {}
    
    if user_id not in tool_context.state['user_memories']:
        tool_context.state['user_memories'][user_id] = {
            "personal_details": {},
            "preferences": {},
            "therapeutic_patterns": {"triggers": {}, "preferred_styles": [], "avoided_styles": []},
            "history": [],
            "interests": []
        }
    
    patterns = tool_context.state['user_memories'][user_id]["therapeutic_patterns"]
    trigger_key = trigger.lower().strip()
    
    if trigger_key not in patterns["triggers"]:
        patterns["triggers"][trigger_key] = {
            "helpful_responses": [],
            "unhelpful_responses": []
        }
    
    entry = {"response": response, "timestamp": datetime.now().isoformat()}
    
    if helpful:
        patterns["triggers"][trigger_key]["helpful_responses"].append(entry)
        logger.info(f"Marked response as HELPFUL for trigger '{trigger}' (user: {user_id})")
        return f"✓ Marked as helpful for '{trigger}'"
    else:
        patterns["triggers"][trigger_key]["unhelpful_responses"].append(entry)
        logger.info(f"Marked response as UNHELPFUL for trigger '{trigger}' (user: {user_id})")
        return f"✓ Marked as unhelpful for '{trigger}' - will try different approach next time"
