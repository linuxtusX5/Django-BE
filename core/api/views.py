from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import (UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, CategorySerializer)
from django.contrib.auth import login, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Category
from django.db.models import Q
from django.utils.decorators import method_decorator
from bson import ObjectId


# Authentication Views
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """User registration endpoint"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        
        # Convert ObjectId to string for response
        user_id = str(user._id) if hasattr(user, '_id') else user.id

        return Response({
            'user_id': user_id,
            'username': user.username,
            'email': user.email,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User login endpoint"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key,
            'message': 'Login Successful'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.AllowAny])
def logout_view(request):
    """User logout endpoint"""
    try:
        request.user.auth_token.delete()
    except:
        pass
    logout(request)
    return Response({'message': 'Logout Successful'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def profile_view(request):
    """Get user profile"""
    try:
        profile = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListCreateView(generics.ListCreateAPIView):
    """List all categories or create a new category"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        return queryset


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Category.objects.get(_id=ObjectId(pk))

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        category.is_active = False
        category.save()
        return Response({'message': 'Category deactivated Successfully'}, status=status.HTTP_200_OK)