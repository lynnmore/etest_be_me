from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Products(models.Model):
    name = models.TextField(verbose_name='产品线名称')
    parent_id = models.IntegerField(verbose_name='父级id', default=0)
    type_choice = ((0, '产品线'), (1, '产品'), (2, '产品模块'))
    type = models.SmallIntegerField(verbose_name='类型', choices=type_choice)
    rm_id = models.IntegerField(verbose_name='release manager里的产品id', null=True, blank=True)
    wx_hook = models.JSONField(verbose_name='企业微信机器人')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    old_id = models.TextField(verbose_name='原始项目id', null=True, blank=True)
    last_modified_user = models.IntegerField(verbose_name='最后修改人id', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_user = models.IntegerField(verbose_name="创建人id")


class Testers(AbstractUser):
    account = models.TextField(verbose_name='账户')
    role_choice = ((0, '管理员'), (1, '主管'), (3, '普通人员'))
    role = models.SmallIntegerField(verbose_name='类型', choices=role_choice)
    is_first_login = models.BooleanField(verbose_name='是否第一次登录', default=True)
    product = models.ManyToManyField(to=Products, db_constraint=False)
    old_id = models.IntegerField(verbose_name='原始id', null=True, blank=True)


class Services(models.Model):
    name = models.TextField(verbose_name='服务名称')
    last_modified_user = models.IntegerField(verbose_name='最后修改人id', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_user = models.ForeignKey(to=Testers, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='创建人id')
    product = models.ForeignKey(to=Products, db_constraint=False, on_delete=models.DO_NOTHING)


class Apis(models.Model):
    name = models.TextField(verbose_name='请求名称')
    tag = models.TextField(verbose_name='分组标签')
    version = models.SmallIntegerField(verbose_name='版本')
    path = models.TextField(verbose_name='api 路径')
    method = models.TextField(verbose_name='请求类型')
    parameters = models.JSONField(verbose_name='请求参数')
    content_type = models.TextField(verbose_name='请求参数类型', null=True, blank=True)
    request_body = models.JSONField(verbose_name='请求体')
    responses = models.JSONField(verbose_name='响应体')
    security = models.JSONField(verbose_name='token')
    original_parameters = models.JSONField(verbose_name='原始swagger中的请求参数')
    original_request_body = models.JSONField(verbose_name='原始swagger中的请求体')
    original_responses = models.JSONField(verbose_name='原始swagger中的响应体')
    module_id = models.IntegerField(verbose_name='模块id', default=0)
    ref_data_structs = models.JSONField(verbose_name='依赖的数据结构')
    different = models.JSONField(verbose_name='与上个版本的不同', null=True, blank=True)
    is_latest = models.BooleanField(verbose_name='是否为最新版本')
    source_id = models.TextField(verbose_name='原始api id')
    body_format = models.JSONField(verbose_name='请求体格式', default=dict)
    response_format = models.JSONField(verbose_name='响应体格式', default=dict)
    struct_format = models.JSONField(verbose_name='数据模型格式', default=dict)
    commit_id = models.TextField(verbose_name='记录每一次导入的id')
    last_modified_user = models.IntegerField(verbose_name='最后修改人id', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    api_type = models.SmallIntegerField(verbose_name='api 来源类型', default=int)
    remark = models.TextField(verbose_name='接口备注', null=True, blank=True)
    status = models.SmallIntegerField(verbose_name='手动添加接口的状态', null=True, blank=True)
    create_user = models.ForeignKey(to=Testers, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='创建人id')
    product = models.ForeignKey(to=Products, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='产品id')
    service = models.ForeignKey(to=Services, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='服务id')


class Envs(models.Model):
    name = models.TextField(verbose_name='名称')
    type_choice = ((0, '产品线全局变量'), (1, '产品级变量'), (2, '环境变量'))
    type = models.SmallIntegerField(verbose_name='类型', choices=type_choice)
    description = models.TextField(verbose_name='描述')
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    last_modified_user = models.IntegerField(verbose_name='最后修改人id', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_user = models.ForeignKey(to=Testers, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='创建人id')
    product = models.ForeignKey(to=Products, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='产品id')


class EnvVariables(models.Model):
    name = models.TextField(verbose_name='名称')
    description = models.TextField(verbose_name='描述')
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    last_modified_user = models.IntegerField(verbose_name='最后修改人id', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_user = models.ForeignKey(to=Testers, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='创建人id')
    env = models.ForeignKey(to=Envs, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='产品id')

    class Meta:
        db_table = 'app_env_variables'


class Cases(models.Model):
    api_source_id = models.TextField(verbose_name='api 模型的source id')
    source_id = models.TextField(verbose_name='case 的source id')
    version = models.SmallIntegerField(verbose_name='用例版本')
    method = models.TextField(verbose_name='请求方式')
    path = models.TextField(verbose_name='api地址')
    name = models.TextField(verbose_name='名称')
    priority = models.TextField(verbose_name='优先级')
    tag = models.TextField(verbose_name='分类标签', default=list)
    description = models.TextField(verbose_name='描述', default=str)
    setup = models.JSONField(verbose_name='前置操作')
    teardown = models.JSONField(verbose_name='后置操作')
    pre_depend = models.JSONField(verbose_name='前置依赖', default=dict)
    headers = models.JSONField(verbose_name='请求头')
    query_params = models.JSONField(verbose_name='query 参数', default=dict)
    rest_params = models.JSONField(verbose_name='rest 参数', default=dict)
    request_body = models.TextField(verbose_name='请求体', default=str)
    assert_response_status_code = models.SmallIntegerField(verbose_name='断言状态码')
    assert_response_header = models.JSONField(verbose_name='断言返回头', default=dict)
    assert_response_body = models.JSONField(verbose_name='断言返回体', default=dict)
    assert_response_time = models.IntegerField(verbose_name='断言返回时间')
    ref_vars = models.JSONField(verbose_name='依赖变量key集合',default=list)
    exec_num = models.IntegerField(verbose_name='用例执行次数', default=int)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    last_modified_user = models.IntegerField(verbose_name='最后修改人id', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_user = models.ForeignKey(to=Testers, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='创建人id')
    api = models.ForeignKey(to=Apis, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='api id')
    product = models.ForeignKey(to=Products, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='产品 id')


class CaseVariables(models.Model):
    case_source_id = models.IntegerField(verbose_name='case的source id', null=True, blank=True)
    name = models.TextField(verbose_name='变量名')
    value = models.TextField(verbose_name='变量值')
    extract_type = models.TextField(verbose_name='提取方式')
    description = models.TextField(verbose_name='描述', default=str)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    last_modified_user = models.IntegerField(verbose_name='最后修改人id', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_user = models.ForeignKey(to=Testers, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='创建人id')
    case = models.ForeignKey(to=Cases, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='用例 id')
    product = models.ForeignKey(to=Products, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='产品 id')

    class Meta:
        db_table = 'app_case_variables'


class Iterations(models.Model):
    name = models.TextField(verbose_name='迭代计划名')
    description = models.TextField(verbose_name='迭代计划描述', default=str)
    rm_version = models.TextField(verbose_name='rm 中的版本号', default=str)
    plan_start_date = models.DateTimeField(verbose_name='计划开始时间')
    plan_end_date = models.DateTimeField(verbose_name='计划结束时间')
    actual_release_date = models.DateTimeField(verbose_name='实际发版时间', null=True, blank=True)
    testers = models.JSONField(verbose_name='测试人员', default=list)
    type_choice = ((0, '进行中'), (1, '已完成'), (2, '已延期'))
    status = models.SmallIntegerField(verbose_name='迭代计划状态', choices=type_choice)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    last_modified_user = models.IntegerField(verbose_name='最后修改人id', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_user = models.ForeignKey(to=Testers, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='创建人id')
    leader = models.ForeignKey(to=Testers, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='负责人id')
    env = models.ForeignKey(to=Envs, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='环境 id')
    product = models.ForeignKey(to=Products, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='产品 id')


class Tasks(models.Model):
    name = models.TextField(verbose_name='任务名')
    description = models.TextField(verbose_name='描述', default=str)
    cron = models.TextField(verbose_name='定时表达式', default=str)
    product_line_id = models.IntegerField(verbose_name='产品线id')
    wx_hook = models.JSONField(verbose_name='企业微信机器人', default=list)
    job_id = models.IntegerField(verbose_name='job id')
    enable = models.BooleanField(verbose_name='是否启用定时任务', default=False)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    last_modified_user = models.IntegerField(verbose_name='最后修改人id', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_user = models.ForeignKey(to=Testers, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='创建人id')
    env = models.ForeignKey(to=Envs, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='环境 id')
    product = models.ForeignKey(to=Products, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='产品 id')


class Scenes(models.Model):
    name = models.TextField(verbose_name='场景名')
    description = models.TextField(verbose_name='描述', default=str)
    is_release = models.BooleanField(verbose_name='是否被导出为交付物', default=False)
    type = models.SmallIntegerField(verbose_name='场景类型', default=0)
    error_continue = models.BooleanField(verbose_name='失败是否继续', default=False)
    last_execution_status_choices = ((0, '未执行'), (1, '成功'), (2, '失败'))
    last_execution_status = models.BooleanField(verbose_name='最后执行的状态', choices=last_execution_status_choices, null=True, blank=True)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    last_execution_time = models.DateTimeField(verbose_name='最后执行的时间', null=True, blank=True)
    last_modified_user = models.IntegerField(verbose_name='最后修改人id', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_user = models.ForeignKey(to=Testers, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='创建人id')
    iteration = models.ForeignKey(to=Iterations, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='迭代计划id')
    task = models.ForeignKey(to=Tasks, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='定时任务id')


class IterationApiRelation(models.Model):
    api_version = models.SmallIntegerField(verbose_name='接口版本')
    api_source_id = models.TextField(verbose_name='接口source id')
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    last_modified_user = models.IntegerField(verbose_name='最后修改人id', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_user = models.ForeignKey(to=Testers, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='创建人id')
    iteration = models.ForeignKey(to=Iterations, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='迭代计划id')
    api = models.ForeignKey(to=Apis, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='接口id')

    class Meta:
        db_table = 'api_iteration_api_relation'


class SceneCaseRelation(models.Model):
    case_source_id = models.TextField(verbose_name='用例source id', null=True, blank=True)
    is_first = models.BooleanField(verbose_name='是否为第一条用例', default=False)
    next_case_id = models.IntegerField(verbose_name='下一条用例id', null=True, blank=True)
    index = models.IntegerField(verbose_name='在场景中的顺序')
    is_skip = models.BooleanField(verbose_name='是否跳过', default=False)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)
    last_modified_user = models.IntegerField(verbose_name='最后修改人id', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_user = models.ForeignKey(to=Testers, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='创建人id')
    scene = models.ForeignKey(to=Scenes, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='场景id')
    case = models.ForeignKey(to=Cases, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='用例id')

    class Meta:
        db_table = 'api_scene_case_relation'


class Reports(models.Model):
    uuid = models.TextField(verbose_name='uuid')
    result = models.JSONField(verbose_name='执行结果')
    success = models.BooleanField(verbose_name='总览的执行结果')
    scene_id = models.IntegerField(null=True, blank=True)
    iteration_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class TaskSceneRelation(models.Model):
    scene = models.ForeignKey(to=Scenes, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='场景id')
    task = models.ForeignKey(to=Tasks, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='任务id')

    class Meta:
        db_table = 'api_task_scene_relation'










