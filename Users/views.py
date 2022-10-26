import re
from django.contrib.auth import login,authenticate,logout
from Areas.models import Address
from utils.views import LoginRequiredJSONMixin
# Create your views here.
from .models import User,UserModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from Books.models import SKU
from django_redis import get_redis_connection

#检查用户名是否已存在
class usernameCountAPI(APIView):

    def get(self,request,username):


        count = User.objects.filter(username=username).count()
        return Response({'code':0,'count':count,'errmsg':'ok'})

#检查手机号是否已存在
class mobileCountAPI(APIView):
    def get(self,request,phonenumber):

        count = User.objects.filter(phonenumber=phonenumber).count()
        return Response({'code':0,'count':count,'errmsg':'ok'})

#新用户注册API
class registerNewAPI(APIView):
    def post(self,request):
        user=request.data
        username=user.get('username')
        password=user.get('password')
        password2=user.get('password2')
        mobile=user.get('mobile')
        allow=user.get('allow')

        if not all([username,password,password2,mobile,allow]):
            return Response({'code':400,'errmsg':'Incomplete parameters'})

        if not re.match('[a-zA-Z0-9_-]{5,20}',username):
            return Response({'code':400,'errmsg':'Incorrect user name'})
        
        if not password==password2:
            return Response({'code':400,'errmsg':'Password error'})

        if not re.match('1[345789]\d{9}',mobile):
            return Response({'code':400,'errmsg':'Incorrect mobilephone number'})

        if not 8<=len(password)<=20:
            return Response({'code':400,'errmsg':'Incorrect password length'})

        if not allow:
            return Response({'code':400,'errmsg':'Agreement not agreed'})

        #保存用户注册信息到数据库
        user_save=User.objects.create_user(username=username,password=password,mobile=mobile)

        login(request,user_save)

        return Response({'code':0,'errmsg':'ok'})

#用户登录API
class userloginAPI(APIView):
    def post(self,request):
        data=request.data
        username=data.get('username')
        password=data.get('password')
        remembered=data.get('remembered')

        if not all([username,password]):
            return Response({'code':400,'errmsg':'Incomplete parameters'})

        
        #判断是否是手机号登录
        if re.match('1[345789]\d{9}',username):
            User.USERNAME_FIELD='mobile'
        else:
            User.USERNAME_FIELD='username'
        
        #登录验证
        user=authenticate(username=username,password=password)
        if not user:
            return Response({'code':400,'errmsg':'Incorrect user name or password'})

        
        #是否登录保持
        if remembered:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        
        login(request,user)

        #获取登录用户信息
        a=object()
        if User.USERNAME_FIELD=='mobile':
            a=User.objects.get(mobile=username)
        else:
            a=User.objects.get(username=username)

        #制作响应信息
        response=Response({'code':0,'errmsg':'ok'})
        response.set_cookie('username',a.username)

        return response

#用户退出API
class logoutAPI(APIView):
    def delete(self,request):
        logout(request)

        response=Response({'code':0,'errmsg':'ok'})
        response.delete_cookie('username')

        return response


#用户中心进入API
class centerViewAPI(LoginRequiredJSONMixin,APIView):

    def get(self,request):
        user=request.user
        try:
            address=Address.objects.filter(user=user)
            addstr=str(address[0].province.name+address[0].city.name+address[0].district.name+address[0].detail_address)
        except:
            addstr = ''
        info=UserModelSerializer(instance=user)
        info_data = info.data
        info_data['mobile'] = info_data['phonenumber']
        return Response({'code':0,'errmsg':'ok','info_data':info_data,'address':addstr})


#用户修改密码
class passwordChangeAPI(APIView):
    def put(self,request):
        user=request.user
        data = request.data
        old_password=data.get('old_password')
        new_password=data.get('new_password')
        new_cpassword=data.get('new_password2')
        if not user.check_password(old_password):
            return Response({"code":400,"errmsg":"Inconrent password"})
        if new_cpassword!=new_password:
            return Response({"code":400,"errmsg":"Inconrent data"})

        user.set_password(new_password)
        user.save()
        response = Response({'code':0,'errmsg':'ok'})
        response.delete_cookie('username')
        return response


class UserHistoryView(LoginRequiredJSONMixin,APIView):
    #保存浏览记录
    def post(self,request):
        user=request.user
        data=request.data
        sku_id=data.get('sku_id')
        try:
            sku=SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return Response({'code':400,'errmsg':'没有此商品'})
        # 连接redis 
        redis_cli=get_redis_connection('history')
        # 去重
        redis_cli.lrem('history_%s'%user.id,0,sku_id)
        # 保存到redis中
        redis_cli.lpush('history_%s'%user.id,sku_id)
        # 只保存5条记录
        redis_cli.ltrim("history_%s"%user.id,0,9)
        return Response({'code':0,'errmsg':'ok'})


    def get(self,request):
        redis_cli=get_redis_connection('history')

        ids=redis_cli.lrange('history_%s'%request.user.id,0,9)
        history_list=[]
        for sku_id in ids:
            sku=SKU.objects.get(id=sku_id)
            history_list.append({
                'id':sku.id,
                'name':sku.name,
                'default_image_url': 'http://'+str(sku.image1),
                'price': sku.price
            })
        return Response({'code':0,'errmsg':'ok','skus':history_list})