import json
from datetime import datetime
from django.utils.timezone import utc
from django.utils.timezone import localtime
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from requests.adapters import HTTPAdapter

from Task.models import Task, Record
from Repository.models import Repository, Member
from User.models import User, Join_request
import requests
import datetime


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
        # infos = []
        for dev in developers:
            info = {'member_id': dev.pk, 'user_id': dev.user_id_id,
                    'username': dev.username, 'identity': dev.identity}
            result["data"].append(info)
            
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    return JsonResponse({"message": 'wrong'})


# 获取当前任务的历史操作记录, 一个任务只有一个开发者  (已完成)
def getTaskRecord(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        # repo_id = int(request.POST.get('repo_id'))
        task_id = int(request.POST.get('task_id'))
        try:
            task_record = Record.objects.filter(task_id_id=task_id)
        except:
            return JsonResponse({"message": 'Parameter error!'})

        for x in task_record:
            s_time = x.submit_time
            c_time = x.check_time
            record = {"pk": x.pk,
                      "submit_time": (s_time.year, s_time.month, s_time.day, s_time.hour, s_time.minute, s_time.second),
                      "submit_info": x.submit_info, "task_id": task_id,
                      "submitMember": x.submitMember_id, "request_id": x.request_id, "checkMember": x.checkMember_id,
                      "check_time": (c_time.year, c_time.month, c_time.day, c_time.hour, c_time.minute, c_time.second),
                      "result": x.result, "comment": x.comment}
            s_id = x.submitMember_id
            s_name = Member.objects.get(pk=s_id).username
            record["s_name"] = s_name
            c_id = x.checkMember_id
            # print(s_id)
            # print(c_id)
            if c_id:
                c_name = Member.objects.get(pk=c_id).username
                record["c_name"] = c_name
            else:
                record["c_name"] = ""
            result["data"].append(record)
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    return JsonResponse({"message": 'wrong'})


# 管理员通过任务  (已完成)
def checkTask(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        checkMember_id = int(request.POST.get('checkMember_id'))
        repo_id = int(request.POST.get('repo_id'))
        task_id = int(request.POST.get('task_id'))
        comment = str(request.POST.get('comment'))
        try:
            task = Task.objects.get(pk=task_id)
            task_records = Record.objects.filter(task_id=task_id).order_by('-submit_time')
            repository = Repository.objects.get(pk=repo_id)
            submit_member = Member.objects.get(pk=task.member_id)
        except:
            # print(task.member_id)
            return JsonResponse({"message": 'Parameter error!'})

        task.status = 2
        task.save()

        task_record = task_records[0]
        task_record.result = 1  # 审核通过结果为 1
        task_record.comment = comment  # 管理员评价
        task_record.checkMember_id = checkMember_id
        task_record.save()

        # if repository.checking > 0:
        repository.checking -= 1
        repository.finished += 1
        repository.save()

        c_time = task_record.check_time
        check_time = (c_time.year, c_time.month, c_time.day, c_time.hour, c_time.minute, c_time.second)
        print(check_time)
        info = {'submit_member': submit_member.username, 'request_id': task_record.request_id,
                'task_info': task.task_info, 'comment': task_record.comment,
                'check_time': check_time
                }
        result['data'].append(info)
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')

    return JsonResponse({"message": 'wrong'})


# 管理员驳回任务 (已完成)
def revokeTask(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        checkMember_id = int(request.POST.get('checkMember_id'))
        repo_id = int(request.POST.get('repo_id'))
        task_id = int(request.POST.get('task_id'))
        comment = str(request.POST.get('comment'))
        try:
            task = Task.objects.get(pk=task_id)
            task_records = Record.objects.filter(task_id_id=task_id).order_by('-submit_time')
            repository = Repository.objects.get(pk=repo_id)
            submit_member = Member.objects.get(pk=task.member_id)
        except:
            return JsonResponse({"message": 'Parameter error!'})

        task.status = 0  # 未完成状态
        task.save()

        task_record = task_records[0]
        task_record.result = 0  # 审核不通过
        task_record.comment = comment  # 不通过评价
        task_record.checkMember_id = checkMember_id
        task_record.save()

        repository.checking -= 1
        repository.incomplete += 1
        repository.save()

        c_time = task_record.check_time
        check_time = (c_time.year, c_time.month, c_time.day, c_time.hour, c_time.minute, c_time.second)
        print(check_time)
        info = {'submit_member': submit_member.username, 'request_id': task_record.request_id,
                'task_info': task.task_info, 'comment': task_record.comment,
                'check_time': check_time
                }
        result['data'].append(info)
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    return JsonResponse({"message": 'wrong'})


# 管理员添加任务 (已完成)
def addTask(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        task_name = str(request.POST.get('task_name'))
        task_info = str(request.POST.get('task_info'))
        deadline = str(request.POST.get('deadline'))
        repo_id = int(request.POST.get('repo_id'))
        username = str(request.POST.get('username'))
        try:
            repo = Repository.objects.get(pk=repo_id)
            member = Member.objects.get(username=username, repo_id=repo_id)
            # print(member.username)
        except:
            return JsonResponse({"message": 'Parameter error!'})

        task = Task.objects.create(task_info=task_info, status=0, deadline=deadline,
                                   repo_id=repo_id, member_id=member.pk, task_name=task_name)

        repo.incomplete += 1  # 仓库待完成任务 ++
        repo.save()
        infos = {'task_id': task.pk}
        result['data'].append(infos)
        return JsonResponse(result)

    return JsonResponse({"message": 'wrong'})


# 开发者提交任务 (已完成)
def submitTask(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        submit_info = str(request.POST.get('submit_info'))
        submit_id = int(request.POST.get('submit_id'))
        request_id = int(request.POST.get('request_id'))
        task_id = int(request.POST.get('task_id'))
        repo_id = int(request.POST.get('repo_id'))
        try:
            record = Record.objects.create(submit_info=submit_info, submitMember_id=submit_id,
                                           request_id=request_id, task_id_id=task_id)
            task = Task.objects.get(pk=task_id)
        except:
            return JsonResponse({"message": 'Parameter error!'})
        task.record_id = record.pk
        task.status = 1
        task.save()

        repo = Repository.objects.get(pk=repo_id)
        repo.checking += 1  # 仓库待审核 ++
        repo.incomplete -= 1  # 待完成 --
        repo.save()
        infos = {'record_id': record.pk}
        result['data'].append(infos)
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    return JsonResponse({'message': 'wrong'})


# 获取 pull requests 信息 (已完成)
def getRequest(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        owner_repo = str(request.POST.get('owner_repo'))
        url = f'https://api.github.com/repos/{owner_repo}/pulls'
        print(url)
        response = getPullRequests(url)
        response = response.json()
        # infos = []
        for i in response:
            info = {'request_id': i['number'], 'title': i['title'], 'created_at': i['created_at'],
                    'updated_at': i['updated_at'], 'user_name': i['user']['login']}
            # infos.append(info)
            result['data'].append(info)
        # print(infos)
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    return JsonResponse({'message': 'wrong'})


# 获取 pull requests 信息
def getPullRequests(url):
    # api_token = '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'
    hd = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/94.0.4606.81 Safari/537.36'  # + api_token
    }
    print(url)
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    try:
        res = s.get(url=url, headers=hd, timeout=5)
        # print(res.json())
        return res
    except requests.exceptions.RequestException as e:
        print(e)

    # try:
    #     r = requests.get(url, headers=hd, timeout=30)
    #     r.raise_for_status()
    #     r.encoding = r.apparent_encoding
    #     return r
    # except:
    #     return "产生异常"


# 删除任务
def deleteTask(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        repo_id = request.POST.get('repo_id')
        task_id = request.POST.get('task_id')
        try:
            del_task = Task.objects.get(pk=task_id)
            repo = Repository.objects.get(pk=repo_id)
        except:
            return JsonResponse({"message": 'Parameter error!'})
        del_task.delete()
        repo.incomplete -= 1
        repo.save()
        tasks = Task.objects.filter(repo_id=repo_id)  # .values('pk', 'task_name', 'deadline')
        infos = {'finished': [], 'checking': [], 'incomplete': []}
        for task in tasks:
            time = task.deadline
            status = task.status
            info = {'task_id': task.pk, 'task_name': task.task_name, 'task_info': task.task_info,
                    'deadline': (time.year, time.month, time.day, time.hour, time.minute, time.second)}
            if status == 0:  # 未完成任务分组
                infos['incomplete'].append(info)
            elif status == 1:  # 待审核任务分组
                infos['checking'].append(info)
            elif status == 2:  # 已完成任务分组
                infos['finished'].append(info)

        print(infos)
        result['data'].append(infos)
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    return {"message": 'wrong'}
