from app import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/ac/', consumers.MyAsyncConsumer.as_asgi()),
    path('ws/sc/', consumers.MySyncConsumer.as_asgi()),  
]
