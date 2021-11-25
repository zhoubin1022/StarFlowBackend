from django.db import models
from Task.models import *
from User.models import *


class Repository(models.Model):
    url = models.CharField(max_length=100)  # 仓库地址
    repo_name = models.CharField(max_length=30)  # repo_name表示仓库名
    finished = models.IntegerField(default=0)  # finished表示已完成数目int类型 默认值为0
    checking = models.IntegerField(default=0)  # checking表示待审核任务数int类型 默认值为0
    incomplete = models.IntegerField(default=0)  # incomplete表示待完成任务数目 int类型 默认值为0
    repo_member = models.IntegerField(default=1)  # repo_member表示项目人数 int类型 默认值为1


class Member(models.Model):
    repo_id = models.ForeignKey('Repository', on_delete=models.CASCADE)  # repo表的主键
    # on_delete=models.CASCADE
    user_id = models.ForeignKey('User.User', on_delete=models.CASCADE)  # user表的主键
    username = models.CharField(max_length=50)  # github用户名
    # 字符串字段  单行输入，用于较短的字符串，如要保存大量文本, 使用 TextField。
    # 必须 max_length 参数，django会根据这个参数在数据库层和校验层限制该字段所允许的最大字符数。
    identity = models.IntegerField()  # 身份职位    models.IntegerField()整形   用于保存一个整数
