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
from func import get_count, string_range_date, get_count_many
from create_bot import bot, dp, collection, Form

async def send_stata_week(bot: Bot, chat_id):
    await bot.send_message(text=string_range_date(datetime.now()-timedelta(days=7), datetime.now())+get_count(collection), chat_id=chat_id, parse_mode="Markdown")
async def send_stata_month(bot: Bot, chat_id):
    await bot.send_message(text=string_range_date(datetime.now()-timedelta(dayss=30), datetime.now())+get_count(collection), chat_id=chat_id, parse_mode="Markdown")
async def send_stata_quarter(bot: Bot, chat_id):
    await bot.send_message(text=string_range_date(datetime.now()-timedelta(weeks=13), datetime.now())+get_count(collection), chat_id=chat_id, parse_mode="Markdown")

@dp.message(CommandStart())
async def send_welcome(msg: Message):
    await msg.answer(f'Привет, {msg.from_user.username}! Выберете опцию статистики:', reply_markup=start_menu)
    
@dp.callback_query(F.data == "All")
async def display_all(callback_query: CallbackQuery):
    messages=get_count_many(collection)
    messages[0]= string_range_date(False, datetime.now())+messages[0]
    for x in messages:
        await callback_query.message.answer(x, parse_mode="Markdown")

@dp.callback_query(F.data == "Week")
async def display_week(callback_query: CallbackQuery):
    date1=datetime.now()-timedelta(weeks=1)
    date=datetime.now()
    messages=get_count_many(collection, date1, date)
    messages[0]= string_range_date(date1, date)+messages[0]
    for x in messages:
        await callback_query.message.answer(x, parse_mode="Markdown")

@dp.callback_query(F.data == "Month")
async def display_month(callback_query: CallbackQuery):
    date1=datetime.now()-timedelta(days=31)
    date=datetime.now()
    messages=get_count_many(collection, date1, date)
    messages[0]= string_range_date(date1, date)+messages[0]
    for x in messages:
        await callback_query.message.answer(x, parse_mode="Markdown")
@dp.callback_query(F.data == "Quarter")
async def display_quarter(callback_query: CallbackQuery):
    date1=datetime.now()-timedelta(weeks=13)
    date=datetime.now()
    messages=get_count_many(collection, date1, date)
    messages[0]= string_range_date(date1, date)+messages[0]
    for x in messages:
        await callback_query.message.answer(x, parse_mode="Markdown")       



@dp.callback_query(F.data == "Range")
async def range_handler(callback_query: CallbackQuery):
    await callback_query.message.answer('Выберете начальную дату:', reply_markup=date_menu1)
    
@dp.callback_query(F.data == "SMS")
async def send_sms(callback_query: CallbackQuery, apscheduler: AsyncIOScheduler):
    apscheduler.add_job(send_stata_week, 'cron', day_of_week='fri', hour=22, minute=59, kwargs={"bot": bot,"chat_id": callback_query.message.chat.id}, id='week')
    apscheduler.add_job(send_stata_month, 'cron', day='last', hour=22, minute=59, kwargs={"bot": bot,"chat_id": callback_query.message.chat.id}, id='month')
    apscheduler.add_job(send_stata_quarter, 'cron', day='1st fri', month='1,4,7,9', hour=22, minute=59, kwargs={"bot": bot,"chat_id": callback_query.message.chat.id}, id='quarter')
    await callback_query.message.answer('вкл')
@dp.callback_query(F.data == "DELETE_SMS")
async def delete_sms(callback_query: CallbackQuery, apscheduler: AsyncIOScheduler):
    apscheduler.remove_job('week')
    apscheduler.remove_job('month')
    apscheduler.remove_job('quarter')
    await callback_query.message.answer('выкл')


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
    messages=get_count_many(collection, date, now)
    messages[0]= string_range_date(date, now)+messages[0]
    for x in messages:
        await callback_query.message.answer(x, parse_mode="Markdown")


@dp.callback_query(DialogCalendarCallback.filter(), Form.date)
async def process_dialog_calendar2(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.delete()
        data = await state.get_data()
        date1 = data['date']
        await state.clear()
        messages=get_count_many(collection, date1, date)
        messages[0]= string_range_date(date1, date)+messages[0]
        for x in messages:
            await callback_query.message.answer(x, parse_mode="Markdown")


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
