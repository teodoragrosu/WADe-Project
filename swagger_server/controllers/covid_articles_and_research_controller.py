import connexion
import six

from swagger_server.models.articles import Articles  # noqa: E501
from swagger_server import util


def api_articles_filter_type_get(type, offset=None, limit=None):  # noqa: E501
    """Latest articles and research related to the COVID disease

    ### Filter research articles by their type. If no limit is specified, the newest 20 articles will be returned  # noqa: E501

    :param type: ### Allowed article types: article, research, journal contribution
    :type type: str
    :param offset: ### The number of items to skip before starting to collect the result set
    :type offset: int
    :param limit: ### The numbers of items to return
    :type limit: int

    :rtype: List[Articles]
    """
    return 'do some magic!'


def api_articles_latest_get(offset=None, limit=None):  # noqa: E501
    """Latest articles and research related to the COVID disease

    ### Get the latest research articles related to COVID-19. If no limit is specified, the newest 20 articles will be returned  # noqa: E501

    :param offset: ### The number of items to skip before starting to collect the result set
    :type offset: int
    :param limit: ### The numbers of items to return
    :type limit: int

    :rtype: List[Articles]
    """
    return 'do some magic!'
