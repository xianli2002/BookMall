from rest_framework.views import APIView
from utils.views import LoginRequiredJSONMixin
from Areas.models import Address
from django_redis import get_redis_connection
from Books.models import SKU
from rest_framework.response import Response
from Orders.models import OrderInfo,OrderGoods
from django.db import transaction
from django.utils import timezone
from decimal import Decimal

class OrderSettlementAPIView(LoginRequiredJSONMixin,APIView):
    def get(self,request):
        user=request.user
        addresses=Address.objects.filter(is_deleted=False)
        addresses_list=[]
        for address in addresses:
            print(address.receiver)
            addresses_list.append({
                'id': address.id,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'detail_address':address.detail_address,
                'receiver': address.receiver,
                'mobile': address.mobile
            })
        # 购物车中选中商品的信息
        redis_cli=get_redis_connection('carts')
        pipeline=redis_cli.pipeline()

        pipeline.hgetall('carts_%s'%user.id)
        pipeline.smembers('selected_%s'%user.id)
        result=pipeline.execute()
      
        sku_id_counts=result[0]        
        selected_ids=result[1]          
        #重新组织一个 选中的信息
        selected_carts={}
        for sku_id in selected_ids:
            selected_carts[int(sku_id)]=int(sku_id_counts[sku_id])

        #根据商品的id 查询商品的具体信息 [SKU,SKU,SKu...]
        sku_list=[]
        for sku_id,count in selected_carts.items():
            sku=SKU.objects.get(id=sku_id)
            #需要将对象数据转换为字典数据
            sku_list.append({
                'id':sku.id,
                'name':sku.name,
                'count':count,
                'default_image_url': 'http://'+str(sku.image1),
                'price': sku.price
            })

        # 运费
        from decimal import Decimal
        freight=Decimal('10')


        context = {
            'skus':sku_list,
            'addresses':addresses_list,
            'freight':freight        
        }

        return Response({'code':0,'errmsg':'ok','context':context})




class OrderCommitAPIView(LoginRequiredJSONMixin,APIView):

    def post(self,request):
        user=request.user

        data=request.data
        address_id=data.get('address_id')
        pay_method=data.get('pay_method')

        # 验证数据
        if not all([address_id,pay_method]):
            return Response({'code':400,'errmsg':'参数不全'})

        try:
            address=Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return Response({'code':400,'errmsg':'参数不正确'})


        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'],OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return Response({'code': 400, 'errmsg': '参数不正确'})

        
        
        order_id=timezone.localtime().strftime('%Y%m%d%H%M%S%f') + '%09d'%user.id

        
        if pay_method == OrderInfo.PAY_METHODS_ENUM['CASH']:
            status=OrderInfo.ORDER_STATUS_ENUM['UNSEND']
        else:
            status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']

        total_count=0
        
        total_amount=Decimal('0')        #总金额

        freight=Decimal('10.00')

        with transaction.atomic():

            # 事务开始点
            point = transaction.savepoint()

            # 数据入库     生成订单

            orderinfo=OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                address=address,
                total_count=total_count,
                total_amount=total_amount,
                freight=freight,
                pay_method=pay_method,
                status=status
            )
      
            redis_cli=get_redis_connection('carts')
            
            sku_id_counts=redis_cli.hgetall('carts_%s'%user.id)
            
            selected_ids=redis_cli.smembers('selected_%s'%user.id)
            
            carts={}
            
            for sku_id in selected_ids:
                carts[int(sku_id)]=int(sku_id_counts[sku_id])

           
            for sku_id,count in carts.items():

                
                while True:
                    # 根据选中商品的id进行查询
                    sku=SKU.objects.get(id=sku_id)
                    # 判断库存是否充足
                    if sku.stock<count:

                        
                        transaction.savepoint_rollback(point)

                        #  如果不充足，下单失败
                        return Response({'code':400,'errmsg':'库存不足'})
                    
                    old_stock=sku.stock

                   
                    new_stock=sku.stock-count
                    new_sales=sku.sales+count

                    result=SKU.objects.filter(id=sku_id,stock=old_stock).update(stock=new_stock,sales=new_sales)
                    

                    if result == 0:
                       
                        continue
                      

                    # 累加总数量和总金额
                    orderinfo.total_count+=count
                    orderinfo.total_amount+=(count*sku.price)

                    #  保存订单商品信息
                    OrderGoods.objects.create(
                        order=orderinfo,
                        sku=sku,
                        count=count,
                        price=sku.price
                    )
                    break
          
            orderinfo.save()
            redis_cli=get_redis_connection('carts')

            redis_cli.delete('carts_%s'%user.id)
            redis_cli.delete('selected_%s'%user.id)
            transaction.savepoint_commit(point)


        
        return Response({'code':0,'errmsg':'ok','order_id':order_id})

    def getGoods(self,order):
        try:
            goods=OrderGoods.objects.filter(order=order)
        except Exception as e:
            return []
        goods_ret=[]
        for good in goods:
            goods_ret.append({
                'id':str(good.sku.id),
                'name':good.sku.name,
                'image':'http://'+str(good.sku.image1),
                'price':good.price,
                'count':good.count,
                'total_amount':good.price*Decimal(good.count),
                'url':'detail.html?book='+str(good.sku.id)
            })

        return goods_ret

    def get(self,request):
        user=request.user
        try:
            orders=OrderInfo.objects.filter(user=user)
        except Exception as e:
            return Response({'code':400,'errmsg':'无订单信息'})
        orders_return=[]
        for order in orders:

            orders_return.append({
                'order_id':order.order_id,
                'time':order.update_time,
                'total_count':order.total_count,
                'total_amount':order.total_amount,
                'pay_method':order.pay_method,
                'goods':self.getGoods(order),
            })

        return Response({'code':0,'errmsg':'ok','orders':orders_return})
