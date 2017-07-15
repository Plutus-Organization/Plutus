"""
Handles Stock articles pipeline.
"""
import webhoseio
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
        :param num_articles:  number of articles to pull using the webhose api.
        :param num_sentences: number of sentences returned by the SMMRY api.
        """
        self.num_articles = num_articles
        self.num_sentences = num_sentences

    def retrieve_topmost_article(self, stock_symbol):
        # Check if the article is already in db. If so return article.
        # Else, use api
        webhoseio.config(token=webhose_api_key)
