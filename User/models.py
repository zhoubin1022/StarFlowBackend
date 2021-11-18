from django.db import models
from Task.models import *
from Repository.models import *

'''
openid 是 用户唯一标识符
session_key 是 密钥
username 是 Github用户名
password 是 GitHub密码
'''


class User(models.Model):
    openid = models.CharField(max_length=100)
    session_key = models.CharField(max_length=100)
    username = models.CharField(max_length=50, null=True)


'''
repo 是 Repository表id
user 是 User表id,申请加入的成员
identity 是 身份/职位
request_time 是 申请时间
'''


class Join_request(models.Model):
    repo = models.ForeignKey('Repository.Repository', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    identity = models.IntegerField(default=-1)  # 0 拒绝， 1 同意
    request_time = models.DateTimeField(auto_now_add=True)

