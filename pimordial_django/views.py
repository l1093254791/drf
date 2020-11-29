from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Category


class CategoryView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            """
            查询所有分类
            路由：GET /category/
            """
            # 操作数据库
            queryset = Category.objects.filter(is_show=True, is_deleted=False).order_by('-orders')
            # 序列化过程
            category_list = []
            for category in queryset:
                category_list.append({
                    'id': category.id,
                    'name': category.name,
                    'orders': category.orders,
                    'created_time': category.created_time,
                    'updated_time': category.updated_time
                })
            # 响应数据
            return JsonResponse({
                'status': 200,
                'msg': 'ok',
                'results': category_list,
            }, safe=False)
        else:
            """
            获取单个分类息
            路由： GET  /category/<pk>/
            """
            try:
                category_dic = Category.objects.get(pk=pk, is_show=True, is_deleted=False)
            except Category.DoesNotExist:
                return JsonResponse({
                    'status': 404,
                    'msg': '分类已删除或不显示',
                })
            print(category_dic)
            print(type(category_dic))
            return JsonResponse({
                'status': 200,
                'msg': 'ok',
                'results': {
                    'id': category_dic.id,
                    'name': category_dic.name,
                    'orders': category_dic.orders,
                    'created_time': category_dic.created_time,
                    'updated_time': category_dic.updated_time
                }
            })

    # postman可以完成不同方式的请求:get | post | put ...
    # postman发送数据包有三种方式:form-data| urlencoding | json
    # 原生django对urlencoding方式数据兼容最好
    def post(self, request, *args, **kwargs):
        """
        添加分类
        路由：POST /category/
        """
        # 前台通过urlencoding方式提交数据
        try:
            category_obj = Category.objects.create(**request.POST.dict())
            if category_obj:
                return JsonResponse({
                    'status': 200,
                    'msg': 'ok',
                    'results': {
                        'id': category_obj.id,
                        'name': category_obj.name,
                        'orders': category_obj.orders,
                        'created_time': category_obj.created_time,
                        'updated_time': category_obj.updated_time
                    }
                })
        except:
            return JsonResponse({
                'status': 404,
                'msg': '参数有误',
            })
        print(request.POST)
        print(request.body)
        return JsonResponse({
            'status': 200,
            'msg': '添加成功',
        }, safe=False)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        """
        删除分类
        路由： DELETE /category/<pk>/
        """
        try:
            category = Category.objects.get(pk=pk)
            print(category)
        except Category.DoesNotExist:
            return HttpResponse(status=404)

        # category.delete()
        return HttpResponse(status=204)
