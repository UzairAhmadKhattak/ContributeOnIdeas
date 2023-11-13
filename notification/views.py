from rest_framework.decorators import api_view
from rest_framework.response import Response
from ideas_app.models import UserProfile
from ideas_app.models import NewFeed
from .models import Notification
import sys
from .serializers import notification_app_NewFeed_serializer
from .serializers import notification_app_notification_get_serializer
from .serializers import notification_app_notification_insert_serializer
from .serializers import notification_app_notification_update_serializer

@api_view(["GET"])
def return_user_projects(request):
    try:
        user_profile_row = UserProfile.objects.get(fk_user_id=request.user.id)
        user_projects_rows = NewFeed.objects.filter(fk_user_profile_id=user_profile_row.id)
        serializer = notification_app_NewFeed_serializer(user_projects_rows, many=True)
        return Response(serializer.data)
    except Exception as e:
        _, _, line_tb = sys.exc_info()
        line_num = line_tb.tb_lineno
        print('problem in return_user_projects API:',e,'line_num:',line_num)
        return Response({'message':'No resources'})

@api_view(["POST"])
def insert_notification(request):
    try:
        serializer = notification_app_notification_insert_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Notification is saved"})
        else:
            return Response({'msg':serializer.errors})
    except Exception as e:
        print(e)
        return Response({'msg':'Error'})

@api_view(["GET"])
def get_notifications(request):
    notification = Notification.objects.filter(notification_to=request.user.id).order_by('-notified_at')
    serializer = notification_app_notification_get_serializer(notification,many=True)
    return Response(serializer.data)

@api_view(["PUT"])
def mark_notifications_as_checked(request):
    try:
        notifications = Notification.objects.filter(notification_to=request.user.id)
        for notification in notifications:
            serializer = notification_app_notification_update_serializer(notification,data={'checked':True})
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'msg':serializer.errors})
        return Response({"msg":"Notifications are checked successfully"})
    except Exception as e:
        print(e)
        return Response({'msg':''})