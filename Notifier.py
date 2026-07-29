"""
Telegram Notifier Engine
AI Powered Government Jobs Telegram Bot
"""

import requests
from typing import List
from .models.job import Job
from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from .utils.logger import telegram_logger


ORG_PORTAL_MAP = {
    "drdo": "https://rac.gov.in",
    "ongc": "https://ongcindia.com",
    "rrb": "https://www.rrbald.gov.in",
    "ntpc": "https://careers.ntpc.co.in",
    "barc": "https://barcoces.gov.in",
    "uppsc": "https://uppsc.up.nic.in",
    "upsc": "https://upsc.gov.in",
    "isro": "https://isro.gov.in",
    "ssc": "https://ssc.gov.in",
    "iocl": "https://iocl.com",
    "hpcl": "https://hindustanpetroleum.com",
    "bpcl": "https://bharatpetroleum.in",
    "gail": "https://gailonline.com",
    "bhel": "https://bhel.com",
    "bel": "https://bel-india.in",
    "npcil": "https://npcilcareers.co.in"
}


def resolve_job_portal(job: Job) -> str:
    if job.apply_link and job.apply_link.startswith("http"):
        return job.apply_link
    org_lower = (job.organisation or job.source or "").lower()
    for key, portal in ORG_PORTAL_MAP.items():
        if key in org_lower:
            return portal
    return "https://www.india.gov.in/my-government/jobs"


def format_job(job: Job) -> str:
    """
    Formats a Job object into HTML styled message for Telegram.
    """
    title = job.title or "Government Job Opening"
    org = job.organisation or "Government Organisation"
    qualification = job.qualification or "B.E / B.Tech / Diploma / Any Graduate"
    vacancies = job.vacancies or "As per notification"
    last_date = job.last_date or "Refer Official PDF"
    salary = job.salary or "Standard Pay Scale"
    apply_link = resolve_job_portal(job)
    pdf_link = job.notification_pdf if (job.notification_pdf and job.notification_pdf.startswith("http")) else apply_link
    job_type = job.job_type or "Government"

    message = (
        f"<b>🏛️ {org} Recruitment Notification</b>
"
        f"━━━━━━━━━━━━━━━━━━

"
        f"📌 <b>Post Title:</b> {title}
"
        f"🏢 <b>Category:</b> {job_type}
"
        f"🎓 <b>Qualification:</b> {qualification}
"
        f"👥 <b>Total Vacancies:</b> {vacancies}
"
        f"💰 <b>Salary / Pay Scale:</b> {salary}
"
        f"⏳ <b>Last Date to Apply:</b> <code>{last_date}</code>
"
        f"⭐ <b>AI Relevancy Match:</b> {job.score:.0f}%

"
        f"🔗 <a href="{apply_link}"><b>Click Here to Apply Online</b></a>
"
    )

    if pdf_link and pdf_link != apply_link:
        message += f"📄 <a href="{pdf_link}"><b>Download Official PDF Notification</b></a>
"

    message += "━━━━━━━━━━━━━━━━━━
🤖 <i>AI Powered Govt Jobs Alert</i>"
    return message


class TelegramNotifier:
    """
    Handles outbound HTTP POST calls to Telegram Bot API.
    """

    def __init__(self, bot_token: str = None, chat_id: str = None):
        self.bot_token = bot_token or TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or TELEGRAM_CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        if not self.bot_token or self.bot_token == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
            telegram_logger.warning("Telegram Bot Token is not configured. Skipping message send.")
            return False

        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": False
        }

        try:
            res = requests.post(self.api_url, json=payload, timeout=15)
            if res.status_code == 200:
                telegram_logger.info("Successfully delivered message to Telegram channel/chat.")
                return True
            else:
                telegram_logger.error("Failed to send message. Telegram response: %s", res.text)
                return False
        except Exception as e:
            telegram_logger.exception("Exception while calling Telegram API: %s", e)
            return False

    def send_jobs(self, jobs: List[Job]) -> int:
        sent_count = 0
        for job in jobs:
            msg = format_job(job)
            if self.send_message(msg):
                sent_count += 1
        return sent_count
  
