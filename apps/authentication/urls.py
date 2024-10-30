# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user ,course_list
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login', login_view, name="login"),
    path('register', register_user, name="register"),
    path("logout", LogoutView.as_view(), name="logout"),    
    path('listcours', course_list, name='listcours'),  
]
