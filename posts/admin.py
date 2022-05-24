from django.contrib import admin
from .models import Post
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "created", "image", "edit_time", "edited"]
    list_filter = ("created", "edited")