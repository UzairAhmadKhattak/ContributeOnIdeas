
from django.urls import path
from .views import home,profile,ideas,logout_form
from .views import search_idea,login_form,signup,specific_idea
from .views import post_idea,edit_profile

urlpatterns = [
    path('home/', home,name='home'),
    path('home/post_idea',post_idea,name='post_idea'),
    path('profile/<slug:username>/',profile,name='profile'),
    path('edit_profile',edit_profile,name='edit_profile'),
    path('ideas/<slug:username>',ideas,name='ideas'),
    path('login',login_form,name='login'),
    path('logout',logout_form,name='logout'),
    path('specific_idea/<str:idea_name>',specific_idea,name='specific_idea'),
    path('search_idea',search_idea,name='search_idea'),
    path('signup',signup,name='signup'),


]
