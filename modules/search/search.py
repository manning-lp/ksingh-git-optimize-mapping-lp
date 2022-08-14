from elasticsearch import Elasticsearch
from datetime import datetime
import os
import json
import logging

search_log = logging.getLogger("search")

ALIAS_NAME = "sneakers"
HOST = os.environ.get('ELASTICSEARCH_HOST', 'http://localhost:9200')
es = Elasticsearch(hosts=[HOST])


def get_elasticsearch_health():
    """
    Use this endpoint to check if Elasticsearch is available.
    :return:
    """
    health = es.cluster.health()
    search_log.info(f'Cluster health: {health["status"]}')
    return health


def create_elasticsearch_index():
    """
    Create a new index. Name of the index is a combination of the configured ALIAS_NAME and a time stamp in the format
    of YearMonthDayHourMinuteSecond. Before the index is created, we remove it if it already exists. The settings
    and mappings are obtained from the shoes_index.json in the config folder.
    :return: The name of the created index
    """
    index_name = f'{ALIAS_NAME}-{datetime.now().strftime("%Y%m%d%H%M%S")}'
    search_log.info(f'Creating a new index with the name {index_name}')

    body_from_file = _load_index_body_from_file(file_name='./config/shoes_index.json')
    json_body = json.loads(body_from_file)

    es.indices.delete(index=index_name, ignore_unavailable=True)
    es.indices.create(index=index_name, body=json_body)

    search_log.info(f'Created a new index with the name {index_name}')
    return index_name


def index_shoe(shoe, index_name):
    """
    Send the provided shoe to Elasticsearch to index that shoe into the provided index.
    :param shoe: The Shoe to index
    :param index_name: The index to use for indexing the shoe
    :return:
    """
    search_log.info(f'Indexing shoe: {shoe["id"]} into index with name {index_name}')
    es.index(index=index_name, id=shoe["id"], body=shoe)


def switch_alias_to(index_name):
    """
    Checks if the alias as configured is already available, if so, remove all indexes it points to. When finished add
    the provided index to the alias.
    :param index_name: Name of the index to assign to the alias
    :return:
    """
    search_log.info(f'Assign alias {ALIAS_NAME} to {index_name}')
    if es.indices.exists_alias(name=ALIAS_NAME):
        response = es.indices.get_alias(name=ALIAS_NAME)
        for index in response:
            es.indices.delete_alias(name=ALIAS_NAME, index=index)
    es.indices.put_alias(index=index_name, name=ALIAS_NAME)


def _load_index_body_from_file(file_name):
    """
    Load the index body from a file.
    :param file_name: The name of the file.
    :return: The index body.
    """
    with open(file_name, 'r') as file:
        return file.read()
