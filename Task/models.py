from django.db import models
from Repository.models import *
from User.models import *


class Task(models.Model):
    repo = models.ForeignKey('Repository.Repository', on_delete=models.CASCADE)  # Repository表 id
    member = models.ForeignKey('Repository.Member', on_delete=models.CASCADE)  # Member表 id
    task_info = models.CharField(max_length=100)  # 任务信息
    status = models.IntegerField(default=0)  # 任务状态
    deadline = models.DateTimeField()  # 截止日期
    record = models.ForeignKey('Record', on_delete=models.CASCADE, null=True)  # Task_Record表 id


class Record(models.Model):
    submit_time = models.DateTimeField(auto_now_add=True)  # 提交时间
    submit_info = models.CharField(max_length=100)  # 提交描述
    submitMember = models.ForeignKey('Repository.Member', to_field='id',
                                     on_delete=models.CASCADE, related_name='submit', null=True)
    request_id = models.IntegerField()  # 在仓库 pull request 的 id
    checkMember = models.ForeignKey('Repository.Member', to_field='id',
                                    on_delete=models.CASCADE, related_name='checking', null=True)
    # Member表 id
    check_time = models.DateTimeField(auto_now=True)  # 审核时间
    result = models.IntegerField(null=True)  # 审核结果
    comment = models.CharField(max_length=100, null=True)  # 评价信息
