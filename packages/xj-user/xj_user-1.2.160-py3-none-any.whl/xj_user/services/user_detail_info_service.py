# encoding: utf-8
"""
@project: djangoModel->user_info_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户信息服务
@created_time: 2022/6/27 19:51
"""
from django.core.paginator import Paginator, EmptyPage
from django.db.models import F

from ..models import ExtendField, DetailInfo, BaseInfo
from ..utils.custom_tool import *


class DetailInfoService:

    @staticmethod
    def get_list_detail(params=None, user_id_list: list = None, filter_fields: list = None):
        """
        详细信息列表
        :param filter_fields: 需要过滤的字段
        :param params: 搜索参数
        :param user_id_list: 用户ID列表
        :return: list,err
        """
        if params is None:
            params = {}
        page = params.pop('page', 1)
        size = params.pop('size', 20)
        # 查询排序字段处理
        sort = params.pop('sort', "-register_time")
        sort = sort if sort in ["register_time", "-register_time", "user_id", "-user_id"] else "-id"
        # 扩展字段映射字典
        field_map_list = list(ExtendField.objects.all().values("field", 'field_index'))
        field_map = {item['field_index']: item['field'] for item in field_map_list}
        reversal_filed_map = {item['field']: item['field_index'] for item in field_map_list}
        # 过滤字段相关列表
        remove_field_list = [i.name for i in DetailInfo._meta.fields if i.name[0:6] == "field_"] + ["id"]
        all_field_list = [i.name for i in DetailInfo._meta.fields if not i.name[0:6] == "field_"] + \
                         ["user_name", "full_name", "nickname", "phone", "email", "register_time", "user_info",
                          "privacies", "user_type", "user_id"] + \
                         list(field_map.values())
        default_field_list = format_list_handle(  # 默认字段移除了用户的敏感信息
            param_list=all_field_list,
            remove_filed_list=["phone", "email", "register_time", "user_info", "privacies"],
        )

        # 过滤字段处理
        filter_fields = filter_fields_handler(
            default_field_list=default_field_list,
            input_field_expression=filter_fields,
        )
        filter_fields = format_list_handle(
            param_list=filter_fields,
            filter_filed_list=all_field_list,
            alias_dict=reversal_filed_map
        )

        # 查询ORM构建
        detail_info_obj = DetailInfo.objects.annotate(
            user_name=F("user__user_name"),
            full_name=F("user__full_name"),
            nickname=F("user__nickname"),
            phone=F("user__phone"),
            email=F("user__email"),
            register_time=F("user__register_time"),
            user_info=F("user__user_info"),
            privacies=F("user__privacies"),
            # wechat_openid=F("user__wechat_openid"),
            # wechat_appid=F("user__wechat_appid"),
            user_type=F("user__user_type"),
        ).order_by(sort).values(*filter_fields)

        total = 0
        if not user_id_list is None and isinstance(user_id_list, list):  # id搜索,并且不分页，作为服务提供者
            res_list = detail_info_obj.filter(user_id__in=user_id_list)
        else:  # 分页 条件数据，接口提供者
            # 搜索字典过滤处理,过滤掉不允许搜索的字段
            search_params = format_params_handle(
                param_dict=params,
                filter_filed_list=all_field_list,
                alias_dict=reversal_filed_map
            )
            search_params = format_params_handle(
                param_dict=search_params,
                alias_dict={
                    "user_name": "user_name__contains",
                    "nickname": "nickname__contains",
                    "email": "email__contains",
                    "phone": "phone__contains",
                    "full_name": "full_name__contains",
                    "real_name": "real_name__contains"
                }
            )
            list_set = detail_info_obj.filter(**search_params)
            total = list_set.count()
            paginator = Paginator(list_set, size)
            try:
                list_set = paginator.page(page)
            except EmptyPage:
                list_set = paginator.page(paginator.num_pages)
            except Exception as e:
                return None, e.__str__()
            res_list = list(list_set.object_list)

        res_data = filter_result_field(
            result_list=res_list,
            alias_dict=field_map,
        )
        res_data = filter_result_field(
            result_list=res_data,
            remove_filed_list=remove_field_list,
            alias_dict={"user": "user_id", "cover": "user_cover"}
        )

        if not user_id_list is None and isinstance(user_id_list, list):
            return res_data
        else:
            return {'size': int(size), 'page': int(page), 'total': total, 'list': res_data}, None

    @staticmethod
    def get_detail(user_id: int = None, search_params: dict = None):
        """
        获取当前用户的基础信息和详细信息集合
        :param search_params: 根据参数搜索，取第一条
        :param user_id: 通过用户ID搜索
        :return: detail_info,err_msg
        """
        # 参数验证
        if search_params is None:
            search_params = {}
        search_params = format_params_handle(
            param_dict=search_params,
            filter_filed_list=["user_name", "full_name", "nickname", "phone", "email"]
        )
        if not user_id and not search_params:
            return None, "参数错误，无法检索用户"

        user_base = BaseInfo.objects

        user_base = user_base.extra(
            select={'register_time': 'DATE_FORMAT(register_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})

        # 允许使用用户ID或者使用条件参数搜素
        if user_id:
            user_base = user_base.filter(id=user_id).first()
        else:
            user_base = user_base.filter(**search_params).first()
        if not user_base:
            return None, '用户不存在'

        # 获取用户信息字典，补充用户ID
        user_base_info = user_base.to_json()
        user_id = user_id if user_id else user_base_info.get("id")

        # 获取扩展字段
        field_dict = {item['field_index']: item['field'] for item in ExtendField.objects.all().values("field", 'field_index')}
        # 剔除未配置的扩展字段,以及添加基础信息字段
        out_put_fields = [i.name for i in DetailInfo._meta.fields if not i.name[0:6] == "field_"] + \
                         [i.name for i in BaseInfo._meta.fields] + \
                         ["user_group_id_list", "user_role_id_list", "user_id"] + \
                         list(field_dict.values())

        # 获取详细信息
        user_detail = DetailInfo.objects.filter(user_id=user_id).annotate(
            user_name=F("user__user_name"),
            full_name=F("user__full_name"),
            nickname=F("user__nickname"),
            phone=F("user__phone"),
            email=F("user__email"),
            register_time=F("user__register_time"),
            user_info=F("user__user_info"),
            privacies=F("user__privacies"),
            # wechat_openid=F("user__wechat_openid"),
            # wechat_appid=F("user__wechat_appid"),
        ).values().first()

        # 获取用户的部门信息
        try:
            if not getattr(sys.modules.get("xj_role.services.role_service"), "RoleService", None):
                from xj_role.services.role_service import RoleService
            else:
                RoleService = getattr(sys.modules.get("xj_role.services.role_service"), "RoleService")
            user_role_list, err = RoleService.get_user_role_info(user_id=user_id, field_list=["role_id"])
            user_role_list = [i["role_id"] for i in user_role_list]
        except Exception:
            user_role_list = []

        # 获取角色的信息信息
        try:
            if not getattr(sys.modules.get("xj_role.services.user_group_service"), "UserGroupService", None):
                from xj_role.services.user_group_service import UserGroupService
            else:
                UserGroupService = getattr(sys.modules.get("xj_role.services.user_group_service"), "UserGroupService")
            user_group_list, err = UserGroupService.get_user_group_info(user_id=user_id, field_list=["user_group_id"])
            user_group_list = [i["user_group_id"] for i in user_group_list]
        except Exception:
            user_group_list = []

        # 返回用户信息
        if not user_detail:  # 当前用户没有填写详细信息的时候
            # 默认空字段返回
            user_base_info_fields = user_base_info.keys()
            for i in out_put_fields:
                if i in user_base_info_fields:
                    continue
                user_base_info[i] = ""
            user_base_info["user_id"] = user_base_info["id"]  # 把user_id重新赋值

            user_base_info["user_role_list"] = user_role_list
            user_base_info["user_group_id_list"] = user_group_list
            return format_params_handle(
                param_dict=user_base_info,
                alias_dict={"user": "user_id"},
                is_remove_null=False,
                date_format_dict={"register_time": ("%Y-%m-%dT%H:%m:%s", "%Y-%m-%d %H:%m:%s")}
            ), None
        else:
            # 扩展字段转换
            alias_dict = format_params_handle(
                param_dict=user_detail,
                alias_dict=field_dict,
                is_remove_null=False
            )
            # 去掉未配置的扩展字段
            filter_dict = format_params_handle(
                param_dict=alias_dict,
                filter_filed_list=out_put_fields,
                is_remove_null=False,
                date_format_dict={"register_time": ("%Y-%m-%dT%H:%m:%s", "%Y-%m-%d %H:%M:%S")}
            )
            filter_dict.pop("id", None)

            # 当前用户填写过详细信息
            filter_dict["user_role_id_list"] = user_role_list
            filter_dict["user_group_id_list"] = user_group_list
            return filter_dict, None

    @staticmethod
    def create_or_update_detail(params):
        """
        添加或者更新用户的详细信息
        :param params: 添加/修改参数
        :return: None,err_msg
        """
        # 参数判断
        if not params:
            return None, None
        user_id = params.pop('user_id', None)

        # 判断类型
        try:
            user_id = int(user_id)
        except TypeError:
            user_id = None

        if not user_id:
            return None, "参数错误"

        # 判断用户是否存在
        user_base = BaseInfo.objects.filter(id=user_id)
        user_base_info = user_base.first()
        if not user_base_info:
            return None, '用户不存在'

        # 扩展字段处理，还原
        extend_field_list = ExtendField.objects.all().values("field", 'field_index', 'default')
        alias_dict = {item['field']: item['field_index'] for item in extend_field_list}  # 字段还原映射字典
        default_map = {item['field_index']: item['default'] for item in extend_field_list if not item['default'] is None}  # 默认字段

        filter_filed_list = [i.name for i in DetailInfo._meta.fields]  # 字段列表
        # 强制类型转换,防止修改报错
        filter_filed_list.remove("birth")
        filter_filed_list.remove("region_code")
        filter_filed_list.append("birth|date")
        filter_filed_list.append("region_code|int")

        # 把扩展字段还原成field_1 ....
        alias_params = format_params_handle(
            param_dict=params,
            alias_dict=alias_dict
        )
        # 剔除掉不是配置的扩展字段,还有原表的字段
        transformed_params = format_params_handle(
            param_dict=alias_params,
            filter_filed_list=filter_filed_list
        )
        if not transformed_params:
            return None, None

        transformed_params.setdefault("user_id", user_id)
        # 进行数据库操作
        try:
            # 判断是否添加过
            detail_user_obj = DetailInfo.objects.filter(user_id=user_id)
            if not detail_user_obj.first():
                # 没有添加，进行添加操作
                transformed_params.pop("id", None)  # 添加的时候不能有ID主键，防止主键冲突
                # 在添加的时候给字段默认值
                for field_index, default in default_map.items():
                    transformed_params.setdefault(field_index, default)

                DetailInfo.objects.create(**transformed_params)
            else:
                # 添加过进行跟新
                detail_user_obj.update(**transformed_params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)

    @staticmethod
    def get_extend_fields():
        fields = ExtendField.objects.order_by("-sort").all().to_json()
        return fields, None
