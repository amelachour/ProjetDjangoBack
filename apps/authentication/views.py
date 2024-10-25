# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
# views.py
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from .models import UserProfile
import face_recognition
from django.core.files.storage import default_storage
import json
import base64
import os
import io
from django.http import JsonResponse
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from .models import User


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

import face_recognition
import numpy as np
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .forms import UserProfile  # Assurez-vous d'avoir un formulaire pour cela

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model

from django.shortcuts import render
from django.contrib.auth.models import User
from apps.authentication.models import UserProfile

from django.shortcuts import render
from django.contrib.auth.models import User
from apps.authentication.models import UserProfile
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index.html')  # Redirect to the dashboard if credentials are correct
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})





def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Save face image and role in user profile
            UserProfile.objects.create(user=user, face_image=form.cleaned_data.get('face_image'), role='student',teaching_subject=form.cleaned_data.get('teaching_subject'),
                                    about_me=form.cleaned_data.get('about_me') ) # Save user profile # Set role to "student"
            msg = 'User created - please <a href="/login">log in</a>.'
            success = True
        else:
            msg = 'The form is invalid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})




def user_list(request):
    # Get all users and their corresponding profiles
    users = User.objects.all()
    user_profiles = UserProfile.objects.select_related('user')  # Use select_related for optimization

    # Apply search filter
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(Q(username__icontains=search_query) | Q(email__icontains=search_query))

    # Apply role filter
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(userprofile__role=role_filter)

    # Implement pagination
    from django.core.paginator import Paginator
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    return render(request, 'authentication/user_list.html', {'users': users})




@login_required
def edit_user(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)  # Récupère l'utilisateur par son identifiant
    user_profile = get_object_or_404(UserProfile, user=user)  # Récupérer le UserProfile lié à cet utilisateur

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)  # Utilisez request.FILES pour gérer les fichiers
        if form.is_valid():
            # Mettre à jour le nom d'utilisateur et l'email
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.save()  # Sauvegarder les modifications de l'utilisateur

            form.save()  # Sauvegarder les modifications du UserProfile
            return redirect('user_list')  # Redirige vers la liste des utilisateurs
    else:
        form = UserProfileForm(instance=user_profile)  # Pré-remplit le formulaire avec les données de UserProfile

    return render(request, 'authentication/edit_user.html', {'form': form, 'user': user})



@login_required
def edit_profile(request, pk):
    user = request.user

    # Get the user profile or return a 404 if not found
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        # Create a form instance with the data from the request
        form = UserProfileForm(request.POST, instance=user_profile)
        
        if form.is_valid():
            # Save the form to update the user profile
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to the profile page
    else:
        # Prepopulate the form with existing data
        form = UserProfileForm(instance=user_profile)

    return render(request, 'authentication/edit_profile.html', {
        'form': form,
        'user': user,
    })
@login_required
def delete_user(request, pk):
    User = get_user_model()  # Récupère le modèle utilisateur personnalisé
    user = get_object_or_404(User, pk=pk)  # Récupère l'utilisateur par son identifiant

    if request.method == 'POST':
        user.delete()  # Supprime l'utilisateur
        messages.success(request, f'User {user.username} has been deleted successfully.')
        return redirect('user_list')  # Redirige vers la liste des utilisateurs

    return render(request, 'authentication/delete_user.html', {'user': user})



# def profile_view(request):
#     user = get_object_or_404(UserProfile, user=request.user)

#     context = {
#         'user': user,
#     }
#     return render(request, 'profile.html', context)
@login_required
def user_profile_view(request):
    # Retrieve the user profile associated with the logged-in user
    user_profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'user': request.user,  # The logged-in User object
        'user_profile': user_profile,  # The UserProfile object
    }
    return render(request, 'home/profile.html', context)  # Adjust the template path as needed


def get_user_stats(request):
    total_students = UserProfile.objects.filter(role='student').count()  # Count the number of students
    total_teachers = UserProfile.objects.filter(role='teacher').count()  # Count the number of teachers
    return JsonResponse({'total_students': total_students, 'total_teachers': total_teachers})

def user_details_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    return render(request, 'authentication/user_details.html', {'user_profile': user_profile})    