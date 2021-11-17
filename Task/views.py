import json
from datetime import datetime
from django.utils.timezone import utc
from django.utils.timezone import localtime
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
        result["data"] = serializers.serialize('python', developers)
        return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})


# 获取当前任务的历史操作记录, 一个任务只有一个开发者  (已完成)
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
            # print(s_id)
            # print(c_id)
            if c_id:
                c_name = Member.objects.get(pk=c_id).username
                record["c_name"] = c_name
            record["c_name"] = ""
            result["data"].append(record)
        return JsonResponse(result)
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

        time = datetime.datetime.now()
        check_time = (time.year, time.month, time.day, time.hour, time.minute, time.second)
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

        time = datetime.datetime.now()
        check_time = (time.year, time.month, time.day, time.hour, time.minute, time.second)
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
            return JsonResponse({"message": 'wrong'})

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
        record = Record.objects.create(submit_info=submit_info, submitMember_id=submit_id,
                                       request_id=request_id, task_id_id=task_id)
        task = Task.objects.get(pk=task_id)
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
        owner = str(request.POST.get('owner'))
        repo = str(request.POST.get('repo'))
        url = 'https://api.github.com/repos/{}/{}/pulls'.format(owner, repo)
        print(url)
        response = getPullRequests(url)
        response = response.json()
        infos = []
        for i in response:
            info = {'request_id': i['id'], 'title': i['title'], 'created_at': i['created_at'],
                    'updated_at': i['updated_at'], 'user_name': i['user']['login']}
            infos.append(info)
        print(infos)
        result['data'].append(infos)
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    return JsonResponse({'message': 'wrong'})


# 获取 pull requests 信息
def getPullRequests(url):
    api_token = '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'
    hd = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/94.0.4606.81 Safari/537.36' + api_token
    }
    try:
        r = requests.get(url, headers=hd, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r
    except:
        return "产生异常"
