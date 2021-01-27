# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.cases import Cases  # noqa: E501
from swagger_server.models.country import Country  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCovidDataByCountryController(BaseTestCase):
    """CovidDataByCountryController integration test stubs"""

    def test_countries_country_code_cases_range_get(self):
        """Test case for countries_country_code_cases_range_get

        Returns cases in the specified country for a specific date range
        """
        query_string = [('_from', '2013-10-20'),
                        ('to', '2013-10-20'),
                        ('filter_new_confirmed', false),
                        ('filter_new_deceased', false),
                        ('filter_new_recovered', false),
                        ('filter_new_tested', false),
                        ('filter_total_confirmed', false),
                        ('filter_total_deceased', false),
                        ('filter_total_recovered', false),
                        ('filter_total_tested', false)]
        response = self.client.open(
            '/v1/countries/{countryCode}/cases/range'.format(country_code='country_code_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_countries_country_code_date_get(self):
        """Test case for countries_country_code_date_get

        Returns the cases in a specific day for the specified country
        """
        query_string = [('filter_new_confirmed', false),
                        ('filter_new_deceased', false),
                        ('filter_new_recovered', false),
                        ('filter_new_tested', false),
                        ('filter_total_confirmed', false),
                        ('filter_total_deceased', false),
                        ('filter_total_recovered', false),
                        ('filter_total_tested', false)]
        response = self.client.open(
            '/v1/countries/{countryCode}/{date}'.format(country_code='country_code_example', _date='2013-10-20'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_countries_country_code_download_get(self):
        """Test case for countries_country_code_download_get

        Download data for a specified country
        """
        query_string = [('format', 'json'),
                        ('_from', '2013-10-20'),
                        ('to', '2013-10-20')]
        response = self.client.open(
            '/v1/countries/{countryCode}/download'.format(country_code='country_code_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_countries_country_code_download_head(self):
        """Test case for countries_country_code_download_head

        Check the data to be downloaded
        """
        query_string = [('format', 'json'),
                        ('_from', '2013-10-20'),
                        ('to', '2013-10-20')]
        response = self.client.open(
            '/v1/countries/{countryCode}/download'.format(country_code='country_code_example'),
            method='HEAD',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_countries_country_code_latest_get(self):
        """Test case for countries_country_code_latest_get

        Returns the lastest info for the specified country
        """
        query_string = [('filter_new_confirmed', false),
                        ('filter_new_deceased', false),
                        ('filter_new_recovered', false),
                        ('filter_new_tested', false),
                        ('filter_total_confirmed', false),
                        ('filter_total_deceased', false),
                        ('filter_total_recovered', false),
                        ('filter_total_tested', false)]
        response = self.client.open(
            '/v1/countries/{countryCode}/latest'.format(country_code='country_code_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_countries_get(self):
        """Test case for countries_get

        Returns all countries available
        """
        response = self.client.open(
            '/v1/countries',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
