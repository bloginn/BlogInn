from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^news/(?P<id>[0-9]+)$', views.news)
]
