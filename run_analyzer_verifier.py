"""run_analyzer_verifier.py
Verifies your analyzer body as requested in step 3. Change the content of analyzer_body.json, to check your code
"""
import requests
import os

# Original text: adidas by <strong>Stella McCartney</strong> Ultra-boost 21 Shoes
# rules contains the tokens that need to be returned or not
rules = {
    "adidas": True,
    "by": False,
    "strong": False,
    "stella": True,
    "Stella": False,
    "mccartney": True,
    "mc": True,
    "cartney": True,
    "ultra": True,
    "boost": True,
    "ultra-boost": True,
    "Shoes": False,
    "shoes": True
}


def load_analyze_body_from_file(file_name):
    """
    Load the body to post to analyze endpoint from a file.
    :param file_name: The name of the file.
    :return: The index body.
    """
    with open(file_name, 'r') as file:
        return file.read()


def verify_rules(tokens, rules_to_verify):
    """
    Accepts a dictionary with rules. The key is a token, the value is a boolean indicating if the token
    should be in the response.
    :param tokens: List of tokens that should be checked for correctness
    :param rules_to_verify: Dictionary with tokens and if they should be included or not
    """
    verified_ok = True
    for rule_key in rules_to_verify:
        if (rule_key in tokens) is not rules_to_verify[rule_key]:
            print(f'Token in error: {rule_key}')
            verified_ok = False

    if verified_ok:
        print("Congratulations, your solution is correct.")
    else:
        print("Great, you have an opportunity to learn, the answer is not as expected.")


def get_tokens_from_analyze(url, body):
    """
    Calls the Elasticsearch analyze endpoint with the provided body, the body should include the text
    :param url: The host of Elasticsearch including the analyze endpoint
    :param body: The body to sent to the analyzer endpoint
    :return: A list with the found tokens
    """
    headers = {"Content-Type": "application/json; charset=utf-8"}
    r = requests.post(url=url, headers=headers, data=body)
    data = r.json()
    if r.status_code != 200:
        print(f'ERROR: {data["error"]["reason"]}')
        SystemExit()

    found_tokens = []
    for token in data["tokens"]:
        found_tokens.append(token["token"])

    return found_tokens


if __name__ == '__main__':
    print('Started analyzer verifier')
    HOST = os.environ.get('ELASTICSEARCH_HOST', 'http://localhost:9200')
    elasticsearch_url = HOST + "/_analyze"
    analyzer_body_file_name = "analyzer_body.json"
    analyzer_tokens = get_tokens_from_analyze(url=elasticsearch_url,
                                              body=load_analyze_body_from_file(analyzer_body_file_name))

    verify_rules(tokens=analyzer_tokens, rules_to_verify=rules)

    print('Finished analyzer verifier')
