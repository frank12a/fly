#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask

# from auth.auth import Auth
#第一步添加SQLAlchemy
from flask_session import Session
from flask_sqlalchemy import  SQLAlchemy
db=SQLAlchemy()
from .views.login import account#这个account是蓝图的app
# from .views.main import main
# from .views.user import user

from .models import *
def create_app():
    '''创建这个应用'''
    app = Flask(__name__,template_folder='templates')
    app.debug = True
    app.secret_key = 'sdiusdfsdf'
    # 设置配置文件
    app.config.from_object('settings.TestingConfig')

    # 注册蓝图
    app.register_blueprint(account)
    # app.register_blueprint(user)
    # app.register_blueprint(main)
    #
    # @app.before_request
    # def check_login():
    #     print('定义验证方法')

    # 注册组件
    Session(app)
    # Auth(app)
    #第二步
    #这是给app添加SQLAlchemy
    db.init_app(app)
    return app