from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin
from rest_framework.filters import OrderingFilter
from drf_haystack.viewsets import HaystackViewSet

from .models import SKU

from .serializers import SKUSerializer, SKUIndexSerializer
from . import constants

# Create your views here.

class HotSKUListView(ListCacheResponseMixin, ListAPIView):
    """
    返回热销数量
    """
    serializer_class = SKUSerializer
    pagination_class = None

    # 指定查询集
    def get_queryset(self):
        # 获取url路径中 正则组起别名提取参数
        category_id = self.kwargs.get('category_id')

        return SKU.objects.filter(is_launched=True, category_id=category_id).order_by('-sales')[:constants.HOT_SKUS_COUNT_LIMIT]




class SKUListView(ListAPIView):
    """
    商品列表数据
    /categories/(?P<category_id>\d+)/skus?page=xxx&page_size=xxx&ordering=xxx
    """
    queryset = SKU.objects.all()

    # 指定序列化器
    serializer_class = SKUSerializer

    # 指定过滤后端实现排序行为
    filter_backends = [OrderingFilter]
    # 指定以那些字段进行排序
    ordering_fields = ['create_time', 'price', 'sales']

    # 指定查询集
    def get_queryset(self):
        # 获取url路径中 正则组起别名提取参数
        category_id = self.kwargs.get('category_id')

        return SKU.objects.filter(is_launched=True, category_id=category_id)



class SKUSearchViewSet(HaystackViewSet):
    """
    SKU搜索
    """
    index_models = [SKU]

    serializer_class = SKUIndexSerializer



# class OrderListView(APIView):
#     """订单列表信息获取"""
#
#     def get(self, request):
#         """查询订单列表信息"""
#
#         # 获取当前用户对象
#         user = request.user
#
#         """获取当前用户的订单信息"""
#         # 获取当前商品订单号
#         user_orders = user.orderinfo_set.all()
#
#         # 订单号、支付方式、订单金额 列表
#         user_orders_list = []
#
#         # 组织订单数据
#         user_order_dict = {}
#
#         for user_order in user_orders:
#
#             if user_order.pay_method == 1:
#                 pay_method = '货到付款'
#             elif user_order.pay_method == 2:
#                 pay_method = '支付宝'
#             else:
#                 pass
#
#             user_order_dict = {
#                 'order_id': user_order.order_id,  # 订单号
#                 'pay_method': pay_method,  # 支付方式
#                 'total_amount': user_order.total_amount,  # 订单金额
#                 'total_count': user_order.total_count,  # 商品数量
#
#             }
#             user_orders_list.append(user_order_dict)
#
#
#             # 当前订单对应的订单商品
#             user_order_goods = user_order.skus.all()
#
#             for user_order_sku in user_order_goods:
#
#                 sku = user_order_sku.sku
#
#                 user_order_dict['name'] = sku.name
#                 user_order_dict['price'] = sku.price
#
#                 user_orders_list.append(user_order_dict)
#
#
#         print(user_orders_list)
#
#
#         return Response(data=user_orders_list)
#
#
#
# class GoodsInventoryView(APIView):
#     """判断库存"""
#
#     def get(self, request, sku_id):
#         """查询当前商品库存"""
#
#         # 获取当前商品的库存
#         try:
#             goods_stock = SKU.objects.get(id=sku_id).stock
#         except SKU.DoesNotExist:
#             return Response(data={'message':'获取当前数据错误'})
#
#         data={
#             'goods_stock':goods_stock
#         }
#
#         return Response(data=data)