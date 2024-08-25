from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Через include подключим blog_app.urls
    # http://127.0.0.1:8000/blog/post/django-osnovnye-komandy
    # path('blog/', include('blog_app.urls')),
    
    # http://127.0.0.1:8000/post/django-osnovnye-komandy
    path('', include('blog_app.urls')),
    
]
