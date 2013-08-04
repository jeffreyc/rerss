*****
RERSS
*****

ReRSS is a simple Django/Google App Engine application meant to re-syndicate
RSS feeds in a post-Google Reader world. It maintains a list of feed URLs,
downloads them on a regular basis, and re-syndicates the contents, preventing
items from aging off before they can be read. It's meant to be used with
stand-alone (i.e., non-synching) desktop RSS Readers, as this functionality is
provided by most RSS synching services.

Requirements
============

ReRSS runs on Google App Engine.

Configuration
=============

If deploying to Google App Engine, update the ``application`` in ``app.yaml``.

The file ``settings_private.py`` is not included. It needs to be created in
the same directory as ``settings.py`` (``rerss/rerss``) with the contents::

  # Make this unique, and don't share it with anybody.
  SECRET_KEY = '...'

Version History
===============

0.1 -- 2013-07-29 -- proof-of-concept
