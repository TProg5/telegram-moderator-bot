from typing import List

from aiogram import Bot, Dispatcher

from .inner import setup_inner_middlewares
from .outer import setup_outer_middlewares

def setup_middlewares(bot: Bot, dp: Dispatcher):
    setup_outer_middlewares(bot=bot, dp=dp)
    setup_inner_middlewares(bot=bot, dp=dp)


__all__: List[str] = ["setup_middlewares"]