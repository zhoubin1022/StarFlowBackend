import json
from datetime import datetime

import requests
from django.http import JsonResponse,HttpResponse
from requests.adapters import HTTPAdapter

from Repository.models import Repository,Member
from Task.models import Task
from django.core import serializers
from User.models import User


# 展示该用户参与的项目列表
def showRepo(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        u_id = int(request.POST.get('u_id'))  # 获取用户id
        print(u_id)
        user = User.objects.filter(pk=u_id)
        if not user:
            return JsonResponse({"message": 'id错误'})
        if not user.first().username:
            return JsonResponse({"message": "请先登录GitHub"})
        mem = Member.objects.filter(username=user.first().username)  # 找出该用户的所有仓库
        if mem:
            for x in mem:
                repo_info = {"repo": []}
                repo = Repository.objects.filter(pk=x.repo_id_id)
                repo_info['repo'] = serializers.serialize('python', repo)
                repo_info['role'] = x.identity
                repo_info['member_id'] = x.pk
                result['data'].append(repo_info)
            return JsonResponse(result)
        return JsonResponse({"message": "用户未参与项目"})
    return JsonResponse({"message": '请求方式错误'})


# 展示项目的任务列表
def showTask(request):
    if request.method == 'POST':
        result = {"message": "success", "finish": [], "checking": [], "incomplete": []}
        repo_id = int(request.POST.get('repo_id'))
        print(repo_id)
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
            # print(task['deadline'])
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


# 获取当前用户GitHub账号的所有仓库
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
        # print(json_dict)
        for i in range(len(json_dict)):
            repo = {'url': json_dict[i].get('html_url'), 'repo_name': json_dict[i].get('full_name')}
            result['data'].append(repo)
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# #根据关键词获取当前用户GitHub账号的仓库
def getReposByKeyword(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        u_id = int(request.POST.get('u_id'))
        keyword = request.POST.get('keyword')
        user = User.objects.filter(pk=u_id)
        if not user:
            return JsonResponse({"message": "用户id错误"})
        username = user.first().username
        info = getGithubRepo(username)
        json_dict = json.loads(info)
        # print(json_dict)
        for i in range(len(json_dict)):
            if not(keyword in json_dict[i].get('full_name')):
                continue
            repo = {'url': json_dict[i].get('html_url'), 'repo_name': json_dict[i].get('full_name')}
            result['data'].append(repo)
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# #获取仓库信息
def getGithubRepo(username):
    url = f"https://api.github.com/users/{username}/repos"
    print(url)
    s = requests.Session()
    headers = {"Authorization": "token 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"}
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    try:
        res = s.get(url=url, timeout=5, headers=headers)
        # print(res.json())
        return res.text
    except requests.exceptions.RequestException as e:
        print(e)


# 获取项目管理员、开发者、游客列表
def getAllMember(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": [], "owner": []}
        repo_id = int(request.POST.get('repo_id'))
        owner = Member.objects.filter(repo_id_id=repo_id, identity=0)
        if not owner:
            return JsonResponse({"message": "超级管理员出错"})
        result['owner'] = serializers.serialize('python', owner)
        developers = Member.objects.filter(repo_id_id=repo_id, identity__in=[1, 2, 3]).order_by('identity')
        if not developers:
            return JsonResponse({"message": '暂无其他参与者'})
        result["data"] = serializers.serialize('python', developers)
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 仓库人员身份调整
def changeIdentity(request):
    if request.method == 'POST':
        result = {"message": "success"}
        mem = json.loads(request.body.decode("utf-8"))
        for x in range(len(mem)):
            mem_id = mem[x]['member_id']
            try:
                member = Member.objects.get(pk=mem_id)
            except :
                return JsonResponse({"message": "member的id存在错误"})
            identity = mem[x]['identity']
            if identity == 0:
                return JsonResponse({"message": "不能修改为超级管理员"})
            if identity == -1:
                return JsonResponse({"message": "不能修改为待审核状态"})
            print(mem_id, identity)
            member.identity = identity
            member.save()
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


def test(request):
    if request.method == "POST":
        url = "https://api.github.com/users/zhoubin1022/repos"
        print(url)
        s = requests.Session()
        headers = {"Authorization": "token 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"}
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        try:
            res = s.get(url=url, timeout=10, headers=headers)
            print(res.json())
            return res.text
        except requests.exceptions.RequestException as e:
            print(e)
    return JsonResponse({"aaa"})
