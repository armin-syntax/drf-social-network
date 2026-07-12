from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

from utils.paths import post_media_upload_path


User = settings.AUTH_USER_MODEL


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    media = models.FileField(
        upload_to=post_media_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "jpeg",
                    "png",
                    "gif",
                    "webp",
                    "mp4",
                    "mov",
                    "webm",
                ],
            ),
        ],
    )
    description = models.TextField(max_length=2200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.get_short_description
    
    @property
    def get_short_description(self):
        return self.description[:20] + '...' if len(self.description) > 20 else self.description
    
    @property
    def comments_count(self):
        return self.comments.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.get_short_body

    @property
    def get_short_body(self):
        return self.body[:20] + '...' if len(self.body) > 20 else self.body
