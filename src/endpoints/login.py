import json

from flask import Response, request, Blueprint

from src.models.user import User
from src.utils.decorators import http_handling

user_bp = Blueprint('user', __name__, template_folder='templates', url_prefix='/user')


@user_bp.route('/login', methods=['POST'])
@http_handling
def login():
    session_id = User.login(request.json)
    response = Response(response=json.dumps({'message': "Successfully logged in"}), status=200)
    response.set_cookie("session_id", session_id)
    return response


@user_bp.route('/logout', methods=['POST'])
@http_handling
def logout():
    session_id = request.cookies.get('session_id')

    User.logout(session_id)
    response = Response(response=json.dumps({'message': "Logged out successfully"}), status=200)
    response.set_cookie("session_id", "")
    return response
