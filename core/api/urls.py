from django.urls import path
from .views import register_view

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', register_view, name='register'),
]