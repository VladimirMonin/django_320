from django.urls import path
from .views import post_by_slug, blog, add_post

urlpatterns = [
    path("<slug:post_slug>/view/", post_by_slug, name="post_by_slug"),
    path("", blog, name="blog"),
    path("add/", add_post, name="add_post"),
]
