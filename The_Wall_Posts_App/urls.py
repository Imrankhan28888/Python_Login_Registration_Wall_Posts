from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('wall', views.wall),
    path('post_message', views.post_message),
    path('add_comment/<int:id>', views.post_comment),
    path('delete_Mesg/<int:id>', views.delete_Mesg),
    path('delete/<int:id>', views.delete_comment),
    path('user_profile/<int:id>', views.profile),
    path('edit/<int:id>', views.edit),
    path('like/<int:id>', views.add_like),
 
]