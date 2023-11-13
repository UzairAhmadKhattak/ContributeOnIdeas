
from django.urls import path
from .views import insert_comment,update_status

urlpatterns = [
    path('insert_comment/',insert_comment,name='insert_comment'),
    path('update_status/',update_status,name='update_status')
]