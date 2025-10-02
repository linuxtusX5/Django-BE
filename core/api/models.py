from djongo import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class BaseModel(models.Model):
    """Base model with common fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class UserProfile(BaseModel):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.JSONField(default=dict, blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"