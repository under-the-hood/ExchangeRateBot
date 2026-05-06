import requests

def get_exchange_rate(url: str, currency: str):

    query_params = {
        'text': currency
    }
    
    resp = requests.get(url, params=query_params)

    if resp.status_code != 200:
        print('The request failed with an error', resp.text) 

    all_data = resp.json()
    target_currency = all_data["usd"][currency]

    return target_currency