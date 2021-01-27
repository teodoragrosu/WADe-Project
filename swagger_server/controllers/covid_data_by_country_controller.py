import connexion
import six

from swagger_server.models.cases import Cases  # noqa: E501
from swagger_server.models.country import Country  # noqa: E501
from swagger_server import util


def api_countries_get():  # noqa: E501
    """Returns all countries available

    ## Get a list of all countries and their URIs  # noqa: E501


    :rtype: List[Country]
    """
    return 'do some magic!'


def api_country_country_code_download_get(country_code, format, _from=None, to=None):  # noqa: E501
    """Download the cases data for a specified country, in a chosen format

     # noqa: E501

    :param country_code: ### ISO(alpha-2) country code to return the information for
    :type country_code: str
    :param format: ### File format for the download
    :type format: str
    :param _from: ### Filter cases in a specific range, starting \&quot;from\&quot; (ISO format)
    :type _from: str
    :param to: ### Filter cases in a specific range, until \&quot;to\&quot; (ISO format)
    :type to: str

    :rtype: None
    """
    return 'do some magic!'


def api_country_country_code_get(country_code, _date=None, _from=None, to=None):  # noqa: E501
    """Returns all the cases recorded for the specified country

    ### Returns all information related to the cases in the specified country from the first day recorded to the current day.  ### A specific day or a date range can be specified in the query parameters.  # noqa: E501

    :param country_code: ### ISO(alpha-2) country code to return the information for
    :type country_code: str
    :param _date: ### filter cases for a specific day (ISO format)
    :type _date: str
    :param _from: ### filter cases in a specific range, starting &lt;from&gt; (ISO format)
    :type _from: str
    :param to: ### filter cases in a specific range, until &lt;to&gt; (ISO format)
    :type to: str

    :rtype: List[Cases]
    """
    return 'do some magic!'


def api_country_country_code_latest_get(country_code):  # noqa: E501
    """Returns the latest recorded cases for the specified country

     # noqa: E501

    :param country_code: ### ISO(alpha-2) country code to return the information for
    :type country_code: str

    :rtype: List[Cases]
    """
    return 'do some magic!'


def api_country_monthly_country_code_get(country_code):  # noqa: E501
    """Returns the average number of cases per day for each month

     # noqa: E501

    :param country_code: ### ISO(alpha-2) country code to return the information for
    :type country_code: str

    :rtype: List[Cases]
    """
    return 'do some magic!'