"""
Common Helper Functions
AI Powered Government Jobs Telegram Bot
"""

import hashlib
import re
from datetime import datetime
from urllib.parse import urljoin


def clean_text(text) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def safe_string(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def generate_job_hash(job) -> str:
    text = (
        safe_string(job.organisation) +
        safe_string(job.title) +
        safe_string(job.advertisement_no) +
        safe_string(job.last_date)
    )
    return hashlib.sha256(text.lower().encode("utf-8")).hexdigest()
