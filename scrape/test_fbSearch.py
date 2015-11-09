from unittest import TestCase
from domain.Listing import Listing
from scrape.FbSearch import FbSearch

__author__ = 'sarath'


class TestFbSearch(TestCase):
    def setUp(self):
        self.fbSearch = FbSearch()

    def test_search_show(self):
        print(self.fbSearch.search_show(Listing("Escape From Planet Earth|movie")))