from django.shortcuts import render
from django.http import HttpResponse
from . import models


def index(request):
    news = models.News.objects.all()
    return render(request, 'blog/index.html', {'news': news})


def news(request, id):
    news = models.News.objects.get(pk=id)
    return render(request, 'blog/news.html', {'news': news})
