"""
Handles Stock articles pipeline.
"""
import webhoseio
import json
import requests
from static.credentials import *


class StockArticle:
    def __init__(self, stock_name, article_url, article_summary):
        """
        Initializes a Stock Article.
        :param stock_name:      name for the stock the article is associated with.
        :param article_url:     url of the article.
        :param article_summary: summary of the article.
        """
        self.stock_name = stock_name
        self.article_url = article_url
        self.article_summary = article_summary


class RelevantArticlesSource:
    def __init__(self, num_sentences):
        """
        Initializes the Source class.
        :param num_sentences: number of sentences returned by the SMMRY api.
        """
        self.db = {}
        self.num_sentences = num_sentences

    def retrieve_topmost_article(self, stock_name):
        """
        Retrieves the topmost article about the stock.
        :param stock_name:   stock name.
        :return:             a StockArticle object.
        """
        if stock_name in self.db:
            return self.db[stock_name]
        return self.retrieve_topmost_article_new(stock_name)

    def retrieve_topmost_article_new(self, stock_name):
        """
        Retrieves the topmost article about the stock, but solely through the usage of the webhose API. This
        does not involve checking the database for an already existing article for the stock.
        :param stock_name:   stock name.
        :return:             a StockArticle object.
        """
        webhoseio.config(token=webhose_api_key)
        filters = {'language': 'english', 'text': stock_name, 'site_type': 'news', 'site_category': 'finance', 'thread.title': stock_name}
        query_result = webhoseio.query('filterWebContent', filters)
        stock_posts = query_result['posts']
        if len(stock_posts) == 0:
            return None
        article_url = stock_posts[0].get('url')
        article_text = stock_posts[0].get('text')
        article_summary = self.summarize_article(article_text)

        return StockArticle(stock_name, article_url, article_summary)

    def add_article_to_db(self, stock_article):
        """
        Adds a stock article into the database.
        :param stock_article: stock article to be added.
        """
        self.db[stock_article.stock_name] = stock_article

    def summarize_article(self, article_text):
        """
        Summarizes an article using the SMMRY API.
        :param article_text: text of article to summarize.
        :return:            text of the summarized article.
        """

        url = "http://api.smmry.com/"

        querystring = {"SM_API_KEY":"B6AA6865EE","SM_LENGTH":"2"}

        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"sm_api_input\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--".format(article_text)
        #payload = payload.encode('utf-8', 'ignore').decode('utf-8', 'ignore')

        payload = str.encode(payload, 'utf-8', 'ignore')

        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'sm_api_key': "B6AA6865EE",
            'sm_length': "2",
            'cache-control': "no-cache",
            'postman-token': "14691712-dada-24a5-06df-15e2bdfb2df6"
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

        print(response.text)

        return response.text

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
