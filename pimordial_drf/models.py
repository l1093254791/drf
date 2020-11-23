from django.db import models

from utils.base_model import BaseModel


class User(models.Model):
    SEX_CHOICES = [
        (0, '男'),
        (1, '女'),
    ]
    name = models.CharField(max_length=64)
    pwd = models.CharField(max_length=32)
    phone = models.CharField(max_length=11, null=True, default=None)
    sex = models.IntegerField(choices=SEX_CHOICES, default=0)
    icon = models.ImageField(upload_to='icon', default='icon/default.jpg')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text='添加时间')

    class Meta:
        db_table = 'UserInfo'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % self.name


class Book(BaseModel):
    """书籍模型"""
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    img = models.ImageField(upload_to='img', default='img/default.jpg')

    # 关联作者表
    authors = models.ManyToManyField(
        to='Author',
        db_constraint=True,  # 断开关联
        related_name='books'  # 反向查询字段
    )
    # 关联出版社表
    publish = models.ForeignKey(
        to='Publish',  # 关联publish表
        db_constraint=False,  # 断关联（断开Book表和Publish表的关联,方便删数据,虽然断开了关联但是还能正常使用）
        related_name='books',  # 反向查询字段：publish_obj.books就能查出当前出版社出版的的所有书籍
        on_delete=models.DO_NOTHING,  # 设置连表操作关系
    )

    class Meta:
        db_table = 'book'
        verbose_name = '书籍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 出版社表
class Publish(BaseModel):
    """出版社模型"""
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)

    class Meta:
        db_table = 'publish'
        verbose_name = '出版社'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 作者表
class Author(BaseModel):
    """作者模型"""
    name = models.CharField(max_length=64)
    age = models.IntegerField()

    class Meta:
        db_table = 'author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 作者详情
class AuthorDetail(BaseModel):
    """mobile, author、is_delete、create_time"""
    mobile = models.CharField(max_length=11)
    author = models.OneToOneField(
        to='Author',
        db_constraint=False,
        related_name='detail',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'author_detail'
        verbose_name = '作者详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author.name
