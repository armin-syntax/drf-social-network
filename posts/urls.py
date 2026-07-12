from django.urls import path

from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.PostListCreateAPIView.as_view(), name='post-list-create'),
    path('<int:post_id>/', views.PostDetailAPIView.as_view(), name='post-detail'),
    path('<int:post_id>/comments/', views.CommentListCreateAPIView.as_view(), name='comment-list-create'),
]
