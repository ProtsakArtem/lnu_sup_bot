from aiogram import types

#FAQ markup

faq_mark = [
    [types.InlineKeyboardButton(text="Контакти деканату та кафедр факультету іноземних мов", callback_data="?decanat")],
    [types.InlineKeyboardButton(text="Години прийому заступниць декана", callback_data="?zam_dekan")],
    [types.InlineKeyboardButton(text="Графік роботи деканату факультету іноземних мов", callback_data="?timetable_dekan")],
    [types.InlineKeyboardButton(text="Реквізити на оплату навчання", callback_data="?study_pay")],
    [types.InlineKeyboardButton(text="Реквізити на оплату проживання в гуртожитках", callback_data="?hurt_pay")]
]
faq_keyboard = types.InlineKeyboardMarkup(inline_keyboard=faq_mark)