"""
Goal and routine management tools for Personal Assistant
Handles creating, saving, fetching, and displaying goals with routines
"""

from datetime import datetime
from typing import Dict, Any, List
from google.adk.tools.tool_context import ToolContext


def create_goal_with_routine(
    title: str,
    goal_description: str,
    routine: str,
    frequency: str,
    duration: str,
    start_date: str,
    tool_context: ToolContext
) -> str:
    """Create a goal with an associated routine.
    
    Args:
        title: Short title for the goal (e.g., "Morning Fitness", "Better Sleep")
        goal_description: What the user wants to achieve
        routine: The specific routine/steps to follow
        frequency: How often (e.g., "3x per week", "daily", "every morning")
        duration: How long to commit (e.g., "1 month", "30 days", "2 weeks")
        start_date: When to start (YYYY-MM-DD format)
    
    Returns:
        Confirmation message with goal ID for approval
    """
    user_id = tool_context.user_id
    
    if 'goals' not in tool_context.state:
        tool_context.state['goals'] = []
    
    goal_id = len(tool_context.state['goals']) + 1
    
    goal = {
        "id": goal_id,
        "user_id": user_id,
        "title": title,
        "description": goal_description,
        "routine": routine,
        "frequency": frequency,
        "duration": duration,
        "start_date": start_date,
        "status": "pending_approval",
        "created_at": datetime.now().isoformat(),
        "approved": False
    }
    
    # Store temporarily for approval
    goals = tool_context.state['goals']
    goals.append(goal)
    tool_context.state['goals'] = goals
    
    # Format output
    result = f"""
📋 Goal Created (ID: {goal_id}) - Pending Your Approval

**{title}**

🎯 Goal: {goal_description}

📅 Routine:
{routine}

⏰ Frequency: {frequency}
⏳ Duration: {duration}
🚀 Start Date: {start_date}

Type 'approve' to activate this goal, or tell me what you'd like to change.
"""
    
    return result


def approve_goal(goal_id: int, tool_context: ToolContext) -> str:
    """Approve and activate a pending goal.
    
    Args:
        goal_id: The ID of the goal to approve
    
    Returns:
        Confirmation message
    """
    user_id = tool_context.user_id
    
    if 'goals' not in tool_context.state:
        return "❌ No goals found to approve."
    
    goals = tool_context.state['goals']
    goal_found = False
    
    for goal in goals:
        if goal.get('id') == goal_id and goal.get('user_id') == user_id:
            goal['approved'] = True
            goal['status'] = 'active'
            goal['approved_at'] = datetime.now().isoformat()
            goal_found = True
            break
    
    if not goal_found:
        return f"❌ Goal ID {goal_id} not found."
    
    # Reassign to trigger state change
    tool_context.state['goals'] = goals
    
    return f"✅ Goal '{goal['title']}' is now active! Let's make it happen! 🎉"


def get_goal(goal_id: int, tool_context: ToolContext) -> str:
    """Retrieve and display a specific goal by ID.
    
    Args:
        goal_id: The ID of the goal to retrieve
    
    Returns:
        Formatted goal details
    """
    user_id = tool_context.user_id
    
    if 'goals' not in tool_context.state:
        return "❌ No goals found."
    
    for goal in tool_context.state['goals']:
        if goal.get('id') == goal_id and goal.get('user_id') == user_id:
            status_emoji = "✅" if goal.get('approved') else "⏳"
            status_text = "Active" if goal.get('approved') else "Pending Approval"
            
            result = f"""
{status_emoji} Goal #{goal_id}: **{goal['title']}** ({status_text})

🎯 Goal: {goal['description']}

📅 Routine:
{goal['routine']}

⏰ Frequency: {goal['frequency']}
⏳ Duration: {goal['duration']}
🚀 Start Date: {goal['start_date']}
📆 Created: {goal['created_at'][:10]}
"""
            return result
    
    return f"❌ Goal ID {goal_id} not found."


def list_goals(tool_context: ToolContext) -> str:
    """List all goals for the current user.
    
    Returns:
        Formatted list of all goals
    """
    user_id = tool_context.user_id
    
    if 'goals' not in tool_context.state:
        return "You don't have any goals yet. Let's create one!"
    
    user_goals = [g for g in tool_context.state['goals'] if g.get('user_id') == user_id]
    
    if not user_goals:
        return "You don't have any goals yet. Let's create one!"
    
    result = f"📋 Your Goals ({len(user_goals)}):\n\n"
    
    for goal in user_goals:
        status_emoji = "✅" if goal.get('approved') else "⏳"
        status_text = "Active" if goal.get('approved') else "Pending"
        
        result += f"{status_emoji} #{goal['id']}: **{goal['title']}** - {status_text}\n"
        result += f"   {goal['description']}\n"
        result += f"   {goal['frequency']} | Start: {goal['start_date']}\n\n"
    
    result += "\nUse 'show goal #ID' to see full details of any goal."
    
    return result


def update_goal_status(
    goal_id: int,
    status: str,
    tool_context: ToolContext
) -> str:
    """Update the status of a goal (e.g., completed, paused, cancelled).
    
    Args:
        goal_id: The ID of the goal
        status: New status (active, completed, paused, cancelled)
    
    Returns:
        Confirmation message
    """
    user_id = tool_context.user_id
    
    if 'goals' not in tool_context.state:
        return "❌ No goals found."
    
    goals = tool_context.state['goals']
    goal_found = False
    
    for goal in goals:
        if goal.get('id') == goal_id and goal.get('user_id') == user_id:
            goal['status'] = status
            goal['updated_at'] = datetime.now().isoformat()
            goal_found = True
            break
    
    if not goal_found:
        return f"❌ Goal ID {goal_id} not found."
    
    # Reassign to trigger state change
    tool_context.state['goals'] = goals
    
    status_messages = {
        'completed': f"🎉 Congratulations! Goal '{goal['title']}' marked as completed!",
        'paused': f"⏸️ Goal '{goal['title']}' paused. You can resume it anytime.",
        'cancelled': f"🚫 Goal '{goal['title']}' cancelled.",
        'active': f"✅ Goal '{goal['title']}' is now active!"
    }
    
    return status_messages.get(status, f"✓ Goal status updated to: {status}")
