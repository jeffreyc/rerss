from django.conf import urls

from feeds import views


urlpatterns = urls.patterns(
    '',
    urls.url(r'^$', 'feeds.views.index', name='index'),
    urls.url(r'^about/$', 'feeds.views.about', name='about'),
    urls.url(r'^feed/$', 'feeds.views.feed', name='feed_api'),
    urls.url(r'^feed/(?P<key>[a-zA-Z0-9]+)/$', views.Feed(), name='feed'),
    urls.url(r'^feeds/$', 'feeds.views.feeds', name='feeds'),
)
