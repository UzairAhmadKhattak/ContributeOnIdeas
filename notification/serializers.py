
from rest_framework import serializers
from ideas_app.models import NewFeed
from .models import Notification

class notification_app_NewFeed_serializer(serializers.ModelSerializer):
    class Meta:
        model = NewFeed
        fields = "__all__"

class notification_app_notification_get_serializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class notification_app_notification_insert_serializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notification_message','notification_from','notification_to']

class notification_app_notification_update_serializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['checked']
