# 博客系统
* 这是一个使用django搭建的博客系统，提供了多个用户注册和登录的博客站点。
* 用户可以注册一个专属的博客站点，并配置个人详情比如头像、个人信息等。
* 用户可以在后台管理界面中管理博客文章、文章分类。
* 用户可以访问所属的博客站点，站点将会展示所有的文章分类和博客文章，以及文章具体的属性信息。
* 用户也可以访问其他用户的博客站点，并对其他用户的文章进行点赞、评论文章内容。

# QuickStart
## 数据库配置
```python3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'blog_db',  # 要连接的数据库，连接前需要创建好
        'USER':'root',  # 连接数据库的用户名
        'PASSWORD':'root',  # 连接数据库的密码
        'HOST':'127.0.0.1',  # 连接主机，默认本级
        'PORT':3306  #  端口 默认3306
    }
}
```


## 数据库导入
项目已经提供一份mysql数据库数据，可供直接导入。

* 创建数据库

```
# 登陆数据库
>mysql -uroot -ppassword  --default-character-set=utf8

# 创建数据库
>CREATE DATABASE blog_db;
```

* 数据库迁移

```python3
# 执行迁移
python manage.py makemigrations
python manage.py migrate
```

* 导入数据
```
>use blog_db;
>set names utf8;
>source your\path\blog_db.sql (你的blog_db.sql文件所在位置);
```

* 导出数据库
```
mysqldump -uroot -p  --default-character-set=utf8  blog_db > blog_db.sql
```


## 启动服务器
在项目所在目录启动命令行，执行：`python manage.py runserver 127.0.0.1:8080`

## 访问网站
在浏览器地址栏中访问`http://127.0.0.1:8080`



