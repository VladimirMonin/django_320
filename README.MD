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

### Read Update Delete

Для поиска постов по `slug` или `id` используем метод `get`

```python
get_post_1 = Post.objects.get(id = 1)
get_post_1 = Post.objects.get(pk = 1) # Primary Key
```

Обновим slug

```python
get_post_1.slug = "vvedenie_v_yazik_python"
get_post_1.save()
```

Удаление постов

```python
Post.objects.get(id=1).delete()
get_post_1.delete()
```

Коммит: **Посты: Read Update Delete**

### Подключение этой модели в админку

У нас есть 2 способа это сделать. Простой, в одну строку, для старта - отличный вариант.

Второй, с описанием класса модели, с помощью декоратора `admin.site.register(Post)`. Который даст возможность кастомизировать внешний вид админки.

```python
admin.site.register(Post)

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'created_at', 'updated_at')
#     search_fields = ('title', 'text')
#     prepopulated_fields = {'slug': ('title',)}

```

Коммит: **Подключение модели Post в админку**

## Lesson 49. Django ORM. Работа со связью один ко многим

Добавили ссылку на пользователей в модели постов.

```python
class Post(models.Model):
    title = models.CharField(max_length=300, unique=True, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    slug = models.SlugField(unique=True, verbose_name='Адрес страницы')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Автор')
    tags = models.JSONField(null=True, blank=True, default=list, verbose_name='Теги')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return str(self.title)
    
    def get_absolute_url(self):
        return reverse("post_by_slug", args=[str(self.slug)])
        # return f"blog/{self.slug}/view/ # Это 2-й вариант работы с адресами в Django

    
    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

```

### Достать username из поста

```python
post = Post.objects.get(pk=1)
author_name = post.author.username

author_name_post_1 = Post.objects.get(pk=1).author.username

# Добываем все посты юзернейм admin
user_admin_all_posts = User.objects.get(username='admin').posts.all()

# Запуск shell plus
python manage.py shellplus
```

## Параметр `related_name` в Django ORM

Параметр `related_name` используется в полях ForeignKey и ManyToManyField для определения имени обратного отношения от связанной модели обратно к этой.

### Пример использования:

```python
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
```

**Преимущества**:
Удобный доступ к связанным объектам:

Без related_name: User.objects.get(id=1).post_set.all()
С related_name: User.objects.get(id=1).posts.all()

- Избежание конфликтов имен при множественных связях с одной моделью.

Улучшение читаемости кода.

Возможность использования в аннотациях и агрегациях.

related_name значительно упрощает работу с обратными отношениями в Django ORM, делая код более интуитивным и эффективным.

## Lesson 52. Django ORM. Lookups. Работа со связью многие ко многим

### Наши модели на текущий момент

```python

class Post(models.Model):
    STATUS_CHOICES = (
        ("published", "Опубликовано"),
        ("draft", "Черновик"),
    )
    
    title = models.CharField(max_length=300, unique=True, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    slug = models.SlugField(unique=True, verbose_name="Адрес страницы")
    author = models.ForeignKey(
        get_user_model(),
        related_name="posts",
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    category = models.ForeignKey(
        "Category",
        related_name="posts",
        null=True,
        default=None,
        on_delete=models.CASCADE,
    )
    # Категории
    tags = models.ManyToManyField(
        "Tag", related_name="posts", blank=True, verbose_name="Теги"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.IntegerField(default=0, verbose_name="Просмотры")
    cover_image = models.ImageField(blank=True, null=True, verbose_name="Обложка", upload_to="media/images/")
   
    status = models.CharField(
            max_length=12, choices=STATUS_CHOICES, default="draft", verbose_name="Статус"
        )

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("post_by_slug", args=[str(self.slug)])
        # return f"blog/{self.slug}/view/ # Это 2-й вариант работы с адресами в Django

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для автоматической генерации slug
        """
        slug = slugify(unidecode(self.title))
        self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.name)

    
    def get_absolute_url(self):
        return reverse("posts_by_category", args=[str(self.slug)])

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для автоматической генерации slug
        """
        slug = slugify(unidecode(self.name))
        self.slug = slug
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower().replace(" ", "_")
        slug = slugify(unidecode(self.name))
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.name}"

    def get_absolute_url(self):
        """
        Возвращает маршрут posts_by_tag
        """
        url = reverse("posts_by_tag", args=[str(self.slug)])
        return url


class Comment(models.Model):

    STATUS_CHOICES = (
        ("unchecked", "Не проверен"),
        ("accepted", "Проверен"),
        ("rejected", "Отклонен"),
    )

    text = models.TextField(verbose_name="Текст комментария", max_length=2000)
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default="unchecked"
    )

    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name="Автор"
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

```

### Lookups - лукапы.

