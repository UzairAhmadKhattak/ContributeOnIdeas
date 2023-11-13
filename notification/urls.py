
from django.urls import path
from .views import return_user_projects
from .views import insert_notification
from .views import get_notifications
from .views import mark_notifications_as_checked
urlpatterns = [
    path('return_user_projects/', return_user_projects,name='return_user_projects'),
    path('insert_notification/', insert_notification,name='insert_notification'),
    path('get_notifications/', get_notifications,name='get_notifications'),
    path('mark_notifications_as_checked/', mark_notifications_as_checked,name='mark_notifications_as_checked'),
]