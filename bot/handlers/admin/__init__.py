from typing import List

from aiogram import Dispatcher

from .admin_handlers import admin_command


def setup_admin_router(dp: Dispatcher):
    dp.include_router(admin_command)


__all__: List[str] = [
    "setup_admin_router"
]