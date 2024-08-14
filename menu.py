from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_menu = [
    [InlineKeyboardButton(text="Статистика", callback_data="All")],
    [InlineKeyboardButton(text="Диапазон", callback_data="Range")]
]
start_menu = InlineKeyboardMarkup(inline_keyboard=start_menu)

date_menu1 = [
    [InlineKeyboardButton(text="Выбрать дату", callback_data="Another date")],
    [InlineKeyboardButton(text="Неважно", callback_data="Nevermind")]
]
date_menu1 = InlineKeyboardMarkup(inline_keyboard=date_menu1)

date_menu2 = [
    [InlineKeyboardButton(text="Сегодня", callback_data="Today")],
    [InlineKeyboardButton(text="Выбрать дату", callback_data="Another date")]
]
date_menu2 = InlineKeyboardMarkup(inline_keyboard=date_menu2)
