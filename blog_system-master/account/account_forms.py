# !/usr/bin/python
# -*- coding:utf-8 -*-


import re

from django import forms
from django.forms import ValidationError

from blog.models import Account
from blog_system.settings import USERNAME_SYSTEM_USED


# bootstrap的表单控件样式属性
bootstrap_form_style = {
    'class': 'form-control',
}
register_form_style = bootstrap_form_style
login_form_style = bootstrap_form_style


class RegisterForm(forms.Form):
    """注册表单类
    提供用户账户信息注册使用。
    注意：re_password字段不插入数据库中，仅用于两次密码的一致性验证。

    此表单提供2个分支功能：
    1、用于注册页面中的表单控件html渲染
    2、当用户提交注册数据的时候进行规则校验,校验失败时会提供错误信息
    """

    username = forms.CharField(label='用户名', min_length=1, max_length=16,
                               help_text='用户名长度1-16位，由字母、数字、下划线组成',
                               error_messages={'required': '请提供用户名', },
                               widget=forms.TextInput(attrs=register_form_style))

    password = forms.CharField(label='密码', min_length=8, max_length=32, strip=False,
                               help_text='密码长度8-32位，至少包含1个字母和1个数字',
                               error_messages={
                                   'required': '请提供密码',
                                   'min_length': '密码长度不足8位',
                                   'max_length': '密码长度超过32位',
                               }, widget=forms.PasswordInput(attrs=register_form_style))

    re_password = forms.CharField(label='重复密码', required=False, strip=False,
                                  widget=forms.PasswordInput(attrs=register_form_style))

    telephone = forms.CharField(label='手机号', error_messages={'required': '请提供手机号', },
                                widget=forms.TextInput(attrs=register_form_style))

    email = forms.EmailField(label='邮箱地址',
                             error_messages={
                                 'required': '请提供邮箱地址',
                                 'invalid': '邮箱地址格式错误'
                             }, widget=forms.EmailInput(attrs=register_form_style))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # 如果匹配到了任意一个非字母、数字、下划线的字符就不满足要求
        if re.search('[^a-zA-Z\d_]', username):
            raise ValidationError('用户名格式错误')

        # 判断是否注册的用户名存在于系统使用名单或者是已经存在
        exist_user = Account.objects.filter(username=username).first()
        if username in USERNAME_SYSTEM_USED or exist_user:
            raise ValidationError('此用户名已经存在')

        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # 判断密码是否至少包含1个字母及1个数字
        if not (re.search('[a-zA-Z]', password) and re.search('\d', password)):
            raise ValidationError('密码格式错误')

        return password

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')

        # 判断是否是有效的手机号
        if not re.fullmatch('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', telephone):
            raise ValidationError('无效的手机号')

        return telephone

    def clean(self):
        """密码一致性校验
        判断如果输入了密码，则重复密码必须与密码一致，注意，这应该用联合校验，不应该用局部校验
        因为局部字段校验是无序的，而两次密码的一致性校验有顺序依赖
        """

        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        if password:
            if not re_password:
                self.add_error('re_password', ValidationError('请再次输入密码'))
            elif re_password != password:
                self.add_error('re_password', ValidationError('两次密码输入不一致'))

        return self.cleaned_data


class LoginForm(forms.Form):
    """用户登录表单类
    提供用户登录的信息验证
    """

    username = forms.CharField(label='用户名', max_length=16,
                               widget=forms.TextInput(attrs=login_form_style))

    password = forms.CharField(label='密码', max_length=32,
                               widget=forms.PasswordInput(attrs=login_form_style))
