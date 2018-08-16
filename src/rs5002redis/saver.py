from sys import stderr

from redis import StrictRedis, RedisError

from rs500common.configuration import ConfigProvider


def save_data_to_redis(data: dict, config_file: str) -> None:
    conf = ConfigProvider(config_file).get_config()
    host = conf.get(section='redis', option='host', fallback='localhost')
    port = conf.getint(section='redis', option='port', fallback=6379)
    db = conf.getint(section='redis', option='db', fallback=0)
    password = conf.get(section='redis', option='password', fallback=None)
    ttl = conf.getint(section='redis', option='result_lifetime_seconds', fallback=30)
    prefix = conf.get(section='redis', option='prefix', fallback='')
    try:
        redis = StrictRedis(host=host, port=port, db=db, password=password)
        with redis.pipeline() as pipe:
            for k, v in data.items():
                key = '{0}{1}'.format(prefix, k)
                pipe.set(key, v).expire(key, ttl)
            pipe.execute()
    except RedisError as e:
        print('Redis error:', file=stderr)
        print(e, file=stderr)
