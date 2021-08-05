import json

from flask import Response, Blueprint

from src.models.deal import Deal
from src.utils.decorators import http_handling, hubspot_session

deal_bp = Blueprint('deals', __name__, template_folder='templates', url_prefix='/deals')


# @is_authorized
@deal_bp.route('/', methods=['GET'])
@hubspot_session
@http_handling
def get_deals():
    deals = Deal.get_all()
    return Response(response=json.dumps(deals), status=200)
