from rest_framework.views import APIView
from rest_framework.response import Response

from .. import models
from ..serializers import UserSerializer, UserDeserializer


class User(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        print(pk)
        if pk:  # 单查
            try:
                # 用户对象不能直接作为数据返回给前台
                # type(user_obj):class 'app01.models.User'
                user_obj = models.User.objects.get(pk=pk)
                # 序列化一下用户对象
                # type(user_ser)   <class 'app01.serializers.UserSerializer'>
                user_ser = UserSerializer(user_obj)
                return Response({
                    'status': 200,
                    'msg': 0,
                    'results': user_ser.data  # 如果你在序列化的时候没有.data,那么在传给前端的时候必须要.data
                })
            except:
                return Response({
                    'status': 201,
                    'msg': '用户不存在',
                })
        else:  # 群查
            # 用户对象列表(queryset)不能直接作为数据返回给前台
            user_obj_list = models.User.objects.all()
            # 序列化一下用户对象
            user_ser_data = UserSerializer(user_obj_list, many=True).data
            return Response({
                'status': 200,
                'msg': 0,
                'results': user_ser_data
            })

    # 只考虑单增
    def post(self, request, *args, **kwargs):
        # 请求数据
        print(request.data)
        request_data = request.data
        # 数据是否合法（增加对象需要一个字典数据）
        if not isinstance(request_data, dict) or request_data == {}:
            return Response({
                'status': 1,
                'msg': '数据有误',
            })
        # 数据类型合法，但数据内容不一定合法，需要校验数据，校验(参与反序列化)的数据需要赋值给data
        book_ser = UserDeserializer(data=request_data)

        # 序列化对象调用is_valid()完成校验，校验失败的失败信息都会被存储在 序列化对象.errors
        if book_ser.is_valid():
            # 校验通过，完成新增
            book_obj = book_ser.save()
            return Response({
                'status': 0,
                'msg': 'ok',
                'results': UserSerializer(book_obj).data
            })
        else:
            # 校验失败
            return Response({
                'status': 1,
                'msg': book_ser.errors,
            })

    def update(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
