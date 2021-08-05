import re

from src.exceptions import ValidationError


def validate_email(email):
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    res = re.search(email_regex, email)
    if not res:
        raise ValidationError(f'Invalid email address: {email}', status=400)


def validate_name(name):
    if not name:
        raise ValidationError(f"Invalid name: {name}", status=400)


def validate_user_body(body):
    validate_name(body.get('first_name'))
    validate_name(body.get('last_name'))
    validate_email(body["email"])
