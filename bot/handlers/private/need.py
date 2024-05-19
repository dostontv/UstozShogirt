from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.i18n import lazy_gettext as __, gettext as _

from bot.keyboards.inline import verification_btn, verification_user_btn
from bot.keyboards.reply import menu_btn
from conf.conf import Conf

need_router = Router()
admin = Conf.bot.ADMIN


class Form(StatesGroup):
    button = ""
    full_name = State()
    age = State()
    technologies = State()
    phone_number = State()
    address = State()
    price = State()
    work_place = State()
    goal = State()


@need_router.message(
    F.text.in_((__("Ish joyi kerak"), __("Sherik kerak"), __("Xodim kerak"), __("Ustoz kerak"), __("Shogird kerak"))))
async def ish_handler(message: Message, state: FSMContext):
    need = _(" kerak")
    button = message.text.split(need)[(-1, 0)[(await state.get_data())['locale'] == 'uz']].strip('a ')
    await state.set_state(Form.full_name)
    await state.update_data(button=button)
    await message.answer(button + _(" kerak Bunga oid sizga bir nechta savollar beriladi"),
                         reply_markup=ReplyKeyboardRemove())
    if button == _("Xodim"):
        await message.answer(_("🏢 Idora: \n🎓 Idora nomi?"))
        return
    await message.answer(button + _("\nIsm, familiyangizni kiriting?"))


@need_router.message(Form.full_name)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    await state.set_state(Form.age)
    if data['button'] == _("Xodim"):
        await message.answer(_("✍️ Mas'ul: \n\n✍️Mas'ul ism sharifi?"))
        return
    await message.answer(_("🕑 Yosh: \nYoshingizni kiriting? \nMasalan, 19"))


@need_router.message(Form.age)
async def full_name(message: Message, state: FSMContext):
    await state.set_state(Form.technologies)
    await state.update_data(age=message.text)
    await message.answer(
        _("📚 Texnologiya:\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating. Masalan, \nJava, C++, C#"))


@need_router.message(Form.technologies)
async def full_name(message: Message, state: FSMContext):
    await state.set_state(Form.phone_number)
    await state.update_data(technologies=message.text)
    await message.answer(_("📞 Aloqa: \n\nBog`lanish uchun raqamingizni kiriting?\nMasalan, +998 90 123 45 67"))


@need_router.message(Form.phone_number)
async def full_name(message: Message, state: FSMContext):
    await state.set_state(Form.address)
    await state.update_data(phone_number=message.text)
    await message.answer(
        _("🌐 Hudud: \n\nQaysi hududdansiz?\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting."))


@need_router.message(Form.address)
async def full_name(message: Message, state: FSMContext):
    await state.set_state(Form.price)
    await state.update_data(address=message.text)
    data = await state.get_data()
    if data['button'] == _("Xodim"):
        await message.answer(_("💰 Maosh: \n\n💰 Maoshni kiriting?"))
        return
    await message.answer(_("💰 Narxi:\n\nTolov qilasizmi yoki Tekinmi?\nKerak bo`lsa, Summani kiriting?"))


@need_router.message(Form.price)
async def full_name(message: Message, state: FSMContext):
    await state.set_state(Form.work_place)
    await state.update_data(price=message.text)
    data = await state.get_data()
    if data['button'] == _("Xodim"):
        await message.answer(_("🕰 Ish vaqti: \n\n🕰 Ish vaqtini kiriting?"))
        return
    await message.answer(_("👨🏻‍💻 Kasbi: \n\nIshlaysizmi yoki o`qiysizmi?\nMasalan, Talaba"))


@need_router.message(Form.work_place)
async def full_name(message: Message, state: FSMContext):
    await state.set_state(Form.goal)
    await state.update_data(work_place=message.text)
    data = await state.get_data()
    if data['button'] == _("Xodim"):
        await message.answer(_("‼️ Qo`shimcha: \n\n‼️ Qo`shimcha ma`lumotlar?"))
        return
    await message.answer(_("🔎 Maqsad: \n\nMaqsadingizni qisqacha yozib bering."))


@need_router.message(Form.goal)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    data = await state.get_data()
    button = data["button"]
    if button == _("Xodim"):
        msg = _("""
    Xodim kerak:
    🏢 Idora: {full_name}
    📚 Texnologiya: {technologies}
    📞 Aloqa: {phone_number}
    🌐 Hudud: {address}
    ✍️ Mas'ul: {age}
    🕰 Ish vaqti: {work_place}
    💰 Maosh: {price}
    ‼️ Qo`shimcha: {goal}""")
    else:
        if button == _("Sherik"):
            a = _("Sherik")
        elif button == _("Ustoz"):
            a = _("Ustoz")
        elif button == _("Shogird"):
            a = _("Shogird")
        else:
            a = '👨‍💼' + _("Xodim")
        msg = _("""
    {button} kerak:
    {a}: {full_name}
    🕑 Yosh: {age}
    📚 Texnologiya: {technologies}
    📞 Aloqa: {phone_number}
    🌐 Hudud: {address}
    💰 Narxi: {price}
    💼 Kasbi: {work_place}
    🔎 Maqsad: {goal}
    """)
        data['a'] = a
    del data['locale']
    await message.answer(msg.format(**data), reply_markup=verification_user_btn())


@need_router.callback_query(F.data.in_({"confirm", "cancel"}))
async def confirm_or_cancel_handler(call: CallbackQuery, state: FSMContext):
    if call.data == "confirm":
        lang = (await state.get_data())["locale"]
        await call.message.copy_to(admin, reply_markup=verification_btn(call.from_user.id, lang))
        await call.message.answer(_("adminga yuborildi"), reply_markup=menu_btn())
    else:
        await call.message.answer(_("Bekor qilindi"), reply_markup=menu_btn())
    await call.message.delete()
    await state.clear()


@need_router.callback_query(F.data.startswith("send="))
async def confirm_or_cancel_handler(call: CallbackQuery):
    data = call.data.split('=')
    if data[1] == "Yes":
        await call.message.copy_to(Conf.bot.CHANNEL_ID, reply_markup=None)
    else:
        await call.bot.send_message(data[2], _("Bekor qilindi", locale=data[-1]))
    await call.message.delete()
