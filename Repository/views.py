from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponse
from Repositpry.models import Repository,Member
from StarFlowBackend import settings


def databasequery(request):  # 展示该用户参与的项目列表
    if request.method =='POST':
        userid= int(request.POST.get('uid'))
        repository_id=Repository_member.objects.filter(user_id=userid)
        records=Repository_reposiry.objects.filter(repo_id=repository_id)
        result = {"message": 'success', "data": serializers.serialize('python', records)}
        return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})

def database_query_tasklist(request):  #展示项目的任务列表
    if request.method=='POST':
        userid = int(request.POST.get('repo_id'))
        repository_id = Repository_member.objects.filter(user_id=userid)
        records = Task_task.objects.filter(repo_id=repository_id)
        result = {"message": 'success', "data": serializers.serialize('python', records)}
        return JsonResponse(result)
    return JsonResponse({"message": 'wrong'})



def database_project_insert(request):  # 用户选择一个项目，把该项目放入数据库，并将当前用户设为超级管理员
    if request.method == 'POST':
        repo_member=request.POST.get('repo_member')
        url = request.POST.get('url')
        repo_name =request.POST.get('repo_name')
        finished =request.POST.get('finished')
        checking = request.POST.get('checking')
        incomplete = request.POST.get('incomplete')
        insert_records=
def databasedelete():  # 数据库删除操作

def databasemodify():  # 数据库数据修改