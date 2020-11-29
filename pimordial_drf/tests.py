from django.test import TestCase

# Create your tests here.
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_Source_code.settings")
    import django

    django.setup()
    # 在这个代码块的下面就可以测试django里面的单个py文件了
    from pimordial_drf import models

    # 外键建在文章表中
    # CASCADE--分类删除，作者跟着删除
    # res = models.Article.objects.all()
    # print(res)
    # res = models.Category.objects.all()
    # print(res)

    models.Category.objects.filter(id=2).delete()
