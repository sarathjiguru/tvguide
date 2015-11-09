"""FbSearch: This class is designed to search for a tv listing(as of now a tv show, or a movie
 and get its official Facebook page, likes count etc if ever exists
"""
from __builtin__ import file
import os
import sys
import ujson
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from domain.Listing import Listing

__author__ = 'sarath'

import facebook


class FbSearch():
    def __init__(self):
        self.graph_api = facebook.GraphAPI(
            access_token='CAACEdEose0cBAPxJ3ZCXeXJzu2vZCpUN5aBTyG6wFbDdFriZCaQNT0hwhEUBnQZCI9NdshD4LrxNGzJ1YQX4ZAZAB3NxddUeLPVRcnaDfVY7kfO3f7V6EpgbcbqM6kVUstLuQHScbGQHRa3aZB4X00Vlylx04gCVY6yVEZAQCPvrC9wxCYxDlDZAkMEntJUhUodQVVGsZAgenwNAZDZD')

    def search_show(self, tv_listing):
        result_list = self.graph_api.request('/search', {'q': tv_listing.show_name, 'type': 'page',
                                                         'fields': 'likes,id,name,talking_about_count', 'limit': 1})
        data_ = result_list['data']
        if data_:
            result = data_[0]
            result['fans'] = result.pop('likes')
            return result
        time.sleep(2)
        return {}


if __name__ == '__main__':
    search = FbSearch()
    listing_file = file(sys.argv[1], 'r')
    scores = open(sys.argv[2], 'a')
    for line in listing_file:
        value = line.strip()
        print(value)
        listing = Listing(value)
        try:
            score = search.search_show(listing)
            scores.write(value + '\t' + ujson.dumps(score) + "\n")
        except Exception as e:
            print(value, e)
            time.sleep(30 * 60)
    scores.close()