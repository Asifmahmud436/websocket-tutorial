from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from time import sleep
import asyncio
from asgiref.sync import async_to_sync
import json
from .models import Group,Chat
from channels.db import database_sync_to_async

class MyWebSocketConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        
        # Add this consumer to the group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['msg']

        group = Group.objects.get(name = self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content = data['msg'],
                group = group
            )
            chat.save()
        # Send message to group
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': message
                }
            )
        else:
            self.send(text_data=json.dumps({
                'msg':"Login Required"
            }))

    def chat_message(self, event):
        # Send message to WebSocket client
        self.send(text_data=json.dumps({
            'message': event['message']
        }))

    def disconnect(self, close_code):
        # Remove this consumer from the group when disconnecting
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

class MyAsyncWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        
        # Add this consumer to the group
        self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
    async def receive(self,text_data=None,bytes_data=None):
        data = json.loads(text_data)
        message = data['msg']
        group = await database_sync_to_async(Group.objects.get)(name = self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content = data['msg'],
                group = group
            )
            await database_sync_to_async(chat.save)()
            # Send message to group
            self.channel_layer.group_send(
                await self.group_name,
                {
                    'type': 'chat.message',
                    'message': message
                }
            )
        else:
            await self.send(text_data=json.dumps({
                'msg':"Login Required"
            }))

    async def chat_message(self, event):
        # Send message to WebSocket client
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))


    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )