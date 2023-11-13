import os

from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from chat import routing as chat_rout
from notification import routing as notification_rout 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ContributeOnIdeas.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_rout.websocket_urlpatterns +
            notification_rout.websocket_urlpatterns
        )
        )
    }
)