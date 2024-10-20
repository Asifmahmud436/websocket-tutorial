from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer

# This is SyncConsumer 
class MySyncConsumer(SyncConsumer):
    # this handler is called when client initially opens a connection and is about to finish the websocket handshake
    def websocket_connect(self,event):
        print('Websocket Connected ...')

    # this handler is called when data is recieved from client
    def websocket_recieve(self,event):
        print('Message Recieved...')

    # this handler is called when either or both connection from client/server is lost or disconnected or loss of the socket
    def websocket_disconnect(self,event):
        print('Websocket Disconnected...')


# This is AsyncConsumer 
class MyAsyncConsumer(AsyncConsumer):
    # this handler is called when client initially opens a connection and is about to finish the websocket handshake
    async def websocket_connect(self,event):
        print('Websocket Connected ...')

    # this handler is called when data is recieved from client
    async def websocket_recieve(self,event):
        print('Message Recieved...')

    # this handler is called when either or both connection from client/server is lost or disconnected or loss of the socket
    async def websocket_disconnect(self,event):
        print('Websocket Disconnected...')