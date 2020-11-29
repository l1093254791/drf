from rest_framework.views import APIView
from rest_framework.response import Response

from .. import serializers, models


class V2Book(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:  # 单查
            try:
                book_obj = models.Book.objects.get(pk=pk, is_deleted=False, is_show=True)
                book_ser = serializers.V2BookModelSerializer(book_obj).data
            except:
                return Response({
                    'status': 1,
                    'msg': '书籍不存在'
                })
        else:  # 群查
            book_query = models.Book.objects.filter(is_deleted=False, is_show=True).order_by('-orders')
            book_ser = serializers.V2BookModelSerializer(book_query, many=True).data

        return Response({
            'status': 200,
            'msg': 'ok',
            'results': book_ser
        })

    def post(self, request, *args, **kwargs):
        '''
        单增: 传的数据是与model对应的一个字典
        群增：设计传递的是多个model对应的字典列表,在postman中通过列表嵌套字典传值
        '''
        request_data = request.data  # 拓展，兼容性最强，三种传参方式都可以：form-data,urlencoding,json
        print(isinstance(request_data, dict))
        if isinstance(request_data, dict):  # 判断获取的数据是否是dict
            many = False
        elif isinstance(request_data, list):  # 判断获取的数据是否是list
            many = True
        else:
            return Response({
                'status': 1,
                'msg': '数据错误'
            })
        book_ser = serializers.V2BookModelSerializer(data=request_data, many=many)
        # 检验是否合格 raise_exception=True必填的
        book_ser.is_valid(raise_exception=True)
        # book_result是对象<class 'app01.models.Book'>，群增就是列表套一个个对象
        book_obj = book_ser.save()
        return Response({
            'status': 200,
            'msg': 'ok',
            'results': serializers.BookModelSerializer(book_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        '''
        单删： 有pk —— 通过路径传参
        群删： 有pks —— 通过json传参
        '''
        pk = kwargs.get('pk')
        if pk:  # 单删
            pks = [pk]
        else:
            pks = request.data.get('pks')
        if models.Book.objects.filter(pk__in=pks, is_deleted=False).update(is_deleted=True):
            return Response({
                'status': 0,
                'msg': '删除成功'
            })
        return Response({
            'status': 1,
            'msg': '书籍不存在或已删除'
        })

    def put(self, request, *args, **kwargs):
        '''
        单整体改：对v2/books/(pk)传的数据是与model对应的字典{name|price|publish|authors}
        '''
        request_data = request.data
        pk = kwargs.get('pk')
        try:
            old_book_obj = models.Book.objects.get(pk=pk, is_deleted=False)
        except:
            # 当输入不存在的pk
            return Response({
                'status': 1,
                'msg': '参数错误'
            })
        # 目的：将众多数据的校验交给序列化类来处理 —— 让序列化类扮演反序列化角色校验成功后，序列化类来帮你入库
        book_ser = serializers.V2BookModelSerializer(instance=old_book_obj, data=request_data)
        book_ser.is_valid(raise_exception=True)
        # 校验通过，完成数据的更新：要更新的目标，用来更新的新数据
        book_obj = book_ser.save()
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.V2BookModelSerializer(book_obj).data
        })

    def patch(self, request, *args, **kwargs):
        '''
        单局部改：对v2/books/(pk)传的数据，数据字段key都是选填
        '''
        request_data = request.data
        if not request_data:
            return Response({
                'status': 1,
                'msg': '请输入要修改的信息',

            })
        pk = kwargs.get('pk')

        try:
            old_book_obj = models.Book.objects.get(pk=pk, is_deleted=False)
        except:
            # 当输入不存在的pk
            return Response({
                'status': 1,
                'msg': '参数错误'
            })
        book_ser = serializers.V2BookModelSerializer(instance=old_book_obj, data=request_data, partial=True)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.V2BookModelSerializer(book_obj).data
        })

    def patch(self, request, *args, **kwargs):
        request_data = request.data  # 数据包数据
        pk = kwargs.get('pk')
        # 将单改，群改的数据都格式化成 pks=[要需要的对象主键标识] | request_data=[每个要修改的对象对应的修改数据]
        if pk and isinstance(request_data, dict):  # 单改
            pks = [pk, ]
            request_data = [request_data, ]
        elif not pk and isinstance(request_data, list):  # 群改
            pks = []
            # 遍历前台数据[{pk:1, name:123}, {pk:3, price:7}, {pk:7, publish:2}]，拿一个个字典
            for dic in request_data:
                pk = dic.pop('pk', None)  # 返回pk值
                if pk:
                    pks.append(pk)
                # pk没有传值
                else:
                    return Response({
                        'status': 1,
                        'msg': '参数错误'
                    })
        else:
            return Response({
                'status': 1,
                'msg': '参数错误'
            })
        # pks与request_data数据筛选，
        # 1）将pks中的没有对应数据的pk与数据已删除的pk移除，request_data对应索引位上的数据也移除
        # 2）将合理的pks转换为 objs
        objs = []
        new_request_data = []
        for index, pk in enumerate(pks):
            try:
                # 将pk合理的对象数据保存下来
                book_obj = models.Book.objects.get(pk=pk, is_delete=False)
                objs.append(book_obj)
                # 对应索引的数据也保存下来
                new_request_data.append(request_data[index])
            except:
                # 重点：反面教程 - pk对应的数据有误，将对应索引的data中request_data中移除
                # 在for循环中不要使用删除
                # index = pks.index(pk)
                # request_data.pop(index)
                continue
        # 生成一个serializer对象
        book_ser = serializers.V2BookModelSerializer(instance=objs, data=new_request_data, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_objs = book_ser.save()

        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.V2BookModelSerializer(book_objs, many=True).data
        })

    '''
    总结：
    1）单整体改：
    V2BookModelSerializer(
        instance=要被更新的对象,
        data=用来更新的数据,
        partial=默认False，必须的字段全部参与校验
    )
    2）单局部改：
    V2BookModelSerializer(
        instance=要被更新的对象,
        data=用来更新的数据,
        partial=设置True，必须的字段全部变为选填字段
    )
    PS：partial设置True的本质就是使字段 required=True 校验规则失效
    '''
