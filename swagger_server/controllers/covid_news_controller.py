import connexion
import six

from swagger_server.models.news import News  # noqa: E501
from swagger_server import util


def api_news_filter_publication_get(publication, offset=None, limit=None):  # noqa: E501
    """Filter news by publication source

    ### Filter the news related to the COVID disease, based on the source.  # noqa: E501

    :param publication: publication source to filter by
    :type publication: str
    :param offset: ### The number of items to skip before starting to collect the result set
    :type offset: int
    :param limit: ### The numbers of items to return
    :type limit: int

    :rtype: List[News]
    """
    return 'do some magic!'


def api_news_latest_get(offset=None, limit=None):  # noqa: E501
    """Latest news related to the COVID disease

    ### Get the latest news related to COVID-19 worldwide. If no limit is specified, the newest 20 news will be returned  # noqa: E501

    :param offset: ### The number of items to skip before starting to collect the result set
    :type offset: int
    :param limit: ### The numbers of items to return
    :type limit: int

    :rtype: List[News]
    """
    return 'do some magic!'
