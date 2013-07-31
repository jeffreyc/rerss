import json

from django import http
from django import shortcuts
from django.conf import settings
from django.contrib.syndication import views as sv
from django.core import urlresolvers
from django.utils import feedgenerator
from google.appengine.ext import db

from feeds import models


def feed(request):
    """A view to support creating, modifying, and deleting feeds.

    RESTful: uses PUT to create, POST to edit, and DELETE to delete. Django's
    built-in syndication requires its own view, so GET is not implemented.

    """
    params = http.QueryDict(request.body, request.encoding)
    if request.method == 'PUT':
        if db.Query(models.Feed).filter('link = ', params['link']).count() == 0:
            f = models.Feed(link=params['link'], title='Update pending...')
            f.put()
            return http.HttpResponse(json.dumps({'id': f.key().id(),
                                                 'link': f.link,
                                                 'title': f.title}),
                                     mimetype='application/json')
        else:
            return http.HttpResponseNotModified()
    elif request.method == 'POST':
        # Modify an existing Feed object.
        pass
    elif request.method == 'DELETE':
        try:
            f = models.Feed.get_by_id(int(params['id']))
            db.delete(models.Item.all(keys_only=True).filter('feed = ', f))
            f.delete()
            return http.HttpResponse()
        except ValueError:
            return http.HttpResponseBadRequest()
        except db.NotSavedError:
            return http.HttpResponseNotModified()
    else:
        return http.HttpResponseRedirect(urlresolvers.reverse('feeds'))


def feeds(request):
    """A view to display all available feeds."""
    return shortcuts.render(request, 'feeds.html',
                            {'feeds':
                             models.Feed.all().order('title').order('link')})


def index(request):
    """The site's index."""
    return http.HttpResponseRedirect(urlresolvers.reverse('feeds'))


class Feed(sv.Feed):
    """A simple syndication feed class.

    https://docs.djangoproject.com/en/1.5/ref/contrib/syndication/

    """
    feed_type = feedgenerator.Rss201rev2Feed

    def get_object(self, request, key):
        try:
            obj = models.Feed.get_by_id(int(key))
            if obj:
                return obj
            else:
                return http.HttpResponseNotFound()
        except ValueError:
            return http.HttpResponseBadRequest()

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.link

    def description(self, obj):
        return obj.description

    def items(self, obj):
        items = db.Query(models.Item)
        items.filter('feed = ', obj)
        items.order('-pubdate')
        return items.run(limit=settings.MAX_ITEMS)

    def item_description(self, obj):
        return obj.description

    def item_link(self, obj):
        return obj.link

    def item_pubdate(self, obj):
        return obj.pubdate

    def item_title(self, obj):
        return obj.title
