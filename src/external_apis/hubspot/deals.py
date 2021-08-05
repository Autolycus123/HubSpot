import logging
import urllib

import requests

from src.exceptions import HubSpotAuthTokenExpired, HubSpotAPIException
from src.models.hubspot_tokens import HubSpotTokens

LOG = logging.getLogger(__name__)


def get_deals(max_results: int = 500, limit: int = 10):
    tokens = HubSpotTokens.get()
    if tokens is None:
        raise HubSpotAPIException("Failed to get the HubSpot Deals. No acccess tokens!", status=500)
    tokens = tokens[0]
    deal_list = []
    get_all_deals_url = "https://api.hubapi.com/deals/v1/deal/paged?"
    parameter_dict = {'limit': limit}
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    has_more = True
    while has_more:
        parameters = urllib.parse.urlencode(parameter_dict)
        get_url = get_all_deals_url + parameters
        print(f"Performing request to URL: {get_url}")
        r = requests.get(url=get_url, headers=headers)
        response_dict = r.json()
        print(f"Request response-> {r.status_code}:{r.json()}")
        if r.status_code != requests.codes.ok:
            if r.status_code == requests.codes.unauthorized and response_dict.get('category',
                                                                                  '') == 'EXPIRED_AUTHENTICATION':
                raise HubSpotAuthTokenExpired(f"Auth token expired: {r.json()}:{r.status_code}")
            print(f"Failed to get the deals: {r.json()}:{r.status_code}")
            raise HubSpotAPIException(f"Failed to get the HubSpot deals!", status=500)
        has_more = response_dict.get('hasMore', False)
        deal_list.extend(response_dict.get('deals', []))
        parameter_dict['offset'] = response_dict['offset']
        if len(deal_list) >= max_results:
            print(f"Maximum number of results exceeded ({max_results})")
            break
    return deal_list
