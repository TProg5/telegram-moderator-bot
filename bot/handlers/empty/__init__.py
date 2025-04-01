from typing import List

from aiogram import Dispatcher

from .empty_handlers import empty_member


def setup_empty_router(dp: Dispatcher):
    dp.include_router(empty_member)


__all__: List[str] = [
    "setup_empty_route"
]