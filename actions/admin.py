from django.contrib import admin
from .models import Action
# Register your models here.

@admin.register(Action)
class Actionadmin(admin.ModelAdmin):
    list_display = ['user', 'act', 'target', 'created']
    list_filter = ['created']
    search_fields = ["act"]