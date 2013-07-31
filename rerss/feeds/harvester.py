#!/usr/bin/env python

import datetime
import logging
import traceback

from django.conf import settings
import feedparser
from google.appengine.ext import db
import webapp2

from feeds import models


def datetime_from_parsed(parsed):
    return datetime.datetime(parsed[0], parsed[1], parsed[2], parsed[3],
                             parsed[4], parsed[5], parsed[6])


class Harvester(webapp2.RequestHandler):
    def get(self):
        feeds = models.Feed.all()
        for feed in feeds:
            try:
                d = feedparser.parse(feed.link)
                if not d.feed:
                    continue
                if d.feed.has_key('updated_parsed'):
                    dt = datetime_from_parsed(d.feed.updated_parsed)
                else:
                    dt = datetime_from_parsed(d.feed.published_parsed)
                if True or feed.pubdate is None or dt > feed.pubdate:
                    self.update_datastore(feed, d, dt)
            except Exception:
                logging.error('Exception processing %s:\n%r' %
                              (feed.link, traceback.format_exc()))
                pass
        self.purge_old_items()

    def purge_old_items(self):
        before = datetime.datetime.now() - datetime.timedelta(settings.KEEP_FOR)
        db.delete(models.Item.all(keys_only=True).filter('pubdate <=', before))

    def update_datastore(self, feed, d, dt):
        if d.feed.description:
            feed.description = d.feed.description
        if d.feed.title:
            feed.title = d.feed.title
        feed.pubdate = dt
        for entry in d.entries:
            if entry.updated_parsed:
                et = datetime_from_parsed(entry.updated_parsed)
            else:
                et = datetime_from_parsed(entry.published_parsed)
            i = db.Query(models.Item)
            i.filter('feed = ', feed)
            i.filter('link = ', entry.link)
            i.ancestor(feed.key())
            if i.count() == 0:
                item = models.Item(feed=feed, link=entry.link, title=entry.title,
                                   description=entry.description, pubdate=et)
                item.put()
            else:
                item = i.get()
                if et > item.pubdate:
                    if entry.title:
                        item.title = entry.title
                    if entry.description:
                        item.description = entry.description
                    item.pubdate = et
                    item.put()
        feed.put()


application = webapp2.WSGIApplication([('/harvester', Harvester)])
