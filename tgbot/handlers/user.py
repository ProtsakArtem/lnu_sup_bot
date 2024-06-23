from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from tgbot.services.db import all_text
from tgbot.keyboards.reply import start_keyboard
user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, text=all_text["start_text"], reply_markup=start_keyboard)


