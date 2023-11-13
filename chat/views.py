from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .serializers import chat_app_insert_message_serializer
from .serializers import chat_app_get_message_serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q
from ideas_app.models import UserProfile
from django.contrib.auth.models import User

@login_required(login_url="login")
def messages(request):
    user_profile_row = UserProfile.objects.get(fk_user_id=request.user.id)
    chat_users = UserProfile.objects.exclude(fk_user_id__username=request.user.username).select_related('fk_user_id').values('fk_user_id__username')
    return render(request,'chat/messages.html',
                  {"user_profile_row":user_profile_row,
                   'chat_users':chat_users
                   })

@api_view(["POST"])
def insert_message(request):
    if request.user.is_authenticated:
        fk_received_by_user_name = request.data['fk_received_by_user_name']
        message = request.data['message']
        user = User.objects.get(username=fk_received_by_user_name)
        message = {
            'fk_send_by_user_profile_id':request.user.id,
            'fk_received_by_user_id':user.id,
            'message':message
        }
    
        msg_srlzr = chat_app_insert_message_serializer(data=message)
        if msg_srlzr.is_valid():
            msg_srlzr.save()
            return Response({"msg":"message is saved"})
        else:
            return Response({'msg':msg_srlzr.errors})
    else:
        return Response({'msg':'unauthenticated request'},403)

@api_view(['GET'])
def get_messages(request,username):
    if request.user.is_authenticated:
        user = User.objects.get(username=username)
        messages = Message.objects.filter(Q(Q(fk_send_by_user_profile_id=user.id)&Q(fk_received_by_user_id=request.user.id))|
                                          Q(Q(fk_send_by_user_profile_id=request.user.id)&Q(fk_received_by_user_id=user.id))
                                          
                                          ).select_related('fk_send_by_user_profile_id')
        serializer = chat_app_get_message_serializer(messages,many=True)    
        return Response({'messages':serializer.data},200)
    else:
        return Response({'error':'unauthenticated request'},403)

         
        