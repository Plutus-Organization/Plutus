"""
Handles Stock articles pipeline.
"""
import webhoseio
import json
import urllib.request
from static.credentials import *


class StockArticle:
    def __init__(self, stock_symbol, article_url, article_summary):
        """
        Initializes a Stock Article.
        :param stock_symbol:    symbol for the stock the article is associated with.
        :param article_url:     url of the article.
        :param article_summary: summary of the article.
        """
        self.stock_symbol = stock_symbol
        self.article_url = article_url
        self.article_summary = article_summary

    #TODO: store article into db
    def store_article_into_db(self):
        pass


class RelevantArticlesSource:
    def __init__(self, num_articles, num_sentences):
        """
        Initializes the Source class.
        :param num_sentences: number of sentences returned by the SMMRY api.
        """
        self.num_sentences = num_sentences

    def retrieve_topmost_article(self, stock_symbol, stock_name):
        """
        Retrieves the topmost article about the stock.
        :param stock_symbol: stock symbol.
        :param stock_name:   stock name.
        :return:             a StockArticle object.
        """
        # Check if the article is already in db. If so return article.
        # Else, use api
        return self.retrieve_topmost_article_new(stock_symbol, stock_name)

    def retrieve_topmost_article_new(self, stock_symbol, stock_name):
        """
        Retrieves the topmost article about the stock, but solely through the usage of the webhose API. This
        does not involve checking the database for an already existing article for the stock.
        :param stock_symbol: stock symbol.
        :param stock_name:   stock name.
        :return:             a StockArticle object.
        """
        webhoseio.config(token=webhose_api_key)
        stock_name = stock_name.lower()
        filters = {'language': 'english', 'text': stock_name, 'site_type': 'news',
                   'site_category': 'finance', 'thread.title': stock_name}
        query_result = webhoseio.query('filterWebContent', filters)
        stock_posts = query_result['posts']
        if len(stock_posts) == 0:
            return None
        article_info = json.loads(stock_posts[0])
        article_url = article_info['url']
        article_summary = self.summarize_article(article_url)

        return StockArticle(stock_symbol, article_url, article_summary)

    def summarize_article(self, article_url):
        """
        Summarizes an article using the SMMRY API.
        :param article_url: URL pointing to the article to summarize.
        :return:            text of the summarized article.
        """
        query_url = 'http://api.smmry.com/'
        get_params = {'SM_API_KEY': smmry_api_key, 'SM_URL': article_url, 'SM_LENGTH': self.num_sentences}
        query_url += RelevantArticlesSource.construct_get_query(get_params)
        content_json = urllib.request.urlopen(query_url).read().decode('utf-8')
        contents = json.loads(content_json)
        return contents['sm_api_content']

    @staticmethod
    def construct_get_query(get_params):
        """
        Helper function to contruct the query string of a GET request based on a params dictionary.
        :param get_params: params of the GET request URL.
        :return:           constructed query portion of the GET request.
        """
        get_param_url = '?'
        for param_key in get_params:
            get_param_url += param_key + '=' + get_params[param_key] + '&'
        get_param_url = get_param_url[:-1]
        return get_param_url
