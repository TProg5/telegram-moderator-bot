from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class ModerationCallback(CallbackData, prefix='moderation'):
    action: str
    user_id: int
    

async def moderation_keyboard(
    text: Optional[str] = None,
    action: Optional[str] = None,
    user_id: Optional[int] = None
) -> Optional[InlineKeyboardMarkup]:
    if not text:
        return None

    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text=text,
            callback_data=ModerationCallback(
                action=action,
                user_id=user_id
            ).pack()
        )]]
    )

    return keyboard