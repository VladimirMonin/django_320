from django.urls import path
from .views import post_by_slug, blog, add_post, posts_by_tag, posts_by_category, preview_post, AddCategoryView, add_tag, update_category, update_post

urlpatterns = [
    path("<slug:post_slug>/view/", post_by_slug, name="post_by_slug"),
    path("", blog, name="blog"),
    
    # Формы
    path("add_post/", add_post, name="add_post"),
    path("update_post/<slug:post_slug>/", update_post, name="update_post"),
    path("add_category/", AddCategoryView.as_view(), name="add_category"),
    path("update_category/<slug:category_slug>/", update_category, name="update_category"),
    path("add_tag/", add_tag, name="add_tag"),


    # Посты по тегам
    path('tag/<slug:tag>/', posts_by_tag, name='posts_by_tag'),
    # Посты по категориям
    path('category/<slug:category>/', posts_by_category, name='posts_by_category'),
    
    # Маршрут для предпросмотра поста
    path('preview/', preview_post, name='preview_post'),
]
