from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.




import requests
import json

host = "http://37446r369t.zicp.vip"
POST = "POST"
GET = "GET"
headers = {'content-Type': 'application/json', 'Accept': '*/*'}
def test(method,url,data):
    url = host + url
    if method == POST:
        response_data = requests.post(url,data=data, headers=headers)
    response_data = response_data.content.decode("utf-8")
    print(url + " 成功 " + response_data)


    # 展示该用户参与的项目列表
    test(POST, "/database_query",data={'uid': 1})
    # 展示项目的任务列表
    test(POST, "/database_query_task_list",data={'repo_id': 1})
    # 用户选择一个项目，把该项目放入数据库，并将当前用户设为超级管理员
    test(POST, "/database_project_insert", data={'repo_member': 1, 'url': "https://github.com/zhoubin1022/test",
                                                 'repo_name': "zhoubin1022/test", 'finished':0,'checking':0, 'incomplete': 0,
                                                 'username': "zhoubin1022", 'repo_id': 1, 'user_id': 1})
    # 项目人员身份调整
    test(POST, "/identity_change", data={'repo_id': 1,'user_id': 1,'operation': 1})
