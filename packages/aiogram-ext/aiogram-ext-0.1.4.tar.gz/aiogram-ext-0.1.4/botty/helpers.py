from typing import Awaitable
from aiogram.types import ChatType
from .deps import ReplyKeyboardRemove, Message, ReplyMarkup, Query, Chat


def reply(
    msg: Message | Query,
    text: str,
    markup: ReplyMarkup | bool = None,
) -> Awaitable[Message]:
    if isinstance(msg, Query):
        msg = msg.message
    if markup is False:
        markup = ReplyKeyboardRemove()
    return msg.answer(text, reply_markup=markup)


def is_channel(chat: Chat) -> bool:
    return chat.type in [ChatType.CHANNEL]


def is_group(chat: Chat) -> bool:
    return chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]


def is_private(chat: Chat) -> bool:
    return chat.type in [ChatType.PRIVATE]
