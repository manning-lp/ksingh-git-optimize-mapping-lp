"""
importer module
Responsible for the index lifecycle of the sneakers index and importing the shoes into Elasticsearch. It uses the
search module to do the communication with the Elasticsearch library.
"""
from search import get_elasticsearch_health, create_elasticsearch_index, index_shoe, switch_alias_to
from bs4 import BeautifulSoup

import json
import logging


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
    _do_import_shoes_from_file(file_name=file_name, index_name=index_name)
    switch_alias_to(index_name)


def _do_import_shoes_from_file(file_name, index_name):
    """
    Use the index_shoe function of the search module to index
    :param file_name: The name of the file to import shoes from.
    :return:
    """
    logging.info(f'Start importing shoes from the file: {file_name} into index {index_name}')
    lines = _read_file_line_by_line(file_name)
    for line in lines:
        line_obj = json.loads(line)
        if line_obj["description"]:
            line_obj["description"] = _clean_html(line_obj["description"])
        if line_obj["id"]:
            logging.info(line_obj)
            index_shoe(shoe=line_obj, index_name=index_name)


def _read_file_line_by_line(file_name):
    """
    Read a file line by line.
    :param file_name: The name of the file.
    :return: The file contents.
    """
    with open(file_name, 'r') as file:
        return file.readlines()


def _clean_html(raw_html):
    """
    Removes all HTML tags from the provided text and returned the cleaned text
    :param raw_html: String containing the text to be cleaned
    :return: The cleaned string
    """
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text()
