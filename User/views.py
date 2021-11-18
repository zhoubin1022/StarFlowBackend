import re


import requests
import urllib3
from django.core import serializers
from django.http import JsonResponse
from requests.adapters import HTTPAdapter

from Repository.models import Repository, Member
from Task.models import Task
from User.models import User, Join_request


class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        # 维持会话，自动处理cookies
        self.session = requests.Session()

    # 解析出登录所需要的
    def token(self):
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        res = self.session.get(self.login_url, headers=self.headers, timeout=15)
        if res.status_code == requests.codes.ok:
            authenticity_token = re.findall('<input type="hidden" name="authenticity_token" value="(.+?)" />', res.text)
            print("authenticity_token：{}".format(authenticity_token))
            return authenticity_token[1]

    def login(self, username, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': username,
            'password': password
        }
        # 登录 post 提交表单
        res_index = self.session.post(url=self.login_url, headers=self.headers, data=post_data)
        if res_index.status_code == requests.codes.ok:
            return True
        return False

    def get_request(self, repo_name, user_id):
        request_url = 'https://github.com/' + repo_name + '/pulls'
        # user = User.objects.get(user_id=user_id)[0]
        '''post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': user.username,
            'password': user.password
        }'''
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': "zhoubin1022",
            'password': "z20011022b"
        }
        res = self.session.post(url=request_url, headers=self.headers, data=post_data)
        print(res)


def test(request):
    login = Login()
    status = login.login("zhoubin1022", "z20011022b")
    if status:
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
    try:
        urllib3.disable_warnings()
        res = s.get(url=url, params=params, timeout=5, verify=False)
        print(res.text)
        return res.json()
    except requests.exceptions.RequestException as e:
        print(e)


# github登录
def githubLogin(request):
    if request.method == 'POST':
        result = {"message": 'success'}
        uid = int(request.POST.get('id'))
        username = request.POST.get('username')
        users = User.objects.filter(pk=uid)
        if not users:
            return JsonResponse({"message": '小程序登录状态出错'})
        user = users.first()
        # login = Login()
        # status = login.login(username, password)
        # if not status:
        #     return JsonResponse({"message": '账号或密码错误'})
        user.username = username
        user.save()
        return JsonResponse(result)
    return JsonResponse({"message": "请求方式错误"})


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
        req = Join_request.objects.get(pk=request_id)
        identity = int(request.POST.get('identity'))  # -1表示拒绝请求， 1表示设为管理员， 2表示设为开发者， 3表示为游客
        if identity == -1:
            req.identity = 0
            req.save()
            return JsonResponse({"message": "success"})
        # 仓库成员数+1，加入memeber表，修改请求状态
        repo = Repository.objects.get(pk=req.repo_id)
        repo.repo_member += 1
        repo.save()
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
        mem = Member.objects.filter(user_id_id=user_id)  # 查找该用户身为管理员的仓库
        if not mem:
            return JsonResponse({"message": "wrong"})
        for x in mem:
            repo_id = x.repo_id_id  # 仓库号
            reqs = Join_request.objects.filter(repo_id=repo_id, identity=-1)
            for y in reqs:
                req = {"pk": y.pk, "repo_id": repo_id, "repo_name": Repository.objects.get(pk=repo_id).repo_name,
                       "user_id": y.user_id, "user_name": User.objects.get(pk=y.user_id).username}
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
