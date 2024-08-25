from django.contrib import admin
from django.urls import path
# from blog_app import views
from blog_app.views import index, post_by_slug

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index),
    path('', index),
    path('post/<slug:post_slug>', post_by_slug),
]
