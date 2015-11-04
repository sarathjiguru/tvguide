"""FbSearch: This class is designed to search for a tv listing(as of now a tv show, or a movie
 and get its official Facebook page, likes count etc if ever exists
"""

__author__ = 'sarath'

import facebook


class FbSearch():
    def __init__(self):
        self.graph_api = facebook.GraphAPI
        self.request = self.graph_api.request('/search', {'q': 'parenthood', 'type': 'page', 'fields': 'likes,id,name'})