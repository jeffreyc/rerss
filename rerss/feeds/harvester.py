#!/usr/bin/env python

import datetime

import feedparser

from feeds import models


def datetime_from_parsed(parsed):
    return datetime.datetime(parsed[0], parsed[1], parsed[2], parsed[3],
                             parsed[4], parsed[5], parsed[6])


def main():
    feeds = models.Feed.objects.all()
    for feed in feeds:
        d = feedparser.parse(feed.link)
        if not d.feed:
            continue
        if d.feed.has_key('updated_parsed'):
            dt = datetime_from_parsed(d.feed.updated_parsed)
        else:
            dt = datetime_from_parsed(d.feed.published_parsed)
        if True or feed.pubdate is None or dt > feed.pubdate:
            if d.feed.description:
                feed.description = d.feed.description
            if d.feed.title:
                feed.title = d.feed.title
            feed.pubdate = dt
            # TODO: wrap this in a transaction.
            feed.save()
            for entry in d.entries:
                if entry.updated_parsed:
                    et = datetime_from_parsed(entry.updated_parsed)
                else:
                    et = datetime_from_parsed(entry.published_parsed)
                item, cre = models.Item.objects.get_or_create(
                    feed=feed, link=entry.link,
                    defaults={'title': entry.title,
                              'description': entry.description,
                              'pubdate': et})
                if not cre and et > item.pubdate:
                    if entry.title:
                        item.title = entry.title
                    if entry.description:
                        item.description = entry.description
                    entry.pubdate = et
                    entry.save()
    # TODO: purge Items older than x days?


if __name__ == '__main__':
    main()
