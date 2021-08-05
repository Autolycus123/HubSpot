import json
import logging

import pytest

from src import create_app

LOG = logging.getLogger(__name__)


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_login_inxistent_user_fails(client):
    resp = client.post('/user/login',
                       data=json.dumps({"email": "abc@defgh.ghi", "password": "Test123!"}))
    assert resp.status_code == 401
    assert resp.get_json()
    resp_json = resp.get_json()
    assert "message" in resp_json
