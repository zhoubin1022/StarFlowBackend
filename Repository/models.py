from django.db import models


class Repository(models.Model):
    url = models.CharField(max_length=100)
    repo_name = models.CharField(max_length=30)
    finished = models.IntegerField(default=0)
    checking = models.IntegerField(default=0)
    incomplete = models.IntegerField(default=0)
    repo_member = models.IntegerField(default=1)


class Member(models.Model):
    repo = models.ForeignKey('Repository', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    identity = models.IntegerField()
