from django.db import models

from utils.base_model import BaseModel


class Category(BaseModel):
    """分类"""
    name = models.CharField(verbose_name="分类", help_text='分类"', max_length=50)

    class Meta:
        db_table = 'category'
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
