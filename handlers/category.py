"""
Category Filter Handlers
AI Powered Government Jobs Telegram Bot
"""

from telegram import Update
from telegram.ext import ContextTypes
from ..database import Database
from ..notifier import format_job

db = Database()


async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, category_type: str):
    jobs = db.get_jobs_by_type(category_type)

    if not jobs:
        await update.message.reply_text(
            f"❌ No active <b>{category_type}</b> job notifications found right now.\n"
            f"Check back later or try /search keyword.",
            parse_mode="HTML"
        )
        return

    await update.message.reply_text(
        f"🔎 Showing top <b>{len(jobs)}</b> job openings in category: <b>{category_type}</b>",
        parse_mode="HTML"
    )

    for job in jobs[:5]:
        await update.message.reply_text(
            format_job(job),
            parse_mode="HTML",
            disable_web_page_preview=True
        )


async def psu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await category_handler(update, context, "PSU")


async def railway(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await category_handler(update, context, "Railway")


async def defence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await category_handler(update, context, "DRDO")


async def central(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await category_handler(update, context, "Central Government")


async def state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await category_handler(update, context, "State Government")


async def teaching(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await category_handler(update, context, "Professor")
