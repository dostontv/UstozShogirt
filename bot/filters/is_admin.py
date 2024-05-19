from aiogram.filters import Filter
from aiogram.types import Message

from conf.conf import Conf


class IsAdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == int(Conf.bot.ADMIN)
