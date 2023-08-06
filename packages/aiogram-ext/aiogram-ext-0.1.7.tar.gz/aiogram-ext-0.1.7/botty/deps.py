from copy import deepcopy
from os import environ
from typing import TypeVar, Callable, Any

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.handler import SkipHandler, CancelHandler
from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    Update,
    Message,
    Chat,
    User,
    CallbackQuery as Query,
    InlineQuery,
    ChosenInlineResult,
    ShippingQuery,
    PreCheckoutQuery,
    Poll,
    PollAnswer,
    ChatMemberUpdated,
    ReplyKeyboardRemove,
)
from aiogram.utils import executor
from aiogram.utils.mixins import ContextInstanceMixin
from aiogram.utils.exceptions import TelegramAPIError

__all__ = [
    "ReplyKeyboardMarkup",
    "InlineKeyboardMarkup",
    "InlineKeyboardButton",
    "KeyboardButton",
    "Bot",
    "Dispatcher",
    "FSMContext",
    "ContextInstanceMixin",
    "Update",
    "Message",
    "Chat",
    "User",
    "Query",
    "InlineQuery",
    "ChosenInlineResult",
    "ShippingQuery",
    "PreCheckoutQuery",
    "Poll",
    "PollAnswer",
    "ChatMemberUpdated",
    "executor",
    "deepcopy",
    "ReplyKeyboardRemove",
    "State",
    "TypeVar",
    "Callable",
    "Any",
    "environ",
    "MongoStorage",
    "SkipHandler",
    "CancelHandler",
    "StatesGroup",
    "ReplyMarkup",
    "TelegramAPIError",
]

ReplyMarkup = ReplyKeyboardMarkup | InlineKeyboardMarkup | ReplyKeyboardRemove
