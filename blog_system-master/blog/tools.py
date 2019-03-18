# -*- coding: utf-8 -*-
# 'author':'hxy'


"""
工具类模块
用于提供当前app应用的各种函数和类工具
"""


from bs4 import BeautifulSoup


def filter_content(html_content):
    """
    对html字符串进行过滤，得到单纯的字符串文本
    """

    soup = BeautifulSoup(html_content, 'html.parser')
    content = soup.get_text()

    return content
