from redis import Redis
from redis.commands.json.path import Path


class RedisClient:
    __client: Redis = None

    @classmethod
    def get_client(cls):
        if not cls.__client:
            cls.__client = Redis()
        return cls.__client

    @classmethod
    def set_cache(cls, name: str, obj: dict, expire_time=60 * 5):
        client = cls.get_client()
        client.json().set(name, Path.root_path(), obj)
        client.expire(name, expire_time, nx=True)

    @classmethod
    def get_cache(cls, name: str):
        client = cls.get_client()
        return client.json().get(name)

    @classmethod
    def del_cache_name(cls, name: str):
        client = cls.get_client()
        client.json().delete(name, Path.root_path())

    @classmethod
    def del_cache_pattern(cls, pattern: str):
        client = cls.get_client()
        names = client.scan_iter(pattern)
        for name in names:
            client.json().delete(name, Path.root_path())

    @classmethod
    def unlink_cache_name(cls, name: str):
        client = cls.get_client()
        client.unlink(name)

    @classmethod
    def unlink_cache_pattern(cls, pattern: str):
        client = cls.get_client()
        names = client.scan_iter(pattern)
        for name in names:
            client.unlink(name)
