# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user
from . import views
from django.contrib.auth.views import LogoutView
from .views import login_view, facial_recognition_login
from .views import user_list
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views  # Assurez-vous d'importer vos vues



urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
     path("logout/", LogoutView.as_view(), name="logout"),
       path('facial-recognition-login/', facial_recognition_login, name='facial_recognition_login'),
         path('users/', user_list, name='user_list'),
          path('users/edit/<int:pk>/', views.edit_user, name='edit_user'),  # Assurez-vous d'avoir cette ligne
    path('users/delete/<int:pk>/', views.delete_user, name='delete_user'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


