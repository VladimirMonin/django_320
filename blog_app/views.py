from django.shortcuts import render, HttpResponse

# Index - функция, которая будет отдавать HttpResponse с текстом "Привет из Django!"
def index(request):
    return HttpResponse("Привет из Django!")