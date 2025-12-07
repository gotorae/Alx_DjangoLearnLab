

from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # ✅ Tags (via django-taggit)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)   # when created
    updated_at = models.DateTimeField(auto_now=True)       # last edit time

    class Meta:
        ordering = ['created_at']  # oldest first (natural reading order)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


