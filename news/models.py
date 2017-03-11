from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Feed(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    is_active = models.BooleanField(default=False)

class Article(models.Model):
    feed = models.ForeignKey(feed)
    title = models.CharField(max_length=200)
    url = models.URLField
    description = models.TexxField()
    publication_date = models.DateTimeField()
