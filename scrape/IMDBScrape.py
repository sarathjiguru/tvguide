"""IMDBScrape can be used to scrape www.imdb.com website, for a tv listing given.
  It can successfully fetch, imdb rating, no. of ratings, popularity score, reviews etc.
"""

import contextlib
import os
import sys
import urllib
import ujson

from __builtin__ import long
from __builtin__ import file

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from domain.Listing import Listing
from domain.ScrapeHelper import ScrapeHelper

__author__ = 'sarath'

lookup = {'tv': 'ep', 'movie': 'tt'}


class IMDBScrape(object):
    def __init__(self):
        self.url = "http://www.imdb.com"
        self.find = "/find"
        self.q = "q"
        self.exact = "&s=tt&&exact=true"
        self.type = "type="

    def finder_url(self, listing, titles=False):
        """
        fetches IMDB search url
        :param listing: Listing
        :return: imdb search url http://www.imdb.com/find?q=<query>&type=<type>&s=tt&&exact=true
        """
        path = urllib.urlencode({self.q: listing.show_name})
        url = self.url + self.find + "?" + path + "&"

        if titles:
            return url + "s=tt"

        self.type += lookup[listing.type]
        return url + self.type + self.exact

    def page_url(self, tv_listing):
        """
        parses the imdb search url page and retrieves the first listing page url.
        :param read: read object of a resource. This way we can stub it out, in such a way that we can send a url response
        object or file read object
        :return: returns url of the imdb listing page: http://www.imdb.com/title/tt0898266/?ref_=fn_tt_tt_1
        """
        url = self.finder_url(tv_listing)
        with contextlib.closing(urllib.urlopen(url)) as page_response:
            helper = ScrapeHelper(page_response.read())

            if helper.is_table_exists("findList"):
                rows = helper.find_table_by_class("findList")
            else:
                url = self.finder_url(tv_listing, titles=True)
                with contextlib.closing(urllib.urlopen(url)) as page_response_1:
                    helper = ScrapeHelper(page_response_1.read())
                    rows = helper.find_table_by_class("findList")

        top_result = rows[0].find('td').find('a').get('href')
        return self.url + top_result

    def getCount(self, anchor):
        if anchor.get('title') is not None:
            return anchor.get('title').split()[0].replace(',', '')
        return 0

    def meter_change(self, helper):
        try:
            meter_change = helper.find_by_id('div', 'meterChangeRow')
            change = meter_change.find('span').text.strip().lower()
            meter_change_value = int(helper.find_by_id('span', 'meterChange', meter_change).text)
            if change == 'down':
                return -meter_change_value
            else:
                return meter_change_value
        except Exception:
            return 0

    def getPopularity(self, helper):
        popularity = 0
        by_id = helper.find_by_id('span', 'meterRank')
        if by_id is not None:
            popularity = int(by_id.text.replace(",", ""))
            self.meter_change(helper)
        return popularity

    def get_scores(self, read):
        """
        parses IMDB listing page and fetches relevant information
        :param read: read object
        :return: dict of popularity, best_rating, users, reviews, and external_reviews
        """

        helper = ScrapeHelper(read)
        popularity = self.getPopularity(helper)
        popularity_change = self.meter_change(helper)
        score_div = helper.find_div_by_itemtype('http://schema.org/AggregateRating')
        rating = float(helper.find_by_itemprop('span', 'ratingValue', score_div).text.replace(",", ""))
        best_rating = int(helper.find_by_itemprop('span', 'bestRating', score_div).text.replace(",", ""))
        anchors = helper.find_all_anchors(score_div)
        users, reviews, external_reviews = '', '', ''
        for anchor in anchors:
            href = anchor.get('href').split('?')[0]
            count = long(self.getCount(anchor))
            if href == 'ratings':
                users = count
            elif href == 'reviews':
                reviews = count
            elif href == 'externalreviews':
                external_reviews = count

        return {'popularity': popularity,
                'popularity_change': popularity_change,
                'rating': rating,
                'best_rating': best_rating,
                'users': users,
                'reviews': reviews,
                'external_reviews': external_reviews}


if __name__ == '__main__':
    imdb_scrape = IMDBScrape()
    listing_file = file(sys.argv[1], 'r')
    imdb_scores = open(sys.argv[2], 'a')
    imdb_missed = open(sys.argv[3], 'a')
    for line in listing_file:
        try:
            print(line.strip())
            listing = Listing(line.strip())
            page_url = imdb_scrape.page_url(listing)
            with contextlib.closing(urllib.urlopen(page_url)) as response:
                score = imdb_scrape.get_scores(response.read())
            imdb_scores.write(line.strip() + '\t' + ujson.dumps(score) + "\n")
        except AttributeError as e:
            imdb_missed.write(line.strip() + '\n')
    imdb_scores.close()