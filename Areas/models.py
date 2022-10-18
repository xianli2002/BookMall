from django.db import models
from rest_framework.serializers import ModelSerializer
# Create your models here.
#区域类
class Area(models.Model):
    name = models.CharField(max_length=40,verbose_name='名称')
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,related_name='subs',null=True,blank=True,verbose_name='上级行政区')


    class Meta:
        db_table='areas'
        verbose_name='省市区'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name


class AreaModelSerializer(ModelSerializer):

    class Meta:
        model=Area
        fields='__all__'


#地址类

class Address(models.Model):
    user =models.ForeignKey('Users.User',on_delete=models.CASCADE,related_name='addresses')
    title = models.CharField(max_length=30,null=True)
    receiver = models.CharField(max_length=20)
    province = models.ForeignKey('Area',on_delete=models.PROTECT,related_name='province')
    city = models.ForeignKey('Area',on_delete=models.PROTECT,related_name='city')
    district = models.ForeignKey('Area',on_delete=models.PROTECT,related_name='district')
    detail_address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=11)
    tel=models.CharField(max_length=20,null=True,blank=True,default='')
    email=models.CharField(max_length=30,null=True,blank=True,default='')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['user']

class AddressModelSerializer(ModelSerializer):
    class Meta:
        model=Address
        fields='__all__'
