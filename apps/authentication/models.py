from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_image = models.ImageField(upload_to='face_images/')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')  
    teaching_subject = models.CharField(max_length=100)
    about_me = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
