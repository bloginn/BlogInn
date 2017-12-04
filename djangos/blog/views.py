from django.shortcuts import render
from django.http import HttpResponse
from . import models
from logic import list


def index(request):
    news = models.News.objects.all()
    return render(request, 'blog/index.html', {'news': news})


def news(request, id):
    one = list.getById(id)
    if one:
        return render(request, 'blog/news.html', {'news': one})
    else:
        return HttpResponse('error')
