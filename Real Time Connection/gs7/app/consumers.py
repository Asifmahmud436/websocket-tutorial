from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio,json

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print("Websocket Connected",event)
        self.send(
            {'type':'websocket.accept',}
        )
    # can do the same think on async
    def websocket_receive(self,event):
        print(event['text'])
        for i in range(11):
            self.send({
                'type':'websocket.send',
                'text': json.dumps({'count':i}),
            })
            sleep(1)
    # def websocket_receive(self,event):
    #     print(event['text'])
    #     for i in range(11):
    #         self.send({
    #             'type':'websocket.send',
    #             'text': str(i),
    #         })
    #         sleep(1)

    def websocket_disconnect(self,event):
        print("Websocket Disconnected...",event)
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("Websocket Connected",event)
        await self.send({
            'type':'websocket.accept',
        })

    async def websocket_receive(self,event):
        print(event['text'])
        for i in range(11):
            await self.send({
            'type':'websocket.send',
            'text': str(i),
            })
            await asyncio.sleep(1)
        
    async def websocket_disconnect(self,event):
        print("Websocket Disconnected",event)
        raise StopConsumer()