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
        self.purge_unattached_feeds_and_items()
        feeds = models.Feed.all()
        for feed in feeds:
            try:
                logging.debug('Updating "%s"' % feed.link)
                d = feedparser.parse(feed.link)
                if not d.feed:
                    logging.info('"%s" not found, skipping' % feed.link)
                    continue
                if d.feed.has_key('updated_parsed'):
                    dt = datetime_from_parsed(d.feed.updated_parsed)
                elif d.feed.has_key('published_parsed'):
                    dt = datetime_from_parsed(d.feed.published_parsed)
                else:
                    dt = datetime.datetime.now()
                if feed.pubdate is None or dt > feed.pubdate:
                    self.update_datastore(feed, d, dt)
                else:
                    logging.info('"%s" < "%s", skipping' % (dt, feed.pubdate))
            except Exception:
                logging.error('Exception processing "%s":\n%r' %
                              (feed.link, traceback.format_exc()))
                pass
        self.purge_old_items()

    def purge_old_items(self):
        before = datetime.datetime.now() - \
                 datetime.timedelta(days=settings.KEEP_FOR)
        db.delete(models.Item.all(keys_only=True).filter('pubdate <=', before))

    def purge_unattached_feeds_and_items(self):
        before = datetime.datetime.now() - \
                 datetime.timedelta(minutes=settings.PURGE_DELAY)
        f = models.Feed.all(keys_only=True)
        f.filter('usercount =', 0).filter('modified <=', before)
        for feed in f.run():
            db.delete(models.Item.all(keys_only=True).filter('feed =', feed))
        db.delete(f)

    def update_datastore(self, feed, d, dt):
        logging.debug('Updating %s' % feed)
        if d.feed.has_key('description') and d.feed.description:
            feed.description = d.feed.description
        if d.feed.title:
            feed.title = d.feed.title
        feed.pubdate = dt
        for entry in d.entries:
            logging.debug('Adding/updating %s' % entry.title)
            if entry.has_key('updated_parsed'):
                et = datetime_from_parsed(entry.updated_parsed)
            elif entry.has_key('published_parsed'):
                et = datetime_from_parsed(entry.published_parsed)
            else:
                et = datetime.datetime.now()
            i = db.Query(models.Item)
            i.filter('feed =', feed)
            i.filter('link =', entry.link)
            i.ancestor(feed.key())
            if i.count() == 0:
                item = models.Item(feed=feed, link=entry.link,
                                   title=entry.title,
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
