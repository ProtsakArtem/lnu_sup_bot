from aiogram import types
from aiogram.filters.callback_data import CallbackData
from tgbot.config import load_config
#Start markup

start_markup = [[types.KeyboardButton(text='❓ Найчастіші питання')],
[types.KeyboardButton(text='👭Студ. організації')],
[types.KeyboardButton(text="🔗Корисні посилання")],
[types.KeyboardButton(text="🙋 Анонімний чат")]]

start_keyboard = types.ReplyKeyboardMarkup(keyboard=start_markup, resize_keyboard=True,input_field_placeholder="Оберіть з чим вам допомогти")

#Support markup

support_markup = [[types.KeyboardButton(text='Анонімний чат')],
                  [types.KeyboardButton(text='Анонімна скарга')],
                  [types.KeyboardButton(text='Назад ⬅️')]]
support_keyboard = types.ReplyKeyboardMarkup(keyboard=support_markup, resize_keyboard=True,input_field_placeholder="Оберіть тип звернення")


#Just back markup


back_keyboard = types.ReplyKeyboardMarkup(keyboard=[types.KeyboardButton(text='Назад ⬅️')], resize_keyboard=True,input_field_placeholder="Сюди пишіть скаргу одним повідомленням")