from django.test import TestCase
import os
import requests
import json

host = "http://127.0.0.1:8000/user"
headers = {'Accept': '*/*'}

# Create your tests here.

request_info_data = {"user": 1, "repo": 1}
repo_search_data = {"keyword": "test"}


def test(method, url, body_data=None):
    url = host + url
    response_data = requests.post(url, data=body_data, headers=headers)
    print(response_data.status_code)
    response_data = json.loads(response_data.content.decode("utf-8"))
    if response_data['message'] == "success":
        print(url + " 成功!")
    else:
        print(url + " 失败!" + response_data['message'])


test("POST", "/request_info", request_info_data)
test("POST", "/repo_search", repo_search_data)
