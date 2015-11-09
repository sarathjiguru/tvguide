"""
RTScrape: This class is designed to scrape  rottentomatoes website, to extract rating and reviews information
"""
import contextlib
import os
import urllib
from __builtin__ import long
from __builtin__ import file
import sys
import ujson
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain.Listing import Listing
from domain.ScrapeHelper import ScrapeHelper

__author__ = 'sarath'

lookup = {'tv': '#results_tv_tab',
          'movie': '#results_movies_tab'}

url_finder = {'tv': '/tv/', 'movie': '/m/'}


class RTScrape(object):
    def __init__(self):
        self.url = 'http://www.rottentomatoes.com'
        self.find = '/search/'
        self.q = 'search'

    def finder_url(self, tv_listing):
        query = urllib.urlencode({self.q: tv_listing.show_name})
        return self.url + self.find + "?" + query + lookup[tv_listing.type]

    def parse_search_page(self, read, type_):
        helper = ScrapeHelper(read)
        by_id = helper.find_by_id('ul', type_ + '_results_ul')
        return self.url + helper.find_all_anchors(by_id)[0].get('href')

    def page_url(self, tv_listing):
        """
        searches for the tv_listing. RottenTomatoes redirects to the page url, if it is the only result.
         In that case it extracts the redirected url. Else parses the search page and gets the first listing
        :param tv_listing: Listing
        :return: url of the listing page
        """
        finder_url = self.finder_url(tv_listing)
        with contextlib.closing(urllib.urlopen(finder_url)) as page_response:
            request_url = page_response.geturl()
            if url_finder[tv_listing.type] in request_url:
                return request_url
            return self.parse_search_page(page_response.read(), tv_listing.type)

    def get_scores(self, read):
        """
        fetches raing, bestrating, worstrating, users info from the listing page url
        :param read: read object
        :return: dict
        """
        helper = ScrapeHelper(read)
        by_id = helper.find_by_id('div', 'all-critics-numbers')
        all_critic = {'rating': self.getCount(helper.ratingValue_in_span(by_id)),
                      'bestrating': self.getCount(helper.rating_in_meta('bestrating', by_id)),
                      'worstrating': self.getCount(helper.rating_in_meta('worstrating', by_id)),
                      'users': self.getCount(helper.rating_in_meta('reviewCount ratingCount', by_id))}

        audience_score = helper.find_by_class('div', 'audience-score meter')
        avg_audience = {'rating': self.getCount(helper.ratingValue_in_span(audience_score)),
                        'best_rating': self.getCount(helper.rating_in_meta('bestrating', audience_score)),
                        'worst_rating': self.getCount(helper.rating_in_meta('worstrating', audience_score)),
                        'users': self.getCount(helper.rating_in_meta('ratingCount', audience_score))}
        time.sleep(1)
        return {'all_critic': all_critic, 'avg_audience': avg_audience}

    def getCount(self, soup):
        if soup is not None:
            value = soup
            if hasattr(soup, 'text'):
                value = soup.text
            return long(value.replace(",", "").replace("%", ""))
        return 0


if __name__ == '__main__':
    rt_scrape = RTScrape()
    listing_file = file(sys.argv[1], 'r')
    scores = open(sys.argv[2], 'a')
    missed = open(sys.argv[3], 'a')
    for line in listing_file:
        value = line.strip()
        try:
            print(value)
            listing = Listing(value)
            page_url = rt_scrape.page_url(listing)
            with contextlib.closing(urllib.urlopen(page_url)) as response:
                score = rt_scrape.get_scores(response.read())
            scores.write(value + '\t' + ujson.dumps(score) + "\n")
        except AttributeError as e:
            missed.write(value + '\n')
        except IndexError:
            missed.write("no tv listing" + "," + value + "\n")
    scores.close()