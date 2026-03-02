from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.permissions import (
    IsAnonymousPermission,
    IsNotSelfPermission,
    IsOwnerOrReadOnlyPermission,
)
from posts.serializers import PostListSerializer
from .models import Relation
from .serializers import (
    UserCreateSerializer,
    UserListSerializer,
    UserDetailSerializer,
)


User = get_user_model()


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'bio']
    
    def get_permissions(self):
        return [permissions.IsAuthenticated()] if self.request.method == 'GET' else [IsAnonymousPermission()]

    def get_serializer_class(self):
        return UserListSerializer if self.request.method == 'GET' else UserCreateSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.annotate(
        posts_count=Count('posts'),
        followers_count=Count('followers'),
        following_count=Count('following'),
    )
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyPermission]
    serializer_class = UserDetailSerializer
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class UserFollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNotSelfPermission]

    def post(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])

        if Relation.objects.filter(from_user=request.user, to_user=user).exists():
            return Response(status=status.HTTP_409_CONFLICT)
        
        Relation.objects.create(from_user=request.user, to_user=user)
        return Response(status=status.HTTP_201_CREATED)


class UserUnfollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNotSelfPermission]

    def delete(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if not relation.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserFollowerListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return user.get_follower_list()


class UserFollowingListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return user.get_following_list()


class UserPostListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostListSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['body']

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return user.get_post_list()
