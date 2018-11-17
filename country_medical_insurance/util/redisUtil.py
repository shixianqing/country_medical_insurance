from redis.client import Redis
from redis.connection import Connection,ConnectionPool
class Jedis():

    """"
        host:ip地址
        port: 端口号
        pwd:密码
        db:数据库索引
    """
    def __init__(self, host=None, port=None, pwd=None, db=None):
        if host is None:
            host = "localhost"
        if port is None:
            port = 6379
        if db is None:
            db = 0

        self.client = Redis(host='localhost',port=6379)
        # self.client = StrictRedis(ConnectionPool(Connection(host=host,port=port,db=db,password=pwd)))

    def addUrl(self, key, val):
        r = self.client.set(key,val)
        print(self.client.get(key))



