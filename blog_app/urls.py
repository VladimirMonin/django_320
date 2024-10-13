from django.urls import path
from .views import post_by_slug, blog, add_post, posts_by_tag, posts_by_category, preview_post, add_category

urlpatterns = [
    path("<slug:post_slug>/view/", post_by_slug, name="post_by_slug"),
    path("", blog, name="blog"),
    path("add_post/", add_post, name="add_post"),
    path("add_category/", add_category, name="add_category"),
    # Посты по тегам
    path('tag/<slug:tag>/', posts_by_tag, name='posts_by_tag'),
    # Посты по категориям
    path('category/<slug:category>/', posts_by_category, name='posts_by_category'),
    
    # Маршрут для предпросмотра поста
    path('preview/', preview_post, name='preview_post'),
]
