import asyncio
import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncConsumer
from channels.db import database_sync_to_async

from chat.models import Thread


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('connect', event)
        await self.send({
            'type': 'websocket.accept'
        })
        me = self.scope['user']
        other_user = self.scope['url_route']['kwargs']['username']
        print(me, other_user)
        thread_obj = await self.get_thread(me, other_user)
        print(thread_obj)
        await self.send({
            'type': 'websocket.send',
            'text': 'hello world !'
        })

    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def websocket_receive(self, event):
        print('receive', event)

    @database_sync_to_async  # don't use this database make many more connection
    def get_thread(self, user, other_user):
        return Thread.objects.get_or_new(user, other_user)