"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
import xadmin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # 更改为xadmin
    url(r'xadmin/', include(xadmin.site.urls)),

    # 自动生成api接口文档
    url(r'^docs/', include_docs_urls(title='My API title')),

    # 短信模块
    url(r'^', include('verifications.urls')),

    # 用户登陆模块
    url(r'^', include('users.urls')),

    # qq模块
    url(r'oauth/', include('oauth.urls')),

    # 省市区
    url(r'', include('areas.urls')),

    # 商品模块
    url(r'^', include('goods.urls')),

    # 富文本路由，admin站点自动访问，不用定义试图函数
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # 购物车模块
    url(r'^', include('carts.urls')),

    # 订单模块
    url(r'^', include('orders.urls')),

    # 支付模块
    url(r'^', include('payment.urls')),

]
