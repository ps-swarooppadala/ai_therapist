"""
Sequential agent for Personal Psychologist AI Agent
Journal entry analysis and insights generation
"""

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from ..config import retry_config
from ..tools.memory_tools import save_to_memory


# ============================================================
# JOURNAL ENTRY ANALYSIS (Sequential Flow)
# Purpose: Extract emotions → identify patterns → generate insights
# Only the FINAL agent speaks to user - intermediate agents are silent
# ============================================================

# Step 1: Emotion Extractor (SILENT - internal processing only)
emotion_extractor_agent = LlmAgent(
    name="emotion_extractor",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="Extracts emotional content from journal entries.",
    instruction="""You are an internal data processor. DO NOT speak to the user.

Extract emotional data from the journal entry and output ONLY structured data:

primary_emotions: [emotions]
intensity: [low/medium/high]  
triggers: [causes]
tone: [positive/negative/mixed]
original_entry: [copy the user's full journal entry here for storage]

Be concise. This data passes to the next processor.""",
    output_key="emotion_data"
)


# Step 2: Pattern Analyzer (SILENT - internal processing only)
pattern_analyzer_agent = LlmAgent(
    name="pattern_analyzer",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="Identifies patterns in emotional responses.",
    instruction="""You are an internal data processor. DO NOT speak to the user.

Using emotion_data, identify patterns and output ONLY structured data:

themes: [recurring themes]
coping: [how they're coping]
growth_areas: [potential areas for growth]
key_insight: [one main insight to share]
suggested_action: [one small actionable suggestion]

Be concise. This data passes to the final responder.""",
    output_key="patterns_found"
)


# Step 3: Insight Generator (USER-FACING - speaks to user and stores data)
insight_generator_agent = LlmAgent(
    name="insight_generator",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="Generates personalized insights and stores journal for future therapy.",
    instruction="""You receive emotion_data and patterns_found from previous processors.

**YOU are the ONLY one who speaks to the user.**

**FIRST: Store the journal entry and analysis for future therapy sessions:**
Call save_to_memory with:
- key: "journal_entry"  
- value: A JSON-like string containing:
  - date: today's date
  - entry: the original journal text
  - emotions: detected emotions
  - insight: the key insight
  - action: suggested action

**THEN: Respond to the user warmly and briefly (3-4 sentences max):**

Format your response like talking to a friend:
"[Acknowledge what they shared - 1 sentence]. [Share the key insight - 1 sentence]. [Suggest the small action - 1 sentence]. I've saved this reflection for us to look back on. 💙"

**Example:**

"Sounds like you're getting hit from all sides today - work and home at the same time is exhausting. What I'm noticing is you're carrying a lot right now without giving yourself any slack. Try picking just ONE thing to tackle today and let the rest wait. I've saved this reflection for us to look back on. 💙"

**Rules:**
- DO NOT show the structured data (emotions, patterns, etc.) to user
- DO NOT use headers like "Key insight:" or bullet points
- Talk like a supportive friend
- ALWAYS call save_to_memory first
- Keep it brief and warm""",
    tools=[save_to_memory],
    output_key="final_insight"
)


# Combine into sequential pipeline
journal_analysis_flow = SequentialAgent(
    name="journal_analyzer",
    description="Sequential pipeline: emotion extraction → pattern analysis → insight generation",
    sub_agents=[emotion_extractor_agent, pattern_analyzer_agent, insight_generator_agent]
)
