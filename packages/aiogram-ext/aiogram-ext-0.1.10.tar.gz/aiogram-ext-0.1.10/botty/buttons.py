from __future__ import annotations

from .deps import InlineKeyboardButton, KeyboardButton, deepcopy


class InlineButton(InlineKeyboardButton):
    def format(self, *args, **kwargs) -> InlineButton:
        button = deepcopy(self)
        for attr, value in button.values.items():
            if isinstance(value, str):
                button[attr] = value.format(*args, **kwargs)
        return button


class CallbackButton(InlineButton):
    def __init__(self, text: str, data: str = None):
        super().__init__(text, callback_data=data or text)


class UrlButton(InlineButton):
    def __init__(self, text: str, url: str):
        super().__init__(text, url=url)


class InlineQueryButton(InlineButton):
    def __init__(self, text: str, query: str = None, *, current_chat: bool = True):
        query = query or text

        if current_chat:
            super().__init__(text, switch_inline_query_current_chat=query)
        else:
            super().__init__(text, switch_inline_query=query)


class ContactRequestButton(KeyboardButton):
    def __init__(self, text: str):
        super().__init__(text, request_contact=True)
