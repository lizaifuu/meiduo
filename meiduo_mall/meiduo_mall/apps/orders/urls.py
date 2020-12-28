from django.conf.urls import url
from . import views

urlpatterns = [
    # 订单结算
    url(r'order/settlement/$', views.OrderSettlementView.as_view()),
    # 保存订单
    url(r'orders/$', views.SaveOrderView.as_view())
]