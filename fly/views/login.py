from flask import Blueprint, request, render_template, redirect, session

from utils.pool import sqlhelper
from  wtforms import Form
from wtforms.fields import core
from wtforms.fields import html5
from wtforms.fields import simple
from wtforms import validators
from wtforms import widgets

account = Blueprint('account', __name__)


class LoginForm(Form):
    name = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired(message='用户名不能为空.'),
            # validators.Length(min=6, max=18, message='用户名长度必须大于%(min)d且小于%(max)d')
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'}
    )
    pwd = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空.'),
            # validators.Length(min=8, message='用户名长度必须大于%(min)d'),
            # validators.Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}",
            #                   message='密码至少8个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )


@account.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        print('进来啦')
        return render_template('login.html', form=form)
        # return '登陆'
    else:
        name = request.form.get('name')
        pwd = request.form.get('pwd')
        print(name, pwd)
        with sqlhelper.SQLHelper()  as conn:
            result = conn.fetchall('select * from userinfo where name=%s and password=%s', ([name, pwd]))

        if result:
            session['user_info'] = name
            # print()
            return redirect('/index')
        return render_template('login.html')


@account.route('/index', methods=['POST', 'GET'])
def index():
    if request.method=='GET':
        with sqlhelper.SQLHelper()  as conn:
            # sql = 'insert into userinfo22(name,pwd,repwd,email,sex,addr,hobby,favor) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            rows = conn.fetchall('select * from userinfo22',())
        print('rows', rows)
        if rows:
            return render_template('index.html',form=rows)




class RegisterForm(Form):
    name = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired()
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'},
        default='alex'
    )

    pwd = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空.')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

    pwd_confirm = simple.PasswordField(
        label='重复密码',
        validators=[
            validators.DataRequired(message='重复密码不能为空.'),
            validators.EqualTo('pwd', message="两次密码输入不一致")
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

    email = html5.EmailField(
        label='邮箱',
        validators=[
            validators.DataRequired(message='邮箱不能为空.'),
            validators.Email(message='邮箱格式错误')
        ],
        widget=widgets.TextInput(input_type='email'),
        render_kw={'class': 'form-control'}
    )

    gender = core.RadioField(
        label='性别',
        choices=(
            (1, '男'),
            (2, '女'),
        ),
        coerce=int
    )
    city = core.SelectField(
        label='城市',
        choices=(
            ('bj', '北京'),
            ('sh', '上海'),
        )
    )

    hobby = core.SelectMultipleField(
        label='爱好',
        choices=(
            (1, '篮球'),
            (2, '足球'),
        ),
        coerce=int
    )

    favor = core.SelectMultipleField(
        label='喜好',
        choices=(
            (1, '篮球'),
            (2, '足球'),
        ),
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
        coerce=int,
        default=[1, 2]
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.favor.choices = ((1, '篮球'), (2, '足球'), (3, '羽毛球'))

    def validate_pwd_confirm(self, field):
        """
        自定义pwd_confirm字段规则，例：与pwd字段是否一致
        :param field:
        :return:
        """
        # 最开始初始化时，self.data中已经有所有的值

        if field.data != self.data['pwd']:
            raise validators.ValidationError("密码不一致")  # 继续后续验证
            # raise validators.StopValidation("密码不一致")  # 不再继续后续验证


@account.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        # 设置默认值
        form = RegisterForm(data={'gender': 1})
        return render_template('register.html', form=form)
    else:
        form = RegisterForm(formdata=request.form)
        if form.validate():
            print('用户提交数据通过格式验证，提交的值为：', form.data)
            name = form.data.get('name')
            pwd = form.data.get('pwd')
            pwd_confirm = form.data.get('pwd_confirm')
            email = form.data.get('email')
            sex = form.data.get('gender')
            city = form.data.get('city')
            hobby = form.data.get('hobby')
            favor = form.data.get('favor')
            with sqlhelper.SQLHelper()  as conn:
                sql = 'insert into userinfo22(name,pwd,repwd,email,sex,addr,hobby,favor) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
                rows = conn.add(sql, (name, pwd, pwd_confirm, email, sex, city, hobby, favor))
            print('rows', rows)
            if rows:
                session['user_info'] = name
                return redirect('/index')
            return render_template('register.html', form=form)
        else:
            print(form.errors)
        return render_template('register.html', form=form)
