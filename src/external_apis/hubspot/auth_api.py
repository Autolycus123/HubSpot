from flask import session, redirect

from src.exceptions import HubSpotAPIException

HUBSPOT_OAUTH_TOKENS_URL = "https://api.hubapi.com/oauth/v1/token"
HUBSPOT_OAUTH_AUTHORIZE_URL = "https://app.hubspot.com/oauth/authorize"
HUBSPOT_REQUEST_HEADERS = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}


def get_tokens() -> dict:
    from src import app
    headers = HUBSPOT_REQUEST_HEADERS
    resp = requests.post(url=HUBSPOT_OAUTH_TOKENS_URL,
                         data=f"grant_type=authorization_code&client_id={app.config.get('CLIENT_ID')}&client_secret="
                              f"{app.config.get('CLIENT_SECRET')}&redirect_uri=http://localhost:5000/&code="
                              f"{session['code']}",
                         headers=headers)
    resp_json = resp.json()
    if resp.status_code != requests.codes.ok:
        print(resp.text)
        print(resp.status_code)
        raise HubSpotAPIException("Failed to obtain access token", status=500)
    return {"access_token": resp_json['access_token'],
            "refresh_token": resp_json['refresh_token']}


def get_auth_token():
    from src import app
    return redirect(f"{HUBSPOT_OAUTH_AUTHORIZE_URL}?client_id={app.config.get('CLIENT_ID')}"
                    f"&scope=contacts%20automation&redirect_uri=http://localhost:5000/")


def refresh_auth_token(refresh_token) -> dict:
    from src import app
    headers = HUBSPOT_REQUEST_HEADERS
    resp = requests.post(url=HUBSPOT_OAUTH_TOKENS_URL,
                         data=f"grant_type=refresh_token&client_id={app.config.get('CLIENT_ID')}&"
                              f"client_secret={app.config.get('CLIENT_SECRET')}&"
                              f"refresh_token={refresh_token}",
                         headers=headers)

    resp_json = resp.json()
    if resp.status_code != requests.codes.ok:
        raise HubSpotAPIException("Failed to refresh access token", status=500)
    return {"access_token": resp_json['access_token'],
            "refresh_token": resp_json['refresh_token']}


if __name__ == "__main__":
    import requests
    from src.settings import CLIENT_ID

    resp = requests.get(
        f"https://app.hubspot.com/oauth/authorize?client_id="
        f"{CLIENT_ID}&scope=contacts%20automation&redirect_uri=http://localhost:5000/")
    print(resp)
    print(resp.text)
