
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from db import connect, create_storage
import config
from aiogram.types import BotCommand


async def setup_bot_commands():
    bot_commands = [
        BotCommand(command="/start", description="Получить статистику"),
    ]
    await bot.set_my_commands(bot_commands)

dp = Dispatcher(storage=create_storage())

dp.startup.register(setup_bot_commands)

bot = Bot(token=config.API_TOKEN, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML))


class Form(StatesGroup):
    date = State()


collection = connect("Dubrovskiy")
