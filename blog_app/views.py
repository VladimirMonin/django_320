from django.shortcuts import render, HttpResponse, get_object_or_404
from .dataset import dataset
from .models import Post

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
    context = {
        'posts': dataset,
        'menu': menu,
        'page_alias': 'blog'
    }
    return render(request, 'blog_app/blog.html', context=context)

def post_by_slug(request, post_slug) -> HttpResponse:
    """
    Проходим словарей dataset и ищем совпадение по слагу    Если пост не, возвращаем 404.
    В противном случае возвращаем детальную информацию о посте.
    """
    post = get_object_or_404(Post, slug=post_slug)
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


def add_post(request):
    
    context = {
        'menu': menu,
        'page_alias': 'add_post'
    }


    # Если запрос типа GET - вернем страничку с формой добавления поста
    if request.method == "GET":
        return render(request, 'blog_app/add_post.html')
    
    # Если запрос типа POST - форма была отправлена и мы можем добавить пост
    elif request.method == "POST":
        # Получаем данные из формы
        # Ключи = атрибуты name в <input>
        title = request.POST['title']
        text= request.POST['text']
        slug = request.POST['slug']
        
        # Пытаемся опознать пользователя
        user = request.user

        if title and text and slug:
            if not Post.objects.filter(slug=slug).exists():
                # Создаем объект поста и сохраняем его в базу данных
                post = Post()
                post.title = title
                post.text = text
                post.slug = slug
                post.author = user
                post.save()

                context.update({'message': 'Пост успешно добавлен!'})
                return render(request, 'blog_app/add_post.html', context)
            else:
                context.update({'message': 'Такой пост уже существует!'})
                return render(request, 'blog_app/add_post.html', context)
            
        else:
            context.update({'message': 'Заполните все поля!'})
            return render(request, 'blog_app/add_post.html', context)
