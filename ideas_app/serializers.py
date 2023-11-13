
from rest_framework import serializers
from .models import Comment,NewFeed

class idea_app_insert_comment_serializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment','comment_by','fk_new_feed_id']
class idea_app_change_status_serializer(serializers.ModelSerializer):
    class Meta:
        model = NewFeed
        fields = ['status']