from django.shortcuts import render, HttpResponse, get_object_or_404
from .dataset import dataset
from .models import Post, Tag, Category
from django.db.models import F, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .templatetags.md_to_html import markdown_to_html

menu = [
    {"name": "Главная", "alias": "main"},
    {"name": "Блог", "alias": "blog"},
    {"name": "О проекте", "alias": "about"},
    {"name": "Добавить пост", "alias": "add_post"}
]


def blog(request) -> HttpResponse:
    """
    Функция представления для отображения главной страницы блога.
    Параметры:
    request: объект запроса Django, который содержит информацию оем запросе.

   вращает:
    HttpResponse: HTTP-ответ с отрендеренной страницей 'index.html' 
    и контекст, содержащим список постов блога.
    """
    """
    query - ключ для поискового запроса
    sort_by - поле для сортировки (по умолчанию - дата создания, desc, популярность - просмотры)
    search_options - ищем по заголовку, тексту, или по заголовку тексту тегам и категоряим
    """
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(
            (Q(title__icontains=search_query) | Q(text__icontains=search_query)) &
            Q(status='published')
            ).order_by('-created_at')
    else:
        # 1. Фильтрация по статусу опубликовано. 2. Сортировка по дате создания по убыванию.
        posts = Post.objects.filter(status='published').order_by('-created_at')
    
    context = {
        'posts': posts,
        'menu': menu,
        'page_alias': 'blog'
    }
    return render(request, 'blog_app/blog.html', context=context)


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
    

def index(request) -> HttpResponse:
    context = {
        'menu': menu,
        'page_alias': 'main'
    }
    return render(request, 'index.html', context=context)

def about(request) -> HttpResponse:
    context = {
        'menu': menu,
        'page_alias': 'about'
    }
    return render(request, 'about.html', context=context)


from django.shortcuts import render, redirect
from .models import Post, Tag

def add_post(request):
    context = {
        'menu': menu,
        'page_alias': 'add_post'
    }

    if request.method == "GET":
        return render(request, 'blog_app/add_post.html', context=context)
    
    elif request.method == "POST":
        title = request.POST['title']
        text = request.POST['text']
        tags = request.POST['tags'] # строка: базы данных, еще тег, sql

        if Post.objects.filter(title=title).exists():
            context.update({'message': 'Такой заголовок уже существует!'})
            return render(request, 'blog_app/add_post.html', context=context)

        user = request.user

        if title and text and tags:
            post = Post.objects.create(
                title=title,
                text=text,
                author=user
            )

            # Обработка тегов
            tag_list = [tag.strip().lower().replace(' ', '_') for tag in tags.split(',') if tag.strip()]
            for tag_name in tag_list:
                # Если тег есть, добываем, если нет, создаем. В переменной в любом случае будет объект модели Tag
                tag, created = Tag.objects.get_or_create(name=tag_name)
                # Создаем связь между этим тегом и постом
                post.tags.add(tag)

            context.update({'message': 'Пост успешно добавлен!'})
            # return redirect('post_by_slug', post_slug=post.slug)
            # Альтернативный вариант, вернуть пользователя на фомру, показать сообщение об успехе
            return render(request, 'blog_app/add_post.html', context=context)
        
        else:
            context.update({'message': 'Заполните все поля!'})
            return render(request, 'blog_app/add_post.html', context=context)

    return render(request, 'blog_app/add_post.html', context=context)

def posts_by_tag(request, tag):
    """
    Функция представления для отображения страницы постов с определенным тегом.
    """
    context = {
        # Можно получить все посты со стороны тега, используя related_name posts в модели Tag
        # Tag.objects.get(slug=tag).posts.all()
        'posts': Post.objects.filter(tags__slug=tag),
        'menu': menu,
        'page_alias': 'blog'
    }
    return render(request, 'blog_app/blog.html', context=context)


def posts_by_category(request, category):
    """
    Функция представления для отображения страницы постов с определенной категорией.
    """
    context = {
        # Можно получить все посты со стороны тега, используя related_name posts в модели Tag
        # Tag.objects.get(slug=tag).posts.all()
        'posts': Category.objects.get(slug=category).posts.all(),
        'menu': menu,
        'page_alias': 'blog'
    }
    return render(request, 'blog_app/blog.html', context=context)


# @csrf_exempt # Отключает проверку CSRF токена при пост запросах для этой вью
def preview_post(request):
    """
    Вью которая работает на AJAX запросы, и дает предпросмотр постов при создании нового поста.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')
        html = markdown_to_html(text)
        return JsonResponse({'html': html})