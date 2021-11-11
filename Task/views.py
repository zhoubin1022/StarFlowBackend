from django.shortcuts import render
from django.http import HttpResponse
from Task.models import Task, Record
from Repository.models import Repository, Member
from User.models import User, Join_request
# Create your views here.
# def getSubmissionHistory(request):  # 获取任务的历史提交记录
#     ret =

def addTask(request):
    if request.method == 'POST':
        task_info = str(request.POST.get('task_info'))
        deadline = str(request.POST.get('deadline'))
        rename = str(request.POST.get('repo_name'))
        username = str(request.POST.get('username'))
    repo = Repository.objects.filter(repo_name=rename)
    user = User.objects.filter(user_name=username)
    member = User.objects.filter(repo[0], user[0])
    task = Task.objects.create(repo=repo.id, member=member.id, task_info=task_info, deadline=deadline)

    task.save()
