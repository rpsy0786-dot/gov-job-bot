from telegram import Bot
from config import BOT_TOKEN, CHAT_ID

bot = Bot(BOT_TOKEN)

async def send_message(msg):
    await bot.send_message(
        chat_id=CHAT_ID,
        text=msg
    )
