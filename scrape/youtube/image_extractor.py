import contextlib
import urllib

from domain.ScrapeHelper import ScrapeHelper


class ImageExtractor:
    def __init__(self, search_criteria):
        self.search_criteria = search_criteria
        self._url = self._get_search_url()
        pass

    def images_for_search_criteria(self):
        """
            1. youtube search url
            2. convert html content to beautiful soup
            3. iterate through each video link in search results
            4. get the link of the hd image
            5. save the hdimage on disk
            """
        with contextlib.closing(urllib.urlopen(self._url)) as page_response:
            helper = ScrapeHelper(page_response.read())
            results_tag = helper.find_by_id('div', 'results')
            elements = helper.find_all_elements('li', results_tag)
            anchor_tags = []
            for element in elements:
                anchor_tags.extend(helper.find_all_anchors(element))
            image_links = []
            for anchor_tag in anchor_tags:
                img_tags = helper.find_all_elements('img', anchor_tag)
                for img_tag in img_tags:
                    image_links.append(img_tag['src'])
            print image_links
            self._save_to_disk(image_links)

    """
    a protected method. Protected methods and variables start with underscore
    """

    def _get_search_url(self):
        formatted_search_criteria = self.search_criteria.replace(' ', '+')
        url = 'https://www.youtube.com/results?search_query=' + formatted_search_criteria
        return url

    def _get_search_page(self):
        with contextlib.closing(urllib.urlopen(self._url)) as page_response:
            helper = ScrapeHelper(page_response.read())
            return helper.soup

    def _save_to_disk(self, image_links):
        ur_lopener = urllib.URLopener()
        for image_link in image_links:
            if 'i.ytimg.com' in image_link:
                file_name = image_link.replace('https://i.ytimg.com/vi/', '').split('/')[0]
                ur_lopener.retrieve(image_link, file_name + '.jpg')
        ur_lopener.close()
