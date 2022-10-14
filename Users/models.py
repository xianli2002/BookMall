from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 用户类
class User(AbstractUser):
    email = models.CharField(max_length=30,verbose_name = '邮箱')
    class Meta:
        db_table = 'Users'
        verbose_name = '用户'
        verbose_name_plural =verbose_name
