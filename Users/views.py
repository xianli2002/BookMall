from django.shortcuts import render
from .models import User
from django.views import View
from django.http import JsonResponse
import json
import re
from django.contrib.auth import login, authenticate, logout
from utils.views import LoginRequiredJSONMixin

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
#   登录数据验证
class LoginView(View):
    def post(self,request):
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')
        if not all([username,password]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        if re.match('1[345789]\d{9}',username):
            User.USERNAME_FIELD='phonenumber'
        else:
            User.USERNAME_FIELD='username'
        user = authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'code':400,'errmsg':'账号或密码错误'})
        if remembered is not None:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        login(request,user)
        a = object()
        if User.USERNAME_FIELD == 'phonenumber':
            a = User.objects.get(phonenumber=username)
        else:
            a = User.objects.get(username=username)
        response = JsonResponse({'code':0,'errmsg':'ok'})
        response.set_cookie('username',a.username)
        print(response.cookies)
        return response
#   退出登录
class LogoutView(View):
    def delete(self,request):
        logout(request)
        response = JsonResponse({'code':0,'errmsg':'ok'})
        response.delete_cookie('username')
        return response
    
#   获取用户信息
class InfoView(LoginRequiredJSONMixin,View):
    def get(self,request):
        info_data={
            'username':request.user.username,
            'mobile':request.user.phonenumber,
        }
        return JsonResponse({'code':0,'errmsg':'ok','info_data':info_data})

#   修改密码
class PasswordView(View):
    def put(self,request):
        body_bytes = request.body
        body_str = body_bytes.decode('utf-8')
        body_dict = json.loads(body_str)
        username = body_dict.get('username')
        old_password = body_dict.get('old_password')
        new_password = body_dict.get('new_password')
        new_password2 = body_dict.get('new_password2')
        user = authenticate(username=username,password=old_password)
        if user is None:
            return JsonResponse({'code':400,'errmsg':'与原密码不一致'})
        if not 8<=len(new_password)<=20:
            return JsonResponse({'code':400,'errmsg':'密码不满足规则'})
        if new_password!=new_password2:
            return JsonResponse({'code':400,'errmsg':'确认密码与密码不一致'})       
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        return JsonResponse({'code':0,'errmsg':'ok'})     

#   修改用户信息
class ChangeinfoView(LoginRequiredJSONMixin,View):
    def put(self, request):
        body_bytes = request.body
        body_str = body_bytes.decode('utf-8')
        body_dict = json.loads(body_str)
        old_username = body_dict.get('old_username')
        username = body_dict.get('new_username')
        mobile = body_dict.get('new_mobile')     
        if not re.match('[a-zA-Z0-9_-]{5,20}',username):
            return JsonResponse({'code':400,'errmsg':'用户名不满足规则'})
        if not re.match('1[345789]\d{9}',mobile):
            return JsonResponse({'code':400,'errmsg':'手机号不满足规则'})
        user = User.objects.get(username=old_username)
        user.username = username
        user.phonenumber = mobile
        user.save()
        return JsonResponse({'code':0,'errmsg':'ok'})