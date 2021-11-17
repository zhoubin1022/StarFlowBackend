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
    if request.method == 'POST':
        username = request.POST.get('username')  # 获取用户名
        user_id = request.POST.get('user_id')  # 获取用户名
        repository_id = Member.objects.filter(username=username,user_id_id=user_id)  # 找出该用户的所有仓库
        if repository_id.exists():
            for i in repository_id:
                records = Repository.objects.get(id=i.repo_id_id)  # 不知道怎么存下每一个对象？？？

            return JsonResponse(result)
        else:
            return JsonResponse({"message": 'the user is not exist'})

    return JsonResponse({"message": 'wrong'})

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
        new_record_repo = Repository.objects.create(url=str(url), repo_name=str(repo_name))  #创建仓库表的一个数据
        new_record_repo.save()  # 记录保存
        #return HttpResponse(new_record_repo.id)
        new_record_member = Member.objects.create(repo_id_id=new_record_repo.id, user_id_id=user_id, username=username,identity=0)
        new_record_member.save()
        records = Repository.objects.filter(id=new_record_repo.id)  # 查询刚刚创建的仓库数据
        result = {"message": 'success', "data": serializers.serialize('python',records)}
        return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})







def identity_change(request):  # 项目人员身份调整   member中-1代表加入项目待审核、0表示超级管理员、1表示管理员、2表示开发者、3表示游客
    if request.method == 'POST':
        repo_id = request.POST.get('repo_id')
        user_id = request.POST.get('user_id')
        operation = request.POST.get('operation')
        user = Member.objects.get(user_id_id=user_id, repo_id_id=repo_id)
        if operation == '1':  # 操作码为1表示要将一个成员设置成管理员
            if user.identity == 0:
                user.identity = 1
                user.save()
                return JsonResponse({"message":'success set a  manager'})
            elif user.identity == 1:
                return JsonResponse({"message": 'the member is a  manager already'})
            elif user.identity == 3:  # 将3设置为游客身份，不能操作
                return JsonResponse({"message": 'error'})
            elif user.identity == 2:
                user.identity = 1
                user.save()
                return JsonResponse({"message": 'success set a  manager'})
        elif operation == '0':  # 操作码为0设置为超级管理员
            if user.identity == 1:
                user.identity = int(0)
                user.save()
                return JsonResponse({"message": 'success set a super manager'})
            elif user.identity == int(0):
                return JsonResponse({"message": 'the member is a super manager already'})
            elif user.identity == 2:
                user.identity = 0
                user.save()
                return JsonResponse({"message": 'success set a  super manager'})
            elif user.identity == 3:  # 将3设置为游客身份，不能操作
                return JsonResponse({"message": 'error'})
        elif operation == '2':  # 设置成开发者
            if user.identity == 1:
                user.identity = int(2)
                user.save()
                return JsonResponse({"message": 'success set a common member'})
            elif user.identity == int(0):
                user.identity = int(2)
                user.save()
                return JsonResponse({"message": 'success set common member'})
            elif user.identity == int(2):
                return JsonResponse({"message": 'the member is a common member already'})
            elif user.identity == 3:  # 将3设置为游客身份，不能操作
                return JsonResponse({"message": 'error'})

        elif operation == '3':  # 设置成游客
            if user.identity == int(1):
                user.identity = 3
                user.save()
                return JsonResponse({"message": 'success set a visitor'})
            elif user.identity == int(0):
                user.identity = 3
                user.save()
                return JsonResponse({"message": 'success set a  visitor'})
            elif user.identity == 2:
                user.identity =3
                user.save()
                return JsonResponse({"message": 'success set a  visitor'})
            elif user.identity == 3:
                return JsonResponse({"message": 'the member is visitor already'})
# 操作码错误直接报错，没有找到这个项目get函数会报错
        return JsonResponse({"message": 'wrong'})





