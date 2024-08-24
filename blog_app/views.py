from django.shortcuts import render, HttpResponse

# Index - функция, которая будет отдавать HttpResponse с текстом "Привет из Django!"
def index(request):
    context = {'name': 'Zigmund'}
    return render(request, 'index.html', context=context)


