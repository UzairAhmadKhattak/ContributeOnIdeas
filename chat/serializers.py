from rest_framework import serializers
from .models import Message
from ideas_app.models import UserProfile
from django.contrib.auth.models import User


class chat_app_insert_message_serializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['fk_send_by_user_profile_id','fk_received_by_user_id','message']

class User(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user']

    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        fk_user_id = obj.fk_user_id
        return User(fk_user_id).data

class chat_app_get_message_serializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
    
    user_profile = serializers.SerializerMethodField()

    def get_user_profile(self, obj):
        fk_send_by_user_id = obj.fk_send_by_user_profile_id
        return UserProfileSerializer(fk_send_by_user_id).data