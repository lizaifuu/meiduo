# 自定义Django认证系统后端类
from django.contrib.auth.backends import ModelBackend
from users.models import User

import re
def jwt_response_payload_handler(token, user=None, request=None):
    """自定义jwt登录视图响应数据"""
    return {
        'user_id': user.id,
        'username': user.username,
        'token': token
    }



def get_user_by_account(account):
    """
        根据账号信息,查找用户对象
    :param account:可以是手机号,用户名
    :return:User对象,None
    """
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            # 根据手机号查询用户
            user = User.objects.get(mobile=account)
        else:
            # 根据用户名查询用户
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        user = None

    return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        username: 可能是用户名或手机号
        """
        # 根据用户名或手机号查询用户的信息
        user = get_user_by_account(username)

        # 如果用户存在，调用check_password方法检验密码是否正确
        if user and user.check_password(password):
            # 验证成功,返回对象
            return user
