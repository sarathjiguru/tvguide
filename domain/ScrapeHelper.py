"""
ScrapeHelper: BeautifulSoup dom parser helper. Contains all relevant methods required to scrape IMDB, rottentomatoes
 websites
"""
import BeautifulSoup

__author__ = 'sarath'


class ScrapeHelper(object):
    def __init__(self, read):
        self.soup = BeautifulSoup.BeautifulSoup(read.decode('utf-8', 'ignore'))

    def find_table_by_class(self, class_, soup=None):
        """
        find table and extract rows by a class name
        :param class_: table class
        :param soup: [BeautifulSoup object]. Optional, if not present searches with the soup initialized with the ScrapeHelper class
        :return: returns soup object of list of rows
        """
        soup = soup or self.soup
        table = soup.find('table', attrs={'class': class_})
        rows = table.findAll('tr')
        return rows

    def find_by_id(self, tag, id_, soup=None):
        """
        find the tag with id
        :param tag: tag name
        :param id_: id
        :param soup: [BeautifulSoup object]
        :return: div soup object
        """
        soup = soup or self.soup
        return soup.find(tag, attrs={'id': id_})

    def find_div_by_itemtype(self, schema_org_type, soup=None):
        """
        find div tag by schema.org itemtype
        :param schema_org_type: schema.org itemType
        :param soup: [BeautifulSoup object]
        :return: div soup object
        """
        soup = soup or self.soup
        return soup.find('div', attrs={'itemtype': schema_org_type})

    def find_by_itemprop(self, tag, schema_org_prop, soup=None):
        """
        find tag by schema.org itemprop
        :param tag: tag name
        :param schema_org_prop: schema.org itemprop
        :param soup: [Beautiful soup] object
        :return: tag soup object
        """
        soup = soup or self.soup
        return soup.find(tag, attrs={'itemprop': schema_org_prop})

    def find_all_anchors(self, soup=None):
        """
        find all anchor tags in the soup
        :param soup: [Beautiful soup] object
        :return: list of anchor tags
        """
        soup = soup or self.soup
        return soup.findAll('a')

    def find_by_class(self, tag, class_, soup=None):
        """
        find the fist tag with the class name
        :param tag:  tag
        :param class_:  class
        :param soup: [Beautiful soup]
        :return: tag soup object
        """
        soup = soup or self.soup
        return soup.find(tag, attrs={'class': class_})

    def ratingValue_in_span(self, soup=None):
        soup = soup or self.soup
        return self.find_by_itemprop('span', 'ratingValue', soup)

    def rating_in_meta(self, itemProp, soup=None):
        soup = soup or self.soup
        ratingValue = self.find_by_itemprop('meta', itemProp, soup)
        if ratingValue is not None:
            return ratingValue.get('content')
        return str(0)

    def __del__(self):
        self.soup.close()

    def close(self):
        self.soup.close()