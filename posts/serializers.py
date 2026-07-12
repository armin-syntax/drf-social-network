from rest_framework import serializers

from accounts.serializers import UserInlineSerializer
from .models import Comment, Post


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'media', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PostListSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer(read_only=True)
    comments_count = serializers.ReadOnlyField()
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='posts:post-detail',
        lookup_field='pk',
        lookup_url_kwarg='post_id',
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'media',
            'description',
            'comments_count',
            'detail_url',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'detail_url', 'created_at', 'updated_at']


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer(read_only=True)
    comments_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'media',
            'description',
            'created_at',
            'updated_at',
            'comments_count',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
