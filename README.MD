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

## Знакомство с Шаблонизатором Django

1. Создаём папку `templates` в директории `blog_app`
2. Размещаем в ней файл `index.html` (Простой HTML-файл с заголовком 1 уровня)
3. Изменяем `views.py`. Используя функцию `render` из `django.shortcuts` передаём в неё `request` и `index.html`

```python
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

```

Коммит: **Создание первого шаблона**

### Первая переменная шаблона

Добавили переменную `{{name}} в index.html`
Добавили передачу контекста в шаблон

```python
def index(request):
    context = {'name': 'Zigmund'}
    return render(request, 'index.html', context=context)
```

Коммит: **Создание первой переменной шаблона**

### Типы данных которые можно передавать в шаблон

Мы можем передать в контекст шаблона любой тип данных, который можно сериализовать в JSON.

- Строки
- Числа
- Списки
- Словари
- Объекты
- Вызовы методов
- Обращения по ключу или индексу к коллекциям

## Знакомство с концепцией конвертеров в Django

`Конвертер` в маршрутизации Django - это функция, которая принимает строку и возвращает объект.

Например мы можем из маршрута получить id поста или slug его заголовка и передать в функцию представления, которорая поищет данные в БД и вернет ответ.

**Типы конвертеров в Django**

- `<int:pk>` - принимает только целые числа (пример:: /posts/1/)
- `<slug:slug>` - принимает только строки, содержащие буквы, цифры, дефисы и подчеркивания (например, "my-slug-123")
- `<str:name>` - принимает любые не пустые строки (но останавливается на `/`) (пример: `http://127.0.0.1:8000/blog/`)
- `<uuid:uuid>` - принимает строку в формате UUID (пример: 123e4567-e89b-12d3-a456-426655440000)
- `<path:subpath>` - принимает строку, которая может содержать слеши (то есть любые символы, используемые в URL) (пример: /path/to/resource)

Для определения маршрута с конкретным конвертером используется следующий синтаксис:

```python
from django.urls import path

urlpatterns = [
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),        # Маршрут с целочисленным идентификатором поста
    path('posts/<slug:slug>/', views.post_by_slug, name='post_by_slug'),   # Маршрут с slug заголовка поста
]
```

### Что такое `slug`?

`Slug` - это короткий фрагмент текста, который используется для идентификации объекта или страницы в URL. Он обычно состоит из букв, цифр и дефисов и используется для улучшения читаемости URL.

Его очень любят поисковики, так как он помогает им понять, что за страница находится по данному URL.

`Пирожки с мясом и картошкой` -> `pirozhki-s-myasom-i-kartoshkoi`

`234` -> `234` - Поисковый робот не поймет, что это за страница.

### Как это выглядит со стороны `View`?

```python
from django.shortcuts import render

def post_detail(request, slug):

    # Ищем пост в базе данных по slug
    pass
```

### Создали представление

```python
def post_by_slug(request, post_slug):
    return HttpResponse(f'Пост с названием {post_slug}')

# Маршрут
path('post/<slug:post_slug>', post_by_slug),
```

### Создали `dataset` и положили его в файл `dataset.py`

Формат

```python
    {
        "title": "Что нового в Python 3.10?",
        "slug": "chto-novogo-v-python-310",
        "post": "В версии Python 3.10 появилось множество улучшений и новых функций. Например, улучшенные операторы сравнения и структурированное сопоставление с образцом.",
        "hashtags": ["python", "новости", "выпуск"],
        "is_published": True,
        "views": 5832,
        "likes": 142,
        "comments": [
            {"username": "alex_dev", "text": "Отличное обновление!"},
            {"username": "pythonista", "text": "Эти нововведения сильно ускорят работу."}
        ]
    },
....
```

Коммит: **Создание первого представления и датасета**

### Сделали поиск по нашей "базе данных" по Slug и отдачу в шаблон

Шаблон:

```html
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ title }}</title>
  </head>
  <body>
    <h1>{{title}}</h1>
    <p>Текст поста: {{post}}</p>
    <p>Теги: {{hashtags}}</p>
    <p>Просмотры: {{views}}</p>
    <p>Лайки: {{likes}}</p>
  </body>
</html>
```

Вью:

```python
def post_by_slug(request, post_slug):
    # Проходим список словарей dataset и ищем совпадение по слагу
    post = [post for post in dataset if post['slug'] == post_slug]
    if not post:
        # 404 - Пост не найден
        return HttpResponse('404 - Пост не найден', status=404)
    else:
        return render(request, 'post_detail.html', context=post[0], status=200)
```

Коммит: **Поиск по слагу в dataset и передача в шаблон**

### Вынесли `urls.py` в отдельный файл в приложении `blog_app`

1. Создали файл `urls.py` в директории `blog_app` - в котором будут маршруты именно этого приложения

```python
urlpatterns = [
    path('post/<slug:post_slug>', post_by_slug),
    path('', index),
]
```

2. В конфигурационном пакете в `urls.py` подключили файл `urls.py` из приложения `blog_app` функцией `include`

При этом дали префикс `''` - пустой строке. Это значит, что все маршруты из `urls.py` в приложении `blog_app` будут в корне сайта

```python
path('', include('blog_app.urls')),
```

Коммит: **Вынесение urls.py в отдельный файл**

