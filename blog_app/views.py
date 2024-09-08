from django.shortcuts import render, HttpResponse
from .dataset import dataset


def index(request) -> HttpResponse:
    """
    Функция представления для отображения главной страницы блога.
    Параметры:
    request: объект запроса Django, который содержит информацию оем запросе.

   вращает:
    HttpResponse: HTTP-ответ с отрендеренной страницей 'index.html' 
    и контекст, содержащим список постов блога.
    """
    context = {
        'posts': dataset
    }
    return render(request, 'blog_app/index.html', context=context)

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
        return render(request, 'blog_app/post_detail.html', context=post[0], status=200)