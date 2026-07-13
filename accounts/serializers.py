from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Relation


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'full_name',
            'password',
            'confirm_password',
        ]

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValidationError({'confirm_password': "Passwords didn`t match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'full_name'
            'bio',
            'avatar',
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.user != instance:
            data['email'] = None

        return data


class UserDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    is_owner = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'full_name',
            'bio',
            'avatar',
            'posts_count',
            'followers_count',
            'following_count',
            'is_owner',
            'is_following',
        ]
        read_only_fields = [
            'id',
            'posts_count',
            'followers_count',
            'following_count',
            'is_owner',
            'is_following',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.user != instance:
            data['email'] = None

        return data

    def get_is_owner(self, obj):
        request = self.context.get('request')

        if not request or request.user.is_anonymous:
            return False

        return request.user == obj

    def get_is_following(self, obj):
        request = self.context.get('request')

        if not request or request.user.is_anonymous:
            return False

        if request.user == obj:
            return False

        return Relation.objects.filter(from_user=request.user, to_user=obj).exists()


class UserInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'bio', 'avatar']
