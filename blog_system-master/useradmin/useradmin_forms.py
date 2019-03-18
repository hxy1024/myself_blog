# !/usr/bin/python
# -*- coding:utf-8 -*-
# date:2018/10/29


from django import forms


# bootstrap的表单控件样式属性
bootstrap_form_style = {
    'class': 'form-control',
}
profile_form_style = bootstrap_form_style


class ProfileForm(forms.Form):
    """
    用户个人详情表单，用于提供个人详情数据编辑
    """

    nick_name = forms.CharField(label='昵称', widget=forms.TextInput(attrs=profile_form_style))
    city = forms.CharField(label='所在城市', widget=forms.TextInput(attrs=profile_form_style))
    introduction = forms.CharField(label='个人介绍', widget=forms.Textarea(attrs=profile_form_style))
    college = forms.CharField(label='毕业学校', widget=forms.TextInput(attrs=profile_form_style))
    company = forms.CharField(label='所在公司', widget=forms.TextInput(attrs=profile_form_style))
    title = forms.CharField(label='职位', widget=forms.TextInput(attrs=profile_form_style))
