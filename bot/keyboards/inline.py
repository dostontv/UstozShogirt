from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


def lang_btn():
    btn = InlineKeyboardBuilder()
    btn.add(
        *[InlineKeyboardButton(text="🇬🇧", callback_data='l=en'), InlineKeyboardButton(text='🇺🇿', callback_data='l=uz')])
    return btn.as_markup()


def verification_btn(chat_id, lang):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Kanalga jo'natish", callback_data="send=Yes")],
            [InlineKeyboardButton(text="❌", callback_data=f"send=No={chat_id}={lang}")]
        ])


def verification_user_btn():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Ha "), callback_data="confirm")],
            [InlineKeyboardButton(text=_("Yoq "), callback_data="cancel")]
        ])
