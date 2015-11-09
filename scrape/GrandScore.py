import json
from sys import argv
import collections
import operator


__author__ = 'sarath'


class JsonToCsv(object):
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
        ratings = {}
        min_sum = min_rating * confidence
        actual_sum = 0
        for key in self.imdb:
            show = self.imdb[key]
            if metric in show:
                actual_sum = show[metric] * show[users]
                total_users = confidence + show[users]
            value = {'imdb': (min_sum + actual_sum) / total_users}
            self.update_grand_rating(key, value)

    def update_grand_rating(self, key, value):
        if key in self.grand_rating:
            self.grand_rating[key].update(value)
        else:
            self.grand_rating[key] = value

    def avg_support(self, fans):
        users = []
        for key in self.imdb:
            show = self.imdb[key]
            users.append(show.get(fans, 0))
        max_users = max(users)

        for key in self.imdb:
            show = self.imdb[key]
            value = {fans: float(show.get(fans, 0)) / max_users * 10}
            self.update_grand_rating(key, value)

    def get_grand_ranking(self, ratings_file):
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
    jsontocsv = JsonToCsv(argv[1])
    jsontocsv.get_grand_ranking(argv[2])