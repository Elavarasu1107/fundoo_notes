import logging
import jwt
from django.conf import settings

logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


class JWT:
    @staticmethod
    def encode(payload, exp=None):
        """
        This method return encoded token for user data
        """
        try:
            if not isinstance(payload, dict):
                raise Exception("Payload should be in dict")
            payload.update(exp=settings.JWT_EXP)
            if exp:
                payload.update({'exp': exp})
            return jwt.encode(payload, "secret", algorithm="HS256")
        except Exception as ex:
            logger.exception(ex)

    @staticmethod
    def decode(token):
        """
        This method return decoded data from the token
        """
        try:
            return jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            raise Exception("Token Expired")
        except jwt.exceptions.InvalidTokenError:
            raise Exception("Invalid Token")
        except Exception as ex:
            logger.exception(ex)


def verify_token(function):
    def wrapper(self, request):
        token = request.headers.get('token')
        if not token:
            raise Exception("Auth token required")
        decode = JWT.decode(token=token)
        user_id = decode.get('user_id')
        if not user_id:
            raise Exception("User not found")
        request.data.update({"user": user_id})
        return function(self, request)
    return wrapper
