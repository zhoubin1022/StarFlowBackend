import json
import re


import requests
import urllib3
from django.core import serializers
from django.http import JsonResponse
from requests.adapters import HTTPAdapter

from Repository.models import Repository, Member
from Task.models import Task
from User.models import User, Join_request


def test(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        print(getUsername(token))
        return JsonResponse({"status": "yes"})
    return JsonResponse({"status": "no"})


# 微信登录
def wxLogin(request):
    if request.method == 'POST':
        result = {"status": 0}  # 0表示不存在已创建，1表示已存在
        code = request.POST.get('code')
        print(code)
        user_info = getUserInfo(code)
        print(111)
        openid = user_info['openid']
        print(openid)
        session_key = user_info['session_key']
        print(session_key)
        user = User.objects.filter(openid=openid)
        if user:
            result['id'] = user.first().pk
            result['username'] = user.first().username
            result['status'] = 1
            print(result)
            return JsonResponse(result)
        new_user = User(openid=openid, session_key=session_key)
        new_user.save()
        user = User.objects.filter(openid=openid)
        result['id'] = user.first().pk
        result['username'] = user.first().username
        print(result)
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 根据code获取相应信息
def getUserInfo(code):
    params = {
        "appid": 'wx153042b6c64c0ef4',
        "secret": 'a0319e9533871389be9239e289029a98',
        "js_code": code,
        "grant_type": 'authorization_code'
    }
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    print(url)
    try:
        urllib3.disable_warnings()
        res = s.get(url=url, params=params, timeout=5, verify=False)
        print(res.status_code)
        print(res.text)
        return res.json()
    except requests.exceptions.RequestException as e:
        print(e)


# github登录
def githubLogin(request):
    if request.method == 'POST':
        result = {"message": 'success'}
        uid = int(request.POST.get('id'))
        token = request.POST.get('token')
        print(id)
        users = User.objects.filter(pk=uid)
        if not users:
            return JsonResponse({"message": '小程序登录状态出错'})
        user = users.first()
        username = getUsername(token)
        if username == "":
            return JsonResponse({"message": 'token有误'})
        user.username = username
        mem = Member.objects.filter(user_id_id=user.pk)
        for x in mem:
            x.username = username
            x.save()
        user.token = token
        user.save()
        result['username'] = username
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 获取token对应的用户名
def getUsername(token):
    url = "https://api.github.com/user"
    print(url)
    s = requests.Session()
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
        "Accept": "application/vnd.github.cloak-preview+json",
        "Authorization": "token " + token,
    }
    print(headers['Authorization'])
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    try:
        res = s.get(url=url, timeout=10, headers=headers)
        # res = requests.get(url=url, headers=headers)
        print(1)
        if res.status_code != requests.codes.ok:
            return ""
        json_dict = json.loads(res.text)
        return json_dict['login']
    except requests.exceptions.RequestException as e:
        print(e)


# 加入项目请求
def repo_request(request):
    if request.method == 'POST':
        user_id = int(request.POST.get('user'))
        repo_id = int(request.POST.get('repo'))
        print(user_id)
        print(repo_id)
        user = User.objects.get(pk=user_id)
        if not user:
            return JsonResponse({"message": "用户信息错误"})
        repo = Repository.objects.get(pk=repo_id)
        if not repo:
            return JsonResponse({"message": "仓库信息错误"})
        mem = Member.objects.filter(user_id_id=user_id, repo_id_id=repo_id)
        if mem:
            if mem.first().identity == -2:
                x = Join_request.objects.filter(user_id=user_id, repo_id=repo_id)
                if x:
                    x_join = x.first()
                    x_join.identity = -1
                    x_join.save()
                    return JsonResponse({"message": "success"})
            else:
                return JsonResponse({"message": "您已在该项目中"})
        join = Join_request.objects.filter(user_id=user_id, repo_id=repo_id, identity=-1)
        if join:
            return JsonResponse({"message": "您已发送申请，请稍等片刻"})
        new_request = Join_request(user_id=user_id, repo_id=repo_id)
        new_request.save()
        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "请求方式错误"})


# 管理员处理请求
def reply_request(request):
    if request.method == 'POST':
        request_id = int(request.POST.get('request_id'))
        try:
            req = Join_request.objects.get(pk=request_id)
        except:
            return JsonResponse({"message": "不存在该申请"})
        identity = int(request.POST.get('identity'))  # -1表示拒绝请求， 1表示设为管理员， 2表示设为开发者， 3表示为游客
        print(request_id, identity)
        if identity == -1:
            req.identity = 0
            req.save()
            return JsonResponse({"message": "success"})
        # 仓库成员数+1，加入memeber表，修改请求状态
        repo = Repository.objects.get(pk=req.repo_id)
        repo.repo_member += 1
        repo.save()
        mem = Member.objects.filter(repo_id_id=req.repo_id, user_id_id=req.user_id)
        if mem:
            new_member = mem.first()
            new_member.identity = identity
            req.identity = 1
            req.save()
            new_member.save()
            return JsonResponse({"message": "success"})
        new_member = Member(repo_id_id=req.repo_id, user_id_id=req.user_id,
                            username=User.objects.get(pk=req.user_id).username, identity=identity)
        new_member.save()
        req.identity = 1
        req.save()
        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "请求方式错误"})


# 查询加入项目请求的信息列表
def request_info(request):
    if request.method == 'POST':
        result = {"message": "success", "data": []}
        user_id = int(request.POST.get('user'))  # 用户id
        print(user_id)
        repo_id = int(request.POST.get('repo'))
        print(repo_id)
        try:
            x = Member.objects.get(user_id_id=user_id, repo_id_id=repo_id, identity__in=[0, 1])  # 查找该用户身为管理员的仓库
        except:
            return JsonResponse({"message": "参数错误或不是管理员"})
        reqs = Join_request.objects.filter(repo_id=repo_id, identity=-1)
        for y in reqs:
            req = {"pk": y.pk, "repo_id": repo_id, "repo_name": Repository.objects.get(pk=repo_id).repo_name,
                   "user_id": y.user_id, "user_name": User.objects.get(pk=y.user_id).username}
            r_time = y.request_time
            req['request_time'] = [r_time.year, r_time.month, r_time.day, r_time.hour, r_time.minute, r_time.second]
            result['data'].append(req)
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 项目查询
def repo_search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        print(keyword)
        repos = Repository.objects.filter(repo_name__icontains=keyword)
        if not repos:
            return JsonResponse({"message": "该关键词无对应仓库"})
        result = {"message": "success", "data": serializers.serialize("python", repos)}
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


# 返回申请人数
def request_num(request):
    if request.method == 'POST':
        result = {"message": "success", "num": 0}
        repo_id = int(request.POST.get('repo_id'))
        print(repo_id)
        result['num'] = Join_request.objects.filter(repo_id=repo_id, identity=-1).count()
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})
