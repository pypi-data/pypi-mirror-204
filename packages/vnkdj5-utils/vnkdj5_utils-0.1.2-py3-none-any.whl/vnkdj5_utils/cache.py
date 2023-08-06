import redis
import redis

class Cache:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = redis.Redis(host='localhost', port=6379, db=0)
        return cls.__instance