import asyncio
import logging
import sys
from datetime import datetime, timedelta

from aiogram import F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram.filters.callback_data import CallbackData
from aiogram_calendar import DialogCalendar, DialogCalendarCallback
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scheduler import SchedulerMiddleware

from menu import start_menu, date_menu1, date_menu2
from func import get_count, string_range_date
from create_bot import bot, dp, collection, Form

async def send_stata(bot: Bot, chat_id):
    await bot.send_message(text=string_range_date(datetime.now()-timedelta(days=7), datetime.now())+get_count(collection), chat_id=chat_id, parse_mode="Markdown")

@dp.message(CommandStart())
async def send_welcome(msg: Message, apscheduler: AsyncIOScheduler):
    apscheduler.add_job(send_stata, 'cron', day_of_week='sun', hour=17, minute=52, kwargs={"bot": bot,"chat_id": msg.chat.id})
    await msg.answer(f'Привет, {msg.from_user.username}! Выберете опцию статистики:', reply_markup=start_menu)


@dp.callback_query(F.data == "All")
async def display_all(callback_query: CallbackQuery):
    await callback_query.message.answer(string_range_date(False, datetime.now())+get_count(collection), parse_mode="Markdown")


@dp.callback_query(F.data == "Range")
async def range_handler(callback_query: CallbackQuery):
    await callback_query.message.answer('Выберете начальную дату:', reply_markup=date_menu1)


@dp.callback_query(F.data == "Another date")
async def another_date_handler(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer("Выберете дату",
                                        reply_markup=await DialogCalendar().start_calendar()
                                        )


@dp.callback_query(F.data == "Nevermind")
async def nevermind_date_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.set_state(Form.date)
    await state.update_data(date=False)
    await callback_query.message.answer('Выберете конечную дату:', reply_markup=date_menu2)


@dp.callback_query(F.data == "Today")
async def today_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    now = datetime.now()
    data = await state.get_data()
    date = data['date']
    await state.clear()
    str = string_range_date(date, now)
    await callback_query.message.answer(str+get_count(collection, date, now))


@dp.callback_query(DialogCalendarCallback.filter(), Form.date)
async def process_dialog_calendar2(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.delete()
        data = await state.get_data()
        date1 = data['date']
        await state.clear()
        str = string_range_date(date1, date)
        await callback_query.message.answer(str+get_count(collection, date1, date))


@dp.callback_query(DialogCalendarCallback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.delete()
        await state.set_state(Form.date)
        await state.update_data(date=date)
        await callback_query.message.answer('Выберете конечную дату:', reply_markup=date_menu2)


async def main() -> None:
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    dp.update.middleware(SchedulerMiddleware(scheduler=scheduler))
    await dp.start_polling(bot)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())
