from enum import Enum


class FailureMessages(Enum):
    USER_INACTIVE = 'This user is not active'
    INVALID_CREDENTIALS = 'Wrong username/password'
    INVALID_INPUT = 'Invalid input'
    TECHNICAL_ERROR = 'Error while saving the user'
    EMAIL_ALREADY_EXISTS = 'Email already exists'


class SuccesMessages(Enum):
    USER_LOGGED_OUT = 'User logged out'


class ResponseKeys(Enum):
    SESSION_ID = 'token'
    USER = 'user'


class RequestKeys(Enum):
    PASSWORD = 'password'
    USER = 'user'
    EMAIL = 'email'
