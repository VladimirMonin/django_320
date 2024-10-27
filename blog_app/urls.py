from django.urls import path
from .views import (
    PostDetailView,
    BlogView,
    add_post,
    PostsByTagListView,
    PostsByCategoryListView,
    AddCategoryView,
    update_post,
    AddTagView,
    UpdateCategoryView,
    PreviewPostView,
)

urlpatterns = [
    path("<slug:slug>/view/", PostDetailView.as_view(), name="post_by_slug"),
    path("", BlogView.as_view(), name="blog"),
    
    # Формы
    path("add_post/", add_post, name="add_post"),
    path("update_post/<slug:post_slug>/", update_post, name="update_post"),
    path("add_category/", AddCategoryView.as_view(), name="add_category"),
    path("update_category/<slug:category_slug>/", UpdateCategoryView.as_view(), name="update_category"),
    path("add_tag/", AddTagView.as_view(), name="add_tag"),


    # Посты по тегам
    path('tag/<slug:tag>/', PostsByTagListView.as_view(), name='posts_by_tag'),
    # Посты по категориям
    path('category/<slug:category>/', PostsByCategoryListView.as_view(), name='posts_by_category'),
    
    # Маршрут для предпросмотра поста
    path('preview/', PreviewPostView.as_view(), name='preview_post'),
]
