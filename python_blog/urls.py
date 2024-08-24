from django.contrib import admin
from django.urls import path
# from blog_app import views
from blog_app.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index),
    path('', index),
]
