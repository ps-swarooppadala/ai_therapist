"""
Configuration settings for Personal Psychologist AI Agent
"""

from google.genai import types

# ============================================================
# RETRY CONFIGURATION
# ============================================================

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)
