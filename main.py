import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeChat
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from bot.handlers import private_router
from conf.conf import Conf

TOKEN = Conf.bot.BOT_TOKEN

dp = Dispatcher()

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def on_startup() -> None:
    dp.include_routers(*[private_router])
    commands = [
        BotCommand(command="start", description="Starts the bot."),
        BotCommand(command="lang", description="Changes the language of the bot.")
    ]
    admin_commands = commands + [
        BotCommand(command="admin", description="Admins the bot."),
        BotCommand(command="send", description="Send messages to the bot."),
    ]
    await bot.set_my_commands(commands)
    await bot.set_my_commands(admin_commands, BotCommandScopeChat(chat_id=Conf.bot.ADMIN))


async def on_shutdown() -> None:
    await bot.delete_my_commands()
    await dp.storage.close()


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    i18n = I18n(path="locales")
    dp.update.outer_middleware(FSMI18nMiddleware(i18n))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
