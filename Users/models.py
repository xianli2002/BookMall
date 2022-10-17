from django.db import models
from django.contrib.auth.models import AbstractUser

# 用户类
class User(AbstractUser):
    phonenumber = models.CharField(max_length=11,verbose_name = '手机号')
    default_address = models.ForeignKey('Areas.Address',related_name='user_address',null=True,blank=True,on_delete=models.SET_NULL,verbose_name='默认地址')
    class Meta:
        db_table = 'Users'
        verbose_name = '用户'
        verbose_name_plural =verbose_name