# -*- coding: utf-8 -*-
# 'author':'hxy'


from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, reverse

from account.account_forms import RegisterForm, LoginForm
from account.tools import build_reg_response, build_login_response, add_new_account


def register(request):
    """
    提供用户注册视图函数，用户根据表单控件提交注册数据。
    此函数使用了django的forms组件以提供注册表单的html渲染和注册表单数据的合法性校验。
    此函数使用了ajax形式承接用户提交的注册数据以便提供更好的用户体验。
    因函数使用了ajax完成用户和服务端之间的注册数据通信，故两端协商的数据格式如下：

    ---> 用户端需提供
    request_data = {
        csrf密码
        username:  # 用户名(string)
        password:  # 账户密码(string, 明文)
        re_password:  # 账户重复密码(string, 明文)
        telephone:  # 账户手机号(string)
        email:  # 账户邮箱(string)
    }

    ---> 服务端需提供
    response_data = {
        status:  # 注册操作状态(True/False)
        fields_error:  # 表单字段错误信息(dict, key=字段名称, value=错误消息)
        next:  # 期望下一跳地址
    }

    此函数提供了如下2个分支功能：
    1、用户以get形式请求注册页面，将会使用forms组件对象显示注册表单以便用户填写注册数据
    2、用户以ajax形式提交post类型的注册数据，将会尝试校验forms组件对象、注册账户数据并返回注册结果
    """

    if request.method == 'GET':  # 客户端请求注册页面
        context = {'register_form': RegisterForm()}
        return render(request, 'account/register.html', context)

    else:  # 客户端提交注册数据
        if not request.is_ajax():
            return HttpResponse('无效请求')

        # 获取客户端提交ajax数据，并执行校验
        register_form = RegisterForm(request.POST)
        check_status = register_form.is_valid()

        if check_status is True:  # 校验成功
            # 校验成功需要加入账户数据表记录
            account_dic = register_form.cleaned_data.copy()
            account_dic.pop('re_password')
            add_new_account(account_dic)
            # 返回注册成功的响应数据
            response_data = build_reg_response(check_status, next=reverse('login'))

        else:  # 校验失败，返回注册失败的响应数据
            response_data = build_reg_response(check_status, errors=register_form.errors)

        return JsonResponse(response_data)


def login(request):
    """
    提供用户账户登录功能，用户根据登录页面提交登录数据。
    此函数调用了auth组件以验证登录账户是否正确。
    此函数调用了forms组件以提供表单控件html渲染及表单数据校验。
    此函数结合ajax形式提供登录数据传递，与用户端协商的数据格式如下：

    ---> 用户端需提供
    request_data = {
        csrf密码
        username:  # 用户名(string)
        password:  # 账户密码(string, 明文)
        validate_code:  # 验证码(string)
    }

    ---> 服务端需提供
    response_data = {
        status:  # 登录操作状态(True/False)
        form_error:  # 登录表单全局错误信息(string)
        next:  # 期望下一跳地址
    }

    此函数提供了如下4个分支功能：
    1、用户以get形式请求登录页面，将会使用forms组件对象显示登录表单以便用户填写登录数据
    2、用户以ajax形式提交post类型的登录数据，并将返回登录结果
    3、用auth组件登录账户
    4、根据用户url的next属性跳转
    """

    if request.method == 'GET':
        context = {'login_form': LoginForm()}
        return render(request, 'account/login.html', context)

    else:  # 客户端提交登录数据
        if not request.is_ajax():
            return HttpResponse('无效请求')

        # 获取用户登录数据,并验证账户数据合法性
        dic = request.POST
        validate_code = dic.get('validate_code')
        auth_user = auth.authenticate(request, username=dic.get('username'), password=dic.get('password'))

        if auth_user:  # 用户名和密码正确，后续再继续校验验证码是否输入正确
            if request.session['validate_code'].upper() == validate_code.upper():
                auth.login(request, auth_user)
                next = request.GET.get('next') or reverse('index')
                response_data = build_login_response(status=True, next=next)
            else:  # 验证码错误
                response_data = build_login_response(status=False, form_error='验证码错误')
        else:  # 用户名或者密码错误
            response_data = build_login_response(status=False, form_error='用户名或密码错误')

        return JsonResponse(response_data)


def logout(request):
    # 用户注销视图函数
    auth.logout(request)

    return redirect(reverse('login'))
