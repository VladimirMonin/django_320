from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=300, unique=True, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    slug = models.SlugField(unique=True, verbose_name='Адрес страницы')
    author = models.ForeignKey(get_user_model(), related_name='posts', on_delete=models.CASCADE, verbose_name='Автор')
    tags = models.JSONField(null=True, blank=True, default=list, verbose_name='Теги')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return str(self.title)
    
    def get_absolute_url(self):
        return reverse("post_by_slug", args=[str(self.slug)])
        # return f"blog/{self.slug}/view/ # Это 2-й вариант работы с адресами в Django

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для автоматической генерации slug
        """
        if not self.slug:
            slug = slugify(self.title)
            self.slug = slug
        super().save(*args, **kwargs)

    
    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

        
