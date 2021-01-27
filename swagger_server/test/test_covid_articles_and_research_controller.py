# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.articles import Articles  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCovidArticlesAndResearchController(BaseTestCase):
    """CovidArticlesAndResearchController integration test stubs"""

    def test_articles_article_id_delete(self):
        """Test case for articles_article_id_delete

        Remove articles
        """
        response = self.client.open(
            '/v1/articles/{article_id}'.format(article_id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_articles_find_by_type_get(self):
        """Test case for articles_find_by_type_get

        Find articles by type
        """
        query_string = [('offset', 0),
                        ('limit', 20),
                        ('type', 'type_example')]
        response = self.client.open(
            '/v1/articles/findByType',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_articles_latest_get(self):
        """Test case for articles_latest_get

        Latest articles and research related to the COVID disease
        """
        query_string = [('offset', 0),
                        ('limit', 20)]
        response = self.client.open(
            '/v1/articles/latest',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
