from rest_framework import serializers

from accounts.serializers import UserInlineSerializer
from .models import Post, Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at']
        read_only_fields = ['id', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PostListSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='posts:post-detail',
        lookup_field='pk',
    )

    class Meta:
        model = Post
        fields = ['id', 'created_at', 'updated_at']


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'body',
            'created_at',
            'updated_at',
            'comments',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
