from unittest import TestCase

from scrape.youtube.image_extractor import ImageExtractor


class TestImageExtractor(TestCase):
    def setUp(self):
        self.i = ImageExtractor('comedy scenes nani')

    def test_if_search_url_properly_formatted(self):
        url = self.i._get_search_url()
        print url
        assert url == 'https://www.youtube.com/results?search_query=comedy+scenes+nani'
        pass

    def test_if_soup_created_for_search_page(self):
        print self.i._get_search_page()

    def test_images_for_search_criteria(self):
        self.i.images_for_search_criteria()
