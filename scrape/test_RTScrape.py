from unittest import TestCase
import urllib
import urllib2
import urllib3
from __builtin__ import file

from domain.Listing import Listing
from scrape.RTScrape import RTScrape


__author__ = 'sarath'


class TestRTScrape(TestCase):
    def setUp(self):
        self.rt = RTScrape()

    def test_finder_url(self):
        listing = Listing("CNN Newsroom|tv")
        self.assertEqual(self.rt.finder_url(listing),
                         "http://www.rottentomatoes.com/search/?search=Law+%26+Order%3A+Special+Victims+Unit#results_tv_tab")

    def test_parse_search_url(self):
        r__read = file('/home/sarath/start-internet-idea/tvguide/resources/RT_search.html', 'r').read()
        print(self.rt.parse_search_page(r__read))

    def test_get_scores(self):
        r__read = file('/home/sarath/start-internet-idea/tvguide/resources/rt_page_2.html', 'r').read()
        print(self.rt.get_scores(r__read))