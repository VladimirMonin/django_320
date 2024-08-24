from django.shortcuts import render, HttpResponse

# Index - функция, которая будет отдавать HttpResponse с текстом "Привет из Django!"
def index(request):
    return render(request, 'index.html')


