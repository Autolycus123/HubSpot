import json

from flask import Response, request, Blueprint, session

from src.models.hubspot_tokens import HubSpotTokens
from src.utils.decorators import http_handling

index_bp = Blueprint('index', __name__, template_folder='templates', url_prefix='/')


@index_bp.route('', methods=['GET', 'POST'])
@http_handling
def index(*args, **kwargs):
    code = request.args.get('code')
    if code is None and session.get('code') is None:
        return HubSpotTokens.get_auth_code()
    session["code"] = code
    tokens = HubSpotTokens.get()
    HubSpotTokens.refresh_tokens()
    return Response(json.dumps({"message": "Auth complete! Please navigate to /deals!"}), status=200)
