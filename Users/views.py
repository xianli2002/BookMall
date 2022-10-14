from django.shortcuts import render
from .models import User
from django.views import View
from django.http import JsonResponse
import json
import re
from django.contrib.auth import login, authenticate, logout
#   判断用户名是否重复
class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code':0,'count':count,'username':username,'errmsg':'ok'})
#   判断手机号码是否重复
class MobileCountView(View):
    def get(self, request, phonenumber):
        count = User.objects.filter(phonenumber=phonenumber).count()
        return JsonResponse({'code':0,'count':count,'mobile':phonenumber,'errmsg':'ok'})
#   接收前端数据并进行验证，同时将用户数据入库
class RegisterView(View):
    def post(self, request):
        body_bytes = request.body
        body_str = body_bytes.decode('utf-8')
        body_dict = json.loads(body_str)
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        if not all([username,password,password2,mobile]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        if not re.match('[a-zA-Z0-9_-]{5,20}',username):
            return JsonResponse({'code':400,'errmsg':'用户名不满足规则'})
        if not 8<=len(password)<=20:
            return JsonResponse({'code':400,'errmsg':'密码不满足规则'})
        if password!=password2:
            return JsonResponse({'code':400,'errmsg':'确认密码与密码不一致'})
        if not re.match('1[345789]\d{9}',mobile):
            return JsonResponse({'code':400,'errmsg':'手机号不满足规则'})
        user=User.objects.create_user(username=username,password=password,phonenumber=mobile)
        login(request,user)
        return JsonResponse({'code':0,'errmsg':'ok'})
