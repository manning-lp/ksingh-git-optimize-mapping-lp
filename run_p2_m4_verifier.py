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
    body = {"analyzer": analyzer, "text": analyze_text}
    found_tokens = _do_call_analyze_endpoint(url, body, step)
    if found_tokens != expected_tokens:
        print(f'Step {step}: ERROR the output of analyzer {analyzer} is not as expected {found_tokens} - {expected_tokens}')
    else:
        print(f'Step {step}: OK')


def _do_call_analyze_endpoint(url, body, step):
    headers = {"Content-Type": "application/json; charset=utf-8"}

    r = requests.post(url=url, headers=headers, data=json.dumps(body))
    data = r.json()
    if r.status_code != 200:
        print(f'Step {step}: ERROR {data["error"]["reason"]}')
        return

    found_tokens = []
    for token in data["tokens"]:
        found_tokens.append(token["token"])

    return found_tokens

if __name__ == '__main__':
    print('Started analyzer verifier for Project 2 Milestone 4')
    print('After changing the mapping in config/shoes_index.json execute the run_importer.py script')
    HOST = os.environ.get('ELASTICSEARCH_HOST', 'http://localhost:9200')
    elasticsearch_url = HOST + "/sneakers/_analyze"

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="search_analyzer",
                               analyze_text="baby",
                               expected_tokens=["toddler", "babi"],
                               step="2")

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="search_analyzer_short",
                               analyze_text="snaeker",
                               expected_tokens=["sneaker"],
                               step="4")

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="search_analyzer_name",
                               analyze_text="snaeker",
                               expected_tokens=["sneaker"],
                               step="6")

    print('Finished analyzer verifier')
