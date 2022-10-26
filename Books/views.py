from .models import SKU,BooksCategory, FamousBooks
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.paginator import Paginator
from rest_framework.response import Response
from haystack.views import SearchView
from django_redis import get_redis_connection
import pickle
import base64

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
                'url':'http://bookmall.com:8080/detail.html?book='+str(book.id),
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

#   获取商品列表
class ListView(APIView):
    def get(self,request,category):
        ordering = request.GET.get('ordering')
        page_size = request.GET.get('page_size')
        page = request.GET.get('page')
        skus,cat1,cat2 = self.get_category_book_id(category)
        skus = skus.order_by(ordering)
        paginator = Paginator(skus,per_page=page_size)
        page_skus = paginator.page(page)
        skus = []
        for sku in page_skus.object_list:
            skus.append({
                'id':sku.id,
                'name':sku.name,
                'price':sku.price,
                'default_image_url':'http://'+str(sku.image1)
            })
        total_num = paginator.num_pages
        if cat2 == '':
            return Response({'code':0,'errmsg':'ok','list':skus,'count':total_num,'breadcrumb':{'cat1':{'name':cat1.name,'url':'http://bookmall.com:8080/list.html?cat='+str(cat1.id)},'cat2':{'name':'','url':'http://bookmall.com:8080/list.html?cat='+str(cat1.id)}}})
        return Response({'code':0,'errmsg':'ok','list':skus,'count':total_num,'breadcrumb':{'cat1':{'name':cat1.name,'url':'http://bookmall.com:8080/list.html?cat='+str(cat1.id)},'cat2':{'name':cat2.name,'url':'http://bookmall.com:8080/list.html?cat='+str(cat1.id)+'&'+str(cat2.id)}}})
    
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
            return Response({"code":404,"errmag":"not exist"})
        context = {
            'categories': '',
            'breadcrumb': '',
            'sku': {
                'name':sku.name,
                'price':sku.price,
                'market_price':sku.price,
                'commits':0,
                'caption':sku.stock,
                'default_image_url':'http://'+str(sku.image1),
                'category_id':str(sku.category.id),
                'profile':sku.profile,
                },
            'specs': '',
        }
        return Response({"code":0,"errmag":"ok","good_detail":context['sku']})

#   商品搜索
class BookSearchView(SearchView):
    def create_response(self):
        context = self.get_context()
        skus=[]
        for sku in context['page'].object_list:
            skus.append({
                'id':sku.object.id,
                'name':sku.object.name,
                'price': sku.object.price,
                'default_image_url': "https://"+str(sku.image1),
                'searchkey': context.get('query'),
                'page_size': context['page'].paginator.num_pages,
                'count': context['page'].paginator.count
            })
        print(skus)

        return JsonResponse(skus,safe=False)

