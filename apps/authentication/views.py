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
from io import BytesIO
from django.db import transaction
from django.core.exceptions import ValidationError 
from django.urls import reverse

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

def validate_image_format(image):
  
    allowed_formats = ['JPEG', 'PNG', 'JPG']

   
    try:
        img = Image.open(image)
        img_format = img.format

        
        if img_format not in allowed_formats:
            raise ValidationError(f"Unsupported image format: {img_format}. Please upload a JPEG or PNG image.")
    except Exception as e:
        raise ValidationError(f"Could not open the image: {str(e)}")


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            try:
               
                face_image = form.cleaned_data.get('face_image')
                validate_image_format(face_image)  

                with transaction.atomic():  
                    
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data.get('password1')) 
                    user.save()
                    print("User created successfully.")  

                    
                    image = Image.open(face_image)
                    image_np = np.array(image)
                    face_encodings = face_recognition.face_encodings(image_np)

                    if face_encodings:
                        face_encoding = face_encodings[0].tolist()  

                      
                        user_profile = UserProfile(
                            user=user,
                            face_image=face_image,
                            role='teacher', 
                            teaching_subject=form.cleaned_data.get('teaching_subject', ''),
                            about_me=form.cleaned_data.get('about_me', ''),
                            address=form.cleaned_data.get('address', ''),
                            phone=form.cleaned_data.get('phone', ''),
                            face_encoding=json.dumps(face_encoding)  
                        )
                        user_profile.save()
                        print("UserProfile created successfully.")  

                      
                        return redirect(reverse('login')) 

                    else:
                        msg = "No face detected in the uploaded image. Please upload a clear face image."
                        print("No face detected in the image.")  

            except ValidationError as ve:
                msg = str(ve) 
                print(f"Validation error occurred: {msg}")  
            except Exception as e:
                msg = f"Error processing the image or saving the user profile: {str(e)}"
                print(f"Exception occurred: {e}") 

        else:
            msg = 'The form is invalid. Please correct the errors below.'
            print(f"Form errors: {form.errors}") 

    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})



def user_list(request):
  
    users = User.objects.all()
    user_profiles = UserProfile.objects.select_related('user')  

    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(Q(username__icontains=search_query) | Q(email__icontains=search_query))

    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(userprofile__role=role_filter)

    # Implement pagination
    from django.core.paginator import Paginator
    paginator = Paginator(users, 10)  
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    return render(request, 'authentication/user_list.html', {'users': users})




@login_required
def edit_user(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk) 
    user_profile = get_object_or_404(UserProfile, user=user) 

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)  
        if form.is_valid():
          
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.save()  

            form.save()  
            return redirect('user_list')  
    else:
        form = UserProfileForm(instance=user_profile)  

    return render(request, 'authentication/edit_user.html', {'form': form, 'user': user})

@login_required
def edit_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        print("Request POST data:", request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid():
           
            user.username = request.POST.get('username', user.username)  
            user.email = request.POST.get('email', user.email) 
            user.first_name = request.POST.get('first_name', user.first_name)  
            user.last_name = request.POST.get('last_name', user.last_name)  
            user.save() 
            
          
            user_profile = profile_form.save(commit=False)

            if 'face_image' in request.FILES:
                face_image = request.FILES['face_image']
                try:
                    image = Image.open(face_image)
                    image_np = np.array(image)
                    face_encodings = face_recognition.face_encodings(image_np)

                    if len(face_encodings) > 0:
                        face_encoding = face_encodings[0].tolist()
                        user_profile.set_face_encoding(face_encoding)

                except Exception as e:
                    messages.error(request, f"Error processing the image for encoding: {str(e)}")

           
            user_profile.save()  
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  
    else:
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'authentication/edit_profile.html', {
        'form': profile_form,
        'user': user,
    })


@login_required
def delete_user(request, pk):
    User = get_user_model()  
    user = get_object_or_404(User, pk=pk)  

    if request.method == 'POST':
        user.delete()  
        messages.success(request, f'User {user.username} has been deleted successfully.')
        return redirect('user_list') 

    return render(request, 'authentication/delete_user.html', {'user': user})



@login_required
def user_profile_view(request):
  
    user_profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'user': request.user,  
        'user_profile': user_profile,  
    }
    return render(request, 'home/profile.html', context)  

def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, "L'utilisateur a été désactivé avec succès.")
    return redirect('user_list')


@login_required
def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'authentication/user_details.html', {
        'user': user,
        'current_user': request.user  
    })
def get_user_stats(request):
    total_students = UserProfile.objects.filter(role='student').count()  
    total_teachers = UserProfile.objects.filter(role='teacher').count()  
    return JsonResponse({'total_students': total_students, 'total_teachers': total_teachers})

def user_details_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    return render(request, 'authentication/user_details.html', {'user_profile': user_profile})    