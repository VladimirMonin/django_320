## Занкомство с Django

### Что такое MTV?
1. Паттерн MTV
Models - Модели - классы, которые описывают структуру данных, которые будут храниться в базе данных.

Views - Вью - классы или функции, которые обрабатывают запросы и возвращают ответы.

Templates - Шаблоны - файлы, которые содержат HTML-код, который будет отправлен клиенту.

### Установка Django

Установили Django и обновили requirements.txt
```bash
pip install django
pip freeze > requirements.txt
```

Создали проект Django
```bash
django-admin startproject python_blog .
```
Создали приложение. Точка - текущая директория.
Иначе Django создат поддиректорию с названием проекта.

Коммит: **Создание проекта Django**

Получаем Django ракету!
**Команда для запуска сервера**

```bash
python manage.py runserver
```

### Главная страница Django (Url -> View -> Template)

1. Создаем первое приложение в проекте

**Приложение** - это отдельный функционал, который вынесен в обособленную часть проекта. Имеет свою логику, свою структуру и свой функционал.

```bash
python manage.py startapp blog_app
```

Коммит: **Создание приложения blog_app**

2. Добавляем приложение в проект
В САМОМ НИЗУ ПОСЛЕ ВСЕХ СЛУЖЕБНЫХ ПРИЛОЖЕНИЙ
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    'blog_app',

```

3. Cоздаем первое `view` - `index` в файле `views.py`

```python
from django.shortcuts import render, HttpResponse

# Index - функция, которая будет отдавать HttpResponse с текстом "Привет из Django!"
def index(request):
    return HttpResponse("Привет из Django!")
```

4. Прописываем маршруты в файле `urls.py`
   
```python
from blog_app.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index),
    path('', index),
]
```

Коммит: **Создание первого view**