#   购物车
class CartsView(APIView):
    def post(self,request):
        # 接收数据
        data=request.data
        sku_id=data.get('sku_id')
        count=data.get('count')
        # 验证数据
        try:
            sku=SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return Response({'code':400,'errmsg':'查无此商品'})
        try:
            count=int(count)
        except Exception:
            count=1
        # 判断用户的登录状态
        user=request.user
        if user.is_authenticated:    
            redis_cli=get_redis_connection('carts')
            redis_cli.hset('carts_%s'%user.id,sku_id,count)
            redis_cli.sadd('selected_%s'%user.id,sku_id)
            return Response({'code':0,'errmsg':'ok'})
        else:
            cookie_carts=request.COOKIES.get('carts')
            if cookie_carts:
                carts = pickle.loads(base64.b64decode(cookie_carts))
            else:
                carts={}
            # 判断新增的商品 有没有在购物车里
            if sku_id in carts:
                origin_count=carts[sku_id]['count']
                count+=origin_count
            carts[sku_id]={
                'count':count,
                'selected':True
            }
            carts_bytes=pickle.dumps(carts)
            base64encode=base64.b64encode(carts_bytes)
            return Response({'code': 0, 'errmsg': 'ok'}).set_cookie('carts',base64encode.decode(),max_age=3600*24*12)

    def get(self,request):
        # 判断用户是否登录
        user=request.user
        if user.is_authenticated:
            # 登录用户查询redis
            redis_cli=get_redis_connection('carts')
            sku_id_counts=redis_cli.hgetall('carts_%s'%user.id)
            selected_ids=redis_cli.smembers('selected_%s'%user.id)
            carts={}
            for sku_id,count in sku_id_counts.items():
                carts[int(sku_id)]={
                    'count':int(count),
                    'selected': sku_id in selected_ids
                }
        else:
            # 未登录用户查询cookie
            cookie_carts=request.COOKIES.get('carts')
            if cookie_carts is not None:
               carts = pickle.loads(base64.b64decode(cookie_carts))
            else:
                carts={}
        sku_ids=carts.keys()
        skus=SKU.objects.filter(id__in=sku_ids)
        sku_list=[]
        for sku in skus:
            # 将对象数据转换为字典数据
            sku_list.append({
                'id':sku.id,
                'price':sku.price,
                'name':sku.name,
                'default_image_url':'http://'+str(sku.image1),
                'selected': carts[sku.id]['selected'],          
                'count': int(carts[sku.id]['count']),                
                'amount': sku.price*carts[sku.id]['count']     
            })
        # 6 返回响应
        return Response({'code':0,'errmsg':'ok','cart_skus':sku_list})

    def put(self,request):
            user=request.user
            # 2.接收数据
            data=request.data
            sku_id=data.get('sku_id')
            count=data.get('count')
            selected=data.get('selected')
            # 3.验证数据
            if not all([sku_id,count]):
                return Response({'code':400,'errmsg':'参数不全'})
            try:
                SKU.objects.get(id=sku_id)
            except SKU.DoesNotExist:
                return Response({'code':400,'errmsg':'没有此商品'})
            try:
                count=int(count)
            except Exception:
                count=1
            if user.is_authenticated:
                redis_cli=get_redis_connection('carts')
                redis_cli.hset('carts_%s'%user.id,sku_id,count)
                if selected:
                    redis_cli.sadd('selected_%s'%user.id,sku_id)
                else:
                    redis_cli.srem('selected_%s'%user.id,sku_id)
       
                return Response({'code':0,'errmsg':'ok','cart_sku':{'count':count,'selected':selected}})
            else:
                cookie_cart=request.COOKIES.get('carts')
                if cookie_cart is not None:
                    carts=pickle.loads(base64.b64decode(cookie_cart))
                else:
                    carts={}
                if sku_id in carts:
                    carts[sku_id]={
                        'count':count,
                        'selected':selected
                    }
                new_carts=base64.b64encode(pickle.dumps(carts))
                return Response({'code':0,'errmsg':'ok','cart_sku':{'count':count,'selected':selected}}).set_cookie('carts',new_carts.decode(),max_age=14*24*3600)
   
    def delete(self,request):
        data=request.data
        sku_id=data.get('sku_id')
        try:
            SKU.objects.get(pk=sku_id)  # pk primary key
        except SKU.DoesNotExist:
            return Response({'code':400,'errmsg':'没有此商品'})
        user=request.user
        if user.is_authenticated:
            redis_cli=get_redis_connection('carts')
            redis_cli.hdel('carts_%s'%user.id,sku_id)
            redis_cli.srem('selected_%s'%user.id,sku_id)
            return Response({'code':0,'errmsg':'ok'})
        else:
            cookie_cart=request.COOKIES.get('carts')
            #  判断数据是否存在
            if cookie_cart is not None:
                carts=pickle.loads(base64.b64decode(cookie_cart))
            else:
                carts={}
            # 删除数据 
            del carts[sku_id]
            new_carts=base64.b64encode(pickle.dumps(carts))
            return Response({'code':0,'errmsg':'ok'}).set_cookie('carts',new_carts.decode(),max_age=14*24*3600)