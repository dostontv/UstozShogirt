from aiogram.types import KeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def menu_btn(lang=None):
    btn = ReplyKeyboardBuilder()
    if lang:
        b1 = _("Sherik kerak", locale=lang)
        b2 = _("Ish joyi kerak", locale=lang)
        b3 = _("Xodim kerak", locale=lang)
        b4 = _("Ustoz kerak", locale=lang)
        b5 = _("Shogird kerak", locale=lang)
    else:
        b1 = _("Sherik kerak")
        b2 = _("Ish joyi kerak")
        b3 = _("Xodim kerak")
        b4 = _("Ustoz kerak")
        b5 = _("Shogird kerak")
    btn.add(*[KeyboardButton(text=b1), KeyboardButton(text=b2)])
    btn.add(*[KeyboardButton(text=b3), KeyboardButton(text=b4)])
    btn.add(KeyboardButton(text=b5))
    btn.adjust(2, repeat=True)
    return btn.as_markup(resize_keyboard=True)


def cancel_btn():
    btn = ReplyKeyboardBuilder()
    btn.add(KeyboardButton(text="Bekor qilish"))
    return btn.as_markup(resize_keyboard=True)
