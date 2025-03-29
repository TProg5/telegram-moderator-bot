from datetime import datetime
from typing import List

from aiogram import Bot
from aiogram.types import Message, User
from aiogram_i18n import I18nContext
from spacy.language import Language
from spacy.tokens import Doc

from bot.utils import mute_with_message
from bot.keyboards import ModerationCallback

from bot.database import get_locale


async def check_message_to_bad_words(
    bot: Bot,
    message: Message,
    nlp_model: Language,
    forbidden_words: List[str],
    i18n: I18nContext,
    until_date: datetime
) -> None:
    if not message.from_user:
        return

    if not message.text:  
        return

    user: User = message.from_user
    chat_id: int = message.chat.id
    locale: str = await get_locale(chat_id=chat_id)
    doc: Doc = nlp_model(message.text)  

    for token in doc:
        if token.text.lower() in forbidden_words:
            await mute_with_message(
                bot=bot,
                i18n=i18n,
                chat_id=chat_id,
                user_id=user.id,
                until_date=until_date,
                buttons_text=[
                    i18n.get(
                        'unmute-button',
                        locale
                    )
                ],
                callback_data=[
                    ModerationCallback(
                        action='unmute',
                        user_id=user.id
                    ).pack()
                ],
                message_text=(
                    i18n.get(
                        "mute-user",
                        user_id=user.id,
                        user_full_name=user.full_name,
                        time=30,
                        reason='Profanity',
                        reable_time=i18n.get(
                            'minute1',
                            locale
                        )
                    )
                )
            )
