from google.appengine.ext import db


class Feed(db.Model):
    description = db.TextProperty()
    link = db.LinkProperty()
    title = db.StringProperty(default='Update pending...')
    pubdate = db.DateTimeProperty()
    users = db.StringListProperty()
    usercount = db.IntegerProperty(default=0)
    established = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)


class Item(db.Model):
    description = db.TextProperty()
    link = db.LinkProperty()
    title = db.StringProperty()
    pubdate = db.DateTimeProperty()
    feed = db.ReferenceProperty(Feed)
    established = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
