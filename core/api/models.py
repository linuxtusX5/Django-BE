from mongoengine import Document, EmbeddedDocument, fields
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class BaseDocument(Document):
    """Base document with common fields"""
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {'abstract': True}
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)


class Address(EmbeddedDocument):
    """Embedded document for user address"""
    street = fields.StringField(max_length=200)
    city = fields.StringField(max_length=100)
    state = fields.StringField(max_length=100)
    country = fields.StringField(max_length=100)
    postal_code = fields.StringField(max_length=20)


class UserProfile(BaseDocument):
    """Extended user profile document"""
    user_id = fields.IntField(required=True, unique=True)  # Reference to Django User ID
    username = fields.StringField(max_length=150, required=True)  # Denormalized
    email = fields.EmailField()  # Denormalized
    bio = fields.StringField()
    avatar = fields.URLField()
    phone = fields.StringField(max_length=20)
    address = fields.EmbeddedDocumentField(Address)
    preferences = fields.DictField()
    is_verified = fields.BooleanField(default=False)
    
    meta = {
        'collection': 'user_profiles',
        'indexes': ['user_id', 'username', 'email']
    }
    
    def __str__(self):
        return f"{self.username}'s Profile"
    
    @classmethod
    def create_from_user(cls, user):
        """Create profile from Django User instance"""
        profile = cls(
            user_id=user.id,
            username=user.username,
            email=user.email
        )
        profile.save()
        return profile