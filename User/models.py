from django.db import models


class User(models.Model):
    openid = models.CharField(max_length=100)
    session_key = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class Join_request(models.Model):
    repo = models.ForeignKey('Repository', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    identity = models.IntegerField()
    request_time = models.DateTimeField(auto_now_add=True)
