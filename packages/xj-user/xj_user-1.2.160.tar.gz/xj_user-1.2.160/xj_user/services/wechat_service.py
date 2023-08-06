# encoding: utf-8
"""
@project: djangoModel->Auth
@author: 孙楷炎,高栋天
@Email: sky4834@163.com
@synopsis: 小程序SDK
@created_time: 2022/7/7 9:38
"""
from datetime import datetime, timedelta
import json
from logging import getLogger
from pathlib import Path

import jwt
import redis
import requests
from django.forms import model_to_dict
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from main.settings import BASE_DIR
from xj_captcha.services.sms_service import SmsService
from xj_role.services.user_group_service import UserGroupService
from xj_user.services.user_service import UserService
from xj_user.utils.wechat import get_openid
from .user_detail_info_service import DetailInfoService, write_to_log
from ..models import BaseInfo, Auth, UserSsoToUser, Platform
from ..services.user_relate_service import UserRelateToUserService
from ..utils.custom_tool import get_short_id
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.model_handle import parse_model
from ..utils.nickname_generate import gen_one_word_digit

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))

payment_main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
payment_module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

sub_appid = payment_main_config_dict.wechat_merchant_app_id or payment_module_config_dict.wechat_merchant_app_id or ""
sub_app_secret = payment_main_config_dict.wechat_merchant_app_secret or payment_module_config_dict.wechat_merchant_app_secret or ""
wechat_merchant_name = payment_main_config_dict.wechat_merchant_name or payment_module_config_dict.wechat_merchant_name or ""

app_id = payment_main_config_dict.app_id or payment_module_config_dict.app_id or ""
app_secret = payment_main_config_dict.secret or payment_module_config_dict.secret or ""

subscription_app_id = payment_main_config_dict.wechat_subscription_app_id or payment_module_config_dict.wechat_subscription_app_id or ""
subscription_app_secret = payment_main_config_dict.wechat_subscription_app_secret or payment_module_config_dict.wechat_subscription_app_secret or ""

app_app_id = payment_main_config_dict.wechat_app_app_id or payment_module_config_dict.wechat_app_app_id or ""
app_app_secret = payment_main_config_dict.wechat_app_app_secret or payment_module_config_dict.wechat_app_app_secret or ""

jwt_secret_key = main_config_dict.jwt_secret_key or module_config_dict.jwt_secret_key or ""
expire_day = main_config_dict.expire_day or module_config_dict.expire_day or ""
expire_second = main_config_dict.expire_second or module_config_dict.expire_second or ""

redis_main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="main"))
redis_module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="main"))

redis_host = redis_main_config_dict.redis_host or redis_module_config_dict.redis_host or ""
redis_port = redis_main_config_dict.redis_port or redis_module_config_dict.redis_port or ""
redis_password = redis_main_config_dict.redis_password or redis_module_config_dict.redis_password or ""

# print(">", sub_appid)
logger = getLogger('log')


