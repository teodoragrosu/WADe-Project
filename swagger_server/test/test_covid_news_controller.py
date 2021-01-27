# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.news import News  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCovidNewsController(BaseTestCase):
    """CovidNewsController integration test stubs"""

    def test_news_filter_country_code_get(self):
        """Test case for news_filter_country_code_get

        Filter news by country
        """
        query_string = [('offset', 0),
                        ('limit', 20),
                        ('_from', '2013-10-20'),
                        ('to', '2013-10-20'),
                        ('keywords', 'keywords_example')]
        response = self.client.open(
            '/v1/news/filter/{countryCode}'.format(country_code='country_code_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_news_latest_get(self):
        """Test case for news_latest_get

        Latest news related to the COVID disease
        """
        query_string = [('offset', 0),
                        ('limit', 20)]
        response = self.client.open(
            '/v1/news/latest',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_news_news_id_delete(self):
        """Test case for news_news_id_delete

        Remove news
        """
        response = self.client.open(
            '/v1/news/{news_id}'.format(news_id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
