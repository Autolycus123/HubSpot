from datetime import datetime

from mongoengine import DoesNotExist

from extensions import db
from src.adapters.user import UserAdapter
from src.exceptions import InvalidCredentials
from src.utils.validators import validate_user_body


class User(UserAdapter, db.Document):
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    phone = db.StringField(required=False, default=None)
    role = db.StringField(required=True, defaul='REGULAR')
    password = db.StringField(required=True)
    salt = db.StringField(required=True)
    session_id = db.StringField(required=False, default=None)
    session_ts = db.DateTimeField(required=False, default=None)
    active = db.BooleanField(required=True, default=False)

    @classmethod
    def login(cls, body):
        user = cls.get_by_email(body.get("email"))
        if not user:
            raise InvalidCredentials("Invalid credentials", status=401)
        password, _ = cls.generate_password(body.get("password"), user.salt.encode('utf-8'))
        if password != user.password:
            raise InvalidCredentials("Invalid credentials", status=401)
        session_id = cls.generate_session()
        user.session_id = session_id
        user.session_ts = datetime.utcnow()
        user.save()
        return session_id

    @classmethod
    def logout(cls, session_id):
        user = cls.get_by_session_id(session_id)
        if not user:
            raise InvalidCredentials("User not found", status=400)
        user.session = None
        user.save()

    @classmethod
    def get_all(cls, filter_dict):
        return cls.to_json(User.objects(**filter_dict))

    @classmethod
    def get_by_email(cls, email):
        return User.objects.get(email=email)

    @classmethod
    def get_by_session_id(cls, session_id):
        if session_id is None:
            return
        try:
            return User.objects.get(session_id=session_id)
        except DoesNotExist:
            pass

    @classmethod
    def create(cls, body):
        validate_user_body(body)
        user = User()
        user.to_object(body)
        user.save()
        return cls.to_json(user)
