import functools
import json
import logging
from datetime import datetime, timedelta

from flask import Response, request, redirect, url_for

from src.exceptions import HubSpotAuthTokenExpired
from src.models.hubspot_tokens import HubSpotTokens
from src.models.user import User

logger = logging.getLogger(__name__)


def hubspot_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        hubspot_tokens = HubSpotTokens.get()
        if hubspot_tokens is None:
            return redirect(url_for('index.index'))
        try:
            return func(*args, **kwargs)
        except HubSpotAuthTokenExpired as e:
            logger.error(e)
            HubSpotTokens.refresh_tokens()
            return func(*args, **kwargs)

    return wrapper


def http_handling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            status = getattr(e, 'status', 500)
            return Response(status=status, response=json.dumps({"error": e.args[0]}))

    return wrapper


def is_authorized(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        user = User.get_by_session_id(session_id)
        if not user:
            return Response(json.dumps({"message": "You are not allowed to access this"}), status=401)
        if user.session_ts - datetime.now() > timedelta(minutes=30):
            user.logout(session_id)
            return Response(json.dumps({"message": "Session expired"}), status=401)
        kwargs["user"] = user
        res = func(*args, **kwargs)
        user.session_ts = datetime.now()
        user.save()
        return res

    return wrapper
