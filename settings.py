#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis

class BaseConfig(object):
    SESSION_TYPE = 'redis'  # session类型为redis
    SESSION_KEY_PREFIX = 'session:'  # 保存到session中的值的前缀
    SESSION_PERMANENT = False  # 如果设置为True，则关闭浏览器session就失效。
    SESSION_USE_SIGNER = True  # 是否对发送到浏览器上 session:cookie值进行加密

class ProductionConfig(BaseConfig):

    SESSION_REDIS = redis.Redis(host='192.168.20.100', port='6379',password='')  # 用于连接redis的配置
    v=SESSION_REDIS.keys()
    print('session',SESSION_REDIS.get('frank').decode("utf-8"))
    # print(v)

class DevelopmentConfig(BaseConfig):
    pass
    # SESSION_REDIS = redis.Redis(host='47.93.4.198', port=6379, password='123123')  # 用于连接redis的配置

class TestingConfig(BaseConfig):
    SESSION_REDIS = redis.Redis(host='192.168.20.100', port='6379', password='')  # 用于连接redis的配置
    pass
    # SESSION_REDIS = redis.Redis(host='47.93.4.198', port=6379, password='123123')  # 用于连接redis的配置
