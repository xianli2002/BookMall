from django.db import models
from rest_framework.serializers import ModelSerializer

class BooksCategory(models.Model):
    name = models.CharField(max_length=20,verbose_name = '类别')
    parent = models.ForeignKey('self', related_name='subs', null=True, blank=True, on_delete=models.CASCADE, verbose_name='父类别')
    class Meta:
        db_table = 'book_category'
        verbose_name = '书籍类别'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class BooksCategoryModelSerializer(ModelSerializer):
    class Meta:
        model=BooksCategory
        fields='__all__'

class SKU(models.Model):
    category = models.ForeignKey(BooksCategory, on_delete=models.PROTECT, verbose_name='从属类别')
    name = models.CharField(max_length=50,verbose_name = '书名')
    author = models.CharField(max_length=50,verbose_name = '作者')
    profile = models.CharField(max_length=200,verbose_name = '简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    image1 = models.ImageField(verbose_name='图片1')
    image2 = models.ImageField(verbose_name='图片2')
    image3 = models.ImageField(verbose_name='图片3')
    class Meta:
        db_table = 'books'
        verbose_name = '书籍信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class SKUModelSerializer(ModelSerializer):
    class Meta:
        model=SKU
        fields='__all__'