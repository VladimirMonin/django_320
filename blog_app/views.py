from django.shortcuts import render, HttpResponse
from .dataset import dataset

# Index - функция, которая будет отдавать HttpResponse с текстом "Привет из Django!"
def index(request):
    context = {
        'posts': dataset
    }
    return render(request, 'blog_app/index.html', context=context)


def post_by_slug(request, post_slug):
    # Проходим список словарей dataset и ищем совпадение по слагу
    post = [post for post in dataset if post['slug'] == post_slug]
    if not post:
        # 404 - Пост не найден
        return HttpResponse('404 - Пост не найден', status=404)
    else:
        return render(request, 'blog_app/post_detail.html', context=post[0], status=200)