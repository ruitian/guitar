# -*- coding: utf-8 -*-

from . import BaseService
from guitar.models import ChatModel


class ChatService(BaseService):

    def save_chat_record(self, user, who, content, is_read=True):
        chat = ChatModel(user=user, who=who, content=content, is_read=is_read)
        self.session.add(chat)
        self.session.commit()

    def get_chat_unread(self, who):
        chats = self.session.query(ChatModel).filter_by(
            who=who, is_read=False).all()
        return [chat.to_dict() for chat in chats]

    def get_chat_unread_count(self, who):
         return self.session.query(ChatModel).filter_by(
            who=who, is_read=False).count()
