from unittest import TestCase

from __builtin__ import file

from domain.Listing import Listing
from domain.ScrapeHelper import ScrapeHelper
from scrape.IMDBScrape import IMDBScrape


__author__ = 'sarath'


class TestIMDBScrape(TestCase):
    imdb = IMDBScrape()

    def test_fetch(self):
        listing = Listing("Top 20 Most Shocking|tv")
        self.assertEqual(self.imdb.finder_url(listing, titles=True),
                         'http://www.imdb.com/find?q=Law+%26+Order%3A+Special+Victims+Unit&type=ep&s=tt&&exact=true')

    def test_page_url(self):
        listing = Listing("CNN Newsroom|tv")
        print(self.imdb.page_url(listing))

    def test_get_scores(self):
        r__read = file('/home/sarath/start-internet-idea/tvguide/resources/imdb_title.html', 'r').read()
        print(self.imdb.get_scores(r__read))

    def test_meter_change_ascend(self):
        helper = ScrapeHelper(open('/home/sarath/start-internet-idea/tvguide/resources/imdb_listing_with_popularity_ascend.html', 'r').read())
        print(self.imdb.meter_change(helper))

    def test_meter_change_descend(self):
        helper = ScrapeHelper(open('/home/sarath/start-internet-idea/tvguide/resources/imdb_listing_with_popularity_descend.html', 'r').read())
        print(self.imdb.meter_change(helper))