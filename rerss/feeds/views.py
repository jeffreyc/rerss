import json

from django import http
from django import shortcuts
from django.conf import settings
from django.contrib.syndication import views as sv
from django.core import urlresolvers
from django.utils import feedgenerator

from feeds import models


def feed(request):
    """A view to support creating, modifying, and deleting feeds.

    RESTful: uses PUT to create, POST to edit, and DELETE to delete. Django's
    built-in syndication requires its own view, so GET is not implemented.

    """
    params = http.QueryDict(request.body, request.encoding)
    if request.method == 'PUT':
        feed, cre = models.Feed.objects.get_or_create(link=params['link'],
                                                      title='Update pending...')
        if cre:
            return http.HttpResponse(json.dumps({'id': feed.pk,
                                                 'link': feed.link,
                                                 'title': feed.title}),
                                     mimetype='application/json')
        else:
            return http.HttpResponseNotModified()
    elif request.method == 'POST':
        # Modify an existing Feed object.
        pass
    elif request.method == 'DELETE':
        try:
            models.Feed.objects.get(pk=params['id']).delete()
            return http.HttpResponse()
        except models.Feed.DoesNotExist:
            return http.HttpResponseNotModified()
    else:
        return http.HttpResponseRedirect(urlresolvers.reverse('feeds'))


def feeds(request):
    """A view to display all available feeds."""
    return shortcuts.render(request, 'feeds.html',
                            {'feeds': models.Feed.objects.all()})


def index(request):
    """The site's index."""
    return http.HttpResponseRedirect(urlresolvers.reverse('feeds'))


class Feed(sv.Feed):
    """A simple syndication feed class.

    https://docs.djangoproject.com/en/1.5/ref/contrib/syndication/

    """
    feed_type = feedgenerator.Atom1Feed

    def get_object(self, request, key):
        return shortcuts.get_object_or_404(models.Feed, pk=key)

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.link

    def description(self, obj):
        return obj.description

    def items(self, obj):
        return models.Item.objects.filter(
            feed=obj).order_by('-pubdate')[:settings.MAX_ITEMS]

    def item_description(self, obj):
        return obj.description

    def item_link(self, obj):
        return obj.link

    def item_pubdate(self, obj):
        return obj.pubdate

    def item_title(self, obj):
        return obj.title
