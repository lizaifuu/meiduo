from django.conf import settings
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen
import logging
import json

from .exceptions import QQAPIException


logger = logging.getLogger('django')

class OAuthQQ(object):
    """
        用于QQ登录的工具类
        提供了QQ登录的可能使用的方法
    """
    def __init__(self, app_id=None, app_key=None, redirect_url=None, state=None):
        self.app_id = app_id or settings.QQ_APP_ID
        self.app_key = app_key or settings.QQ_APP_KEY
        self.redirect_url = redirect_url or settings.QQ_REDIRECT_URL
        self.state = state or settings.QQ_STATE

    def generate_qq_login_url(self):
        """
            用于拼接用户QQ登录的链接地址
        :return: 链接地址
        """
        # 组织参数
        params = {
            'response_type': 'code',
            'client_id': self.app_id,
            'redirect_uri': self.redirect_url,
            'state': self.state,
            'scope': 'get_user_info' #获取用户的qq的openid
        }

        # 拼接url地址  #response_type=cpde&client_idxxx&redirect_uri=xxx
        url = 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(params)

        return url

    def get_access_token(self, code):
        """
            获取QQ的access_token
        :param code: 调用的凭据
        :return:
        """
        url = 'https://graph.qq.com/oauth2.0/token?'
        req_date = {
            'grant_type': 'authorization_code',
            'client_id': self.app_id,
            'client_secret': self.app_key,
            'code': code,
            'redirect_uri': self.redirect_url,
        }

        url += urlencode(req_date)

        try:
            # 发送请求
            response = urlopen(url)
            # 读取QQ返回的响应体数据
            response = response.read().decode()

            # 将返回的数据转换为字典
            resp_dict = parse_qs(response)
            access_token = resp_dict.get("access_token")[0]
        except Exception as e:
            logger.error(e)
            raise QQAPIException('获取access_token异常')

        return access_token


    def get_openid(self, access_token):
        """
            获取QQ授权用户的openid:
            access_token: QQ返回的access_token
        """
        # 拼接url地址
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token

        try:
            # 访问获取QQ授权用户的openid
            response = urlopen(url)
        except Exception as e:
            raise QQAPIException(str(e))

        # 返回数据格式如下:
        # callback({"client_id": "YOUR_APPID", "openid": "YOUR_OPENID"} )\n;
        res_data = response.read().decode()
        try:
            res_dict = json.loads(res_data[10:-4])
        except Exception:
            res_dict = parse_qs(res_data)
            logger.error('code=%s msg=%s' % (res_dict.get('code'), res_dict.get('msg')))
            raise QQAPIException('获取openid异常')

        # 获取openid
        openid = res_dict.get('openid', None)
        return openid

