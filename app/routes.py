from app import app
import json
from flask import request, redirect, session, url_for
from hubspot_api import hubspot_api
from hubspot_api.deals import get_deals, create_deals


@app.route('/deals')
def deals():
    deals_list = get_deals()
    return {i: deals_list[i] for i in range(len(deals_list))}


@app.route('/deals/create')
def deals_create():
    create_deals()
    return "Created"


@app.route('/')
def index():
    code = request.args.get('code')
    if code is None and session.get('code') is None:
        return hubspot_api.get_auth_token()
    session['code'] = code
    return redirect(url_for('deals'))
