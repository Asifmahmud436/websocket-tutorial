import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gs3.settings')
import app.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        app.routing.websocket_urlpatterns
    )
})
