from django.conf.urls import url
from . import views

urlpatterns = [
    # 发起支付.gitignore
    url(r'^orders/(?P<order_id>\d+)/payment/$', views.PaymentView.as_view()),
    # 支付成功
    url(r'^payment/status/$', views.PyamentStatusView.as_view())

]