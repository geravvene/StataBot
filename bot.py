import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import Bot, Dispatcher

from menu import menu
from calculate import calc
from db import connect
import config
 
dp = Dispatcher()

bot = Bot(token=config.API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

collection=connect("Dubrovskiy")
 
@dp.message(CommandStart())
async def send_welcome(msg: Message):
    await msg.answer(f'Привет, {msg.from_user.username}!', reply_markup=menu)
 
@dp.callback_query(F.data == "All")
async def display_all(callback_query: CallbackQuery):
    data=calc(collection)
    str=f"<b>PNL = {data['pnl']}</b>\n\n"
    
    for key in data['pnl_symbol']:
        str+=f"{key} = {data['pnl_symbol'][key]}\n"
        
    await callback_query.message.answer(str)
   
async def main() -> None:
    await dp.start_polling(bot)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())