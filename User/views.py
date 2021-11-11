import requests
from django.core import serializers
from django.http import JsonResponse
from User.models import User


# 微信登录
def wxLogin(request):
    if request.method == 'POST':
        result = {"message": 'success', "data": []}
        code = request.POST.get('code')
        user_info = getUserInfo(code)
        openid = user_info['openid']
        session_key = user_info['session_key']
        new_user = User(openid=openid, session_key=session_key)
        new_user.save()
        user = User.objects.filter(openid=openid)
        result['data'] = serializers.serialize('python', user)
        return JsonResponse(result)


# 根据code获取相应信息
def getUserInfo(code):
    params = {
        "appid": '',
        "secret": '',
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
