from django.test import TestCase
import os
import requests
import json

host = "http://127.0.0.1:8000/task"
headers = {'Accept': '*/*'}

# Create your tests here.

developer_data = {"repo_id": 1}


def test(method, url, body_data=None, query_string=None, rest_query_string=None):
    url = host + url
    response_data = requests.post(url, data=body_data, headers=headers)
    response_data = json.loads(response_data.content.decode("utf-8"))
    if response_data['message'] == "success":
        print(url + " 成功!")
    else:
        print(url + " 失败!" + response_data['message'])


test("POST", "/developer", developer_data)
