from redis.client import Redis
from redis.connection import ConnectionPool
import country_medical_insurance.settings as cfg


class Jedis():

    def __init__(self):
        pool = ConnectionPool(host=cfg.REDIS_HOST, port=cfg.REDIS_PORT)
        self.client = Redis(connection_pool=pool)

    def page_query(self, redis_key, start, end):
        '''
        分页查询
        :param redis_key: redis中的key名称
        :param start:起始页
        :param end:结束页
        :return:
        '''
        return self.client.lrange(name=redis_key, start=start, end=end)

    def len(self, redis_key):
        return self.client.llen(name=redis_key)

    def lpush(self, key, val):
        self.client.lpush(key, val)


