# coding: utf-8
from . import redis_connection_pool
import redis

r = redis.Redis(connection_pool=redis_connection_pool)


class PopupMessage(object):
    @classmethod
    def register(cls, url, message):
        r.lpush(url, message)

    @classmethod
    def get_message_for_url(cls, url):
        return r.lpop(url)
