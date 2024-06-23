from aiogram import types

#Start markup

start_markup = [[types.KeyboardButton(text='❓ Найчастіші питання')],
[types.KeyboardButton(text='👭Студ. організації')],
[types.KeyboardButton(text="🔗Корисні посилання")],
[types.KeyboardButton(text="🙋 Анонімний чат")]]

start_keyboard = types.ReplyKeyboardMarkup(keyboard=start_markup, resize_keyboard=True,input_field_placeholder="Оберіть з чим вам допомогти")


