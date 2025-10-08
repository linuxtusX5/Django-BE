from django.urls import path
from .views import register_view, login_view, logout_view, profile_view, CategoryListCreateView

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/profile/', profile_view, name='profile'),

    # Categories endpoint
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),

]