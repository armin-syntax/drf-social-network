from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path('', views.UserListCreateAPIView.as_view(), name='user-list-create'),
    path('<str:username>/', views.UserDetailAPIView.as_view(), name='user-detail'),
    path('<str:username>/follow/', views.UserFollowAPIView.as_view(), name='user-follow'),
    path('<str:username>/unfollow/', views.UserUnfollowAPIView.as_view(), name='user-unfollow'),
    path('<str:username>/followers/', views.UserFollowerListView.as_view(), name='user-follower-list'),
    path('<str:username>/following/', views.UserFollowingListAPIView.as_view(), name='user-following-list'),
    path('<str:username>/posts/', views.UserPostListAPIView.as_view(), name='user-post-list'),
]
