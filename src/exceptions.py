class CustomException(Exception):
    def __init__(self, *args, **kwargs):
        self.status = kwargs["status"]
        del kwargs["status"]
        # noinspection PyArgumentList
        super().__init__(*args, **kwargs)


class HubSpotAuthTokenExpired(CustomException):
    pass


class Unauthorized(CustomException):
    pass


class InvalidCredentials(CustomException):
    pass


class ValidationError(CustomException):
    pass


class HubSpotAPIException(CustomException):
    pass


class ResourceNotFound(CustomException):
    pass
