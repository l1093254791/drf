from django.db import models


class BaseModel(models.Model):
    """公共模型"""
    is_show = models.BooleanField(default=False, verbose_name="是否显示", help_text='是否显示')
    orders = models.IntegerField(default=1, verbose_name="排序", help_text='排序')
    # 默认不是删除，数据库中是0/1
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除", help_text='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text='添加时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name="修改时间", help_text='修改时间')

    class Meta:
        # 设置当前模型为抽象模型，在数据迁移的时候django就不会为它单独创建一张表
        abstract = True  # 声明该表只是一个抽象表不出现在数据库中
