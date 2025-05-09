import requests
import sys
import json

API_URL = "https://api.sewan.fr/sophia/SophiaFramework/jsongateway"
USER_AGENT = 'NCO SERVICES API'
TOKEN_API = '01b1b2952c0a7c55119f6964e03761ccdbcc68f1543e4788c0023e409ff7884d'
PERSON_ID = 95848

PERSON_TYPE_RESELLER = 2
PERSON_TYPE_CUSTOMER = 3

headers = {
    'Authorization': f'bearer {TOKEN_API}',
    'User-Agent': USER_AGENT,
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


def demo_get_all_customers():
    """
    Demo Get all reseller/customers (using POST http method)
    """
    print(
        "Get all customers/resellers "
        "(sophia.service.PersonManagement.get_all_persons()) "
    )

    vo_person_filter = {
        "sophia_class_name": "VOPersonFilter",
        "direct_sub_person_of_per_id": PERSON_ID,
        "per_type_in": [PERSON_TYPE_RESELLER, PERSON_TYPE_CUSTOMER],
    }
    post_data = {
        "service": "sophia.service.PersonManagement",
        "method": "get_all_persons",
        "vo_person_filter": json.dumps(vo_person_filter),
        "simple_mode": True,  # search all
        "use_pagination": True,
    }
    print(f"  * URL: {API_URL}")
    print(f"  * post parameters: {post_data}")
    response_get_all_person = requests.post(
        url=API_URL, data=post_data, headers=headers, timeout=10
    )

    print(f"  * HTTP response: {response_get_all_person}")
    if response_get_all_person.status_code != 200:
        sys.stderr.write(
            f"  => HTTP error {response_get_all_person.status_code} "
            "on getting all persons\n"
        )
        sys.stderr.write(f"  => Body {response_get_all_person.content}\n")
        sys.exit(2)
    rjson = response_get_all_person.json()
    print(f"  * Webservice response: {rjson}")

    # Check the result code
    code = int(rjson["code"])
    if code < 200 or code >= 300:
        # Search failed
        sys.stderr.write(
            f"  => Webservice failed with code {rjson['code']} : {rjson['msg']}\n"
            "(see Webservice response for more details)\n"
        )
        sys.exit(2)

    # Get all succeeded
    pager = rjson["result_object2"]
    first_results_array = rjson["result_object1"]
    first_results_array_str = [
        f"      * {item['per_id']} - {item['per_login']}"
        for item in first_results_array
    ]
    first_results_str = "\n".join(first_results_array_str)
    result_count = len(first_results_array)
    total_result_count = pager["total_count"]
    print(f"  => Get all succeeded. {total_result_count} item(s) found.")
    print(f"  => First {result_count} results are: \n{first_results_str}")
