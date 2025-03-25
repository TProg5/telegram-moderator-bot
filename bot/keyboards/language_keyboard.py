from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class LanguageCallback(CallbackData, prefix='language'):
    language: str


async def language_keyboard() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text='🇬🇧English',
                callback_data=LanguageCallback(language='en').pack()
            ),
            InlineKeyboardButton(
                text='🇷🇺Russian',
                callback_data=LanguageCallback(language='ru').pack()
            )
        ]]
    )

    return keyboard