```python
# Поиск по тексту поста (регистронезависимый)
posts = Post.objects.filter(text__icontains=search_text)

# Поиск постов по имени тега (человекочитаемому)
posts = Post.objects.filter(tags__name__iexact=tag_name)

# Это же, но через название тега
posts = Tag.objects.get(name=tag_name).posts.all()

# Поиск постов с количеством просмотров меньше или равно 5
posts = Post.objects.filter(views__lte=5)

# Посты, с вхождением в имя категории Технолог и количеством просмотров 5+
posts = Post.objects.filter(category__name__icontains="Технолог").filter(views__gte=5)
```

### Команда для запуска shell plus
python manage.py shell_plus

### Команда с выводом SQL запросов в консоль
python manage.py shell_plus --print-sql

## Lesson 53 F и Q объекты

Конечно! С удовольствием расскажу о F объектах в Django и коллизиях записи при пиковых активностях на примере постов.

F объекты в Django - это мощный инструмент для работы с полями модели на уровне базы данных. Они позволяют выполнять операции с полями, не загружая их значения в память Python. Это особенно полезно при работе с большими объемами данных или при необходимости атомарных операций.

На примере поля просмотров для постов, F объекты могут быть использованы для безопасного увеличения счетчика просмотров. Вместо того чтобы загружать текущее значение, увеличивать его и сохранять обратно, мы можем использовать F объект для выполнения этой операции непосредственно в базе данных.

Однако при пиковых активностях, когда множество пользователей одновременно просматривают пост, могут возникнуть коллизии записи. Это происходит, когда несколько процессов пытаются одновременно обновить одно и то же поле.

F объекты помогают минимизировать риск таких коллизий, так как операция выполняется атомарно на уровне базы данных. Тем не менее, при очень высокой нагрузке все еще могут возникать ситуации, когда два запроса пытаются обновить поле одновременно.

Для дальнейшего снижения риска коллизий можно использовать дополнительные техники, такие как:

Использование транзакций с соответствующим уровнем изоляции.
Применение оптимистичной блокировки с использованием версионирования.
Использование кэширования для уменьшения нагрузки на базу данных.
Применение очередей для обработки обновлений в асинхронном режиме.
Таким образом, F объекты в Django предоставляют эффективный способ работы с полями модели, значительно снижая риск коллизий при высоких нагрузках, но для полного решения проблемы в критических сценариях могут потребоваться дополнительные меры.

### Увеличение просмотров в посте

```python
def post_by_slug(request, post_slug) -> HttpResponse:
    """
    Проходим словарем и ищем запись по слагу.
    Если пост не найден, возвращаем 404, иначе выводим детальную информацию и увеличиваем количество просмотров.
    """
    post = get_object_or_404(Post, slug=post_slug)

    # 1. Увеличиваем значение просмотров поста на 1, используя F-объект
    Post.objects.filter(slug=post_slug).update(views=F('views') + 1)

    context = {
        "post": post,
        "menu": menu,
        "page_alias": "blog"
    }

    return render(request, 'blog_app/post_detail.html', context=context, status=200)
```

В нашем коде мы видим следующую строку:

Post.objects.filter(slug=post_slug).update(views=F('views') + 1)

Здесь мы используем F-объект для увеличения значения поля 'views' на 1. Разберем этот синтаксис подробнее:

Post.objects - это менеджер модели Post, который предоставляет интерфейс для работы с базой данных.

.filter(slug=post_slug) - фильтрует записи, оставляя только пост с указанным слагом.

.update() - метод для обновления записей в базе данных.

views=F('views') + 1 - это ключевая часть, где используется F-объект:

F('views') ссылается на текущее значение поля 'views' в базе данных.
1 указывает, что мы хотим увеличить это значение на 1.
Такой синтаксис позволяет Django сформировать SQL-запрос, который выполнит увеличение значения непосредственно в базе данных, без необходимости сначала извлекать значение, а затем обновлять его.

Это эффективный и безопасный способ обновления счетчика просмотров, который минимизирует риск возникновения проблем при одновременном доступе нескольких пользователей к одному посту.

#### Почему поле строкой в F?

Отличный вопрос! Использование кавычек при создании F-объекта является важной частью синтаксиса Django.

Мы записываем имя поля в кавычках при создании F-объекта (например, F('views')) по следующим причинам:

Это позволяет Django однозначно интерпретировать строку как имя поля модели.

Такой подход обеспечивает гибкость - мы можем использовать имена полей, которые совпадают с зарезервированными словами Python или Django.

Это соответствует общему стилю Django, где имена полей часто передаются в виде строк (например, в QuerySet.values() или в ORM-запросах).

Использование строк позволяет Django выполнять определенные оптимизации и проверки на уровне ORM.

Это делает код более читаемым и явно указывает, что мы ссылаемся на поле модели, а не на переменную Python.

Такой подход является стандартным в Django и последовательно используется во всем фреймворке, что способствует написанию понятного и поддерживаемого кода.

### Q объект

Q объекты в Django используются для создания сложных запросов к базе данных, позволяя комбинировать условия фильтрации с использованием логических операторов ИЛИ (OR), И (AND) и НЕ (NOT). Эти объекты очень полезны, когда стандартные методы `.filter()` и `.exclude()`, которые по умолчанию используют логику И (AND), не подходят для решения задачи.

