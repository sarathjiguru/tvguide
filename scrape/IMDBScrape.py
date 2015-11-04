"""IMDBScrape can be used to scrape www.imdb.com website, for a tv listing given.
  It can successfully fetch, imdb rating, no. of ratings, popularity score, reviews etc.
"""

import contextlib
import os
import sys
import urllib
import ujson
import logging

logging.basicConfig(filename='imdb.log', level=logging.DEBUG)

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

    def finder_url(self, listing):
        """
        fetches IMDB search url
        :param listing: Listing
        :return: imdb search url http://www.imdb.com/find?q=<query>&type=<type>&s=tt&&exact=true
        """
        self.type += lookup[listing.type]
        path = urllib.urlencode({self.q: listing.show_name})
        return self.url + self.find + "?" + path + "&" + self.type + self.exact

    def page_url(self, read):
        """
        parses the imdb search url page and retrieves the first listing page url.
        :param read: read object of a resource. This way we can stub it out, in such a way that we can send a url response
        object or file read object
        :return: returns url of the imdb listing page: http://www.imdb.com/title/tt0898266/?ref_=fn_tt_tt_1
        """
        helper = ScrapeHelper(read)
        rows = helper.find_table_by_class("findList")
        top_result = rows[0].find('td').find('a').get('href')
        helper.close()
        return self.url + top_result

    def getCount(self, anchor):
        if anchor.get('title') is not None:
            return anchor.get('title').split()[0].replace(',', '')
        return 0

    def getPopularity(self, helper):
        popularity = 0
        by_id = helper.find_by_id('span', 'meterRank')
        if by_id is not None:
            popularity = int(by_id.text.replace(",", ""))
        return popularity

    def get_scores(self, read):
        """
        parses IMDB listing page and fetches relevant information
        :param read: read object
        :return: dict of popularity, best_rating, users, reviews, and external_reviews
        """
        popularity, best_rating, users, reviews, external_reviews = 0, 0, 0, 0, 0
        rating = 0

        helper = ScrapeHelper(read)
        popularity = self.getPopularity(helper)
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
            search_url = imdb_scrape.finder_url(listing)
            with contextlib.closing(urllib.urlopen(search_url)) as response:
                page_url = imdb_scrape.page_url(response.read())
            with contextlib.closing(urllib.urlopen(page_url)) as response:
                score = imdb_scrape.get_scores(response.read())
            imdb_scores.write(line.strip() + '\t' + ujson.dumps(score) + "\n")
        except AttributeError as e:
            imdb_missed.write(line.strip() + '\n')
            logging.error('error fot show', line, e)
    imdb_scores.close()