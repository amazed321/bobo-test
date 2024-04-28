from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from www.forms.account import LoginForm, SmsLoginForm, SendSmsForm
from www import models
from django.shortcuts import HttpResponse


def login(request):
    # 1.GET请求看到登录页面
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    # 2.用户提交
    # 2.1 是否为空
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, "login.html", {"form": form})

    # 2.2 去数据库校验：客户表？管理员表？
    data_dict = form.cleaned_data  # {role：1，username:11,passwrod:123}
    role = data_dict.pop("role")
    print(data_dict)
    if role == "1":
        user_object = models.Administrator.objects.filter(**data_dict).filter(active=1).first()
    else:
        user_object = models.Customer.objects.filter(**data_dict).filter(active=1).first()

    # 2.3 数据不存在
    if not user_object:
        form.add_error("password", "用户名或密码错误")
        return render(request, "login.html", {"form": form})

    # 2.4 数据存在，将用户信息存储session
    mapping = {"1": "ADMIN", "2": "CUSTOMER"}
    request.session[settings.NB_SESSION_KEY] = {
        "role": mapping[role],  # "ADMIN"  "CUSTOMER"
        "id": user_object.id,
        "name": user_object.username,
    }

    # 2.5 成功，跳转后台
    return redirect(settings.HOME_URL)


def logout(request):
    request.session.clear()
    return redirect("login")


def sms_login(request):
    # 1.GET请求看到登录页面
    if request.method == "GET":
        form = SmsLoginForm()
        return render(request, "sms_login.html", {"form": form})

    print(request.META)
    # 2.格式校验（手机号+验证码）
    # 3.验证码是否正确？手机号去redis中校验
    form = SmsLoginForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"status": False, "msg": form.errors})

    # 4.去数据库中读取用户信息 + 保存Session
    role = form.cleaned_data['role']
    mobile = form.cleaned_data['mobile']
    if role == "1":
        user_object = models.Administrator.objects.filter(mobile=mobile).filter(active=1).first()
    else:
        user_object = models.Customer.objects.filter(mobile=mobile).filter(active=1).first()

    # 5.数据不存在
    if not user_object:
        return JsonResponse({"status": False, "msg": {"mobile": ["手机号不存在"]}})

    # 2.4 数据存在，将用户信息存储session
    mapping = {"1": "ADMIN", "2": "CUSTOMER"}
    request.session[settings.NB_SESSION_KEY] = {
        "role": mapping[role],  # "ADMIN"  "CUSTOMER"
        "id": user_object.id,
        "name": user_object.username,
    }
    return JsonResponse({"status": True, "msg": "OK", "data": settings.HOME_URL})


@csrf_exempt
def send_sms(request):
    """ 发送短信"""
    # 1.校验手机格式是否正确（是否已经注册？）
    # 2.校验手机号发送频率（第三方短信平台）
    # 3.生成短信验证码 + 发送
    form = SendSmsForm(data=request.POST)
    if not form.is_valid():
        return JsonResponse({"status": False, "msg": form.errors})

    return JsonResponse({"status": True, "msg": "OK"})


def home(request):
    return render(request, "home.html")


def user(request):
    # return HttpResponse("USER")
    return render(request, "user.html")


def add_user(request):
    # return HttpResponse("USER")
    return render(request, "add_user.html")


def multi_import(request):
    # return HttpResponse("multi_import")
    return render(request, "multi_import.html")


def edit_user(request, uid):
    return HttpResponse("edit_user")
