from pyexpat import model
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from datetime import datetime
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_posts", on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to="posts/images/%Y/%m/%d")
    created = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edit_time = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, max_length=300)
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="posts_like", blank=True)

    def __str__(self): 
        return str(self.user)+" "+str(datetime.now())

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.user)+str(datetime.now()))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id, "slug":self.slug})
    
class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_comments", on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edit_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="comments_like", blank=True)

    def __str__(self):
        return f"{self.post.id} {self.user}"