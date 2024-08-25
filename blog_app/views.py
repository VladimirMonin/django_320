from django.shortcuts import render, HttpResponse
from dataset import dataset

class Data:
    def __init__(self, name):
        self.name = name
        
    def method(self):
        return 'Вызов метода класса Data'


# Index - функция, которая будет отдавать HttpResponse с текстом "Привет из Django!"
def index(request):
    
    data_instance = Data('Гендальф')
    
    context = {'some_str': 'Тест JS переменной',
               'some_int': 88,
               'some_list': ['Один', 1],
               'some_dict': {'fruit': 'apple'},
               'data': data_instance}
    return render(request, 'index.html', context=context)


def post_by_slug(request, post_slug):
    # Проходим список словарей dataset и ищем совпадение по слагу
    post = [post for post in dataset if post['slug'] == post_slug][0]
    if not post:
        # 404 - Пост не найден
        return HttpResponse('404 - Пост не найден', status=404)
    pass