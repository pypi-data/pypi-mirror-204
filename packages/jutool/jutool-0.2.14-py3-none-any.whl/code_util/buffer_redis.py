import time
from functools import wraps
import redis, json
from code_util.log import log_error
from code_util.env import get_config_obj
from code_util.buffer import _get_hash_key_

_redis_instance = None
_redis_buffer_key = "redis_buffer"


def _get_pool():
    global _redis_instance
    if _redis_instance is None:
        config_c = get_config_obj()
        _redis_instance = redis.ConnectionPool(host=config_c.get_config("redis_host"),
                                               port=int(config_c.get_config("redis_port")), decode_responses=True)
    return _redis_instance


def buffer_item(key: str, value):
    """
    缓存一个对象
    :param key: 对象的key
    :param value: 对象的value
    :return: 无返回
    """
    pool = _get_pool()
    rrdis = redis.Redis(connection_pool=pool)

    #nkey = _get_hash_key_(key)
    rrdis.hset(_redis_buffer_key, key, json.dumps(value))


def get_buffer_item(key: str):
    """
    获得一个对象的缓存
    :param key: 对象的key
    :return: 对象，查找不到会抛出异常
    """

    pool = _get_pool()
    rrdis = redis.Redis(connection_pool=pool)

    if rrdis.hexists(_redis_buffer_key, key):
        return json.loads(rrdis.hget(_redis_buffer_key, key))

    log_error("没有此buffer item")


def has_item_key(key: str):
    """
    是否存在某个key的缓存对象
    :param key: 缓存的key
    :return: True标识存在
    """
    pool = _get_pool()
    rrdis = redis.Redis(connection_pool=pool)

    if rrdis.hexists(_redis_buffer_key, key):
        return True

    return False


def remove_item(key: str):
    """
    删除某个缓存对象
    :param key: 需要删除对象的key
    :return: 无返回
    """

    if has_item_key(key):
        pool = _get_pool()
        rrdis = redis.Redis(connection_pool=pool)

        rrdis.hdel(_redis_buffer_key, key)


def buffer(permanent=False):
    '''
    缓存方法的标识符
    :param permanent: 是否永久化存储
    :return: 无
    '''

    def dector(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global _buffer_items
            nkey = _get_hash_key_(func.__name__, args, kwargs)
            if has_item_key(nkey):
                return get_buffer_item(nkey)

            func_result = func(*args, **kwargs)
            buffer_item(nkey, func_result)

            return func_result

        return wrapper

    return dector
