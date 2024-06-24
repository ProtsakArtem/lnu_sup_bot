from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from tgbot.services.db import all_text
from tgbot.keyboards.reply import start_keyboard, support_keyboard, back_keyboard
from tgbot.keyboards.inline import faq_keyboard
from tgbot.states import fsm


user_router = Router()


@user_router.message(CommandStart(), StateFilter(None))
async def user_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, text=all_text["start_text"], reply_markup=start_keyboard)


@user_router.message(F.text=="❓ Найчастіші питання")
async def user_stop(message: Message, bot:Bot):
    await bot.send_message(message.from_user.id, text="Що вам підказати?", reply_markup=faq_keyboard)


@user_router.message(F.text=="👭Студ. організації")
async def stud_org(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, text=all_text["stud_orgs_text"])


@user_router.message(F.text=="🔗Корисні посилання")
async def help_links(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, text=all_text["help_links_text"])


@user_router.message(F.text=="🙋 Анонімний чат")
async def anon_chat(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, text="123")


@user_router.message(Command("chat"))
async def chat_test(message: Message, bot:Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Обери що саме ти хочеш зробити 👇", reply_markup=support_keyboard)
    await state.set_state(fsm.Choose_support)


@user_router.message(StateFilter(fsm.Choose_support))
async def supp_choose_handle(message: Message, bot:Bot, state: FSMContext):
    if message.text.__contains__("чат"):
        await state.set_state(fsm.Chat)
        await bot.send_message(message.from_user.id, text="Очікуйте на під'єднання адміністратора", reply_markup=ReplyKeyboardRemove())
    elif message.text.__contains__("скарга"):
        await state.set_state(fsm.Scarga)
        await bot.send_message(message.from_user.id, text='Напишіть вашу скаргу ОДНИМ ПОВІДОМЛЕННЯМ 👇\nЯкщо ви натиснули випадково, натисніть кнопку "Назад"', reply_markup=back_keyboard)

    elif message.text.__contains__("Назад"):
        await state.set_state(None)
        await bot.send_message(message.from_user.id, text=all_text["start_text"], reply_markup=start_keyboard)


@user_router.message(StateFilter(fsm.Scarga))
async def scarga_handler(message: Message, bot: Bot, state: FSMContext):
    if message.text == "Назад ⬅️":
        await bot.send_message(message.from_user.id, text="Обери що саме ти хочеш зробити 👇",
                               reply_markup=support_keyboard)
        await state.set_state(fsm.Choose_support)
    else:
        await bot.send_message(-4265874588, text=f"Нова скарга! Її текст:\n{message.text}")
        await state.set_state(None)
        await bot.send_message(message.from_user.id, text="Ми отримали вашу скаргу, дякуємо за фідбек!\n", reply_markup=start_keyboard)


@user_router.callback_query(F.data == "?decanat")
async def callback_dekanat(callback: CallbackQuery, bot: Bot):
    await bot.send_message(callback.from_user.id, text=all_text["info_decanat_text"])


@user_router.callback_query(F.data == "?zam_dekan")
async def callback_zam_dekan(callback: CallbackQuery, bot: Bot):
    await bot.send_message(callback.from_user.id, text=all_text["zastup_info_text"])


@user_router.callback_query(F.data == "?timetable_dekan")
async def callback_dekan_time(callback: CallbackQuery, bot: Bot):
    await bot.send_message(callback.from_user.id, text=all_text["decan_time_text"])


@user_router.callback_query(F.data == "?study_pay")
async def callback_study_pay(callback: CallbackQuery, bot: Bot):
    await bot.send_message(callback.from_user.id, text=all_text["pay_req_text"])


@user_router.callback_query(F.data == "?hurt_pay")
async def callback_hurt_pay(callback: CallbackQuery, bot: Bot):
    await bot.send_message(callback.from_user.id, text=all_text["hurt_req_text"])


@user_router.callback_query(F.data)
async def callback_query(callback: CallbackQuery, bot:Bot):
    await bot.send_message(callback.from_user.id, text="123")