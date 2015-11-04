from unittest import TestCase
from domain.Listing import Listing
from scrape.TwitterSearch import TwitterSearch

__author__ = 'sarath'


class TestTwitterSearch(TestCase):
    def setUp(self):
        self.twitter = TwitterSearch()

    def test_search_show(self):
        print(self.twitter.search_show(Listing("The Wendy Williams Show|tv")))
