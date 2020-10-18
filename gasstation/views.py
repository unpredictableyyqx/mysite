from django.shortcuts import render
from .models import Client
from django.http import HttpResponse


def login(request):                                # 登录
    if request.method == "POST":
        telephone = request.POST.get('telephone')
        passwd = request.POST.get('passwd')
        try:
            user = Client.objects.get(tel=telephone)
            if user.pwd != passwd:
                return HttpResponse("用户名或密码错误")
        except Client.DoesNotExist as e:
            return HttpResponse("用户不存在")
        # 登录成功
        print(telephone)
        print(passwd)
        return HttpResponse("登录成功！")
    else:
        return HttpResponse("请求错误")