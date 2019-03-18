# -*- coding: utf-8 -*-
# 'author':'hxy'


from blog.models import Account, Blog, Profile


def add_new_account(account_dic):
    # 校验成功需要加入账户数据表记录
    new_user = Account.objects.create_user(**account_dic)

    # 注册成功为用户创建一个博客站点
    path = account_dic.get('username')
    Blog.objects.create(user=new_user, path=path)

    # 注册成功为用户创建一个个人详情记录
    Profile.objects.create(user=new_user)

    return True


def build_reg_response(status, errors=None, next=''):
    # 此函数用于提供注册结果数据返回给用户端
    fields_error = {}
    if errors:
        # 传递的参数是form.errors需要进一步转换格式
        fields_error = {
            field_name: field_errors[0]
            for field_name, field_errors in errors.items()
        }

    response = {
        'status': status,
        'fields_error': fields_error,
        'next': next,
    }

    return response


def build_login_response(status, form_error='', next=''):
    # 此函数用于提供登录结果返回给用户端
    response = {
        'status': status,
        'form_error': form_error,
        'next': next,
    }

    return response
