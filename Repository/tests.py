from django.test import TestCase
import os
import requests
import json

host = "http://127.0.0.1:8000/repo"
headers = {'Accept': '*/*'}

# Create your tests here.

showRepo_data = {"u_id": 1}


def test(method, url, body_data=None):
    url = host + url
    response_data = requests.post(url, data=body_data, headers=headers)
    response_data = json.loads(response_data.content.decode("utf-8"))
    if response_data['message'] == "success":
        print(url + " 成功!")
    else:
        print(url + " 失败!" + response_data['message'])


test("POST", "/showRepo", showRepo_data)
