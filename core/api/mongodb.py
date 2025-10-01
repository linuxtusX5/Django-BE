from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AnonymousUser
from .models import MongoUser

class MongoUserWrapper:
    """Wrap MongoDB user to behave like a Django user model."""
    def __init__(self, mongo_user):
        self.mongo_user = mongo_user
        self.id = str(mongo_user._id)  # Use MongoDB ObjectId as the PK
        self.username = mongo_user.username
        self.email = mongo_user.email
        self.is_authenticated = True  # Required by Django

    @property
    def pk(self):
        return self.id  # Django uses this as the unique identifier

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_username(self):
        return self.username


class MongoBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = MongoUser.objects.get(username=username)
        except MongoUser.DoesNotExist:
            return None

        if user.check_password(password):
            return MongoUserWrapper(user)
        return None

    def get_user(self, user_id):
        try:
            user = MongoUser.objects.get(_id=user_id)
            return MongoUserWrapper(user)
        except MongoUser.DoesNotExist:
            return None