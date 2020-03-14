from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class UUIDField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64)
        kwargs['blank'] = True
        models.CharField.__init__(self, *args, **kwargs)

    def pre_save(self, model_instance, add):
        if add:
            value = str(uuid.uuid4())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(models.CharField, self).pre_save(model_instance, add)


class UUIDDemo(models.Model):
    id = UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=16, verbose_name='name')

    class Meta:
        verbose_name = "test_uuid"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    资产表，包含相同属性
    """
    asset_type_choices = (
        ('server', u'服务器'), ('networkDevice', u'网络设备'), ('storageDevice', u'存储设备'),
        ('securityDevice', u'安全设备'), ('software', u'软件资产'), ('other', u'其他资产'))
    asset_status_choices = (
        (0, u'下线'), (1, u'在线'), (2, u'故障'), (3, u'备件')
    )
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, default='server')
    name = models.CharField(max_length=64, unique=True)
    sn = UUIDField(u'资产SN号', max_length=128, unique=True, primary_key=True, editable=False)
    manufactory = models.ForeignKey('Manufactory', verbose_name=u'制造商', null=True, blank=True,
                                    related_name='manufactory', on_delete=models.PROTECT)
    management_ip = models.GenericIPAddressField(u'管理IP', blank=True, null=True)  # 资产管理IP,可为空
    status = models.SmallIntegerField(choices=asset_status_choices, default=1)
    buy_date = models.DateField(u'购买时间', null=True, blank=True)
    expire_date = models.DateField(u'过保修期', null=True, blank=True)

    admin = models.ForeignKey('AdminUser', verbose_name=u'管理员', null=True, blank=True, related_name='admins', on_delete=models.PROTECT)
    comment = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<id:%s name:%s>' % (self.id, self.name)


class Server(models.Model):
    """
    服务器模型
    """
    asset = models.OneToOneField('Asset', related_name='servers', on_delete=models.CASCADE)
    sub_asset_type_choices = (
        (0, u'PC服务器'),
        (1, u'塔式服务器'),
        (2, u'小型机'),
    )
    created_by_choices = (
        ('auto', 'Auto'),
        ('manual', 'Manual'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name=u'服务器类型', default=0)
    created_by = models.CharField(choices=created_by_choices, max_length=32, default='auto')
    # auto: 自动录入,  manual:手动录入
    model = models.CharField(verbose_name=u'型号', max_length=128, null=True, blank=True)
    os_type = models.CharField(u'操作系统类型', max_length=64, blank=True, null=True)
    os_release = models.CharField(u'发行版本', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"

    def __str__(self):
        return '%s sn:%s' % (self.asset.name, self.asset.sn)


class SecurityDevice(models.Model):
    """
    安全设备模型
    """
    asset = models.OneToOneField('Asset', related_name='security_servers', on_delete=models.CASCADE)
    sub_asset_type_choices = (
        (0, u'防火墙'),
        (1, u'入侵检测设备'),
        (2, u'防病毒网关'),
        (4, u'审计设备'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name=u'安全设备类型', default=0)
    model = models.CharField(verbose_name=u'型号', max_length=128, null=True, blank=True)

    def __str__(self):
        return self.asset.id


class NetworkDevice(models.Model):
    """
    网络设备模型
    """
    asset = models.OneToOneField('Asset', related_name='network_devices', on_delete=models.CASCADE)
    sub_asset_type_choices = (
        (0, u'路由器'),
        (1, u'交换机'),
        (2, u'负载均衡'),
        (4, u'VPN'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name=u'网络设备类型', default=0)
    intranet_ip = models.GenericIPAddressField(u'内网IP', blank=True, null=True)
    model = models.CharField(u'型号', max_length=128, null=True, blank=True)
    firmware_release = models.CharField(u'固件版本', max_length=64, blank=True, null=True)
    device_detail = models.TextField(u'设置详细配置', null=True, blank=True)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = verbose_name


class Manufactory(models.Model):
    """
    厂商模型
    """
    manufactory = models.CharField(u'厂商名称', max_length=64, unique=True)
    support_num = models.CharField(u'支持电话', max_length=32, blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True)

    def __str__(self):
        return self.manufactory

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = verbose_name


class EventLog(models.Model):
    """
    变更日志
    """
    name = models.CharField(u'事件名称', max_length=100)
    event_type_choices = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务相关'),
        (7, u'其它'),
    )
    event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choices)
    asset = models.ForeignKey('Asset', on_delete=models.DO_NOTHING)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间', auto_now_add=True)
    user = models.ForeignKey('AdminUser', verbose_name=u'事件源', on_delete=models.DO_NOTHING)
    comment = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = verbose_name


class AdminUser(User):
    """
    管理员模型，继承User
    """
    department = models.CharField('部门信息', max_length=64)

    def __str__(self):
        return self.department

    class Meta:
        super(User.Meta)
        verbose_name = '用户'
        verbose_name_plural = verbose_name
