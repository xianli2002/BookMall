from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Address, Area,AddressModelSerializer,AreaModelSerializer
import json
from utils.views import LoginRequiredJSONMixin
# Create your views here.

#获取省份信息
class  ProvinceGetAPIView(APIView):

    def get(self,request):
        try:
            provinces=Area.objects.filter(parent=None)

            provinces_list=AreaModelSerializer(instance=provinces,many=True)

        except Exception as e:
            return Response({"code":400,"errmsg":"Some errors with your database"})

        return Response({"code":0,"errmsg":"ok","province_list":provinces_list.data})


#获取区域信息
class  AreaGetAPIView(APIView):

    def get(self,request,id):
        try:
            parent_name=Area.objects.get(id=id).name
            areas=Area.objects.filter(parent=id)
            areas_list=AreaModelSerializer(instance=areas,many=True)

        except Exception as e:
            return Response({"code":400,"errmsg":"No children area data in database"})
        
        return Response({"code":0,"errmsg":"ok","sub_data":{"id":id,"area":parent_name,"subs":areas_list.data}})


class  AddressAPIView(LoginRequiredJSONMixin,APIView):
    #地址新增
    def post(self,request):
        data = request.data
        user = request.user
        receiver = data.get('receiver')
        province_id=data.get('province_id')
        city_id=data.get('city_id')
        district_id=data.get('district_id')
        detail_address=data.get('detail_address')
        mobile=data.get('mobile')
        tel=data.get('tel')
        email=data.get('email')

        if not all([user,receiver,province_id,city_id,district_id,detail_address,mobile]):
            return Response({"code":400,"errmsg":"Incomplete parameters"})

        add = Address.objects.create(user=user,title = receiver,receiver=receiver,province=Area.objects.get(id=province_id),city=Area.objects.get(id=city_id),district=Area.objects.get(id=district_id),detail_address=detail_address,mobile=mobile,tel=tel,email=email)
        address=AddressModelSerializer(instance=add)
        return Response({'code':0,'errmsg':'ok','address':address.data})

    #地址获取
    def get(self,request):
        user = request.user
        addresses = Address.objects.filter(user = user,is_deleted=False)
        addresses_list=[]
        for add in addresses:
            addresses_list.append({
            'id':add.id,
            'title':add.title,
            'receiver':add.receiver,
            'province':add.province.name,
            'city':add.city.name,
            'district':add.district.name,
            'detail_address':add.detail_address,
            'mobile':add.mobile,
            'tel':add.tel,
            'email':add.email})
        return Response({'code':0,'errmsg':'ok','addresses':addresses_list})

    #地址删除
    def delete(self,request,id):

        user=request.user
        try:
            address=Address.objects.get(id=id)
        except Exception as e:
            return Response({"code":400,"errmsg":"Address is not exist"})

        if not address.user ==user:
            return Response({"code":400,"errmsg":"No permit"})

        address.delete()

        return Response({"code":0,"errmsg":"ok"})
        
    #地址更新
    def put(self,request,id):
        
        data = request.data
        print(data)
        user = request.user
        receiver = data.get('receiver')
        province_id=data.get('province_id')
        city_id=data.get('city_id')
        district_id=data.get('district_id')
        detail_address=data.get('detail_address')
        mobile=data.get('mobile')
        tel=data.get('tel')
        email=data.get('email')

        if not all([user,receiver,province_id,city_id,district_id,detail_address,mobile]):
            return Response({"code":400,"errmsg":"Incomplete parameters"})

        try:
            add=Address.objects.filter(id=id)
        except Exception as e:
            return Response({"code":400,"errmsg":"Address is not exist"})

        if not add[0].user ==user:
            return Response({"code":400,"errmsg":"No permit"})

        add.update(title = receiver,receiver=receiver,province=Area.objects.get(id=province_id),city=Area.objects.get(id=city_id),district=Area.objects.get(id=district_id),detail_address=detail_address,mobile=mobile,tel=tel,email=email)
        address=AddressModelSerializer(instance=add[0])
        return Response({'code':0,'errmsg':'ok','address':address.data})

class TitleUpdateAPIView(APIView):
    #标题更新
    def put(self,request,id):
        data = request.data
        title = data.get('title')
        user =request.user
        try:
            address=Address.objects.get(id=id)
        except Exception as e:
            return Response({"code":400,"errmsg":"Address is not exist"})

        if not address.user ==user:
            return Response({"code":400,"errmsg":"No permit"})

        address.title=title
        address.save()
        print(str(address.title))
        return Response({"code":0,"errmsg":"ok"})