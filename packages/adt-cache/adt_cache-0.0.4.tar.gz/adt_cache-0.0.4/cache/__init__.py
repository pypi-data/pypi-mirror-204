import logging
from abc import abstractmethod, ABCMeta
from typing import List
import redis

logger = logging.getLogger("adt_cache")

class AdtCache(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def intersect(self, key: str, vals: List):
        pass

    @abstractmethod
    def differential(self, key: str, vals: List):
        pass

    @abstractmethod
    def push_values(self, key: str, vals: List):
        pass

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def push(self, key: str, val):
        pass


class RedisCache(AdtCache):
    def __init__(self, host: str, port, db, expire_mins=60*24, clear_cache=False):
        logger.info(f"init redis cache with {host}:{port}:{db}")
        super().__init__()
        self.redis = redis.Redis(host=host, port=port, db=db)
        self.expire_mins=expire_mins
        if clear_cache:
            self.redis.flushdb()

    def intersect(self, key, vals: List):
        return [val for val in vals if self.redis.sismember(key, val)]

    def differential(self, key, vals: List):
        return [val for val in vals if not self.redis.sismember(key, val)]

    def push_values(self, key, vals: List):
        self.redis.expire(key, 60 * self.expire_mins)
        return self.redis.sadd(key, *set(vals))

    def keys(self):
        return self.redis.keys()

    def get(self, key: str):
        return self.redis.get(key)

    def push(self, key: str, val):
        self.redis.expire(key, 60 * self.expire_mins)
        return self.redis.append(str, val)

class MemoryCache(AdtCache):
    def __init__(self):
        super().__init__()
        self.cache = {}

    def intersect(self, key, vals: List):
        return [val for val in vals if val in self.cache.get(key, [])]

    def differential(self, key, vals: List):
        return [val for val in vals if val not in self.cache.get(key, [])]

    def push_values(self, key, vals: List):
        c = self.cache.get(key)
        if c is None:
            self.cache[key] = set(vals)
        else:
            c.update(vals)

    def keys(self):
        return self.cache.keys()

    def get(self, key: str):
        return self.cache.get(str)

    def push(self, key: str, val):
        self.cache[key] = val
