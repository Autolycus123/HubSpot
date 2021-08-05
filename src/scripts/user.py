from pprint import pprint

from src.models.user import User


def create_test_user():
    user_json = {"first_name": "FN",
                 "last_name": "LN",
                 "email": "abc@defgh.ghi",
                 "phone": "1234",
                 "password": "Test123!",
                 "active": True,
                 "role": "REGULAR"}
    return User.create(user_json)


def get_all_users():
    result = User.get_all({})
    pprint(result)
    return result


def get_all(filter_dict):
    result = User.get_all(filter_dict)
    pprint(result)
    return result


def get_by_email(email):
    result = User.get_by_email(email)
    pprint(result)
    return result


if __name__ == "__main__":
    get_all_users()
