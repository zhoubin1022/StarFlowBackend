from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Task.models import Task, Record
from Repository.models import Repository, Member
from User.models import User, Join_request
import json


# Create your views here.


# 获取项目开发者 （已完成）
def getDevelopers(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        repo_id = int(request.POST.get('repo_id'))
        developers = Member.objects.filter(repo_id=repo_id, identity=2)
        if not developers:
            result = {"message": 'repository does not exist'}
            return JsonResponse(result)
        result["data"] = serializers.serialize('python', developers)
        return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})


# 获取当前任务的历史操作记录, 一个任务只有一个开发者  (待修改)
def getTaskRecord(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        # repo_id = int(request.POST.get('repo_id'))
        task_id = int(request.POST.get('task_id'))
        task_record = Record.objects.filter(task_id_id=task_id)
        for x in task_record:
            record = {"pk": x.pk, "submit_time": x.submit_time, "submit_info": x.submit_info, "task_id": task_id,
                      "submitMember": x.submitMember_id, "request_id": x.request_id, "checkMember": x.checkMember_id,
                      "check_time": x.check_time, "result": x.result, "comment": x.comment}
            s_id = x.submitMember_id
            s_name = Member.objects.get(pk=s_id).username
            record["s_name"] = s_name
            c_id = x.checkMember_id
            print(s_id)
            print(c_id)
            if c_id:
                c_name = Member.objects.get(pk=c_id).username
                record["c_name"] = c_name
            record["c_name"] = ""
            result["data"].append(record)
        return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})


# 管理员确认任务  (待完善)
def checkTask(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        checkMember_id = int(request.POST.get('checkMember_id'))
        repo_id = int(request.POST.get('repo_id'))
        task_id = int(request.POST.get('task_id'))
        comment = str(request.POST.get('comment'))
        try:
            task = Task.objects.get(pk=task_id)
            task_record = Record.objects.get(task_id=task_id)
            repository = Repository.objects.get(pk=repo_id)
            submit_member = Member.objects.get(pk=task.member_id)
        except:
            # print(task.member_id)
            return JsonResponse({"message": 'Parameter error!'})

        task.status = 2
        task.save()

        task_record.result = 1  # 审核通过结果为 1
        task_record.comment = comment  # 管理员评价
        task_record.checkMember_id = checkMember_id
        task_record.save()

        repository.checking -= 1
        repository.finished += 1
        repository.save()

        info = {'submit_member': submit_member.username, 'request_id': task_record.request_id,
                'task_info': task.task_info, 'comment': task_record.comment,
                }
        result['data'].append(info)
        return JsonResponse(result)

    return JsonResponse({"message": 'wrong'})


# 管理员撤销任务 (待检测)
def revokeTask(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        checkMember_id = int(request.POST.get('checkMember_id'))
        repo_id = int(request.POST.get('repo_id'))
        task_id = int(request.POST.get('task_id'))
        comment = str(request.POST.get('comment'))
        try:
            task = Task.objects.get(pk=task_id)
            task_record = Record.objects.get(task_id=task_id)
            repository = Repository.objects.get(pk=repo_id)
            submit_member = Member.objects.get(pk=task.member_id)
        except:
            return JsonResponse({"message": 'Parameter error!'})

        task.status = 0  # 未完成状态
        task.save()

        task_record.result = 0  # 审核不通过
        task_record.comment = comment  # 不通过评价
        task_record.checkMember_id = checkMember_id
        task_record.save()

        repository.checking -= 1
        repository.incomplete += 1
        repository.save()

        info = {'submit_member': submit_member.username, 'task_info': task.task_info, 'result': task_record.result,
                'check_time': task_record.check_time,
                'finish': repository.finished, 'checking': repository.checking, 'incomplete': repository.incomplete}
        result['data'].append(info)
        return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})


# 管理员添加任务
def addTask(request):
    if request.method == 'POST':
        task_info = str(request.POST.get('task_info'))
        deadline = str(request.POST.get('deadline'))
        rename = str(request.POST.get('repo_id'))
        username = str(request.POST.get('username'))
        repo = Repository.objects.filter(repo_name=rename)
        user = Member.objects.filter(user_name=username)
        member = User.objects.filter(repo[0], user[0])
        for i in repo:
            for j in member:
                task = Task.objects.create(repo=i.pk, member=j.pk, task_info=task_info, deadline=deadline)
                task.save()
