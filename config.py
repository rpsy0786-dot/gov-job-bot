"""
Configuration Manager
AI Powered Government Jobs Telegram Bot
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Telegram API Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID_HERE")

# Database & Scheduler Config
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "jobs.db"))
SEND_TIME = os.getenv("SEND_TIME", "09:00")  # 24-hr format (HH:MM)

# Default User Filtering Preferences
QUALIFICATIONS = [
    "Mechanical",
    "Mechanical Engineering",
    "B.E",
    "B.Tech",
    "M.E",
    "M.Tech",
    "Bachelor of technology",
    "Master of technology"
]

MAX_EXPERIENCE = int(os.getenv("MAX_EXPERIENCE", "8"))

PREFERRED_LOCATIONS = [
    "All India",
    "Central Government",
    "Uttar Pradesh",
    "Madhya Pradesh",
    "Delhi"
]

PREFERRED_DEPARTMENTS = [
    "Mechanical",
    "Engineering",
    "Maintenance",
    "Mechanical Maintenance",
    "Plant Maintenance",
    "Projects",
    "Utilities",
    "Inspection",
    "Reliability",
    "Power Plant"
]
