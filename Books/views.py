from unicodedata import category
from .models import SKU,BooksCategory, FamousBooks
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.paginator import Paginator
from rest_framework.response import Response

#   获取主页分类数据
class IndexCategoryView(APIView):
    def get(self,request):
        try:
            parents = BooksCategory.objects.filter(parent=None)
            chanels = []           
            for parent in parents:
                cat = {
                    'name':parent.name,
                    'id':parent.id,
                    'url':'http://bookmall.com:8080/list.html?cat='+str(parent.id),
                }
                childs = BooksCategory.objects.exclude(parent=None)            
                sub_cats = []
                for child in childs:
                    if child.parent == parent:
                        sub_cat = {
                            'name':child.name,
                            'id':str(child.id),
                            'url':'http://bookmall.com:8080/list.html?cat='+str(parent.id)+'&'+str(child.id),
                        }
                        sub_cats.append(sub_cat)
                cat['sub_cats']=sub_cats
                chanels.append(cat)
            return Response({'code':0,'errmsg':'ok','content_category':{'chanels':chanels}})
        except Exception as e:
            return Response({'code':400,'errmsg':'error'})

#   获取主页商品数据
class IndexBooksView(APIView):
    def get(self,request):
        try:  
            categorys = BooksCategory.objects.all()
            famous = FamousBooks.objects.all()
            parents = categorys.filter(parent=None)
            childs = categorys.exclude(parent=None)
            parents_f1 = parents
            parents_f2 = parents.get(name='文艺')
            parents_f3 = parents.get(name='教育')
            childs_f1 = childs
            childs_f2 = childs.filter(parent=parents_f2)
            childs_f3 = childs.filter(parent=parents_f3)
            books = SKU.objects.all()
            books_f1 = books.filter(category__in=childs_f1)
            books_f2 = books.filter(category__in=childs_f2)
            books_f2 = books_f2.filter(id__in=[value.book.id for value in famous])
            books_f3 = books.filter(category__in=childs_f3)
            books_f1_1 = books_f1.filter(category__in=childs_f1.filter(parent=parents_f1.get(name='童书')))[:10]
            books_f1_2 = books_f1.filter(category__in=childs_f1.filter(parent=parents_f1.get(name='人文社科')))[:10]
            books_f1_3 = books_f1.filter(category__in=childs_f1.exclude(parent=parents_f1.get(name='童书')).exclude(parent=parents_f1.get(name='人文社科')))[:10]
            books_f1_0 = books_f1.order_by('-sales')[:3]
            books_f2_1 = books_f2.filter(category__in=childs_f2.filter(name='文学'))[:10]
            books_f2_2 = books_f2.filter(category__in=childs_f2.filter(name='小说'))[:10]
            books_f2_0 = books_f2.order_by('-sales')[:3]
            books_f3_1 = books_f3.filter(category__in=childs_f3.filter(name='中小学用书'))[:10]
            books_f3_2 = books_f3.filter(category__in=childs_f3.filter(name='大中专教材'))[:10]
            books_f3_0 = books_f3.order_by('-sales')[:3]
            goods_on_index={'1F':{'1':[],'2':[],'3':[],'0':[]},'2F':{'1':[],'2':[],'0':[]},'3F':{'1':[],'2':[],'0':[]}}
            goods_on_index['1F']['1']=self.books_to_json(books_f1_1)
            goods_on_index['1F']['2']=self.books_to_json(books_f1_2)
            goods_on_index['1F']['3']=self.books_to_json(books_f1_3)
            goods_on_index['1F']['0']=self.books_to_json(books_f1_0)
            goods_on_index['2F']['1']=self.books_to_json(books_f2_1)
            goods_on_index['2F']['2']=self.books_to_json(books_f2_2)
            goods_on_index['2F']['0']=self.books_to_json(books_f2_0)
            goods_on_index['3F']['1']=self.books_to_json(books_f3_1)
            goods_on_index['3F']['2']=self.books_to_json(books_f3_2)
            goods_on_index['3F']['0']=self.books_to_json(books_f3_0)
            return Response({'code':0,'errmsg':'ok','goods_on_index':goods_on_index})
        except Exception as e:
            return Response({'code':400,'errmsg':'error'})
    
    def books_to_json(self,books):
        books_list=[]
        for book in books:
            book_dic = {
                'title':book.name,
                'url':'http://bookmall.com:8080/goods/'+str(book.id)+'.html',
                'image_url':'http://'+str(book.image1),
                'text':book.price,
            }
            books_list.append(book_dic)
        return books_list
    
    #   获取相应类别的书籍信息
    def get_category_book(self,category):
        try:
            categorys = BooksCategory.objects.all()
            books = SKU.objects.all()
            categorys_need = categorys.get(name=category)
            if categorys_need.parent == None:
                category_need_child = categorys.filter(parent=categorys_need)
                books_need = books.filter(category__in=category_need_child)
            else:
                books_need = books.filter(category__in=categorys_need)
            return books_need
        except Exception as e:
            print('无相应类别书籍')
            return None


class ListView(APIView):
    def get(self,request,category):
        ordering = request.GET.get('ordering')
        page_size = request.GET.get('page_size')
        page = request.GET.get('page')
        skus,cat1,cat2 = self.get_category_book_id(category)
        paginator = Paginator(skus,per_page=page_size)
        page_skus = paginator.page(page)
        sku_list = []
        for sku in page_skus.object_list:
            sku_list.append({
                'id':sku.id,
                'name':sku.name,
                'price':sku.price,
                'default_image_url':'http://'+str(sku.image1)
            })
        total_num = paginator.num_pages
        if cat2 == '':
            return Response({'code':0,'errmsg':'ok','list':sku_list,'count':total_num,'breadcrumb':{'cat1':{'name':cat1.name,'url':'http://bookmall.com:8080/list.html?cat='+str(cat1.id)},'cat2':{'name':'','url':'http://bookmall.com:8080/list.html?cat='+str(cat1.id)}}})
        return Response({'code':0,'errmsg':'ok','list':sku_list,'count':total_num,'breadcrumb':{'cat1':{'name':cat1.name,'url':'http://bookmall.com:8080/list.html?cat='+str(cat1.id)},'cat2':{'name':cat2.name,'url':'http://bookmall.com:8080/list.html?cat='+str(cat1.id)+'&'+str(cat2.id)}}})
    
    def get_category_book_id(self,id):
        try:
            categorys = BooksCategory.objects.all()
            books = SKU.objects.all()
            categorys_need = categorys.get(id=id)
            if categorys_need.parent == None:
                category_need_child = categorys.filter(parent=categorys_need)
                books_need = books.filter(category__in=category_need_child)
                return books_need,categorys_need,''
            else:
                books_need = books.filter(category=categorys_need)
                return books_need,categorys_need.parent,categorys_need
        except Exception as e:
            print('无相应类别书籍')
            return None

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
