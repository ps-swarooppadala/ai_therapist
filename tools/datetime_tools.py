"""
DateTime tools for Personal Psychologist AI Agent
Provides current date and time information for scheduling
"""

from datetime import datetime
from google.adk.tools.tool_context import ToolContext


def get_current_datetime(tool_context: ToolContext) -> str:
    """Get the current date and time for scheduling tasks and reminders.
    
    Returns:
        Current date (YYYY-MM-DD) and time (HH:MM) in simple format.
        Use this to calculate relative dates like 'tomorrow' or 'next Friday'.
    """
    now = datetime.now()
    return f"Date: {now.strftime('%Y-%m-%d')} ({now.strftime('%A')}), Time: {now.strftime('%H:%M')}"
