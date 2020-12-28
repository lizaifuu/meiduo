
# 多个数据库可随机选择 import random

class MasterSlaveDBRouter(object):
    """
    数据库的主从读写分离路由
    """
    def db_for_read(self, model, **hints):
        """
        读数据库
        :param model:
        :param hints:
        :return:
        """
        return 'slave'

    def db_for_write(self, model, **hints):
        """
        写数据库
        :param model:
        :param hints:
        :return:
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        是否运行关联操作
        :param obj1:
        :param obj2:
        :param hints:
        :return:
        """
        return True