from unittest import TestCase

from __builtin__ import file

from domain.Listing import Listing
from scrape.IMDBScrape import IMDBScrape


__author__ = 'sarath'


class TestIMDBScrape(TestCase):
    imdb = IMDBScrape()

    def test_fetch(self):
        listing = Listing("The Godfather, Part II|movie")
        self.assertEqual(self.imdb.finder_url(listing),
                         'http://www.imdb.com/find?q=Law+%26+Order%3A+Special+Victims+Unit&type=ep&s=tt&&exact=true')

    def test_page_url(self):
        r__read = file('/home/sarath/start-internet-idea/tvguide/resources/imdb_search.html', 'r').read()
        print(self.imdb.page_url(r__read))
        self.assertEqual(self.imdb.page_url(r__read), 'http://www.imdb.com/title/tt0898266/?ref_=fn_tt_tt_1')

    def test_get_scores(self):
        r__read = file('/home/sarath/start-internet-idea/tvguide/resources/imdb_title.html', 'r').read()
        print(self.imdb.get_scores(r__read))
