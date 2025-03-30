from datetime import datetime
from typing import List

from aiogram import Bot
from aiogram.types import Message, User
from spacy.language import Language
from spacy.tokens import Doc

from ..moderation import mute_with_message
from ..helpers import reply_message_and_delete
from bot.keyboards import ModerationCallback
from bot.database import add_and_get_warns, delete_warns


async def check_message_to_bad_words(
    bot: Bot,
    message: Message,
    nlp_model: Language,
    forbidden_words: List[str],
    until_date: datetime
) -> None:
    if not message.from_user:
        return

    if not message.text:  
        return

    user: User = message.from_user
    chat_id: int = message.chat.id
    doc: Doc = nlp_model(message.text)

    for token in doc:
        if token.text.lower() in forbidden_words:
            warns: int = await add_and_get_warns(
                user_id=user.id,
                chat_id=chat_id
            )

            if warns >= 3:
                await delete_warns(
                    user_id=user.id,
                    chat_id=chat_id,
                    warns=3
                )

                await mute_with_message(
                    bot=bot,
                    chat_id=chat_id,
                    user_id=user.id,
                    until_date=until_date,
                    buttons_text=["Unmute✔️"],
                    message_text=(
                        f"👀<b><a href='tg://user?id={user.id}'>{user.full_name}</a></b>"
                        "<b>is muted for 30 minutes due to exceeding the warning limit.</b>"
                    ),
                    callback_data=[
                        ModerationCallback(
                            action='unmute',
                            user_id=user.id
                        ).pack()
                    ]
                )
                return
                
            await reply_message_and_delete(
                bot=bot,
                chat_id=chat_id,
                text=f"<b>{user.full_name}</b>, you've exceeded the warning limit for the word '{token.text.lower()}'."
            )