
from .views import insert_message,get_messages
from django.urls import path

urlpatterns = [
    path('insert_message/', insert_message,name='insert_message'),
    path('get_messages/<str:username>/', get_messages,name='get_messages'),
]