from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at', 'updated_at']
    list_filter = ['user', 'post', 'created_at']
    search_fields = ['user__username', 'user__email', 'body']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
