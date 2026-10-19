from os import getenv
from asyncio import run

from telegram import Bot
from telegram.constants import ParseMode
from dotenv import load_dotenv

load_dotenv()

TOKEN_BOT = getenv("TOKEN", "")
CHAT = getenv("CHAT", "")

print(TOKEN_BOT, CHAT)
async def enviar_mensagem(texto):
    bot = Bot(token=TOKEN_BOT)
    async with bot:
        await bot.send_message(
            chat_id=CHAT, 
            text=texto, 
            parse_mode=ParseMode.HTML
        )
