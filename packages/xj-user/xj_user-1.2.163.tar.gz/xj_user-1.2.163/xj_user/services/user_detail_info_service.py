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
    # 用户基础表字段列表
    user_base_fields = [i.name for i in BaseInfo._meta.fields]
    # 用户详情表字段
    user_detail_fields = [i.name for i in DetailInfo._meta.fields] + ["user_id"]
    user_detail_expect_extend = [i.name for i in DetailInfo._meta.fields if not "field_" in i.name] + ["user_id"]
    user_detail_remove_fields = [i.name for i in DetailInfo._meta.fields if "field_" in i.name] + ["id", "user"]
    # 详情信息扩展字段获取
    field_map_list = list(ExtendField.objects.all().values("field", 'field_index'))

    @staticmethod
    def get_list_detail(params: dict = None, user_id_list: list = None, filter_fields: list = None):
        """
        详细信息列表
        :param filter_fields: 需要过滤的字段
        :param params: 搜索参数
        :param user_id_list: 用户ID列表
        :return: list,err
        """
        params, is_pass = force_transform_type(variable=params, var_type="int", default={})
        page, is_pass = force_transform_type(variable=params.pop('page', 1), var_type="int", default=1)
        size, is_pass = force_transform_type(variable=params.pop('size', 10), var_type="int", default=10)
        # 查询排序字段处理
        sort = params.pop('sort', "-register_time")
        sort = sort if sort in ["register_time", "-register_time", "user_id", "-user_id"] else "-id"
        # 扩展字段映射字典
        field_map_list = DetailInfoService.field_map_list
        field_map = {item['field_index']: item['field'] for item in field_map_list}
        reversal_filed_map = {item['field']: item['field_index'] for item in field_map_list}
        # 默认返回字段去掉与的敏感信息
        default_field_list = DetailInfoService.user_detail_expect_extend + list(field_map.values()) + ["user_name", "full_name", "nickname", "user_id"]
        all_field_list = DetailInfoService.user_detail_expect_extend + DetailInfoService.user_base_fields + list(field_map.values())
        # 过滤字段处理
        filter_fields = format_list_handle(
            param_list=filter_fields_handler(
                input_field_expression=filter_fields,
                default_field_list=default_field_list,
            ),
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
            user_type=F("user__user_type"),
        ).order_by(sort).values(*filter_fields)
        total = 0

        # id搜索,并且不分页，作为服务提供者
        # 搜索字典过滤处理,过滤掉不允许搜索的字段
        if not user_id_list is None and isinstance(user_id_list, list):
            res_list = detail_info_obj.filter(user_id__in=user_id_list)
        else:
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
            result_list=filter_result_field(  # 扩展字段替换
                result_list=res_list,
                alias_dict=field_map,
            ),
            remove_filed_list=DetailInfoService.user_detail_remove_fields + ["id"],  # 移除未配置的扩展字段已经主键ID
            alias_dict={"user": "user_id", "cover": "user_cover"}
        )
        # 分情况返回数据
        if not user_id_list is None and isinstance(user_id_list, list):
            return res_data
        else:
            return {'size': int(size), 'page': int(page), 'total': total, 'list': res_data}, None

    @staticmethod
    def get_detail(user_id: int = None, search_params: dict = None, filter_fields: list = None):
        """
        获取当前用户的基础信息和详细信息集合
        :param search_params: 根据参数搜索，取第一条
        :param user_id: 通过用户ID搜索
        :param filter_fields: 过滤字段
        :return: detail_info,err_msg
        """
        # ==================== 参数验证 start ==========================
        search_params, is_pass = force_transform_type(variable=search_params, var_type="int", default={})
        search_params = format_params_handle(
            param_dict=search_params,
            filter_filed_list=["user_name", "full_name", "nickname", "phone", "email"]
        )
        if not user_id and not search_params:
            return None, "参数错误，无法检索用户"
        # ==================== 参数验证 end    ==========================

        # ======================= 过滤字段 start ==============================
        # 扩展字段映射
        # 由于联表查询游湖基础表需要加前缀，所以得到了
        extend_field_map = {item['field_index']: item['field'] for item in DetailInfoService.field_map_list}
        filter_fields = format_list_handle(
            param_list=filter_fields_handler(
                input_field_expression=filter_fields,
                all_field_list=DetailInfoService.user_detail_fields + DetailInfoService.user_base_fields
            ),
            alias_dict={i: "user__" + i for i in DetailInfoService.user_base_fields}
        )
        # ======================= 过滤字段 end   ==============================

        # ================== 构建ORM start==========================
        user_base = BaseInfo.objects.extra(select={'register_time': 'DATE_FORMAT(register_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})
        # 允许使用用户ID或者使用条件参数搜素
        if user_id:
            user_base = user_base.filter(id=user_id).first()
        else:
            user_base = user_base.filter(**search_params).first()
        if not user_base:
            return None, '用户不存在'

        # 获取详细信息
        user_detail = DetailInfo.objects.select_related("user").extra(select={
            'birth': 'DATE_FORMAT(birth, "%%Y-%%m-%%d %%H:%%i:%%s")',
            "user__register_time": 'DATE_FORMAT(register_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
        }).filter(user_id=user_id).values(*filter_fields).first()
        # ================== 构建ORM end  ==========================

        # ================== 获取角色模块信息 start ============================
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
        # ================== 获取角色模块信息 end    ============================

        # =========== 判断该用户是否进行过实名制，分情况返回 start =====================
        if not user_detail:  # 当前用户没有填写详细信息的时候
            # 扩展字段默认空字段返回
            user_base_info = user_base.to_json()
            # 获取需要补全的字段
            extend_fields = DetailInfoService.user_detail_expect_extend + list(extend_field_map.values())
            extend_fields.remove("id")
            extend_fields.remove("user_id")
            for i in extend_fields:
                user_base_info[i] = ""

            # 用胡相关权限
            user_base_info["user_role_list"] = user_role_list
            user_base_info["user_group_id_list"] = user_group_list
            # 把user_id重新赋值
            user_base_info["user_id"] = user_base_info["id"]
            return format_params_handle(
                param_dict=user_base_info,
                alias_dict={"user": "user_id"},
                is_remove_null=False
            ), None

        else:
            # 替换用户基础信息字段前缀，替换扩展字段
            filter_dict = format_params_handle(
                param_dict=format_params_handle(
                    param_dict=user_detail,
                    alias_dict=extend_field_map,
                    is_remove_null=False
                ),
                alias_dict={"user__" + i: i for i in DetailInfoService.user_base_fields},
                is_remove_null=False
            )
            # 移除未配置的扩展字段
            filter_dict = format_params_handle(
                param_dict=filter_dict,
                remove_filed_list=DetailInfoService.user_detail_remove_fields,
                is_remove_null=False
            )
            filter_dict["user_role_list"] = user_role_list
            filter_dict["user_group_id_list"] = user_group_list
            # 当前用户填写过详细信息
            return filter_dict, None
        # =========== 判断该用户是否进行过实名制，分情况返回 end =====================

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
