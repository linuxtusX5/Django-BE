from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Category, Item
from django.contrib.auth import authenticate
from bson import ObjectId

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return user

class UserLoginSerializer(serializers.Serializer):
    """Serializer for user Login"""
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            attrs['user'] = user
        else:
            raise serializers.ValidationError("Must include username and password")
        
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user Profile"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email','first_name', 'last_name', 'bio', 'avatar', 'phone', 'address', 'preferences', 'is_verified', 'created_at', 'updated_at')

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category model"""
    items_count = serializers.SerializerMethodField()
    id = serializers.CharField(source='_id', read_only=True) 

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'is_active', 'items_count', 'created_at', 'updated_at')

    def get_items_count(self, obj):
        # return obj.items.filter(is_available=True).count() 
        return len([item for item in obj.items.all() if item.is_available])
        # return Item.objects.filter(category=obj, is_available=True).count()

class ItemSerializer(serializers.ModelSerializer):
    """Serializer for item model"""
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    category = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Item
        fields = ('id', 'title', 'description', 'category', 'category_name', 'owner', 'owner_username', 'price', 'quantity', 'is_available', 'tags', 'metadata', 'created_at', 'updated_at')
        read_only_fields = ['owner']

    def create(self, validated_data):
        # Handle ObjectId for category
        category_id = validated_data.pop('category', None)
        if category_id:
            try:
                category = Category.objects.get(_id=ObjectId(category_id))
                validated_data['category'] = category
            except Category.DoesNotExist:
                raise serializers.ValidationError({"category": "Category not found"})
        
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class ItemListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for item lists"""
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'title', 'category_name', 'owner_username', 'price', 'quantity', 'is_available', 'created_at')