**Q-объекты в Django не являются абсолютно незаменимыми**, но они предоставляют удобный способ для выполнения сложных запросов, особенно когда речь идет о построении динамических условий фильтрации, которые зависят от ввода пользователя или других условий во время выполнения. Они позволяют строить сложные запросы с использованием логических операций «ИЛИ» и «И НЕ», что трудно или не так элегантно реализуемо с использованием стандартных методов QuerySet, таких как `.filter()` и `.exclude()`, которые по умолчанию соединяют условия через логическое "И".

Использование Q-объектов становится особенно ценным, когда вам нужно:
- Соединять условия фильтрации через "ИЛИ" или "И НЕ".
- Конструировать сложные запросы, основываясь на различных условиях, которые могут изменяться в зависимости от контекста выполнения.
- Реализовывать фильтрацию, которая зависит от агрегированных значений, вычисленных на лету.

Хотя многие задачи могут быть решены с использованием обычных запросов и методов QuerySet, Q-объекты упрощают написание сложных запросов, делая код более читаемым и компактным. Однако это не означает, что без них невозможно обойтись. Во многих случаях можно использовать более простые запросы, если логика приложения позволяет это сделать без значительного усложнения кода.

### Операторы Q объектов

- `|` (ИЛИ / OR): Позволяет объединить условия так, что объект удовлетворяет хотя бы одному из условий.
- `&` (И / AND): Используется для группировки условий, когда объект должен удовлетворять всем условиям одновременно.
- `~` (НЕ / NOT): Применяется для инвертирования условия, т.е. выбора объектов, которые не соответствуют указанному критерию.

### Правила и порядок группировки

При комбинировании Q объектов с помощью этих операторов важно правильно использовать скобки для группировки условий. Это определяет порядок выполнения операций и может существенно влиять на результат запроса. В общем случае, выражения в скобках выполняются первыми.

#### Примеры запросов к нашей базе данных:

```bash
python manage.py shell-plus --print-sql
```

1. Получить все опублиокованные посты
```python
published_posts = Post.objects.filter(status='published')
```

2. Найти посты с заголовком, содержащим определенное слово:
```python

posts_with_word = Post.objects.filter(title__icontains='Django')
```

3. Популярные посты:
```python
popular_posts = Post.objects.filter(views__gt=100)
```

4. Посты где есть тег Python
<!-- TODO Вхождение в тег? -->
```python
tag_name = 'python'
tagged_posts = Post.objects.filter(tags__name=tag_name)
```

5. По году
```python
year = 2024
posts_from_year = Post.objects.filter(created_at__year=year)
```

6. Получить посты с комментами:

```python
posts_with_comments = Post.objects.filter(comment__isnull=False).distinct()
```
7. Посты с определенным словом в заголовке или в тексте

```python
keyword = "Python"
posts_with_keyword = Post.objects.filter(Q(title__icontains=keyword) | Q(text__icontains=keyword))
```

#### Финальный вид вьюшки для поисковой формы

### Основы Q-объектов

Q-объекты в Django позволяют формировать сложные запросы с использованием логических операторов, что особенно актуально при комбинировании нескольких условий фильтрации.

### Оператор |=

В контексте Q-объектов оператор `|=` обозначает "ИЛИ равно". Он добавляет новое условие к уже существующему Q-объекту, объединяя их с помощью логического ИЛИ.

**Пример:**

```python
query |= Q(category__name__icontains=search_query)
```

Это эквивалентно следующему:

```python
query = query | Q(category__name__icontains=search_query)
```

### Другие операторы

- `&` (И): `query &= Q(condition)`
- `~` (НЕ): `~Q(condition)`

### Группировка условий

Условия можно группировать с помощью скобок:

```python
Q(condition1) & (Q(condition2) | Q(condition3))
```

### Как работает код

1. Сначала создается базовый запрос для поиска по заголовку и тексту.
2. Затем, в зависимости от выбранных чекбоксов, добавляются дополнительные условия с использованием `|=`.
3. Каждое добавленное условие расширяет область поиска.
4. В конце применяется метод `distinct()`, чтобы убрать дубликаты, которые могут появиться из-за JOIN-запросов.

### Альтернативные подходы

Можно создать список условий и объединять их в конце:

```python
conditions = [Q(title__icontains=search_query), Q(text__icontains=search_query)]
if search_category:
    conditions.append(Q(category__name__icontains=search_query))
# ... добавляем другие условия
query = reduce(operator.or_, conditions)
```

Для более сложных запросов можно использовать Q-объекты внутри метода `filter()`:

```python
Post.objects.filter(
    Q(title__icontains=search_query) |
    Q(text__icontains=search_query) |
    Q(category__name__icontains=search_query)
)
```

Этот подход позволяет создавать гибкие и мощные запросы, адаптируясь к различным комбинациям условий поиска.