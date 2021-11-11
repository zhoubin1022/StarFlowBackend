from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Task.models import Task, Record
from Repository.models import Repository, Member
from User.models import User, Join_request
# Create your views here.


# 获取项目开发者
def getDevelopers(request):
    if request.method == 'GET':
        result = {"message": 'success', "data": []}
        repo_id = int(request.GET.get('repo_id'))
        developers = Member.objects.filter(repo=repo_id, identity=2)
        result["data"] = serializers.serialize('python', developers)
        return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})


# 添加任务
# def addTask(request):
#     if request.method == 'POST':
#         task_info = str(request.POST.get('task_info'))
#         deadline = str(request.POST.get('deadline'))
#         rename = str(request.POST.get('repo_name'))
#         username = str(request.POST.get('username'))
#     repo = Repository.objects.filter(repo_name=rename)
#     user = User.objects.filter(user_name=username)
#     member = User.objects.filter(repo[0], user[0])
#     task = Task.objects.create(repo=repo.id, member=member.id, task_info=task_info, deadline=deadline)
#
#     task.save()
