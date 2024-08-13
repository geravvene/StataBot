from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

menu = [
    [InlineKeyboardButton(text="Статистика", callback_data="All")]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
