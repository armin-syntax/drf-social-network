from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField

from utils.paths import get_user_profile_image_upload_path
from utils.validators import UsernameValidator, NameValidator, URLValidator


User = settings.AUTH_USER_MODEL


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[UsernameValidator()],
        error_messages={
            'unique': 'This username already exists.',
        },
    )
    email = models.EmailField(
        unique=True,
        verbose_name='email address',
        error_messages={
            'unique': 'This email address already exists.',
        },
    )
    first_name = models.CharField(max_length=15, validators=[NameValidator('First Name')])
    last_name = models.CharField(max_length=15, validators=[NameValidator('Last Name')])
    phone_number = PhoneNumberField(
        unique=True,
        error_messages={
            'unique': 'This phone number already exists.',
        },
    )
    bio = models.TextField(max_length=200, blank=True, null=True)
    image = models.ImageField(
        upload_to=get_user_profile_image_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])],
    )
    website_url = models.URLField(
        max_length=100,
        blank=True,
        null=True,
        validators=[URLValidator()],
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']

    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    # ----- COUNTS -----

    def get_followers_count(self):
        return self.followers.count()
    
    def get_following_count(self):
        return self.following.count()
    
    def get_posts_count(self):
        return self.posts.count()

    # ----- LISTS -----

    def get_follower_list(self):
        return CustomUser.objects.filter(following__to_user=self)
    
    def get_following_list(self):
        return CustomUser.objects.filter(followers__from_user=self)

    def get_post_list(self):
        return self.posts.all()


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['from_user', 'to_user']
    
    def __str__(self):
        return f"{self.from_user} followed {self.to_user}"
