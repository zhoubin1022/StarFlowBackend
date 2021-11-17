import json
from datetime import datetime

import requests
from django.http import JsonResponse,HttpResponse
from requests.adapters import HTTPAdapter

from Repository.models import Repository,Member
from Task.models import Task
from django.core import serializers
from User.models import User


def identity_change(request):  # 项目人员身份调整   member中-1代表加入项目待审核、0表示超级管理员、1表示管理员、2表示开发者、3表示游客
    if request.method == 'POST':
        repo_id = request.POST.get('repo_id')
        user_id = request.POST.get('user_id')
        operation = request.POST.get('operation')
        user = Member.objects.get(user_id_id=user_id, repo_id_id=repo_id)
        if operation == '1':  # 操作码为1表示要将一个成员设置成管理员
            if user.identity == 0:
                user.identity = 1
                user.save()
                return JsonResponse({"message":'success set a  manager'})
            elif user.identity == 1:
                return JsonResponse({"message": 'the member is a  manager already'})
            elif user.identity == 3:  # 将3设置为游客身份，不能操作
                return JsonResponse({"message": 'error'})
            elif user.identity == 2:
                user.identity = 1
                user.save()
                return JsonResponse({"message": 'success set a  manager'})
        elif operation == '0':  # 操作码为0设置为超级管理员
            if user.identity == 1:
                user.identity = int(0)
                user.save()
                return JsonResponse({"message": 'success set a super manager'})
            elif user.identity == int(0):
                return JsonResponse({"message": 'the member is a super manager already'})
            elif user.identity == 2:
                user.identity = 0
                user.save()
                return JsonResponse({"message": 'success set a  super manager'})
            elif user.identity == 3:  # 将3设置为游客身份，不能操作
                return JsonResponse({"message": 'error'})
        elif operation == '2':  # 设置成开发者
            if user.identity == 1:
                user.identity = int(2)
                user.save()
                return JsonResponse({"message": 'success set a common member'})
            elif user.identity == int(0):
                user.identity = int(2)
                user.save()
                return JsonResponse({"message": 'success set common member'})
            elif user.identity == int(2):
                return JsonResponse({"message": 'the member is a common member already'})
            elif user.identity == 3:  # 将3设置为游客身份，不能操作
                return JsonResponse({"message": 'error'})

        elif operation == '3':  # 设置成游客
            if user.identity == int(1):
                user.identity = 3
                user.save()
                return JsonResponse({"message": 'success set a visitor'})
            elif user.identity == int(0):
                user.identity = 3
                user.save()
                return JsonResponse({"message": 'success set a  visitor'})
            elif user.identity == 2:
                user.identity =3
                user.save()
                return JsonResponse({"message": 'success set a  visitor'})
            elif user.identity == 3:
                return JsonResponse({"message": 'the member is visitor already'})
# 操作码错误直接报错，没有找到这个项目get函数会报错
        return JsonResponse({"message": 'wrong'})


# 展示该用户参与的项目列表
def showRepo(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        u_id = int(request.POST.get('u_id'))  # 获取用户名
        user = User.objects.filter(pk=u_id)
        if not user:
            return JsonResponse({"message": 'id错误'})
        mem = Member.objects.filter(username=user.first().username)  # 找出该用户的所有仓库
        if mem:
            for x in mem:
                repo_info = {"repo": []}
                repo = Repository.objects.filter(pk=x.repo_id_id)
                repo_info['repo'] = serializers.serialize('python', repo)
                repo_info['member'] = x.identity
                result['data'].append(repo_info)
            return JsonResponse(result)
        return JsonResponse({"message": "用户未参与项目"})
    return JsonResponse({"message": '请求方式错误'})


# 展示项目的任务列表
def showTask(request):
    if request.method == 'POST':
        result = {"message": "success", "finish": [], "checking": [], "incomplete": []}
        repo_id = int(request.POST.get('repo_id'))
        repos = Repository.objects.filter(pk=repo_id)
        if not repos:
            return JsonResponse({"message": "仓库id错误"})
        tasks = Task.objects.filter(repo_id=repo_id)
        if not tasks:
            return JsonResponse({"message": "当前项目没有任务"})
        # print(tasks)
        for x in tasks:  # 0代表未完成。1代表待审核，2代表已完成
            task = {'task_name': x.task_name, 'task_info': x.task_info, 'task_id': x.pk, 'repo_id': x.repo_id,
                    'member_id': x.member_id}
            # print(task)
            ddl = x.deadline
            task['deadline'] = [ddl.year, ddl.month, ddl.day, ddl.hour, ddl.minute, ddl.second]
            print(task['deadline'])
            mem = Member.objects.filter(pk=x.member_id)
            if not mem:
                return JsonResponse({"message": "任务所分配给的成员不存在"})
            user = User.objects.filter(pk=mem.first().user_id_id)
            if not user:
                return JsonResponse({"message": "任务所分配给的成员不存在"})
            task['member_name'] = user.first().username
            if x.status == 0:
                result['incomplete'].append(task)
            elif x.status == 1:
                result['checking'].append(task)
            elif x.status == 2:
                result['finish'].append(task)
            else:
                return JsonResponse({"message": "任务状态异常"})
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 添加项目
def addRepo(request):
    if request.method == 'POST':
        url = str(request.POST.get('url'))
        repo_name = str(request.POST.get('repo_name'))
        user_id = int(request.POST.get('user_id'))
        user = User.objects.filter(pk=user_id)
        if not user:
            return JsonResponse({"message": "用户id错误"})
        username = user.first().username
        new_repo = Repository(url=url, repo_name=repo_name)
        new_repo.save()
        repo_id = Repository.objects.get(url=url).pk
        new_member = Member(repo_id_id=repo_id, user_id_id=user_id, username=username, identity=0)
        new_member.save()
        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "请求方式错误"})


# #获取当前用户GitHub账号的所有仓库
def getRepos(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        u_id = int(request.POST.get('u_id'))
        user = User.objects.filter(pk=u_id)
        if not user:
            return JsonResponse({"message": "用户id错误"})
        username = user.first().username
        info = getGithubRepo(username)
        json_dict = json.loads(info)
        for i in range(len(json_dict)):
            repo = {'url': json_dict[i].get('html_url'), 'repo_name': json_dict[i].get('full_name')}
            result['data'].append(repo)
    return JsonResponse(result)


# #获取仓库信息
def getGithubRepo(username):
    url = f"https://api.github.com/users/{username}/repos"
    print(url)
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    try:
        res = s.get(url=url, timeout=5)
        # print(res.json())
        return res.text
    except requests.exceptions.RequestException as e:
        print(e)


# 仓库人员身份调整
def changeIdentity(request):
    if request.method == 'POST':
        return JsonResponse({})
    return JsonResponse({"message": "请求方式错误"})
