from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),	
    path('newpost', views.newPost),
    path('newcomment', views.newComment),
    path('wall', views.wall),
    path('delete_msg/<int:message_id>', views.deleteMsg),
    path('delete_comment/<int:comment_id>', views.deleteComment),
    path('logout', views.logout) 
]