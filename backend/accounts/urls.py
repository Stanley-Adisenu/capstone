from django.urls import path
from . import views 

urlpatterns = [
    path('topic/',views.topics),
    path('activity/',views.activity),
    path('home/',views.home),
    path('createroom/',views.createRoom),
    path('chat/<int:pk>/',views.room),
    path('updateroom/<int:pk>/',views.updateRoom),
    path('deleteroom/<int:pk>/',views.deleteRoom),
    path('deletemessage/<int:pk>/',views.deleteMessage),
    path('userprofile/<int:pk>/',views.userProfile),



]