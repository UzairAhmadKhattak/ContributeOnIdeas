from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
	path(r'ws/livec/chat/<str:other_user>', consumers.chat.as_asgi()),
]
