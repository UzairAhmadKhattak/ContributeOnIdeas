from django.db import models
from ideas_app.models import UserProfile
# Create your models here.

class Message(models.Model):
    fk_send_by_user_profile_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='send_by')
    fk_received_by_user_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='received_by')
    message = models.TextField()
    time = models.DateTimeField(auto_now=True)
