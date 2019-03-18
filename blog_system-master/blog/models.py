# -*- coding: utf-8 -*-
# 'author':'hxy'


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class Account(AbstractUser):
    """ 用户账户表
    保存用户的账户信息数据,继承django原生的User表中的字段
    """

    nid = models.AutoField(verbose_name='编号', primary_key=True)
    telephone = models.CharField(verbose_name='手机号', max_length=11)

    def __str__(self):
        return self.username

    __repr__ = __str__


class Blog(models.Model):
    """ 站点表
    保存每个用户的个人展示数据
    """

    nid = models.AutoField(primary_key=True)
    user = models.OneToOneField(verbose_name='所属用户', to='Account', on_delete=models.CASCADE)  # 站点与用户表的一对一关系
    path = models.CharField(verbose_name='博客路径', max_length=16, unique=True)
    theme = models.CharField(verbose_name='博客样式', max_length=16)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    article_count = models.IntegerField(verbose_name='文章数量', default=0)
    category_count = models.IntegerField(verbose_name='分类数量', default=0)

    def __str__(self):
        return self.path

    __repr__ = __str__


class Category(models.Model):
    """ 分类表
    保存所有分类数据
    """

    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='分类名称', max_length=16)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog',  # 分类数据与站点的多对一关系
                             to_field='nid', on_delete=models.CASCADE)
    article_count = models.IntegerField(verbose_name='文章数量', default=0)

    def __str__(self):
        return self.name

    __repr__ = __str__


class Article(models.Model):
    """ 文章数据表
    保存全站的所有文章数据，当访问首页的时候展示所有文章数据，
    """

    nid = models.AutoField(primary_key=True)
    blog = models.ForeignKey(verbose_name='所属博客站点', to='Blog',  # 文章与博客站点表的多对一关系
                             to_field='nid', on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name='所属分类', to='Category',  # 文章与分类表的多对一关系
                                 to_field='nid', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='文章标题', max_length=32)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)
    content = models.TextField(verbose_name='文章内容')
    comment_count = models.IntegerField(verbose_name='评论数量', default=0)
    like_count = models.IntegerField(verbose_name='点赞数量', default=0)
    dislike_count = models.IntegerField(verbose_name='反对数量', default=0)
    view_count = models.IntegerField(verbose_name='阅读数量', default=0)
    # 文章题图
    img = models.ImageField(verbose_name='文章题图', upload_to='article_imgs/', null=True)

    def __str__(self):
        return self.title

    __repr__ = __str__


class ArticleUpDown(models.Model):
    """ 点赞/反对表
    记录文章的点赞和反对数据
    """

    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(  # 点赞/反对表与用户表多对一关系
        verbose_name='用户',
        to='Account',
        to_field='nid',
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(  # 点赞/反对表与文章表多对一关系
        verbose_name='文章',
        to='Article',
        to_field='nid',
        on_delete=models.CASCADE
    )
    is_like = models.BooleanField(verbose_name='点赞', null=True)  # 值为True的时候为点赞，为False的时候为反对


class Comment(models.Model):
    """ 评论表
    保存所有文章的评论数据
    """

    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(  # 评论表与用户表多对一关系
        verbose_name='用户',
        to='Account',
        to_field='nid',
        on_delete=models.CASCADE
    )
    reply_to = models.CharField(verbose_name='回复给', null=True, max_length=16)
    article = models.ForeignKey(  # 评论表与文章表多对一关系
        verbose_name='文章',
        to='Article',
        to_field='nid',
        on_delete=models.CASCADE
    )
    content = models.TextField(verbose_name='评论内容')
    parent = models.ForeignKey(  # 评论的父级元素，自关联
        verbose_name='父级元素',
        to='self',
        null=True,
        to_field='nid',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    # 子评论树的根评论id
    root_id = models.IntegerField(verbose_name='根评论id', null=True)


class Profile(models.Model):
    """ 个人详情表
    保存个人账户的详细介绍数据
    """

    nick_name = models.CharField(
        verbose_name='博客名称(昵称)',
        max_length=16,
        null=True,
        default='未知名的博客站点',
        unique=False
    )
    nid = models.AutoField(primary_key=True)
    user = models.OneToOneField(  # 个人详情信息与用户表的一对一关系
        verbose_name='所属用户',
        to='Account',
        to_field='nid',
        on_delete=models.CASCADE
    )
    city = models.CharField(verbose_name='所在城市', max_length=32, null=True, default='未知城市')
    introduction = models.TextField(verbose_name='个人介绍', null=True, default='未知个人信息')
    college = models.CharField(verbose_name='毕业学校', max_length=32, null=True, default='无')
    company = models.CharField(verbose_name='所在公司', max_length=64, null=True, default='无')
    title = models.CharField(verbose_name='职位', max_length=64, null=True, default='无')
    # 个人头像
    avatar = models.ImageField(verbose_name='个人头像', upload_to='avatars/', default='avatars/default_female.png')

    def __str__(self):
        return self.user.username + ' 的个人详情'

    __repr__ = __str__
