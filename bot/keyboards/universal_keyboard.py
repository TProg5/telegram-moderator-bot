from typing import Optional, List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def customed_keyboard(
    buttons_text: Optional[List[str]] = None,
    callback_data: Optional[List[str]] = None
) -> Optional[InlineKeyboardMarkup]:
    if not buttons_text or not callback_data:
        return None
    
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    
    for text, data in zip(buttons_text, callback_data):
        button: InlineKeyboardButton = InlineKeyboardButton(
            text=text,
            callback_data=data
        )

        keyboard.add(button)
        keyboard.adjust(
            len(
                buttons_text
            )
        )

    return keyboard.as_markup()