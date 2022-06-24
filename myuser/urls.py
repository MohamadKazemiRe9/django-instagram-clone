from os import name
from django.urls import path
from .views import edit

app_name = "user"

urlpatterns = [
    path("edit/", edit, name="edit")
]
