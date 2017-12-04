from __future__ import unicode_literals

from django.db import models


# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField(None)

    def __unicode__(self):
        return self.title


class List(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField(None)
    view_time = models.IntegerField(None)
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()

    def __unicode__(self):
        return self.title
