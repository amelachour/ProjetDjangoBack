# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user
from . import views
from django.contrib.auth.views import LogoutView
from .views import login_view
from .views import user_list , edit_profile
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views  # Assurez-vous d'importer vos vues
from .views import UserProfile 
from .views import user_profile_view 
from .views import get_user_stats
from .views import user_details_view
urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
      
    path('users/', user_list, name='user_list'),
    
    path('users/edit-profile/<int:pk>/', views.edit_profile, name='edit_profile'),  # Renamed
    path('users/edit-user/<int:pk>/', views.edit_user, name='edit_user'),  # Renamed
    path('users/details/<int:user_id>/', user_details_view, name='user_details'),
    path('users/delete/<int:pk>/', views.delete_user, name='delete_user'),
     path('users/profile/', user_profile_view, name='profile'), 
     path('api/stats/', get_user_stats, name='user_stats'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


