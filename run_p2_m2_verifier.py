import json

import requests
import os


def verify_tokens_from_analyze(url, analyzer, analyze_text, expected_tokens, step):
    """
    Calls the Elasticsearch analyze endpoint on the sneakers alias
    :param url: The host of Elasticsearch including the analyze endpoint
    :param analyzer: The analyzer to call with the provided text
    :param analyze_text: The text to sent to the analyzer endpoint
    :param expected_tokens: Tokens the analyzer should return
    :param step: Only used for the message
    """
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if analyzer.startswith('sortable'):
        body = {"normalizer": analyzer, "text": analyze_text}
    else:
        body = {"analyzer": analyzer, "text": analyze_text}

    r = requests.post(url=url, headers=headers, data=json.dumps(body))
    data = r.json()
    if r.status_code != 200:
        print(f'Step {step}: ERROR {data["error"]["reason"]}')
        return

    found_tokens = []
    for token in data["tokens"]:
        found_tokens.append(token["token"])

    if found_tokens != expected_tokens:
        print(f'Step {step}: ERROR the output of analyzer {analyzer} is not as expected {found_tokens} - {expected_tokens}')
    else:
        print(f'Step {step}: OK')


if __name__ == '__main__':
    print('Started analyzer verifier for Project 2 Milestone 2')
    print('After changing the mapping in config/shoes_index.json execute the run_importer.py script')
    HOST = os.environ.get('ELASTICSEARCH_HOST', 'http://localhost:9200')
    elasticsearch_url = HOST + "/sneakers/_analyze"

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="searchable_field",
                               analyze_text="Lace clösure shoes<br/>",
                               expected_tokens=["lace", "closure", "shoes"],
                               step="1")

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="searchable_name_field",
                               analyze_text="Lace clösure Shoes<br/>",
                               expected_tokens=["lace", "closure"],
                               step="2")

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="color_searchable_field",
                               analyze_text="Core Black / Cloud White",
                               expected_tokens=["core black", "cloud white"],
                               step="3")

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="color_facetable_field",
                               analyze_text="Core Black / Cloud White",
                               expected_tokens=["Core Black", "Cloud White"],
                               step="4")

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="sortable_field",
                               analyze_text="Röd stripes",
                               expected_tokens=["rod stripes"],
                               step="5")

    print('Finished analyzer verifier')
