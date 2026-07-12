from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import generics, permissions, filters

from utils.permissions import IsOwnerOrReadOnlyPermission
from .models import Post, Comment
from .serializers import (
    PostCreateSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentCreateSerializer,
    CommentSerializer,
)


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'description']
    
    def get_serializer_class(self):
        return PostListSerializer if self.request.method == 'GET' else PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyPermission]
    lookup_field = 'pk'
    lookup_url_kwarg = 'post_id'


class CommentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        get_object_or_404(Post, pk=self.kwargs['post_id'])
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def get_serializer_class(self):
        return (
            CommentSerializer
            if self.request.method == 'GET'
            else CommentCreateSerializer
        )

    def perform_create(self, serializer):
        get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(
            user=self.request.user,
            post_id=self.kwargs['post_id'],
        )