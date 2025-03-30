from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # <-- This handles the "/"
    path("store_user_info/", views.store_user_info, name="store_user_info"),
]
