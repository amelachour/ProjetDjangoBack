# from django.db import models
# from django.contrib.auth.models import User

# class UserProfile(models.Model):
#     ROLE_CHOICES = [
#         ('admin', 'Admin'),
#         ('teacher', 'Teacher'),
#         ('student', 'Student'),
#     ]
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     face_image = models.ImageField(upload_to='face_images/')
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='teacher')  
#     teaching_subject = models.CharField(max_length=100)
#     about_me = models.TextField(blank=True)
#     address = models.CharField(max_length=255, blank=True)
#     phone = models.CharField(max_length=15, blank=True, null=True)
    
#     def __str__(self):
#         return self.user.username
from django.db import models
from django.contrib.auth.models import User
import json

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_image = models.ImageField(upload_to='face_images/')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    teaching_subject = models.CharField(max_length=100, null=True, blank=True, default="unknown")  # Valeur par défaut "unknown" # Make it optional for non-teachers
    about_me = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    face_encoding = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Check if the user is a teacher and ensure that teaching_subject is filled
        if self.role == 'teacher' and not self.teaching_subject:
            raise ValueError("Teaching subject is required for teachers.")
        
        # Handle face encoding
        if isinstance(self.face_encoding, list):
            self.face_encoding = json.dumps(self.face_encoding)
        super().save(*args, **kwargs)

    def set_face_encoding(self, encoding):
        if isinstance(encoding, list):
            self.face_encoding = json.dumps(encoding)
        else:
            raise ValueError("Encoding must be a list.")

    def get_face_encoding(self):
        try:
            return json.loads(self.face_encoding) if self.face_encoding else None
        except json.JSONDecodeError:
            return None  # Handle encoding errors

    def __str__(self):
        return self.user.username
