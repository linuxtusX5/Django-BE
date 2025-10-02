from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer


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
