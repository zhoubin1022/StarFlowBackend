from django.shortcuts import render

# Create your views here.
import os
import re
from django.http import JsonResponse,HttpResponse
from Repository.models import Repository,Member
from Task.models import Task
from django.core import serializers
import os
import django
from StarFlowBackend import settings
def database_query(request):  # 展示该用户参与的项目列表
    data = []
    if request.method == 'POST':
        username = request.POST.get('username')  # 获取用户名
        repository_id = Member.objects.filter(username=username)  # 找出该用户的所有仓库
        if repository_id.exists():
            for i in repository_id:
                records = Repository.objects.get(id=i.repo_id)
                data.append(records)
            return JsonResponse(data)
        else:
            return JsonResponse({"message1": 'the user is not exist'})

    return JsonResponse({"message2": 'wrong'})

dic1={'tpye':'incomplte'}
dic2={'type':'checking'}
dic3={'type':'finish'}
def database_query_task_list(request):  # 展示项目的任务列表
    if request.method == 'POST':
        repo_id = int(request.POST.get('repo_id'))  # 获取仓库id
        # 查询Task表找出所有任务信息，包括任务状态，截至日期等等
        records1 = Task.objects.filter(repo_id=repo_id, status=0) .values('task_info','status','deadline','task_name')
        records2 = Task.objects.filter(repo_id=repo_id, status=1).values('task_info', 'status', 'deadline','task_name')
        records3 = Task.objects.filter(repo_id=repo_id, status=2).values('task_info', 'status', 'deadline','task_name')
        record = records1 | records2
        record = record | records3
        result=record.order_by("status")
        return HttpResponse(result)
    return JsonResponse({"message": 'wrong'})

def database_project_insert_one(request):  # 用户选择一个项目，把该项目放入数据库，并将当前用户设为超级管理员
    if request.method == 'POST':
        url = str(request.POST.get('url'))
        repo_name = str(request.POST.get('repo_name'))
        user_id = str(request.POST.get('user_id'))
        username = str(request.POST.get('username'))
        new_record_repo = Repository.objects.create(url=str(url), repo_name=str(repo_name))
        new_record_repo.save()  # 记录保存
        #return HttpResponse(new_record_repo.id)
        new_record_member = Member.objects.create(repo_id_id=new_record_repo.id, user_id_id=user_id, username=username,identity=1)
        new_record_member.save()
        records = Repository.objects.filter(id=new_record_repo.id)
        result = {"message": 'success', "data": serializers.serialize('python',records)}
        return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})







def identity_change(request):  # 项目人员身份调整
    if request.method == 'POST':
        repo_id = request.POST.get('repo_id')
        user_id = request.POST.get('user_id')
        operation = request.POST.get('operation')
        user = Member.objects.get(user_id=user_id, repo_id=repo_id)
        if operation == '1':  # 操作码为1表示要将一个成员设置成管理员
            if user.identity == 0:
                user.identity = 1
                user.save()
                return JsonResponse({"message":'success set a super manager'})
            elif user.identity == 1:
                return JsonResponse({"message":'the member is a super manager already'})
            elif user.identity == 2:  # 将2设置为游客身份，不能操作
                return JsonResponse({"message": '权限不足'})
        if operation == '0':  # 操作码为0表示要将管理员身份还原为普通成员
            if user.identity == 1:
                user.identity = int(0)
                user.save()
                return JsonResponse({"message": 'success set a common member'})
            elif user.identity == int(0):
                return JsonResponse({"message": 'the member is a common member already'})
            elif user.identity == 2:  # 将2设置为游客身份，不能操作
                return JsonResponse({"message": '权限不足'})
# 操作码错误直接报错，没有找到这个项目get函数会报错
        return JsonResponse({"message": 'wrong'})





