from django.db import models


class Task(models.Model):
    repo = models.ForeignKey('Repository', on_delete=models.CASCADE)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    task_info = models.CharField(max_length=100)
    status = models.IntegerField()
    deadline = models.DateTimeField()
    record = models.ForeignKey('Record', on_delete=models.CASCADE)


class Record(models.Model):
    submit_time = models.DateTimeField(auto_now_add=True)
    submit_info = models.CharField(max_length=100)
    request_id = models.IntegerField()
    checkMember = models.ForeignKey('Member', on_delete=models.CASCADE)
    check_time = models.DateTimeField(auto_now=True)
    result = models.IntegerField()
    comment = models.CharField(max_length=100)