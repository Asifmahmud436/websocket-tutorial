from channels.consumer import SyncConsumer,AsyncConsumer
from channels.consumer import StopConsumer
from asgiref.sync import async_to_sync
import json
from .models import Group,Chat
from channels.db import database_sync_to_async

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print('Websocket connected...',event)
        # get default channel from a project:
        print("Channel Layer...",self.channel_layer)
        # get channel name
        print("Channel Name...",self.channel_name)
        # add a channel to a new or existing group
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, # group name
            self.channel_name)
        self.send({
            'type':'websocket.accept'
        })

    def websocket_receive(self,event):
        print('Message Received From Client...',event['text'])
        
        data = json.loads(event['text'])
        # find group object
        group = Group.objects.get(name=self.group_name)
        # create new chat object
        chat = Chat(
            content = data['msg'],
            group = group
        )
        chat.save()
        async_to_sync(self.channel_layer.group_send)(self.group_name,{
            'type': 'chat.message',
            'message': event['text']
        })

    def chat_message(self,event):
        print("event...",event)
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    def websocket_disconnect(self,event):
        print('Websocket Disconnected...',event)
        print("Channel Layer...",self.channel_layer)
        # get channel name
        print("Channel Name...",self.channel_name)
        # add a channel to a new or existing group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, # group name
            self.channel_name)
        raise StopConsumer()
    
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('Websocket connected...',event)
        # get default channel from a project:
        print("Channel Layer...",self.channel_layer)
        # get channel name
        print("Channel Name...",self.channel_name)
        # make a custom group name:
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        # add a channel to a new or existing group
        await self.channel_layer.group_add(
            self.group_name, # group name
            self.channel_name)
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self,event):
        print('Message Received From Client...',event['text'])
        data = json.loads(event['text'])
        # find group object
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        # create new chat object
        chat = Chat(
            content = data['msg'],
            group = group
        )
        await database_sync_to_async(chat.save)()
        await self.channel_layer.group_send(self.group_name,{
            'type': 'chat.message',
            'message': event['text']
        })

    async def chat_message(self,event):
        print("event...",event)
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self,event):
        print('Websocket Disconnected...',event)
        print("Channel Layer...",self.channel_layer)
        # get channel name
        print("Channel Name...",self.channel_name)
        # add a channel to a new or existing group
        await self.channel_layer.group_discard(
            self.group_name, # group name
            self.channel_name)
        raise StopConsumer()
        
    