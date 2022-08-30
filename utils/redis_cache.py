import redis
import logging
from django.conf import settings
logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()

redis_client = redis.Redis(**settings.REDIS_CONFIG)


class Redis:
    def getter(self, key):
        """
        This function get the data of key from redis server
        """
        try:
            return redis_client.get(key)
        except Exception as ex:
            logger.exception(ex)
            raise Exception("Unable to get data from redis server")

    def setter(self, key, value):
        """
        This function set the key value pair to the redis server
        """
        try:
            return redis_client.set(key, value)
        except Exception as ex:
            logger.exception(ex)
            raise Exception("Unable to set data to redis server")
