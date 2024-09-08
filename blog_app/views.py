from django.shortcuts import render, HttpResponse
from .dataset import dataset

menu = [
    {"name": "Главная", "alias": "main"},
    {"name": "Блог", "alias": "blog"},
    {"name": "О проекте", "alias": "about"},
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
    post = [post for post in dataset if post['slug'] == post_slug]
    if not post:
        # 404 - Пост не найден
        return HttpResponse('404 - Пост не найден', status=404)
    else:
        context = post[0]
        context['menu'] = menu
        context['page_alias'] = 'blog'
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