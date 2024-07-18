from aiogram import Router, Bot, F
from aiogram.types import ContentType
from aiogram.filters import CommandStart, Command, StateFilter, BaseFilter
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from tgbot.services.db import all_text, set_user_in_help_session, get_operator_id_by_session, get_user_id_by_session, delete_session, set_helper_to_session
from tgbot.keyboards.reply import start_keyboard, support_keyboard, back_keyboard, end_session_keyboard, back_plus
from tgbot.keyboards.inline import faq_keyboard, make_personal_session_keyboard
from tgbot.states import fsm
from tgbot.config import get_admins, add_admin, remove_admin

user_router = Router()

class StateEndsWithFilter(BaseFilter):
    def __init__(self, suffix: str):
        self.suffix = suffix

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        return current_state and current_state.endswith(self.suffix)




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
async def anon_chat(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Обери що саме ти хочеш зробити 👇", reply_markup=support_keyboard)
    await state.set_state(fsm.Choose_support)


@user_router.message(Command(commands=["add_admin"]))
async def handle_add_admin(message: Message, bot: Bot):
    if str(message.from_user.id) in get_admins():
        args = message.text.split()
        if len(args) == 2:
            admin_id = args[1]
            add_admin(admin_id)
            await message.answer(f"Адміністратора {admin_id} додано.")
    else:
        await bot.send_message(message.from_user.id, text="Додавати адміністраторів можуть тільки адміністратори")
@user_router.message(Command(commands=["remove_admin"]))
async def handle_remove_admin(message: Message, bot: Bot):
    if str(message.user_id) in get_admins():
        args = message.text.split()
        if len(args) == 2:
            admin_id = args[1]
            remove_admin(admin_id)
            await message.answer(f"Адміністратора {admin_id} видалено.")
    else:
        await bot.send_message(message.from_user.id, text="Видаляти адміністраторів можуть тільки адміністратори")


@user_router.message(Command("chat"))
async def chat_test(message: Message, bot:Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, text=f"input: {message.text}")


@user_router.message(StateFilter(fsm.Choose_support))
async def supp_choose_handle(message: Message, bot:Bot, state: FSMContext):
    if message.text.__contains__("чат"):
        await state.set_state(fsm.Chat)
        await bot.send_message(message.from_user.id, text='Щоб почати чат з адміністратором натисніть "Почати чат"\nЯкщо ви натиснули випадково, натисныть кнопку "Назад', reply_markup=back_plus)
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



@user_router.message(StateFilter(fsm.Chat))
async def sup_chat_handler(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, text='Очікуйте на під\'єднання адміністратора. Щоб закінчити діалог натисніть на кнопку "Завершити діалог".',
                           reply_markup=end_session_keyboard)
    await state.set_state(fsm.create_new_user_session(message.from_user.id))
    set_user_in_help_session(message.from_user.id, fsm.create_new_user_session(message.from_user.id))
    for x in get_admins():
        await bot.send_message(x, text = f"Користувач {message.from_user.full_name} звернувся в підтримку і чекає на відповідь", reply_markup = await make_personal_session_keyboard(fsm.create_new_user_session(message.from_user.id)))



@user_router.callback_query(F.data.startswith("helper_in_"))
async def callback_helper_in(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    session_id = callback.data[10:]  # Extract session ID from callback data
    if get_operator_id_by_session(session_id):
        await bot.send_message(callback.from_user.id, text="Цьому користувачу вже допомагає інший оператор.")
    else:
        await state.set_state(session_id)
        await bot.send_message(callback.from_user.id,
                               text="Вас підключено до користувача, привітайтесь і спитайте в чому проблема. Після завершення діалогу натисніть кнопку 'Завершити діалог'",
                               reply_markup=end_session_keyboard)
        set_helper_to_session(session_id, callback.from_user.id)
        await bot.send_message((session_id.replace("_session", "")), text="Адміністратора знайдено, очікуйте на відповідь")



@user_router.message(StateEndsWithFilter('_session'))
async def in_start(message: Message, bot: Bot, state: FSMContext):
    session = await state.get_state()
    if message.text == "Завершити діалог":
        oper_id = get_operator_id_by_session(session)
        user_id = get_user_id_by_session(session)

        if oper_id and user_id:
            operator_state = FSMContext(storage=state.storage, key=(message.chat.id, oper_id))
            user_state = FSMContext(storage=state.storage, key=(message.chat.id, user_id))

            await operator_state.set_state(None)
            await user_state.set_state(None)

            await message.bot.send_message(oper_id, text="Діалог завершено.", reply_markup=start_keyboard)
            await message.bot.send_message(user_id, text="Діалог завершено.", reply_markup=start_keyboard)
            delete_session(session)

    else:
        if str(message.from_user.id) in get_admins():
            recipient_id = get_user_id_by_session(session)
        else:
            recipient_id = get_operator_id_by_session(session)

        # Handle different content types
        if message.content_type == ContentType.TEXT:
            await bot.send_message(recipient_id, message.text)
        elif message.content_type == ContentType.PHOTO:
            await bot.send_photo(recipient_id, photo=message.photo[-1].file_id, caption=message.caption)
        elif message.content_type == ContentType.VIDEO:
            await bot.send_video(recipient_id, video=message.video.file_id, caption=message.caption)
        elif message.content_type == ContentType.STICKER:
            await bot.send_sticker(recipient_id, sticker=message.sticker.file_id)
        elif message.content_type == ContentType.ANIMATION:
            await bot.send_animation(recipient_id, animation=message.animation.file_id, caption=message.caption)
        # Add other content types as needed



@user_router.callback_query(F.data == "?decanat")
async def callback_dekanat(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await bot.send_message(callback.from_user.id, text=all_text["info_decanat_text"])


@user_router.callback_query(F.data == "?zam_dekan")
async def callback_zam_dekan(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await bot.send_message(callback.from_user.id, text=all_text["zastup_info_text"])


@user_router.callback_query(F.data == "?timetable_dekan")
async def callback_dekan_time(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await bot.send_message(callback.from_user.id, text=all_text["decan_time_text"])


@user_router.callback_query(F.data == "?study_pay")
async def callback_study_pay(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await bot.send_message(callback.from_user.id, text=all_text["pay_req_text"])


@user_router.callback_query(F.data == "?hurt_pay")
async def callback_hurt_pay(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await bot.send_message(callback.from_user.id, text=all_text["hurt_req_text"])


@user_router.callback_query(F.data)
async def callback_query(callback: CallbackQuery, bot:Bot):
    await callback.answer()
    await bot.send_message(callback.from_user.id, text="Unknown callback")
