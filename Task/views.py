from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Task.models import Task, Record
from Repository.models import Repository, Member
from User.models import User, Join_request


# Create your views here.


# 获取项目开发者
def getDevelopers(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        repo_id = int(request.GET.get('repo_id'))
        developers = Member.objects.filter(repo=repo_id, identity=2)
        result["data"] = serializers.serialize('python', developers)
        return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})


# 获取当前任务的历史操作记录, 一个任务只有一个开发者
def getTaskRecord(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        repo_id = int(request.GET.get('repo_id'))
        task_id = int(request.GET.get('task_id'))
        task_record = Record.objects.filter(task_id=task_id)
        records = []
        for i in task_record:
            s_id = i.submitMember
            username = Member.objects.get(pk=s_id).username
            record = {"record": i, "username": username}
            records.append(record)
        result["data"] = serializers.serialize('python', records)
        return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})


# 管理员确认任务
# def checkTask(request):
#     if request.method == 'POST':
#         result = {"message": 'success', "data": []}
#         task_id = int(request.GET.get('task_id'))
#         task = Task.objects.get(pk=task_id)
#         task.status = 2
#         task.save()
#         result['data'] = serializers.serialize('python', task)
#         return JsonResponse(result)
#     return JsonResponse({"message": 'wrong'})


# 管理员撤销任务
# def revokeTask(request):
#     if request.method == 'POST':
#         result = {"message": 'success', "data": []}
#         task_id = int(request.GET.get('task_id'))
#         task = Task.objects.get(pk=task_id)
#         task.status = 0
#         task.save()
#         result['data'] = serializers.serialize('python', task)
#         return JsonResponse(result)
#     return JsonResponse({"message": 'wrong'})


# 添加任务
# def addTask(request):
#     if request.method == 'POST':
#         task_info = str(request.POST.get('task_info'))
#         deadline = str(request.POST.get('deadline'))
#         rename = str(request.POST.get('repo_name'))
#         username = str(request.POST.get('username'))
#         repo = Repository.objects.filter(repo_name=rename)
#         user = User.objects.filter(user_name=username)
#         member = User.objects.filter(repo[0], user[0])
#         for i in repo:
#             for j in member:
#                 task = Task.objects.create(repo=i.pk, member=j.pk, task_info=task_info, deadline=deadline)
#                 task.save()

