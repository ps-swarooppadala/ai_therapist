"""
Task management tools for Personal Psychologist AI Agent
Handles tasks, reminders, and scheduling
"""

import logging
from datetime import datetime
from google.adk.tools.tool_context import ToolContext

# Get logger for this module
logger = logging.getLogger(__name__)


def create_task(
    title: str,
    tool_context: ToolContext,
    due_date: str = "",
    priority: str = "medium"
) -> str:
    """Create a task/todo item.
    
    Args:
        title: Task description
        due_date: Optional due date (YYYY-MM-DD)
        priority: low, medium, or high
    """
    user_id = tool_context.user_id
    logger.debug(f"Creating task for user {user_id}: {title}")
    
    if 'tasks' not in tool_context.state:
        tool_context.state['tasks'] = []
        logger.debug("Initialized tasks list in state")
    
    task = {
        "id": len(tool_context.state['tasks']) + 1,
        "user_id": user_id,
        "title": title,
        "due_date": due_date,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    
    # CRITICAL: Create new list to trigger state delta tracking
    tasks = tool_context.state['tasks']
    tasks.append(task)
    tool_context.state['tasks'] = tasks  # Reassign to trigger state change
    
    logger.info(f"Task created (id: {task['id']}) for user {user_id}: {title}")
    logger.debug(f"Total tasks in state: {len(tool_context.state['tasks'])}")
    
    return f"✓ Task created: {title}" + (f" (due: {due_date})" if due_date else "")


def get_tasks(tool_context: ToolContext) -> str:
    """Get all tasks for the current user.
    
    Returns:
        Formatted string listing all tasks, or message if no tasks exist.
    """
    user_id = tool_context.user_id
    logger.debug(f"Retrieving tasks for user: {user_id}")
    
    if 'tasks' not in tool_context.state:
        tool_context.state['tasks'] = []
    
    user_tasks = [t for t in tool_context.state['tasks'] if t.get("user_id") == user_id]
    
    logger.info(f"Found {len(user_tasks)} tasks for user {user_id}")
    logger.debug(f"Total tasks in state: {len(tool_context.state['tasks'])}")
    
    if not user_tasks:
        return "You have no tasks."
    
    result = f"You have {len(user_tasks)} task(s):\n"
    for task in user_tasks:
        due_info = f" (due: {task.get('due_date')})" if task.get('due_date') else ""
        priority = task.get('priority', 'medium')
        result += f"\n• {task.get('title')} - Priority: {priority}{due_info}"
    
    return result


def schedule_reminder(
    title: str,
    date: str,
    time: str,
    tool_context: ToolContext
) -> str:
    """Schedule a reminder or calendar event.
    
    Args:
        title: Event/reminder title
        date: Date (YYYY-MM-DD)
        time: Time (HH:MM)
    """
    user_id = tool_context.user_id
    logger.debug(f"Scheduling reminder for user {user_id}: {title} at {date} {time}")
    
    if 'reminders' not in tool_context.state:
        tool_context.state['reminders'] = []
        logger.debug("Initialized reminders list in state")
    
    reminder = {
        "id": len(tool_context.state['reminders']) + 1,
        "user_id": user_id,
        "title": title,
        "date": date,
        "time": time,
        "created_at": datetime.now().isoformat()
    }
    
    # CRITICAL: Create new list to trigger state delta tracking
    reminders = tool_context.state['reminders']
    reminders.append(reminder)
    tool_context.state['reminders'] = reminders  # Reassign to trigger state change
    
    logger.info(f"Reminder set (id: {reminder['id']}) for user {user_id}: {title} at {date} {time}")
    logger.debug(f"Total reminders in state: {len(tool_context.state['reminders'])}")
    
    return f"✓ Reminder set: {title} on {date} at {time}"


def get_reminders(tool_context: ToolContext) -> str:
    """Get all reminders for the current user.
    
    Returns:
        Formatted string listing all reminders, or message if no reminders exist.
    """
    user_id = tool_context.user_id
    
    if 'reminders' not in tool_context.state:
        tool_context.state['reminders'] = []
    
    user_reminders = [r for r in tool_context.state['reminders'] if r.get("user_id") == user_id]
    
    # Debug logging
    print(f"📅 Reminders for user {user_id}: {len(user_reminders)} reminders")
    print(f"📊 Total reminders in state: {len(tool_context.state['reminders'])}")
    
    if not user_reminders:
        return "You have no reminders scheduled."
    
    result = f"You have {len(user_reminders)} reminder(s):\n"
    for reminder in user_reminders:
        result += f"\n• {reminder.get('title')} - {reminder.get('date')} at {reminder.get('time')}"
        print(f"  - {reminder.get('title')} on {reminder.get('date')} at {reminder.get('time')}")
    
    return result


def get_all_items(tool_context: ToolContext) -> str:
    """Get all tasks and reminders for the current user.
    
    Returns:
        Formatted string listing all tasks and reminders.
    """
    user_id = tool_context.user_id
    
    # Get tasks
    if 'tasks' not in tool_context.state:
        tool_context.state['tasks'] = []
    user_tasks = [t for t in tool_context.state['tasks'] if t.get("user_id") == user_id]
    
    # Get reminders
    if 'reminders' not in tool_context.state:
        tool_context.state['reminders'] = []
    user_reminders = [r for r in tool_context.state['reminders'] if r.get("user_id") == user_id]
    
    # Debug logging
    print(f"📊 All items for user {user_id}: {len(user_tasks)} tasks, {len(user_reminders)} reminders")
    
    if not user_tasks and not user_reminders:
        return "You have no tasks or reminders."
    
    result = ""
    
    if user_tasks:
        result += f"\n📋 **Tasks** ({len(user_tasks)}):\n"
        for task in user_tasks:
            due_info = f" (due: {task.get('due_date')})" if task.get('due_date') else ""
            priority = task.get('priority', 'medium')
            result += f"\n• {task.get('title')} - Priority: {priority}{due_info}"
    
    if user_reminders:
        result += f"\n\n📅 **Reminders** ({len(user_reminders)}):\n"
        for reminder in user_reminders:
            result += f"\n• {reminder.get('title')} - {reminder.get('date')} at {reminder.get('time')}"
    
    return result.strip()
