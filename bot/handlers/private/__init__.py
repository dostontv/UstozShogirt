from aiogram import Router
from aiogram.enums import ChatType

from bot.filters.is_admin import IsAdminFilter
from bot.handlers.private.admin import admin_router
from bot.handlers.private.need import need_router
from bot.handlers.private.start import start_router
from bot.filters.Chattype_filter import ChatTypeFilter

private_router = Router()
admin_router.message.filter(IsAdminFilter())

private_router.message.filter(ChatTypeFilter(ChatType.PRIVATE))
private_router.include_routers(*[start_router, need_router, admin_router])
