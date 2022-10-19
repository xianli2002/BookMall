from unicodedata import category
from django.shortcuts import render
from .models import SKU,BooksCategory
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.paginator import Paginator
from rest_framework.response import Response

#   获取主页分类数据
class IndexCategoryView(APIView):
    def get(self,request):
        try:
            categorys = BooksCategory.objects.filter(parent=None)
            chanels = []           
            for category in categorys:
                cat = {
                    'name':category.name,
                    'id':category.id,
                    'url':'http://bookmall.com:8080/categorys/'+str(category.id),
                }
                childs = BooksCategory.objects.exclude(parent=None)            
                sub_cats = []
                for child in childs:
                    if child.parent == category:
                        sub_cat = {
                            'name':child.name,
                            'id':child.id,
                            'url':'http://bookmall.com:8080/categorys/'+str(category.id)+'/'+str(child.id),
                        }
                        sub_cats.append(sub_cat)
                cat['sub_cats']=sub_cats
                chanels.append(cat)
            return Response({'code':0,'errmsg':'ok','content_category':{'chanels':chanels}})
        except Exception as e:
            return Response({'code':400,'errmsg':'error'})

#   获取主页商品数据
class IndexBooksView(APIView):
    def get():
        pass

class ListView(APIView):
    def get(self,request,category):
        ordering = request.GET.get('ordering')
        page_size = request.GET.get('page_size')
        page = request.GET.get('page')
        skus = SKU.objects.filter(category=category).order_by(ordering)
        paginator = Paginator(skus,per_page=page_size)
        page_skus = paginator.page(page)
        sku_list = []
        for sku in page_skus.object_list:
            sku_list.append({
                'id':sku.id,
                'name':sku.name,
                'price':sku.price,
                'image_url':sku.image1
            })
        total_num = paginator.num_pages
        return Response({'code':0,'errmsg':'ok','list':sku_list,'count':total_num,'breadcrumb':''})

#   商品详情页
class DetailView(APIView):
    def get(self,request,sku_id):
        try:
            sku=SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({"code":404,"errmag":"not exist"})
        context = {
            'categories': '',
            'breadcrumb': '',
            'sku': {                
                'labels':sku.category,
                'goodsname':sku.name,
                'price':sku.price,
                'image':sku.image1
                },
            'specs': '',
        }
        return Response({"code":0,"errmag":"ok","context":context})

# Create your views here.
