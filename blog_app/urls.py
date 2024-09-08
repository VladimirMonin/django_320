from django.urls import path
from .views import post_by_slug, blog

urlpatterns = [
    path('<slug:post_slug>/view/', post_by_slug, name='post_by_slug'),
    path("", blog, name="blog"),
]