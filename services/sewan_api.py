import requests
import sys
import json

API_URL = "https://api.sewan.fr/sophia/SophiaFramework/jsongateway"
USER_AGENT = 'NCO SERVICES API'
TOKEN_API = '01b1b2952c0a7c55119f6964e03761ccdbcc68f1543e4788c0023e409ff7884d'
PERSON_ID = 0

headers = {
    'Authorization': f'bearer {TOKEN_API}',
    'User-Agent': USER_AGENT,
    'Content-Type': 'application/json',
    'Accept-Language': 'fr_FR'
}

def demo_search():

    print("Search (sophia.service.search.search_unified())... ")

    text_search = "+33604596462"
    url = (
        f"{API_URL}?service=sophia.service.Search&method=search_unified&text={text_search}"
    )
    print(f"    * URL: {url}")

    response_search = requests.get(url, headers=headers, timeout=10)
    print(f"    * HTTP response: {response_search}")

    if response_search.status_code != 200:
        sys.stderr.write(f"  => HTTP error {response_search.status_code} on search.\n")
        sys.stderr.write(f"  => Body {response_search.content}\n")
        sys.exit(2)
    rjson = response_search.json()
    print(f"    * Webservice response: {rjson}")

    code = int(rjson["code"])
    if code < 200 or code >= 300:
        sys.stderr.write(
            f"  => Search failed with code {rjson['code']} : {rjson['msg']}\n"
            "(see Webservice response for more details)\n"
        )
        sys.exit(2)

    results_array = rjson["result_object1"] or []
    results_array_str = [
        f"      * {item['id']} - {item['label']}" for item in results_array
    ]
    results_str = "\n".join(results_array_str)
    print(f"  => Search succeeded. {len(results_array)} item(s) found :\n{results_str}")