class WechatService:
    wx_login_url = "https://api.weixin.qq.com/sns/jscode2session"
    wx_token_url = 'https://api.weixin.qq.com/cgi-bin/token'
    wx_get_phone_url = "https://api.weixin.qq.com/wxa/business/getuserphonenumber"

    def __init__(self):
        self.login_param = {'appid': app_id, 'secret': app_secret, 'grant_type': 'authorization_code'}
        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password
        )

    def get_openid(self, code):
        """
        :param code（openid登录的code）:
        :return:(err,data)
        """
        req_params = {
            'appid': sub_appid,
            'secret': sub_app_secret,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
        user_info = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=req_params, timeout=3,
                                 verify=False)
        return user_info.json()
        # try:
        #     response = requests.get(self.wx_login_url, code).json()
        #     if not response['errcode'] == 0:  # openid 换取失败
        #         return response['errcode'], response['errmsg']
        # except Exception as e:
        #     return 6445, '请求错误'

    def wechat_login(self, phone_code, login_code, sso_serve_id=None, detail_params=None):
        """
        过期续约就是重新登录
        :param detail_params:
        :param code: 换取手机号码的code
        :return:(err,data)
        """
        # code 换取手机号
        phone = ""
        try:
            if detail_params is None:
                detail_params = {}
            url = self.wx_get_phone_url + "?access_token={}".format(self.get_access_token()['access_token'])
            header = {'content-type': 'application/json'}
            response = requests.post(url, json={'code': phone_code}, headers=header).json()
            if not response['errcode'] == 0:
                return response['errmsg'], ""
            phone = response['phone_info']['phoneNumber']
            # 检查是否存在该用户，不存在直接注册
            # current_user = BaseInfo.objects.filter(phone=phone).filter()
            # current_user = parse_model(current_user)
            # if not current_user:
            #     base_info = {
            #         'user_name': '',
            #         'phone': phone,
            #         'email': '',
            #         'full_name': '请修改用户名',
            #     }
            #     current_user = BaseInfo.objects.create(**base_info)
            #     current_user = parse_model(current_user)
            # current_user = current_user[0]
            # # 生成登录token
            # token = self.__set_token(current_user.get('id', None), phone)
            # # 创建用户登录信息，绑定token
            # auth = {
            #     'user_id': current_user.get('id', None),
            #     'password': make_password('123456', None, 'pbkdf2_sha1'),
            #     'plaintext': '123456',
            #     'token': token,
            # }
            # Auth.objects.update_or_create({'user_id': current_user.get('id', None)}, **auth)
            # return 0, {'token': token, 'user_info': current_user}

            # 通过换取的手机号判断用户是否存在
            current_user = BaseInfo.objects.filter(phone=phone).filter()
            current_user = parse_model(current_user)
            if not login_code:
                return None, "微信登录 login_code 必传"
            wechat_openid = self.get_openid(code=login_code)
            if wechat_openid.get("openid", None) is None:
                return None, "获取 openid 失败 查openid是否过期, wechat_openid:" + json.dumps(wechat_openid)
            # 登录即注册操作
            if not current_user:
                # 用户不存在的时候，进行注册用户
                base_info = {
                    'user_name': get_short_id(8),  # 第一次注册的时候给一个唯一的字符串作登录账号
                    'nickname': gen_one_word_digit(),
                    'phone': phone,
                    'email': '',
                    # 'full_name': '请修改用户名',
                    # 'wechat_openid': wechat_openid.get("openid", None)
                }
                BaseInfo.objects.create(**base_info)
                current_user = BaseInfo.objects.filter(phone=phone).filter()
                current_user = parse_model(current_user)
                current_user = current_user[0]
                # 生成登录token
                token = self.__set_token(current_user.get('id', None), phone)
                # 用户第一次登录即注册，允许添加用户的详细信息
                try:
                    detail_params.setdefault("user_id", current_user.get('id', None))
                    data, detail_err = DetailInfoService.create_or_update_detail(detail_params)
                    if detail_err:
                        raise Exception(detail_err)
                except Exception as e:
                    logger.error('---首次登录写入用户详细信息异常：' + str(e) + '---')

                # 创建单点登录
                if sso_serve_id:
                    sso_data = {
                        "sso_serve_id": sso_serve_id,
                        "user_id": current_user.get('id', None),
                        "sso_unicode": wechat_openid['unionid'],
                        "app_id": sub_appid,
                        "openid": wechat_openid['openid']
                    }
                    UserSsoToUser.objects.create(**sso_data)
                # 创建用户登录信息，绑定token
                auth = {
                    'user_id': current_user.get('id', None),
                    'password': make_password('123456', None, 'pbkdf2_sha1'),
                    'plaintext': '123456',
                    'token': token,
                }
                Auth.objects.update_or_create({'user_id': current_user.get('id', None)}, **auth)
                auth_set = Auth.objects.filter(user_id=current_user.get('id', None), password__isnull=False).order_by(
                    '-update_time').first()
            else:
                # 用户存在的时候
                current_user = current_user[0]
                sso = UserSsoToUser.objects.filter(user_id=current_user.get('id', None), app_id=sub_appid).first()
                if not sso:
                    if sso_serve_id:
                        sso_data = {
                            "sso_serve_id": sso_serve_id,
                            "user_id": current_user.get('id', None),
                            "sso_unicode": wechat_openid['openid'],
                            "app_id": sub_appid
                        }
                        UserSsoToUser.objects.create(**sso_data)
                token = self.__set_token(current_user.get('id', None), phone)
                # 创建用户登录信息，绑定token
                auth = {
                    'token': token,
                }
                Auth.objects.filter(user_id=current_user.get('id', None)).update(**auth)
                auth_set = Auth.objects.filter(
                    user_id=current_user.get('id', None),
                    password__isnull=False
                ).order_by('-update_time').first()

            # 绑定用户关系 邀请关系和收益关系
            data, relate_err = UserRelateToUserService.bind_bxtx_relate(params=detail_params, user_info=current_user)
            if relate_err:
                logger.error(
                    '绑定用户关系异常：' + str(relate_err) +
                    ' \n当前用户ID:' + str(current_user.get("id", "")) +
                    '\n detail_params:' + json.dumps(detail_params or {})
                )

            return 0, {'token': auth_set.token, 'user_info': current_user}
        except Exception as g_e:
            logger.error(
                '---登录异常程序错误：' + str(g_e) + 'phone:' + str(phone or "") + "line:" + str(g_e.__traceback__.tb_lineno))
            return None, "登录异常"

    # def __set_token(self, user_id, account):
    #     # 生成过期时间
    #     expire_timestamp = datetime.utcnow() + timedelta(
    #         days=7,
    #         seconds=0
    #     )
    #     # 返回token
    #     return jwt.encode(
    #         payload={'user_id': user_id, 'account': account, "exp": expire_timestamp},
    #         key=jwt_secret_key
    #     )
    @staticmethod
    def __set_token(user_id, account):
        # 生成过期时间
        expire_timestamp = datetime.utcnow() + timedelta(
            days=7,
            seconds=0
        )
        # 返回token
        return jwt.encode(
            payload={'user_id': user_id, 'account': account, "exp": expire_timestamp},
            key=jwt_secret_key
        )

    def get_access_token(self):
        # access_token = self.redis.get('access_token')
        # if access_token:
        #     ttl = self.redis.ttl('access_token')
        #     return {"access_token": access_token.decode('utf-8'), 'expires_in': ttl, 'local': True}
        param = {
            'appid': sub_appid,
            'secret': sub_app_secret,
            'grant_type': 'client_credential'
        }
        response = requests.get(self.wx_token_url, param).json()
        # if 'access_token' in response.keys():
        #     self.redis.set('access_token', response['access_token'])
        #     self.redis.expire('access_token', response['expires_in'])
        return response

    def wechat_login_v2(self, phone_code, login_code, sso_serve_id=None, detail_params=None):
        """
        过期续约就是重新登录
        :param detail_params:
        :param code: 换取手机号码的code
        :return:(err,data)
        """
        # code 换取手机号
        phone = ""
        # try:
        if detail_params is None:
            detail_params = {}
        url = self.wx_get_phone_url + "?access_token={}".format(self.get_access_token()['access_token'])
        header = {'content-type': 'application/json'}
        response = requests.post(url, json={'code': phone_code}, headers=header).json()
        if not response['errcode'] == 0:
            return response['errmsg'], ""
        phone = response['phone_info']['phoneNumber']
        # 通过换取的手机号判断用户是否存在
        current_user = BaseInfo.objects.filter(phone=phone).filter()
        current_user = parse_model(current_user)
        if not login_code:
            return None, "微信登录 login_code 必传"
        wechat_openid = self.get_openid(code=login_code)
        if wechat_openid.get("openid", None) is None:
            return None, "获取 openid 失败 查openid是否过期, wechat_openid:" + json.dumps(wechat_openid)
        # 登录即注册操作
        if not current_user:
            # 用户不存在的时候，进行注册用户
            base_info = {
                'user_name': get_short_id(8),  # 第一次注册的时候给一个唯一的字符串作登录账号
                'nickname': gen_one_word_digit(),
                'phone': phone,
                'email': '',
                # 'full_name': phone,
                # 'wechat_openid': wechat_openid.get("openid", None)
            }
            BaseInfo.objects.create(**base_info)
            current_user = BaseInfo.objects.filter(phone=phone).filter()
            current_user = parse_model(current_user)
            current_user = current_user[0]
            # 生成登录token
            token = WechatService.__set_token(current_user.get('id', None), phone)
            # 用户第一次登录即注册，允许添加用户的详细信息
            try:
                detail_params.setdefault("user_id", current_user.get('id', None))
                data, detail_err = DetailInfoService.create_or_update_detail(detail_params)
                if detail_err:
                    raise Exception(detail_err)
            except Exception as e:
                logger.error('---首次登录写入用户详细信息异常：' + str(e) + '---')
            # 创建单点登录
            if sso_serve_id:
                sso_set, err = WechatService.sso_add(sso_serve_id, current_user.get('id', None),
                                                     wechat_openid['openid'], sub_appid,
                                                     wechat_openid.get("wechat_openid", ""))
                if err:
                    return None, err
            # 创建用户登录信息，绑定token
            auth_set, err = WechatService.get_token(current_user.get('id', None), token)
            if err:
                return None, err
        else:
            # 用户存在的时候
            current_user = current_user[0]
            sso = UserSsoToUser.objects.filter(user_id=current_user.get('id', None), app_id=sub_appid).first()
            if not sso:
                if sso_serve_id:
                    sso_set, err = WechatService.sso_add(sso_serve_id, current_user.get('id', None),
                                                         wechat_openid['openid'], sub_appid,
                                                         wechat_openid.get("wechat_openid", ""))
                    if err:
                        return None, err
            else:
                sso = model_to_dict(sso)
                if not sso.get("union_id", None):
                    UserSsoToUser.objects.filter(user_id=current_user.get('id', None), app_id=sub_appid).update(
                        union_id=wechat_openid.get("wechat_openid", ""))

            token = WechatService.__set_token(current_user.get('id', None), phone)
            # 修改用户登录信息，绑定token
            auth_set, err = WechatService.get_token(user_id=current_user.get('id', None), token=token,
                                                    is_create=False)
            if err:
                return None, err

        # 绑定用户关系 邀请关系和收益关系
        data, relate_err = UserRelateToUserService.bind_bxtx_relate(params=detail_params, user_info=current_user)
        if relate_err:
            logger.error(
                '绑定用户关系异常：' + str(relate_err) +
                ' \n当前用户ID:' + str(current_user.get("id", "")) +
                '\n detail_params:' + json.dumps(detail_params or {})
            )

        return {'token': auth_set.token, 'user_info': current_user}, None
        # except Exception as g_e:
        #     logger.error(
        #         '---登录异常程序错误：' + str(g_e) + 'phone:' + str(phone or "") + "line:" + str(g_e.__traceback__.tb_lineno))
        #     return None, "登录异常"

    @staticmethod
    def wechat_app_login(params):
        unionid = params.get("unionid")
        openid = params.get("openid", None)
        sso_serve_id = params.get("sso_serve_id", 1)
        phone_code = params.get('phone_code', None)
        phone = params.get("phone", None)
        detail_params = params.get("detail_params", None)
        appid = app_app_id
        sso = UserSsoToUser.objects.filter(union_id=unionid, sso_serve_id=sso_serve_id).first()
        if not sso:
            if phone:
                if phone_code is None:
                    return None, "验证码不能为空"
                cache_code = cache.get(phone)
                if phone_code != cache_code:
                    return None, "验证码错误"
                current_user = BaseInfo.objects.filter(phone=phone).first()
                if current_user:
                    user = model_to_dict(current_user)
                    if sso_serve_id:
                        sso_set, err = WechatService.sso_add(sso_serve_id, user.get('id', None), openid, appid,
                                                             unionid)
                        if err:
                            return None, err
                    token = WechatService.__set_token(user.get('id', None), phone)
                    auth_set, err = WechatService.get_token(user.get('id', None), token)
                    if err:
                        return None, err

                    return {'token': auth_set.token, 'user_info': user}, None
                else:
                    base_info = {
                        'user_name': get_short_id(8),  # 第一次注册的时候给一个唯一的字符串作登录账号
                        'nickname': gen_one_word_digit(),
                        'phone': phone,
                        'email': '',
                        # 'full_name': phone
                    }
                    base_info = BaseInfo.objects.create(**base_info)
                    if sso_serve_id:
                        sso_set, err = WechatService.sso_add(sso_serve_id, base_info.id, openid, appid,
                                                             unionid)
                        if err:
                            return None, err
                    token = WechatService.__set_token(base_info.id, phone)
                    auth_set, err = WechatService.get_token(current_user.get('id', None), token)
                    if err:
                        return None, err
                    return {'token': auth_set.token, 'user_info': current_user}, None
            else:
                return None, "PHONE_NOT_NULL"
        else:
            sso_dict = model_to_dict(sso)
            current_user = BaseInfo.objects.filter(id=sso_dict.get("user", 0)).first()
            current_user = model_to_dict(current_user)
            # sso_set, err = WechatService.sso_add(sso_serve_id, current_user.get('id', None), openid, appid,
            #                                      unionid)
            # if err:
            #     return None, err
            token = WechatService.__set_token(current_user.get('id', None), current_user.get('phone', None))
            # 修改用户登录信息，绑定token
            auth_set, err = WechatService.get_token(user_id=current_user.get('id', None), token=token,
                                                    is_create=False)
            if err:
                return None, err

            # 绑定用户关系 邀请关系和收益关系
            data, relate_err = UserRelateToUserService.bind_bxtx_relate(params=detail_params, user_info=current_user)
            if relate_err:
                logger.error(
                    '绑定用户关系异常：' + str(relate_err) +
                    ' \n当前用户ID:' + str(current_user.get("id", "")) +
                    '\n detail_params:' + json.dumps(detail_params or {})
                )

            return {'token': auth_set.token, 'user_info': current_user}, None

    @staticmethod
    def login_integration_interface(params):
        # ----------------------------获取信息----------------------------------------
        platform_id = params.get("platform_id", None)  # 平台
        user_id = params.get("user_id", None)  # 用户id
        platform = params.get("platform", None)
        login_type = params.get("login_type", None)  # 支持的登录方式
        code = params.get("code", None)  # 微信登录code
        phone_code = params.get("phone_code", None)  # 微信手机号code
        sms_code = params.get("sms_code", None)  # 短信验证码
        sso_serve_id = params.get("sso_serve_id", 1)  # 单点登录用户平台
        phone = params.get("phone", None)  # 手机号
        other_params = params.get("other_params", None)
        account = params.get("account", None)  # 账户
        password = params.get("password", None)  # 密码
        bind_data = params.get("bind_data", None)  # 绑定的数据

        # ------------------------边界检查----------------------------------------------
        if not platform_id and not platform:
            return None, "所属平台不能为空"
        if not login_type:
            return None, "登录方式不能为空"
        if not sso_serve_id:
            return None, "单点登录不能为空"
        if platform:
            platform_set = Platform.objects.filter(platform_name__iexact=platform)
            if platform_set.count() is 0:
                return None, "platform不存在平台名称：" + platform
        else:
            platform_set = Platform.objects.filter(platform_id=platform_id).first()
            if not platform_set:
                return None, "所属平台不存在"
            platform = model_to_dict(platform_set)['platform_name']

        # ------------------------登录类型判断----------------------------------------------
        # 初始化
        user_info_set = BaseInfo.objects
        openid = ""
        unionid = ""

        wechat = {}
        if login_type == "ACCOUNT":  # 账号登录

            account_serv, error_text = UserService.check_account(account)
            if error_text:
                return None, error_text
            user_id = account_serv['user_id']

            auth_serv, auth_error = UserService.check_login(user_id=user_id, password=password, account=account,
                                                            platform=platform)
            if auth_error:
                return None, auth_error

            current_user = user_info_set.filter(id=user_id).first()

        elif login_type == "SMS":  # 短信验证码登录 (比较特殊 支持多用户)
            sms, sms_err = SmsService.check_sms({"phone": phone, "sms_code": sms_code})
            if sms_err and not user_id:
                return None, sms_err
            current_user_count = user_info_set.filter(phone=phone).count()
            if current_user_count > 1 and not user_id:
                current_user = user_info_set.filter(phone=phone).values("id", "user_name")
                return list(current_user), None
            elif user_id:
                current_user = user_info_set.filter(id=user_id).first()
            else:
                current_user = user_info_set.filter(phone=phone).first()


        elif login_type == "WECHAT_APPLET":  # 小程序登录
            wechat['appid'] = sub_appid
            wechat['secret'] = sub_app_secret
            wechat['code'] = code
            wechat['phone_code'] = phone_code
            wechat_user_info, err = get_openid(login_type, wechat)
            if err:
                return None, err
            openid = wechat_user_info.get("openid", "")
            unionid = wechat_user_info.get("unionid", "")
            phone = wechat_user_info.get("phone", "")

            sso_set, sso_err = WechatService.sso_verify(sso_serve_id, None, sub_appid, False,
                                                        openid,
                                                        unionid)
            if sso_set:
                current_user = user_info_set.filter(id=sso_set['user']).first()
            else:
                current_user = user_info_set.filter(phone=phone).first()


        elif login_type == "WECHAT_WEB":  # 公众号
            wechat['appid'] = subscription_app_id
            wechat['secret'] = subscription_app_secret
            wechat['code'] = code
            if not bind_data:
                wechat_user_info, err = get_openid(login_type, wechat)
                if err:
                    return None, err
                openid = wechat_user_info.get("openid", "")
                unionid = wechat_user_info.get("unionid", "")
                if unionid:
                    user_info, err = WechatService.backstepping(unionid)
                    if user_info and user_info.get("sso_unicode", None):
                        openid = user_info.get("sso_unicode")
                    else:
                        cache.set(openid, {"openid": openid, "unionid": unionid}, 300)  # 5分钟有效期
                        return None, {"error": "0051", "msg": "请绑定手机号",
                                      "wechat_data": {"openid": openid, "unionid": unionid}}
            else:
                openid = bind_data.get("openid", "")
                unionid = bind_data.get("unionid", "")
                phone = bind_data.get("phone", "")

            sso_set, sso_err = WechatService.sso_verify(sso_serve_id, None, sub_appid, False,
                                                        openid,
                                                        unionid)
            if sso_set:
                current_user = user_info_set.filter(id=sso_set['user']).first()
            else:
                current_user = user_info_set.filter(phone=phone).first()

        elif login_type == "WECHAT_APP":  # APP
            wechat['appid'] = app_app_id
            wechat['secret'] = app_app_secret
            wechat['code'] = code

            wechat['code'] = code
            if not bind_data:
                wechat_user_info, err = get_openid(login_type, wechat)
                if err:
                    return None, err
                openid = wechat_user_info.get("openid", "")
                unionid = wechat_user_info.get("unionid", "")
                if unionid:
                    user_info, err = WechatService.backstepping(unionid)
                    if user_info and user_info.get("sso_unicode", None):
                        openid = user_info.get("sso_unicode")
                    else:
                        cache.set(openid, {"openid": openid, "unionid": unionid}, 300)  # 5分钟有效期
                        return None, {"error": "0051", "msg": "请绑定手机号",
                                      "wechat_data": {"openid": openid, "unionid": unionid}}
            else:
                openid = bind_data.get("openid", "")
                unionid = bind_data.get("unionid", "")
                phone = bind_data.get("phone", "")

            sso_set, sso_err = WechatService.sso_verify(sso_serve_id, None, sub_appid, False,
                                                        openid,
                                                        unionid)
            if sso_set:
                current_user = user_info_set.filter(id=sso_set['user']).first()
            else:
                current_user = user_info_set.filter(phone=phone).first()
        else:
            return None, "未支持登录方式"

        # -----------------------逻辑处理-----------------------------------------------

        if other_params is None:
            other_params = {}

        if not current_user:  # 如果不存在则为注册

            base_info = {
                'user_name': get_short_id(8),
                'nickname': gen_one_word_digit(),
                'phone': phone,
                'email': '',
            }
            create_user = BaseInfo.objects.create(**base_info)
            if not create_user:
                return None, "用户注册失败"
            # 注册完成后 重新获取用户信息
            user_info_set = BaseInfo.objects.filter(phone=phone).first()
            user_info = model_to_dict(user_info_set)

            # 生成登录token
            token = WechatService.set_token(user_info.get('id', None), phone, platform_id)

            try:
                other_params.setdefault("user_id", user_info.get('id', None))
                other_params.setdefault("score", "5")  # 用户评分初始化，镖行天下业务逻辑 TODO 后期业务抽离，路程控制
                data, detail_err = DetailInfoService.create_or_update_detail(other_params)
                if detail_err:
                    raise Exception(detail_err)
            except Exception as e:
                logger.error('---首次登录写入用户详细信息异常：' + str(e) + '---')

            # 用户第一次登录即注册，绑定用户的分组ID
            try:
                group_id = other_params.get("group_id")
                if group_id:
                    data, err = UserGroupService.user_bind_group(user_id=user_info.get('id', None), group_id=group_id)
                    write_to_log(
                        prefix="group_id:" + str(other_params.get("group_id", "")) + "绑定部门ID异常",
                        content=err
                    )
            except Exception as err:
                write_to_log(
                    prefix="绑定部门ID异常",
                    content="group_id:" + str(other_params.get("group_id", "")),
                    err_obj=err
                )

            # 检验单点登录信息
            sso_set, sso_err = WechatService.sso_verify(sso_serve_id, user_info.get('id', None), sub_appid, True,
                                                        openid,
                                                        unionid)
            if sso_err:
                return None, sso_err
            # 创建用户登录信息，绑定token
            auth_set, auth_err = WechatService.get_token(user_info.get('id', None), token)
            if auth_err:
                return None, auth_err
        # ----------------------------------------------------------------------
        else:
            # 用户存在的时候
            user_info = model_to_dict(current_user)
            # 检查单点登录信息

            sso_set, sso_err = WechatService.sso_verify(sso_serve_id, user_info.get('id', None), sub_appid, True,
                                                        openid,
                                                        unionid)
            if sso_err:
                return None, sso_err
            # 获取token
            token = WechatService.set_token(user_info.get('id', None), phone, platform_id)
            # 修改用户登录信息，绑定token
            auth_set, auth_err = WechatService.get_token(user_id=user_info.get('id', None), token=token,
                                                         is_create=False)
            if auth_err:
                return None, auth_err

            # 绑定用户关系 邀请关系和收益关系
            data, relate_err = UserRelateToUserService.bind_bxtx_relate(params=other_params, user_info=user_info)
            if relate_err:
                write_to_log(
                    prefix='绑定用户关系异常：' + str(relate_err),
                    content='当前用户ID:' + str(user_info.get("id", "")) + '\n detail_params:' + json.dumps(other_params),
                    err_obj=relate_err
                )

        return {'token': auth_set.token, 'user_info': user_info}, None

    @staticmethod
    def backstepping(unionid):
        user_sso = UserSsoToUser.objects.filter(union_code=unionid).first()
        if user_sso:
            return model_to_dict(user_sso), None
        return None, "单点记录不存在"

    # # 绑定手机号处理
    # @staticmethod
    # def bind_phone(bind_data, login_type, wechat):
    #     if not bind_data:
    #         wechat_user_info, err = get_openid(login_type, wechat)
    #         if err:
    #             return None, err
    #         openid = wechat_user_info.get("openid", "")
    #         unionid = wechat_user_info.get("unionid", "")
    #         if unionid:
    #             user_info, err = WechatService.backstepping(unionid)
    #             if user_info and user_info.get("sso_unicode", None):
    #                 openid = user_info.get("sso_unicode")
    #             else:
    #                 cache.set(openid, {"openid": openid, "unionid": unionid}, 300)  # 5分钟有效期
    #                 return None, {"error": "0051", "msg": "请绑定手机号",
    #                               "wechat_data": {"openid": openid, "unionid": unionid}}
    #     else:
    #         return bind_data, None

    # 生成单点登录记录
    @staticmethod
    def sso_verify(sso_serve_id, user_id, appid, is_exist=True, sso_unicode=None, union_code=None):
        """
        生成单点登录记录
        :param sso_serve_id: 单点登录服务ID
        :param user_id: 用户ID
        :param appid: appid
        :param sso_unicode: 单点登录唯一识别码(微信openid)
        :param union_code: union_id
        :return: param_dict
        """
        query_dict = {}
        query_dict['user_id'] = user_id,
        query_dict['sso_serve_id'] = sso_serve_id,
        # query_dict['sso_serve__sso_account_id'] = sso_account_id,
        # 短信验证码登录和正常登录方式是不会存在openid、appid、union_code
        if sso_unicode:
            query_dict['sso_serve__sso_appid'] = appid
        sso = UserSsoToUser.objects.filter(**query_dict).first()
        if is_exist:
            if not sso:
                sso_data = {
                    "sso_serve_id": sso_serve_id,
                    "user_id": user_id,
                    "sso_unicode": sso_unicode,
                    "union_code": union_code
                }
                create_sso = UserSsoToUser.objects.create(**sso_data)
                if not create_sso:
                    return None, "单点登录写入失败"
            sso_set = UserSsoToUser.objects.filter(**query_dict).first()
            if not sso_set:
                return None, "单点登录用户信息不存在"
            sso_set = model_to_dict(sso_set)
            if not sso_set.get("union_code", None):
                UserSsoToUser.objects.filter(
                    user_id=user_id,
                    sso_serve__sso_appid=appid
                ).update(union_code=union_code)
        else:
            sso_set = UserSsoToUser.objects.filter(sso_unicode=sso_unicode, sso_serve_id=sso_serve_id).order_by(
                '-id').first()
            # print(">>>>>", sso_set)
            if not sso_set:
                return None, "单点记录不存在"
            sso_set = model_to_dict(sso_set)

        return sso_set, None

    # 生成token
    @staticmethod
    def set_token(user_id, account, platform_id):
        # 生成过期时间
        expire_timestamp = datetime.utcnow() + timedelta(
            days=7,
            seconds=0
        )
        # 返回token
        return jwt.encode(
            payload={'user_id': user_id, 'account': account, 'platform_id': platform_id, "exp": expire_timestamp},
            key=jwt_secret_key
        )

    # 查询用户信息
    @staticmethod
    def get_user_info(user_id):
        current_user = BaseInfo.objects.filter(id=user_id).first()
        if not current_user:
            return None, "用户信息查询失败"
        current_user = model_to_dict(current_user)
        return current_user, None

    # 绑定token
    @staticmethod
    def get_token(user_id, token, is_create=True):
        current_user = BaseInfo.objects.filter(id=user_id).first()
        current_user = model_to_dict(current_user)
        if is_create:
            auth = {
                'user_id': current_user.get("id", ""),
                'password': make_password('123456', None, 'pbkdf2_sha1'),
                'plaintext': '123456',
                'token': token,
            }
        else:
            auth = {
                'token': token,
            }
        Auth.objects.update_or_create({'user_id': current_user.get("id", "")}, **auth)
        auth_set = Auth.objects.filter(
            user_id=current_user.get('id', None),
            token__isnull=False
        ).order_by('-update_time').first()

        if not auth_set:
            return None, "密钥生成失败"
        return auth_set, None

    def __del__(self):
        self.redis.close()
