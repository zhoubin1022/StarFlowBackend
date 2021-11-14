from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse,HttpResponse
from Repository.models import Repository,Member
from Task.models import Task
from django.core import serializers
import os
import django
from StarFlowBackend import settings


def database_query(request):  # 展示该用户参与的项目列表
    if request.method == 'POST':
        userid = int(request.POST.get('uid'))  # 获取用户id
        repository_id = Member.objects.filter(user_id=userid)  # 找出改用户的所有仓库
        for i in repository_id:  # 对仓库循环 找出仓库表中的id与repository_id相等的仓库的所有值
            records = Repository.objects.filter(id=i.repo_id)
            result = {"message": 'success', "data": serializers.serialize('python', records)}
            return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})

def database_query_task_list(request):  # 展示项目的任务列表
    if request.method == 'POST':
        repo_id = int(request.POST.get('repo_id'))  # 获取仓库id
        records1 = Repository.objects.filter(id=repo_id)  # 获取改仓库里的所有任务信息包括，完成数，待审核数等等，看前端需要什么
        records2 = Task.objects.filter(repo_id=repo_id)   # 查询Task表找出所有任务信息，包括任务状态，截至日期等等
        result = {"message": 'success', "data1": serializers.serialize('python', records1), "data2": serializers.serialize('python', records2)}
        return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})



def database_project_insert(request):  # 用户选择一个项目，把该项目放入数据库，并将当前用户设为超级管理员
    if request.method == 'POST':
        repo_member = request.POST.get('repo_member')  # 传入项目信息和用户的信息
        url = request.POST.get('url')
        repo_name = request.POST.get('repo_name')
        finished = request.POST.get('finished')
        checking = request.POST.get('checking')
        incomplete = request.POST.get('incomplete')
        username = request.POST.get('username')
        repo_id = request.POST.get('repo_id')
        user_id = request.POST.get('user_id')
        new_record_repo = Repository.objects.create(repo_member=repo_member, url=url, repo_name=repo_name, finished=finished, checking=checking, incomplete=incomplete)
        # 产生新仓库记录
        new_record_repo.save()  # 记录保存
        new_record_user = Member.objects.create(repo_id=new_record_repo.id, username=username, identity=1, user_id=user_id)
        # 产生新用户记录 identity身份信息为整数，1代表超级管理员，0代表项目普通成员，-1代表游客
        new_record_user.save()  # 记录保存
        return JsonResponse({"message": 'setting success',"data":new_record_repo.id})
    return JsonResponse({"message": 'wrong'})


def identity_change(request):  # 项目人员身份调整
    if request.method == 'POST':
        repo_id = request.POST.get('repo_id')
        user_id = request.POST.get('user_id')
        operation = request.POST.get('operation')
        repo = Repository.objects.filter(repo_id=repo_id)
        if repo.exist():   # 判断该仓库是否存在
            user=repo.objects.get(user_id__exact=user_id)
            if user.exist():  # 判断该仓库中是否存在这个用户
                if operation == 1:  # 操作码为1，表示要把这个成员身份设置成管理员
                    if user.identity == 0: # 成员原来身份是普通成员
                        user.identity = 1  # 设置为1，变为超级管理员
                        user.save()
                    elif user.identity == 1:  # 成员本来就是超级管理员
                        return JsonResponse("the member is a super manager already")

                elif operation == 0:  # 操作码为0，表示要把这个成员身份从超级管理员设置成普通成员
                    if user.identity == 1:  # 原来是超级管理员
                        user.identity = 0
                        user.save()
                    elif user.identity == 0:  # 原来是普通成员
                        return JsonResponse("the member is a common member already")
        return JsonResponse("wrong")


def aa(request):
    return HttpResponse("123123123")



