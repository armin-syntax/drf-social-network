from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.reverse import reverse

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
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'confirm_password',
        ]

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValidationError({'confirm_password': "Passwords don't match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


class UserListSerializer(serializers.ModelSerializer):
    profile_url = serializers.HyperlinkedIdentityField(
        view_name='accounts:user-detail',
        lookup_field='username',
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'bio',
            'image',
            'profile_url',
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.user != instance:
            data['email'] = None
            data['phone_number'] = None
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    posts_count = serializers.IntegerField(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

    post_list_url = serializers.HyperlinkedIdentityField(
        view_name='accounts:user-post-list',
        lookup_field='username',
    )
    follower_list_url = serializers.HyperlinkedIdentityField(
        view_name='accounts:user-follower-list',
        lookup_field='username',
    )
    following_list_url = serializers.HyperlinkedIdentityField(
        view_name='accounts:user-following-list',
        lookup_field='username',
    )
    follow_url = serializers.SerializerMethodField()
    unfollow_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'website_url',
            'bio',
            'image',
            'posts_count',
            'followers_count',
            'following_count',
            'post_list_url',
            'follower_list_url',
            'following_list_url',
            'follow_url',
            'unfollow_url',
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.user != instance:
            data['email'] = None
            data['phone_number'] = None
        return data
    
    def get_follow_url(self, obj):
        request = self.context.get('request')

        if not request or request.user == obj:
            return None
        
        if Relation.objects.filter(from_user=request.user, to_user=obj).exists():
            return None
    
        return reverse('accounts:user-follow', args=[obj.username], request=request)

    def get_unfollow_url(self, obj):
        request = self.context.get('request')

        if not request or request.user == obj:
            return None
        
        if not Relation.objects.filter(from_user=request.user, to_user=obj).exists():
            return None
        
        return reverse('accounts:user-unfollow', args=[obj.username], request=request)


class UserInlineSerializer(serializers.ModelSerializer):
    profile_url = serializers.HyperlinkedIdentityField(
        view_name='accounts:user-detail',
        lookup_field='username',
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_url']
