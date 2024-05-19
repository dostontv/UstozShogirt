import asyncio
import logging
import time

from aiogram import Router, Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest, TelegramNotFound, TelegramForbiddenError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot.keyboards.reply import cancel_btn, menu_btn
from db.database import db

admin_router = Router()


async def broadcast(user_id, text: str, bot: Bot):
    try:
        await bot.send_message(user_id, f'<b> xabar </b>\n' + text)
    except TelegramRetryAfter as e:
        logging.error(f'ozgina sabr qilamiz {e.retry_after} seconds')
        await asyncio.sleep(e.retry_after)
    except TelegramForbiddenError as e:
        logging.error(f'Bu user block qilibdi bizni {user_id} - {e}')
        del db[user_id]
    except TelegramBadRequest as e:
        logging.error(f'xatolik ketti {e}')
    except TelegramNotFound as e:
        logging.error(f'bunaqa narsani ozi yoq {e}')


class Form(StatesGroup):
    txt = State()


@admin_router.message(Command('admin'))
async def send_admin(message: Message):
    await message.answer("Siz adminsiz")


@admin_router.message(Command('send'))
async def send_message(message: Message, state: FSMContext):
    await state.set_state(Form.txt)
    await message.answer("Habarni kiriting yoki Bekor qilishni bosing", reply_markup=cancel_btn())


@admin_router.message(Form.txt)
async def check_messages(message: Message, bot: Bot, state: FSMContext):
    text = message.text
    if text != "Bekor qilish":
        start = time.time()
        users = db.keys()
        tasks = []
        count = 0
        for user_id in users:
            if len(tasks) > 24:
                await asyncio.gather(*[broadcast(*i) for i in tasks])
                await asyncio.sleep(1)
                tasks = []
            tasks.append((user_id, text, bot))
            count += 1
        if len(tasks) > 0:
            await asyncio.gather(*[broadcast(*i) for i in tasks])
        await message.answer(f'{round(time.time() - start)} seconds \n jami xabarlar soni: {count}')
    else:
        await state.clear()
        await message.answer("Bekor qilindi", reply_markup=menu_btn())
