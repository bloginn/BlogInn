from __future__ import unicode_literals

from django.db import models


# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField(None)

    def __unicode__(self):
        return self.title
