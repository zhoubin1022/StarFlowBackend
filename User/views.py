from lxml import html
from xml import etree

import requests
from django.core import serializers
from django.http import JsonResponse
from User.models import User


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
        res = self.session.get(self.login_url, headers=self.headers)
        if res.status_code == requests.codes.ok:
            res_obj = html.etree.HTML(res.text)
            token_value = res_obj.xpath('//div[@id="login"]/form/input[@name="authenticity_token"]/@value')[0]
            return token_value

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
    login.get_request("django/django", 1)
    return JsonResponse({})


# 微信登录
def wxLogin(request):
    if request.method == 'POST':
        result = {"status": 0, "data": []}  # 0表示不存在已创建，1表示已存在
        code = request.POST.get('code')
        user_info = getUserInfo(code)
        openid = user_info['openid']
        session_key = user_info['session_key']
        user = User.objects.filter(openid=openid)
        if user:
            result['data'] = serializers.serialize('python', user)
            result['status'] = 1
            return JsonResponse(result)
        new_user = User(openid=openid, session_key=session_key)
        new_user.save()
        user = User.objects.filter(openid=openid)
        result['data'] = serializers.serialize('python', user)
        return JsonResponse(result)


# 根据code获取相应信息
def getUserInfo(code):
    params = {
        "appid": 'wx153042b6c64c0ef4',
        "secret": 'a0319e9533871389be9239e289029a98',
        "js_code": code,
        "grant_type": 'authorization_code'
    }
    result = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=params, timeout=3, verify=False)
    return result.json()


# github登录
def githubLogin(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        openid = request.POST.get('openid')
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.filter(openid=openid)
        if not users:
            return JsonResponse({"message": '小程序登录状态出错'})
        user = users.first()
        if not (user.openid == openid):
            return JsonResponse({"message": '小程序登录状态错误'})

        user.username = username
        user.password = password
        user.save()
        return JsonResponse(result)
