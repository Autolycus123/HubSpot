from mongoengine import DoesNotExist

from extensions import db
from src.adapters.hubspot_tokens import HubSpotTokensAdapter
from src.external_apis.hubspot.auth_api import get_tokens, refresh_auth_token, get_auth_token


class HubSpotTokens(HubSpotTokensAdapter, db.Document):
    access_token = db.StringField(required=True)
    refresh_token = db.StringField(required=True)

    @classmethod
    def init_tokens(cls):
        try:
            db_tokens = HubSpotTokens.objects.get()
        except DoesNotExist:
            db_tokens = HubSpotTokens()
        tokens = get_tokens()
        db_tokens.access_token = tokens["access_token"]
        db_tokens.refresh_token = tokens["refresh_token"]
        db_tokens.save()

    @classmethod
    def get_auth_code(cls):
        return get_auth_token()

    @classmethod
    def refresh_tokens(cls):
        try:
            db_tokens = HubSpotTokens.objects.get()
        except DoesNotExist:
            db_tokens = HubSpotTokens()
        tokens = refresh_auth_token(db_tokens.refresh_token)
        db_tokens.access_token = tokens["access_token"]
        db_tokens.refresh_token = tokens["refresh_token"]
        db_tokens.save()

    @classmethod
    def get(cls):
        try:
            return cls.to_json(HubSpotTokens.objects.get())
        except DoesNotExist:
            pass
