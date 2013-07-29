from django.db import models


class Feed(models.Model):
    description = models.CharField(max_length=1024, null=True)
    link = models.URLField()
    title = models.CharField(max_length=1024, null=True)
    pubdate = models.DateTimeField(null=True)
    established = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title',]


class Item(models.Model):
    description = models.CharField(max_length=1024)
    link = models.URLField()
    title = models.CharField(max_length=1024)
    pubdate = models.DateTimeField()
    feed = models.ForeignKey(Feed, related_name='items')
    established = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['feed', '-pubdate',]
