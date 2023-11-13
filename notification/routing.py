from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
	path(r'ws/livec/notification/<str:idea_id>', consumers.notification.as_asgi()),
]
