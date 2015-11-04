import os

__author__ = 'sarath'

import ujson
import time
import sys
from __builtin__ import file

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain.Listing import Listing

from TwitterAPI import TwitterAPI, TwitterRequestError


class TwitterSearch:
    def __init__(self):
        self.api = TwitterAPI('9bV6PsfoyLOr2EBL4JInYBVsz',
                              'gYBmmAdd1KWZuMgzI9i8U5wgeBvojvyZNXnXISqi3C3UFcqEan',
                              '3287471448-PgnQvj1GqbBJ8GaVR85XjBE6jQP0qvvo1MJOWKo',
                              'LKgpSjSZwptVoQ0QAB4rtl0DpUijLz8JJBhoN2EtqZl9C')

    def search_show(self, listing):
        results = self.api.request('users/search', {'q': listing.show_name, 'count': 3})
        count = 1
        for twitter_msg in results:
            if self.is_verified(twitter_msg) and count <= 3:
                return self.save_listing_data(twitter_msg)
        time.sleep(1)
        return {}

    def is_verified(self, twitter_msg):
        return 'verified' in twitter_msg and twitter_msg['verified']

    def save_listing_data(self, twitter_msg):
        fans = twitter_msg['followers_count']
        verified = twitter_msg['verified']
        id = twitter_msg['id']
        screen_name = twitter_msg['screen_name']
        return {'fans': fans, 'verified': verified, 'id': id, 'screen_name': screen_name}


if __name__ == '__main__':
    search = TwitterSearch()
    listing_file = file(sys.argv[1], 'r')
    scores = open(sys.argv[2], 'a')
    for line in listing_file:
        value = line.strip()
        print(value)
        listing = Listing(value)
        try:
            score = search.search_show(listing)
        except TwitterRequestError:
            print('wait for 15 min', listing)
            time.sleep(15 * 60)
            score = search.search_show(listing)
        scores.write(value + '\t' + ujson.dumps(score) + "\n")
    scores.close()