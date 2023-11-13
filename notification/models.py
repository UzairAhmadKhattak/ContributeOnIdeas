from django.db import models
from ideas_app.models import UserProfile
# Create your models here.


class Notification(models.Model):
    
    notification_from = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='notification_from')
    notification_to = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='notification_to')
    notification_message = models.CharField(max_length=100)
    checked = models.BooleanField(default=False)
    notified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.notification_message