# !/usr/bin/python
# -*- coding:utf-8 -*-


import random
import string

from PIL import Image, ImageDraw, ImageFont

from django.db.models import F
from django.db.transaction import atomic
from blog.models import ArticleUpDown


def get_random_code(length=5):
    # 生成验证码函数，长度为length
    random_code = ''
    chars_set = string.digits + string.ascii_letters
    for i in range(length):
        random_code += random.choice(chars_set)
    return random_code


def random_color(s=1, e=255):
    # 随机RGB颜色函数
    return (random.randint(s, e), random.randint(s, e), random.randint(s, e))


def build_code_img(lenght=5, width=260, height=40):
    """验证码图片生成函数
    默认有5个验证码字符
    """

    # 创建Image对象
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象,需提供字体ttf文件
    font = ImageFont.truetype('static/fonts/pingfang.ttf', size=32)
    # 创建Draw对象
    draw = ImageDraw.Draw(image)
    # 随机颜色填充每个像素
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=random_color(64, 255))
    # 验证码
    random_code = get_random_code()
    # 随机颜色验证码写到图片上
    for t in range(lenght):
        draw.text((50 * t + 20, 0), random_code[t], font=font, fill=random_color(32, 127))

    return random_code, image


def switch_like(user, article_set, user_choice):
    """
    对指定用户、指定文章集合、用户提供的喜欢/不喜欢数据进行切换，并更新数据
    """

    updown_set = ArticleUpDown.objects.filter(user=user, article=article_set.first())
    updown = updown_set.first()

    with atomic():  # 事务
        # 如果没有此记录，说明第一次点击，直接增加记录，并返回两者数量数据
        if not updown:
            print('first')
            ArticleUpDown.objects.create(user=user, article=article_set.first(), is_like=user_choice)
            # 更新文章的喜欢/不喜欢数量
            if user_choice:
                article_set.update(like_count=F('like_count') + 1)
            else:
                article_set.update(dislike_count=F('dislike_count') + 1)
        # 有记录，但是历史记录中选择了中立,现选择+1
        elif updown.is_like is None:
            # 更新文章的喜欢/不喜欢数量
            updown_set.update(is_like=user_choice)
            if user_choice:
                article_set.update(like_count=F('like_count') + 1)
            else:
                article_set.update(dislike_count=F('dislike_count') + 1)
        # 如果用户点击和记录是一样的标志，说明用户是取消此选择，原选择-1
        elif updown.is_like == user_choice:
            updown_set.update(is_like=None)
            # 更新文章的喜欢/不喜欢数量
            if user_choice:
                article_set.update(like_count=F('like_count') - 1)
            else:
                article_set.update(dislike_count=F('dislike_count') - 1)
        # 如果用户点击和记录是不一样的标志，说明用户点击相对的选择，原选择-1，现选择+1
        else:
            # 更新文章的喜欢/不喜欢数量
            if user_choice:
                updown_set.update(is_like=True)
                article_set.update(dislike_count=F('dislike_count') - 1)
                article_set.update(like_count=F('like_count') + 1)
            else:
                updown_set.update(is_like=False)
                article_set.update(dislike_count=F('dislike_count') + 1)
                article_set.update(like_count=F('like_count') - 1)
