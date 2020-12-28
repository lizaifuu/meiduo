from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework import status
from rest_framework import mixins
import re
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.views import ObtainJSONWebToken

from users.models import User
from users import serializers
# from users.serializers import CreateUserSerializer,CheckSMSCodeSerializer
from verifications.serializers import CherkImageCodeSerializer
from .utils import get_user_by_account
from . import constants
from goods.models import SKU
from goods.serializers import SKUSerializer
from carts.utils import merge_cart_cookie_to_redis

# Create your views here.


# POST /users/
# class UserView(GenericAPIView):
class UserView(CreateAPIView):
    serializer_class = serializers.CreateUserSerializer

    # def post(self, request):
    #     """
    #     注册用户信息的保存:
    #     1. 获取参数并进行校验(参数完整性，两次密码是否一致，手机号格式，手机号是否已注册，短信验证码是否正确，是否同意协议)
    #     2. 保存注册用户信息
    #     3. 返回应答，注册成功
    #     """
    #     # 1. 获取参数并进行校验(参数完整性，两次密码是否一致，手机号格式，手机号是否已注册，短信验证码是否正确，是否同意协议)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 2. 保存注册用户信息(create)
    #     serializer.save()
    #
    #     # 3. 返回应答，注册成功
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
class UsernameCountView(APIView):
    """
    用户名数量
    """
    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }
        # print('data:',data)
        return Response(data)


# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
class MobileCountView(APIView):
    """
    手机号数量
    """
    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)


class SMSCodeTokenView(GenericAPIView):
    """
        获取发送短信验证码的凭据
    """
    # serializer_class = CherkImageCodeSerializer
    def get(self,request,account):
        """

        :param request:
        :param account:
        :return:
        """
        # 校验图片验证码
        # serializer = self.get_serializer(data=request.query_params)
        # serializer.is_valid(raise_ecception=True)

        # 根据account查询User对象
        user = get_user_by_account(account)
        if user is None:
            return Response({"message":'用户不存在'},status=status.HTTP_404_NOT_FOUND)

        # 根据User对象手机号生成access_token
        access_token = user.generate_send_sms_code_token()

        # 修改手机号
        mobile = re.sub(r'(\d{3})\d{4}(\d{4})',r'\1****\2' , user.mobile)
        return Response({
            'mobile':mobile,
            'access_token': access_token,
        })


class PasswordTokenView(GenericAPIView):
    """
        用户账号设置密码的token
    """
    serializer_class = serializers.CheckSMSCodeSerializer

    def get(self,request, account):
        """
            根据用户账号修改密码的token
        :param request:
        :param account:
        :return:
        """
        # 校验短信验证码
        serializer = self.get_serializer(data = request.query_params)
        serializer.is_valid(raise_exception=True)

        user = serializer.user

        # 生成修改用户密码的access token
        access_token = user.generate_set_password_token()

        return Response({'user_id':user.id,'access_token':access_token})


class PasswordView(mixins.UpdateModelMixin, GenericAPIView):
    """
        用户密码
    """
    queryset = User.objects.all()
    serializer_class = serializers.ResetPasswordSerializer

    def post(self,request, pk):
        return self.update(request, pk)


class UserDetailView(RetrieveAPIView):
    """
        用户的详情信息
        /user/<pk>/

        /user/
    """
    # def get(self, request, ):
    #     request.user

    # 在类视图对象中也保存了请求对象request
    # request对象的user属性是通过认证检验之后的请求用户对象
    # 类视图对象还有kwargs属性

    serializer_class = serializers.UserDetailSerializer
    # 补充通过认证才能访问接口的权限
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        返回请求的用户对象
        :return:user
        """
        return self.request.user


class EmailView(UpdateAPIView):
    """
    保存用户邮箱
    /email/
    """
    serializer_class = serializers.EmailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        获取对象
        :return:
        """

        return self.request.user

    # def get_serializer(self, *args, **kwargs):
    #     return EmailSerializer(self.request.user, data=self.request.data)


class EmailVerifyView(APIView):
    """
    邮箱验证
    """
    def get(self, request):
        print('进入验证')
        # 获取token
        token = request.query_params.get('token')
        if not token:
            return Response({'缺少token'}, status=status.HTTP_400_BAD_REQUEST)
        # 校验 保存
        result = User.check_email_verify_token(token)

        if result:
            return Response({'message':'OK'})
        else:
            return Response({'非法的token'}, status=status.HTTP_400_BAD_REQUEST)


class AddressViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    用户地址新增与修改
    """
    serializer_class = serializers.UserAddressSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)

    # GET /addresses/
    def list(self, request, *args, **kwargs):
        """
        用户地址列表数据
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
            'addresses': serializer.data,
        })

    # POST /addresses/
    def create(self, request, *args, **kwargs):
        """
        保存用户地址数据
        """
        # 检查用户地址数据数目不能超过上限
        count = request.user.addresses.filter(is_deleted=False).count()
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            return Response({'message': '保存地址数据已达到上限'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    # delete /addresses/<pk>/
    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        """
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # put /addresses/pk/status/
    @action(methods=['put'], detail=True)
    def status(self, request, pk=None):
        """
        设置默认地址
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    # put /addresses/pk/title/
    # 需要请求体参数 title
    @action(methods=['put'], detail=True)
    def title(self, request, pk=None):
        """
        修改标题
        """
        address = self.get_object()
        serializer = serializers.AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserHistoryView(mixins.CreateModelMixin, GenericAPIView):
    """
    用户的历史记录
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AddUserHistorySerializer

    def post(self, request):
        """
        保存
        :param request:
        :return:
        """
        # 使用序列化器检验数据
        # 保存
        # 返回前端
        return self.create(request)

    def get(self, request):
        """
        获取浏览记录
        :param request:
        :return:
        """
        user_id = request.user.id

        # 查询redis数据库
        redis_conn = get_redis_connection('history')
        sku_id_list = redis_conn.lrange('history_%s' % user_id, 0, constants.USER_BROWSING_HISTORY_COUNTS_LIMIT)

        # 根据redis返回的sku id 查询数据库
        # SKU.objects.filter(id__in=sku_id_list)
        sku_list = []
        for sku_id in sku_id_list:
            sku = SKU.objects.get(id=sku_id)
            sku_list.append(sku)

        # 使用序列化器序列化
        serializer = SKUSerializer(sku_list, many=True)
        return Response(serializer.data)


class UserAuthorizationView(ObtainJSONWebToken):

    def post(self, request):
        # 调用jwt扩展的方法,对用户登录的数据进行验证
        response = super().post(request)

        # 如果用户登录成功,进行购物车数据合并
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 表示用户登录成功
            user = serializer.validated_data.get('user')
            # 合并购物车
            response = merge_cart_cookie_to_redis(request, user, response)

        return response







