from telegram.ext import MessageFilter
from telegram import Message
from tobrot import AUTH_CHANNEL, OWNER_ID


class CustomFilters:
    class _OwnerFilter(MessageFilter):
        def filter(self, message):
            return bool(message.from_user.id == OWNER_ID)

    owner_filter = _OwnerFilter()

    class _AuthorizedUserFilter(MessageFilter):
        def filter(self, message):
            id = message.from_user.id
            return bool(id in AUTH_CHANNEL or id == OWNER_ID)

    authorized_user = _AuthorizedUserFilter()

    class _AuthorizedChat(MessageFilter):
        def filter(self, message):
            return bool(message.chat.id in AUTH_CHANNEL)

    authorized_chat = _AuthorizedChat()
