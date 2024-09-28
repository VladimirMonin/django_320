from telnetlib import STATUS
from django.db import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from unidecode import unidecode

"""
Описание моделей из HW4


1. **Post**
   - Назначение: Модель для хранения информации о постах блога.
   - Поля:
     - `title`: `CharField` с `max_length=200`.
     - `text`: `TextField` для содержания поста.
     - `slug`: `SlugField` с `unique=True` для уникального идентификатора URL.
     - `author`: `ForeignKey` к модели пользователя с `on_delete=models.CASCADE`.
     - `category`: `ForeignKey` к модели `Category` с `on_delete=models.CASCADE`, `related_name='posts'`, `null=True`, `default=None`.
     - `tags`: `ManyToManyField` к модели `Tag` с `related_name='posts'`.
     - `published_date`: `DateTimeField` с `auto_now_add=True`.
     - `updated_date`: `DateTimeField` с `auto_now=True`.
     - `views`: `IntegerField` с значением по умолчанию 0 (для хранения количества просмотров).
     - `cover_image`: Поле изображения для обложки (опционально).
     - Статус: Выбор из 'Опубликовано' и 'Черновик'.

   - Методы:
     - `save(self, *args, **kwargs)`: Переопределение для автоматической генерации slug.
     - __str__(self): Строковое представление модели.
     - get_absolute_url(self): Метод для получения абсолютного URL поста.


2. **Category**
   - Назначение: Модель для категорий постов.
   - Поля:
     - `name`: `CharField` с `max_length=200`, `unique=True`.
     - `slug`: `SlugField` с `unique=True`.
   - Методы:
     - `save(self, *args, **kwargs)`: Переопределение для автоматической генерации `slug`.
     - `__str__(self)`: Строковое представление модели.
     - `get_absolute_url(self)`: Метод для получения абсолютного URL категории (необязательно, но рекомендуется).

3. **Tag**
   - Назначение: Модель для тегов постов.
   - Поля:
     - `name`: `CharField` с `max_length=100`, `unique=True`.
     - `slug`: `SlugField` с `unique=True`.
   - Методы:
     - `save(self, *args, **kwargs)`: Переопределение для автоматической генерации `slug` и приведения имени к нижнему регистру.
     - `__str__(self)`: Строковое представление модели.
     - `get_absolute_url(self)`: Метод для получения абсолютного URL тега (необязательно, но рекомендуется).

4. **Comment**
   - Назначение: Модель для комментариев к постам.
   - Поля:
     - `author`: `ForeignKey` к модели пользователя с `on_delete=models.CASCADE`.
     - `text`: `TextField` для содержания комментария.
     - `status`: `CharField` с `max_length=10`, `choices=STATUS_CHOICES`, `default='unchecked'`.
     - `post`: `ForeignKey` к модели `Post` с `on_delete=models.CASCADE`.
   - Методы:
     - `__str__(self)`: Строковое представление модели.

"""


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
