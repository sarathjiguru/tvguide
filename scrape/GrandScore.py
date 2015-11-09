"""
GrandScore: loads the file contains ratings from all sources; creates an grand rating score
"""
import json
from sys import argv
import collections
import operator


__author__ = 'sarath'


class GrandScore(object):
    def __init__(self, imdb_file):
        self.grand_rating = collections.defaultdict(dict)
        handle = open(imdb_file, 'r')
        self.imdb = collections.defaultdict(dict)
        for line_ in handle:
            value = line_.strip()
            splits = value.split("\t")
            key = splits[0]
            current_dict = json.loads(splits[1])
            if current_dict is not None:
                if key in self.imdb:
                    self.imdb[key].update(current_dict)
                else:
                    self.imdb[key] = current_dict
        handle.close()

    def parseTsv(self):
        """
        function is used to return grand rating; this is used to explore data in excel and not used for any calculation
        :return: prints csv data
        """
        for key in self.imdb:
            val = self.imdb[key]
            msg = key + "|" + str(val.get('users', 0)) + "|" + str(val.get('rating', 0)) + "|" + str(
                val.get('popularity', 0)) + "|" + str(val.get('fans', 0)) + "|" + str(
                val.get('twitter_fans', 0))
            if 'avg_audience' in val:
                msg = msg + "|" + str(val['avg_audience'].get('rt_users', 0)) + "|" + str(
                    val['avg_audience'].get('rt_rating', 0) / 10)
            print(msg)

    def normalized_rating(self, metric, users, min_rating, confidence):
        """
        given the min rating and confidence, calculates the normalized rating.
        Since we have multiple rating keys like rt_rating for rottentomatoes and ratings for imdb, need to send metric and users.

        The task of finding the min_rating and confidence is unburdened from this module. As of now, we are eye balling on the graph
        created for exploring and setting the min_rating and confidence
        :param metric: rating: example rating
        :param users: users: example users
        :param min_rating: min_rating
        :param confidence: confidence
        :return: normalized rating
        """
        # sum of ratings for the show, if there is no rating given by any user
        min_sum = min_rating * confidence

        for key in self.imdb:
            # actual sum of ratings given for the show
            actual_sum = 0
            show = self.imdb[key]
            total_users = confidence
            if metric in show:
                actual_sum = show[metric] * show[users]
                total_users = confidence + show[users]
            value = {'imdb': (min_sum + actual_sum) / total_users}
            self.update_grand_rating(key, value)

    def update_grand_rating(self, key, value):
        """
        upate the grandrating with the current rating value
        :param key:
        :param value:
        :return:
        """
        if key in self.grand_rating:
            self.grand_rating[key].update(value)
        else:
            self.grand_rating[key] = value

    def avg_support(self, fans):
        """
        calculate the support of fb/twitter users for the listing. fans_for_listing/max_fans
        :param fans: fan type twitter_fans for twitter
        :return: return support for the listing (in the range of 1 to 10)
        """
        users = []
        for key in self.imdb:
            show = self.imdb[key]
            users.append(show.get(fans, 0))
        # get maximum no. of users
        max_users = max(users)

        for key in self.imdb:
            show = self.imdb[key]
            value = {fans: float(show.get(fans, 0)) / max_users * 10}
            self.update_grand_rating(key, value)

    def get_grand_ranking(self, ratings_file):
        """
        calculates grand ranking. Formuala: (5*imdb_rating+2.5*twitter_support+2.5*facebook_support)/10
        :param ratings_file:
        :return:
        """
        ratings = {}
        sorted_output = open(ratings_file, 'w')
        self.normalized_rating('rating', 'users', 3.5, 28230)
        self.avg_support('fans')
        self.avg_support('twitter_fans')
        for key in self.grand_rating:
            imdb = self.grand_rating[key].get('imdb', 0)
            fans = self.grand_rating[key].get('fans', 0)
            tw_fans = self.grand_rating[key].get('tw_fans', 0)
            ratings[key] = (5 * imdb + 2.5 * fans + 2.5 * tw_fans) / 10
        sorted_ratings = sorted(ratings.items(), key=operator.itemgetter(1), reverse=True)
        print(self.grand_rating['Game of Thrones|tv'])
        for ratingtuple in sorted_ratings:
            sorted_output.write(ratingtuple[0] + "," + str(ratingtuple[1]) + "\n")
        sorted_output.close()


if __name__ == '__main__':
    # expects the file, that contains the ratings from all sources and the file to write the sorted tv listings
    grandscore = GrandScore(argv[1])
    grandscore.get_grand_ranking(argv[2])