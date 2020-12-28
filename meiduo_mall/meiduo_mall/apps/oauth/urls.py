from django.conf.urls import url
from . import views

urlpatterns = [
    # 获取qq扫码url
    url(r'^qq/authorization/$', views.OAuthQQURLView.as_view()),
    # qq oAuth2.0认证过程
    url(r'^qq/user/$', views.OAuthQQUserView.as_view()),
]