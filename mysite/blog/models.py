from django.db import models
from django.utils import timezone
from django.conf import settings

# Defining Custom Manager to Retrieve Published Posts
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    # Draft and Published statuses for posts
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    # Attributes
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, 
        choices=Status, 
        default=Status.DRAFT
    )
    # From Users to Post, access like user.blog_posts
    # AUTH_USER_MODEL: Default: 'auth.User' The model to use to represent a User
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="blog_posts"
    )

    # Model Managers
    objects = models.Manager() # default manager
    published = PublishedManager() # custom manager
    
    class Meta:
        # Order in reverse chronological order whenever query retrieves Post objects by default
        # Unless Order is provided in the query.
        ordering = ['-publish'] 
        # Index Creation since most queries will be based on publish attr
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
