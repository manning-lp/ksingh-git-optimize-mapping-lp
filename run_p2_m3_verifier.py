import json

import requests
import os


def verify_tokens_from_field(url, field, analyze_text, expected_tokens, step):
    """
    Calls the Elasticsearch analyze endpoint on the sneakers alias
    :param url: The host of Elasticsearch including the analyze endpoint
    :param field: The field to call with the provided text
    :param analyze_text: The text to sent to the analyzer endpoint
    :param expected_tokens: Tokens the analyzer should return
    :param step: Only used for the message
    """
    body = {"field": field, "text": analyze_text}
    found_tokens = _do_call_analyze_endpoint(url, body, step)
    if found_tokens != expected_tokens:
        print(f'Step {step}: ERROR the output of field {field} is not as expected {found_tokens} - {expected_tokens}')
    else:
        print(f'Step {step}: OK')


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
    print('Started analyzer verifier for Project 2 Milestone 3')
    print('After changing the mapping in config/shoes_index.json execute the run_importer.py script')
    HOST = os.environ.get('ELASTICSEARCH_HOST', 'http://localhost:9200')
    elasticsearch_url = HOST + "/sneakers/_analyze"

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="searchable_field",
                               analyze_text="toddler shoes",
                               expected_tokens=["toddler", "shoe"],
                               step="1a")

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="searchable_field",
                               analyze_text="toddlers' shoes",
                               expected_tokens=["toddler", "shoe"],
                               step="1b")

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="searchable_field",
                               analyze_text="toddlers shoes",
                               expected_tokens=["toddler", "shoe"],
                               step="1c")

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="searchable_field",
                               analyze_text="vibes",
                               expected_tokens=["vibe"],
                               step="1d")

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="searchable_field",
                               analyze_text="Adidas",
                               expected_tokens=["adidas"],
                               step="1e")

    verify_tokens_from_analyze(url=elasticsearch_url,
                               analyzer="searchable_short_field",
                               analyze_text="Flowerbombprint",
                               expected_tokens=["fl","flo","flow","flow","flower","flowerb","flowerbo",
                                                "flowerbom","flowerbomb","flowerbombprint"],
                               step="2")

    verify_tokens_from_field(url=elasticsearch_url,
                               field="base_material.searchable",
                               analyze_text="Flowerbombprint",
                               expected_tokens=["fl","flo","flow","flow","flower","flowerb","flowerbo",
                                                "flowerbom","flowerbomb","flowerbombprint"],
                               step="3a")

    verify_tokens_from_field(url=elasticsearch_url,
                               field="product_type.searchable",
                               analyze_text="Flowerbombprint",
                               expected_tokens=["fl","flo","flow","flow","flower","flowerb","flowerbo",
                                                "flowerbom","flowerbomb","flowerbombprint"],
                               step="3b")

    verify_tokens_from_field(url=elasticsearch_url,
                               field="sport.searchable",
                               analyze_text="Flowerbombprint",
                               expected_tokens=["fl","flo","flow","flow","flower","flowerb","flowerbo",
                                                "flowerbom","flowerbomb","flowerbombprint"],
                               step="3c")

    verify_tokens_from_field(url=elasticsearch_url,
                               field="usps",
                               analyze_text="Flowerbombprint",
                               expected_tokens=["fl","flo","flow","flow","flower","flowerb","flowerbo",
                                                "flowerbom","flowerbomb","flowerbombprint"],
                               step="3d")

    verify_tokens_from_field(url=elasticsearch_url,
                               field="color",
                               analyze_text="Flowerbombprint / Core Black",
                               expected_tokens=["fl","flo","flow","flow","flower","flowerb","flowerbo",
                                                "flowerbom","flowerbomb","flowerbombprint", "co", "cor", "core",
                                                "core ", "core b", "core bl", "core bla", "core blac", "core black"],
                               step="4a")

    verify_tokens_from_field(url=elasticsearch_url,
                               field="name",
                               analyze_text="Flowerbombprint",
                               expected_tokens=["fl","flo","flow","flow","flower","flowerb","flowerbo",
                                                "flowerbom","flowerbomb","flowerbombprint"],
                               step="4b")

    print('Finished analyzer verifier')
