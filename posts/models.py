from distutils.command.upload import upload
from django.db import models
from django.conf import settings
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_posts", on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to="posts/images/%Y/%m/%d")
    created = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edit_time = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, max_length=300)

    def __str__(self):
        return self.user+" "+self.created
