"""
importer module
Responsible for the index lifecycle of the sneakers index and importing the shoes into Elasticsearch. It uses the
search module to do the communication with the Elasticsearch library.
"""
import logging

from search import get_elasticsearch_health, create_elasticsearch_index, index_shoe_bulk, switch_alias_to

logging = logging.getLogger("importer")


def verify_connection():
    """
    Chekc if we can connect to Elasticsearch.
    :return:
    """
    result = get_elasticsearch_health()
    logging.info(f'Name of Elasticsearch cluster: {result["cluster_name"]}')
    logging.info(f'Status of Elasticsearch cluster: {result["status"]}')
    return result


def import_shoes_from_file(file_name):
    """
    Import shoes from a file containing a shoe on each line. Use the index_shoe function of the search module to index
    :param file_name: The name of the file to import shoes from.
    :return:
    """
    index_name = create_elasticsearch_index()
    _do_import_shoes_from_file_bulk(file_name=file_name, index_name=index_name)
    switch_alias_to(index_name)


def _do_import_shoes_from_file_bulk(file_name, index_name):
    """
    Use the batch index function of the search module to index
    :param file_name: The name of the file to import shoes from.
    :return:
    """
    index_shoe_bulk(index_name=index_name, file_name=file_name)
