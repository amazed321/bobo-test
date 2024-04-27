import random

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from utils.encrypt import md5_string
from www import models
from utils import tencent
from django_redis import get_redis_connection
from utils.bootstrap import BootStrapForm


class LoginForm(BootStrapForm, forms.Form):
    # exclude_field_list = ['username']
    role = forms.ChoiceField(
        label="角色",
        required=True,
        choices=(("2", "客户"), ("1", "管理员"),)
    )

    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput
    )

    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True)
    )

    def clean_password(self):
        old = self.cleaned_data['password']
        return md5_string(old)


class SmsLoginForm(BootStrapForm, forms.Form):
    role = forms.ChoiceField(
        label="角色",
        required=True,
        choices=(("2", "客户"), ("1", "管理员"),)
    )

    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3578]\d{9}$', '手机格式错误'), ],
        widget=forms.TextInput
    )

    code = forms.CharField(
        label="短信验证码",
        validators=[RegexValidator(r'^[0-9]{4}$', '验证码格式错误'), ],
        widget=forms.TextInput
    )

    def clean_code(self):
        mobile = self.cleaned_data.get('mobile')
        code = self.cleaned_data['code']
        if not mobile:
            return code

        conn = get_redis_connection("default")
        cache_code = conn.get(mobile)
        if not cache_code:
            raise ValidationError("未发送或已失效")
        if code != cache_code.decode('utf-8'):
            raise ValidationError("验证码错误")

        # 将redis中的键值对删除 key=mobile
        conn.delete(mobile)

        return code


class SendSmsForm(forms.Form):
    role = forms.ChoiceField(
        label="角色",
        required=True,
        choices=(("2", "客户"), ("1", "管理员"),)
    )

    mobile = forms.CharField(
        label="手机号",
        widget=forms.TextInput,
        required=True,
        validators=[RegexValidator(r'^1[3578]\d{9}$', '手机格式错误'), ]
    )

    def clean_mobile(self):
        role = self.cleaned_data['role']
        old = self.cleaned_data['mobile']

        # 去数据库查询，手机号是否已注册？
        if role == "1":
            exists = models.Administrator.objects.filter(active=1).filter(mobile=old).exists()
        else:
            exists = models.Customer.objects.filter(active=1).filter(mobile=old).exists()

        if not exists:
            raise ValidationError("手机号不存在")

        # 生成短信验证码 + 发送短信
        sms_code = str(random.randint(1000, 9999))
        print("随机短信验证码：", sms_code)
        is_ok = tencent.send_sms(old, sms_code)
        if not is_ok:
            raise ValidationError("短信发送失败")

        # 短信验证码写入redis中+超时时间
        from django_redis import get_redis_connection
        conn = get_redis_connection("default")
        conn.set(old, sms_code, ex=5 * 60)

        return old