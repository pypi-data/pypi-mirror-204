from typing import Awaitable

from aiogram.types import ChatType

from .deps import (
    ReplyKeyboardRemove,
    Message,
    ReplyMarkup,
    Query,
    Chat,
    State,
    InlineKeyboardMarkup,
)


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


async def ask(
    state: State,
    msg: Message,
    text: str,
    markup: ReplyMarkup | bool = False,
):
    await state.set()
    await reply(msg, text, markup)


def edit(
    msg: Message | Query,
    text: str,
    markup: InlineKeyboardMarkup = None,
):
    if isinstance(msg, Query):
        msg = msg.message
    return msg.edit_text(text, reply_markup=markup)


def is_channel(chat: Chat) -> bool:
    return chat.type in [ChatType.CHANNEL]


def is_group(chat: Chat) -> bool:
    return chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]


def is_private(chat: Chat) -> bool:
    return chat.type in [ChatType.PRIVATE]


async def get_photo_url(msg: Message) -> str:
    return await msg.photo[-1].get_url()
