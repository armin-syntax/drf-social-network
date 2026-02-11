from django.urls import path

from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.PostListCreateAPIView.as_view(), name='post-list-create'),
    path('<int:pk>/', views.PostDetailAPIView.as_view(), name='post-detail'),
]
