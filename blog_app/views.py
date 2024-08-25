from django.shortcuts import render, HttpResponse

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
    return HttpResponse(f'Пост с названием {post_slug}')