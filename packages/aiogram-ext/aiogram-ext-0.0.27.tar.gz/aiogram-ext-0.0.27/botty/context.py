from __future__ import annotations

from typing import TypeVar

from .deps import (
    ContextInstanceMixin,
    FSMContext,
    Dispatcher,
    Update,
    Message,
    Chat,
    User,
    Query,
    InlineQuery,
    ChosenInlineResult,
    ShippingQuery,
    PreCheckoutQuery,
    Poll,
    PollAnswer,
    ChatMemberUpdated,
)

T = TypeVar("T")


def make_context_obj(obj_type: type[ContextInstanceMixin]) -> T:
    class ContextObject(obj_type):
        def __getattribute__(self, item):
            ctx_obj = obj_type.get_current()
            if hasattr(ctx_obj, item):
                return getattr(ctx_obj, item)
            return super().__getattribute__(item)

    return ContextObject()


class ContextStorage(FSMContext):
    # noinspection PyMissingConstructor
    def __init__(self):
        pass

    def __getattribute__(self, item):
        ctx_storage = Dispatcher.get_current().current_state()
        if hasattr(ctx_storage, item):
            return getattr(ctx_storage, item)
        return super().__getattribute__(item)


update = make_context_obj(Update)
message = make_context_obj(Message)
chat = make_context_obj(Chat)
user = make_context_obj(User)
callback_query = make_context_obj(Query)
inline_query = make_context_obj(InlineQuery)
chosen_inline_result = make_context_obj(ChosenInlineResult)
shipping_query = make_context_obj(ShippingQuery)
pre_checkout_query = make_context_obj(PreCheckoutQuery)
poll = make_context_obj(Poll)
poll_answer = make_context_obj(PollAnswer)
chat_member_updated = make_context_obj(ChatMemberUpdated)

storage = ContextStorage()
