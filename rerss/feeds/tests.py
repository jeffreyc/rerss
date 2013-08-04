import datetime

from django import test
from django.test import client
from google.appengine.ext import testbed

from . import harvester
from . import views


class TestHarvester(test.SimpleTestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_datetime_from_parsed(self):
        self.assertEqual(
            harvester.datetime_from_parsed([2013, 1, 2, 3, 4, 5, 6]),
            datetime.datetime(2013, 1, 2, 3, 4, 5, 6))

    def test_get(self): pass
    def test_harvester_get(self): pass
    def test_harvester_purge_old_items(self): pass
    def test_harvester_purge_unattached_feeds_and_items(self): pass
    def test_harvester_update_datastore(self): pass


class TestViews(test.SimpleTestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
        self.client = client.Client()

    def tearDown(self):
        self.testbed.deactivate()

    def test_feed_delete(self): pass
    def test_feed_delete_bad_id(self): pass
    def test_feed_delete_not_saved(self): pass
    def test_feed_get(self): pass
    def test_feed_post(self): pass
    def test_feed_put_adds_user_to_existing(self): pass
    def test_feed_put_creates_new(self): pass
    def test_feed_put_user_in_users_not_modified(self): pass
    def test_feed_with_id_bad_key(self): pass
    def test_feed_with_id_get(self): pass
    def test_feed_with_id_not_found(self): pass
    def test_feeds_feeds(self): pass
    def test_feeds_no_feeds(self): pass

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