### Аргумент `name` в маршруте

`name` - это имя маршрута, которое используется для ссылки на маршрут из других частей приложения. Это удобно, потому что маршрут может поменятся, но если псевдоним останется прежним, то ссылка на него не сломается.

Подключили маршрут с псевдонимом

```python
path('post/<slug:post_slug>', post_by_slug, name='post_by_slug'),
```

Протестировали в шаблоне главной страницы построение ссылки через шаблонный тег
`url`

## Работа с `Django Templates`

```html
 {% for post in posts %}
    <hr>
    <p>Title: {{ post.title }}</p>
    <p>Slug: {{ post.slug }}</p>
    {% comment %} Захардкодили ссылку. Если маршрут поменятся надо будет везде править руками {% endcomment %}
    <a href="post/{{ post.slug }}">{{ post.title }}</a>

    {% comment %} Чтобы ссылку не хардкодить, мы используем псевдонимы
    маршрутов {% endcomment %}
    <p>Ссылка с использованием шаблонного тега <code>url</code>:</p>
    <a href = {% url 'post_by_slug' post.slug %}>{{ post.title }}</a>
    <hr>
    {% endfor %}
```

### Подпапки в `templates`

Это нужно для того, чтобы не было конфликтов имен файлов в разных приложениях.
Потому что шаблонизатор берет первое попавшееся совпадение.

Коммит: **Подпапки в templates первый цикл шаблона и тег url**

### Теги шаблонов

- `{% cooment %}` - комментарий
- `{% endcomment %}` - конец комментария
- `{% for %}` - цикл
- `{% endfor %}` - конец цикла
- `{% if %}` - условие
- `{% elif %}` - условие
- `{% else %}` - условие
- `{% endif %}` - конец условия
- `{% url %}` - генерация ссылки на маршрут по псеводониму

### `If` и `For` в шаблонах Django

В общий каталог постов добавили цикл и условие. Попробовали выводить посты
только с `is_published=True` а так же сделали разные цвета и подписи для постов с `is_published=True` и `is_published=False`

Коммит: **Второй цикл шаблона и условия в шаблонах**

### Цикл внутри цикла
Вложенным циклом вывели список хештегов для поста
И задали им определенный класс для оформления

Коммит: **Вложенный цикл в шаблонах**

## Подключение статики 

1. Надо оформить 2 константы в `settings.py`

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
```

2. Создать папку `static` в корне проекта
3. Загрузить статику в нужные шаблоны `{% load static %}`
4. Обратиться к нужному файлу допустим так `<link rel="stylesheet" href="{% static "css/main.css" %}" />`

Коммит: **Подключение статики**

## Lesson 48 знакомство с Django ORM

1. Применим служебные миграции Django. Теперь если зайти в БД мы увидим достаточно много таблиц.
   
```bush
python manage.py migrate
```

2. Создадим суперпользователя. Это администратор, у которого есть полный набор прав на любые действия в приложении.

Теперь, если заглянуть в БД, можно увидеть в таблице `auth_user` нового пользователя.

```bush
python manage.py createsuperuser
```

3. Cоздадим модель `Post`

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    slug = models.SlugField(unique=True)
    tags = models.JSONField(null=True, blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

```

Выполним миграции

```bush
python manage.py makemigrations
python manage.py migrate
```

Коммит: **Создание модели Post**


### Django Shell Plus

```bush
pip install django-extensions
```

Подключение в `settings.py`

```python
INSTALLED_APPS = [
    ...
    'django_extensions',
```

`shell_plus` автоматически импортирует все модели вашего проекта при запуске, что упрощает работу с данными. Чтобы запустить `shell_plus`, используйте следующую команду:

```bash
python manage.py shell_plus
```

Если вы хотите видеть SQL-запросы, генерируемые вашими операциями с моделями в реальном времени, используйте флаг `--print-sql`:

```bash
python manage.py shell_plus --print-sql
```

### Первые запросы
Для выполнения запроса, нам надо обратится к модели по имени, например `User`, после чего обратится к объектному менеджеру `objects` и вызвать нужный метод, например `all()`

`User.objects.all()`

Запрос вернет всех пользователей в базе данных. Тип данных будет `QuerySet`. Это означает, что это не просто список, а набор объектов, которые можно фильтровать, сортировать и выполнять другие операции.

Коммит: **Первый запрос**

### Создание постов

```python
   post1 = Post.objects.create(
       title='Введение в Python',
       text='Python — это высокоуровневый язык программирования...',
       slug='vvedenie-v-python',
       tags= ['основы', 'синтаксис', 'советы']
   )

post2 = Post.objects.create(
       title='Введение в Django',
       text='Django — это веб-фреймворк написанный на языке Python...',
       slug='vvedenie-v-django',
       tags= ['django', 'веб', 'феймворк']
   )

```

Теперь мы можем попробовать достать из переменной пост данные

```python
post1.title
post1.text
post1.slug
post1.tags
```

Альтернативное создание постов (Экземпляр модели + Save)

```python
post3 = Post(
       title='Введение в SQL',
       text='SQL — это язык запросов к базам данных...',
       slug='vvedenie-v-sql',
       tags= ['sql', 'базы данных']

)

post3.save()
```

Коммит: **Создание постов**
