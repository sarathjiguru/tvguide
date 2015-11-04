__author__ = 'sarath'


class Listing(object):

    def __init__(self, tv_listing):
        self.tv_listing = tv_listing
        self.show_name = tv_listing.split('|')[0]
        self.type = tv_listing.split('|')[1]
