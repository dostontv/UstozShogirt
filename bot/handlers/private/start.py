from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.keyboards.inline import lang_btn
from bot.keyboards.reply import menu_btn
from db.database import db

start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: Message) -> None:
    data = message.from_user.model_dump(include={"id", "first_name"})
    data["locale"] = "en"
    if not db.get(data["id"]):
        db[data["id"]] = data
    await message.answer(_("Assalomu alaykum ") + message.from_user.full_name, reply_markup=menu_btn())


@start_router.message(Command('lang'))
async def chose_lang_handler(msg: Message):
    await msg.answer(_("Tilni tanglang"), reply_markup=lang_btn())


@start_router.callback_query(F.data.startswith('l='))
async def select_handler(call: CallbackQuery, state: FSMContext):
    lang = call.data[2:]
    await state.update_data(locale=lang)
    db[str(call.from_user.id)]["locale"] = lang
    await call.message.answer(_("Til tanlandi", locale=lang), reply_markup=menu_btn(lang))
    await call.message.delete()
