from flask import Blueprint, request, render_template, redirect

from utils.pool import sqlhelper

account = Blueprint('account', __name__)


@account.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        print('进来啦')
        return render_template('login.html')
        # return '登陆'
    else:
        name = request.form.get('name')
        pwd = request.form.get('pwd')
        print(name,pwd)
        with sqlhelper.SQLHelper()  as conn:
            result = conn.fetchall('select * from userinfo where name=%s and password=%s', ([name, pwd]))

        if result:
            return redirect('/index')
        return render_template('login.html')


@account.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
