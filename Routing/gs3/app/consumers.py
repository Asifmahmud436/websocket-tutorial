from channels.consumer import AsyncConsumer, SyncConsumer
from channels.exceptions import StopConsumer

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket Connected...", event)
        self.send({'type': 'websocket.accept'})

    def websocket_receive(self, event): 
        print("Message Received...", event)
        print(event['text'])
        # if the server wants to send message to client
        self.send({
            'type':'websocket.send',
            'text':'Message Sent to Client'
        })

    def websocket_disconnect(self, event):
        print("Websocket Disconnected...", event)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket Connected...", event)
        await self.send({'type': 'websocket.accept'})

    async def websocket_receive(self, event): 
        print("Message Received...", event)
        print(event.get('text', ''))  
        # if the server wants to send message to client
        self.send({
            'type':'websocket.send',
            'text':'Message Sent to Client'
        })

    async def websocket_disconnect(self, event):
        print("Websocket Disconnected...", event)
        raise StopConsumer()
