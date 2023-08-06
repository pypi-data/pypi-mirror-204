# encoding: utf-8
"""
@project: djangoModel->thread_v2
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/7/29 15:11
"""
from django.db.models import F

from xj_user.services.user_detail_info_service import DetailInfoService
from ..models import Thread
from ..services.thread_extend_service import ThreadExtendService, ThreadExtendOutPutService
from ..services.thread_statistic_service import StatisticsService
from ..utils.custom_tool import format_params_handle, force_transform_type
from ..utils.join_list import JoinList


class ThreadItemService:
    """
    信息表新增、修改、详情服务
    """

    @staticmethod
    def add(params: dict = None, **kwargs):
        """
        信息添加
        :param params: 添加参数子字典
        :param kwargs:
        :return:
        """
        # 参数整合与空值验证
        params, is_void = force_transform_type(variable=params, var_type="dict", default={})
        kwargs, is_void = force_transform_type(variable=kwargs, var_type="dict", default={})
        params.update(kwargs)
        # 过滤主表修改字段和扩展表修改字段
        filter_filed_list = [
            "is_deleted", "show", "title", "subtitle", "content", "summary", "access_level", "author", "ip",
            "has_enroll", "has_fee", "has_comment", "has_location", "cover", "photos", "video", "files", "price",
            "is_original", "link", "create_time", "update_time", "logs", "more", "sort",
            "language_code"
        ]
        main_form_data = format_params_handle(
            params.copy(),
            filter_filed_list=filter_filed_list + ["show_id|int", "category_id|int", "classify_id|int", "user_id|int", "with_user_id|int"]
        )
        except_main_form_data = format_params_handle(
            params.copy(),
            remove_filed_list=filter_filed_list + ["show_id", "category_id", "classify_id", "user_id", "with_user_id"]
        )
        # if not main_form_data.get("category_id"):
        #     return None, "不是一个有效的category_id，无法添加信息"

        # IO操作
        try:
            # 主表插入数据
            instance = Thread.objects.create(**main_form_data)
            # 扩展表 插入或更新
            add_extend_res, err = ThreadExtendService.create_or_update(except_main_form_data, instance.id)
        except Exception as e:
            return None, f'''{str(e)} in "{str(e.__traceback__.tb_frame.f_globals["__file__"])}" : Line {str(e.__traceback__.tb_lineno)}'''

        return {"id": instance.id}, None

    @staticmethod
    def detail(pk: int = None):
        """
        获取信息内容
        :param pk: 信息表主键搜索
        :return: data_dict,err
        """
        # 类型转换，判断是否是有效的int类型
        try:
            pk = int(pk)
        except TypeError:
            pk = None

        if pk is None:
            return None, "主键不能为空"

        thread_dict = Thread.objects.filter(id=pk, is_deleted=False).annotate(
            category_value=F("category__value"),
            category_name=F("category__name"),
            category_platform_code=F("category__platform_code"),
            classify_value=F("classify__value"),
            classify_name=F("classify__name"),
            show_value=F("show__value"),
            show_name=F("show__name"),
        ).values(
            "id", "is_deleted", "category_value", "category_name", "category_id", "classify_id", "classify_value", "classify_name",
            "show_id", "show_value", "show_name", "user_id", "with_user_id",
            "title", "subtitle", "content", "summary", "access_level", "author", "ip", "has_enroll", "has_fee", "has_comment", "has_location",
            "cover", "photos", "video", "files", "price", "is_original", "link",
            "create_time", "update_time", "logs", "more", "sort", "language_code"
        ).first()

        # 信息统计表更新数据
        if not thread_dict:
            return None, "数据不存在"

        # ============ 拼接扩展数据 start ============
        #  TODO 代码逻辑待简化
        extend_merge_service = ThreadExtendOutPutService(category_id_list=[thread_dict.get("category_id")], thread_id_list=[pk])
        statistic_list = StatisticsService.statistic_list(id_list=[pk])
        user_info_list = DetailInfoService.get_list_detail(user_id_list=[thread_dict["user_id"]] if thread_dict.get("user_id") else [])
        [extend_data_dict] = extend_merge_service.merge([thread_dict])
        [join_statistic_dict] = JoinList(l_list=[extend_data_dict], r_list=statistic_list, l_key="id", r_key='thread_id').join()
        [join_user_info_list] = JoinList(l_list=[join_statistic_dict], r_list=user_info_list, l_key="user_id", r_key='user_id').join()
        # ============ 拼接扩展数据 end  ============
        # 所有访问成功，则进行统计计数
        StatisticsService.increment(thread_id=pk, tag='views', step=1)
        return join_user_info_list, 0

    @staticmethod
    def edit(params: dict = None, pk: int = None, **kwargs):
        """
        信息编辑服务
        :param params: 信息编辑的字段
        :param pk: 信息表需要修改的主键
        :return: instance，err
        """
        # 参数校验
        params, is_void = force_transform_type(variable=params, var_type="dict", default={})
        kwargs, is_void = force_transform_type(variable=kwargs, var_type="dict", default={})
        params.update(kwargs)
        if not params:
            return None, None
        # 获取要修改的信息主键ID
        pk, is_void = force_transform_type(variable=pk or params.pop("id", None), var_type="int")
        if not pk:
            return None, "不是一个有效的pk"
        # 检查受否是有效的信息ID
        main_res = Thread.objects.filter(id=pk)
        if not main_res.first():
            return None, "数据不存在，无法进行修改"
        # 过滤主表修改字段和扩展表修改字段
        filter_filed_list = [
            "is_deleted", "title", "subtitle", "content", "summary", "access_level", "author", "ip",
            "has_enroll", "has_fee", "has_comment", "has_location", "cover", "photos", "video", "files", "price",
            "is_original", "link", "create_time", "update_time", "logs", "more", "sort",
            "language_code"
        ]
        main_form_data = format_params_handle(
            params.copy(),
            filter_filed_list=filter_filed_list + ["show_id|int", "category_id|int", "classify_id|int", "user_id|int", "with_user_id|int"]
        )
        except_main_form_data = format_params_handle(
            params.copy(),
            remove_filed_list=filter_filed_list + ["show_id", "category_id", "classify_id", "user_id", "with_user_id"]
        )
        # IO操作
        try:
            if main_form_data:
                main_res.update(**main_form_data)  # 主表修改
            if except_main_form_data:
                ThreadExtendService.create_or_update(except_main_form_data, pk, main_form_data.get("category_id", None))  # 扩展字段修改
            return None, None
        except Exception as e:
            return None, "msg:" + "信息主表写入异常：" + str(e) + "  line:" + str(e.__traceback__.tb_lineno) + ";tip:参数格式不正确，请参考服务文档使用"

    @staticmethod
    def delete(pk: int = None):
        """
        软删除信息
        :param pk: 主键ID
        :return: None,err
        """
        pk, is_void = force_transform_type(variable=pk, var_type="int")
        if not pk:
            return None, "非法请求"
        main_res = Thread.objects.filter(id=pk, is_deleted=0)
        if not main_res:
            return None, "数据不存在，无法进行删除"

        main_res.update(is_deleted=1)
        return None, None
