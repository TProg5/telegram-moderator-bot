from typing import List

from aiogram import Dispatcher

from .admin import setup_admin_router
from .empty import setup_empty_router


def setup_routers(dp: Dispatcher):
    setup_admin_router(dp)
    setup_empty_router(dp)


__all__: List[str] = [
    "admin_command"
]