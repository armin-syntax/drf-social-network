from django.db.models import Count
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response

from utils.permissions import IsOwnerOrReadOnlyPermission
from .models import Post
from .serializers import (
    PostCreateSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentCreateSerializer,
)


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.annotate(comments_count=Count('comments'))
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['body']
    
    def get_serializer_class(self):
        return PostListSerializer if self.request.method == 'GET' else PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyPermission]
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
