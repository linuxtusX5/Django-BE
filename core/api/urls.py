from django.urls import path
from .views import register_view, login_view, logout_view, profile_view, CategoryListCreateView, CategoryDetailView, ItemListCreateView, ItemDetailView, MyItemView, dashboard_stats

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/profile/', profile_view, name='profile'),

    # Categories endpoints
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<str:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    #Item endpoints
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<str:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('my-items/', MyItemView.as_view(), name='my-items'),

    # Dashboard
    path('dashboard/stats/', dashboard_stats, name='dashboard-stats'),
]