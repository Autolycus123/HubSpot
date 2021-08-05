import hashlib

import bcrypt
from numpy import random


class UserAdapter:

    @staticmethod
    def to_json(results):
        return [{
            'id': str(user.id),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'active': user.active,
            'session_id': user.session_id,
            'created_ts': user.id.generation_time.strftime('%Y-%m-%d %H:%M:%S')
        } for user in results]

    def to_object(self, body):
        for key, value in body.items():
            if key == 'password':
                password, salt = self.generate_password(value)
                self.password = password
                self.salt = salt
            else:
                if hasattr(self, key):
                    setattr(self, key, value)

    @staticmethod
    def generate_password(password, salt=None):
        if not salt:
            salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password.decode('utf-8'), salt.decode('utf-8')

    @staticmethod
    def generate_session():
        return hashlib.sha256(random.bytes(1024)).hexdigest()
