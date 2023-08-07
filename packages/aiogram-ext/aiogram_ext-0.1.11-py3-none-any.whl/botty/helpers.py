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


async def reply(
        event: Message | Query,
        text: str,
        markup: ReplyMarkup | bool = None,
) -> Message:
    if isinstance(event, Query):
        await event.answer()
        event = event.message
    if markup is False:
        markup = ReplyKeyboardRemove()
    return await event.answer(text, reply_markup=markup)


async def ask(
        state: State,
        msg: Message,
        text: str,
        markup: ReplyMarkup | bool = False,
):
    await state.set()
    await reply(msg, text, markup)


async def edit(
        event: Message | Query,
        text: str,
        markup: InlineKeyboardMarkup = None,
) -> Message:
    if isinstance(event, Query):
        await event.answer()
        event = event.message
    return await event.edit_text(text, reply_markup=markup)


def is_channel(chat: Chat) -> bool:
    return chat.type in [ChatType.CHANNEL]


def is_group(chat: Chat) -> bool:
    return chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]


def is_private(chat: Chat) -> bool:
    return chat.type in [ChatType.PRIVATE]


async def get_photo_url(msg: Message) -> str:
    return await msg.photo[-1].get_url()
