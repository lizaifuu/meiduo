from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from users import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet, base_name='addresses')


urlpatterns = [
    # 判断用户名是否已存在
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    # 判断手机号是否已存在
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 注册
    url(r'^users/$', views.UserView.as_view()),
    # JWT登录,获取JWT.token
    # url(r'^authorizations/$', obtain_jwt_token),
    url(r'^authorizations/$', views.UserAuthorizationView.as_view()),
    #获取发送短信验证码的token
    url(r'^accounts/(?P<account>\w{4,20})/sms/token/$',views.SMSCodeTokenView.as_view()),
    #获取修改密码的token
    url(r'^accounts/(?P<account>\w{4,20})/password/token/$',views.PasswordTokenView.as_view()),
    #重置密码
    url(r'users/(?P<pk>\d+)/password/$',views.PasswordView.as_view()),
    # 获取用户个人信息
    url(r'^user/$', views.UserDetailView.as_view()),
    #绑定邮箱验证
    url(r'^email/$', views.EmailView.as_view()),
    # 邮箱激活
    url(r'^emails/verification/$', views.EmailVerifyView.as_view()),
    # 用户浏览历史记录
    url(r'browse_histories/$', views.UserHistoryView.as_view())


]

urlpatterns += router.urls

