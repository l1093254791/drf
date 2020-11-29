from rest_framework.response import Response
from rest_framework.views import APIView

from .. import models, serializers


class Publish(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                publish_obj = models.Book.Publish.get(pk=pk, is_deleted=False, is_show=True)
                publish_ser_data = serializers.PublishModelSerializer(publish_obj).data
            except:
                return Response({
                    'status': 201,
                    'msg': '书籍不存在',
                })
        else:
            publish_obj_list = models.Publish.objects.filter(is_deleted=False, is_show=True).order_by('-orders')
            publish_ser_data = serializers.PublishModelSerializer(publish_obj_list, many=True).data
        return Response({
            'status': 200,
            'msg': 0,
            'results': publish_ser_data
        })


class Book(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:  # 单查
            try:
                book_obj = models.Book.objects.get(pk=pk, is_deleted=False, is_show=True)
                book_ser_data = serializers.BookModelSerializer(book_obj).data
            except:
                return Response({
                    'status': 201,
                    'msg': '书籍不存在',
                })
        else:  # 群查
            book_obj_list = models.Book.objects.filter(is_deleted=False, is_show=True).order_by('-orders')
            # 不管是一条还是多条，只要数据是被[]嵌套，都要写many=True
            # 返回前端数据
            book_ser_data = serializers.BookModelSerializer(book_obj_list, many=True).data
        return Response({
            'status': 200,
            'msg': 'ok',
            'results': book_ser_data
        })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        book_ser = serializers.BookModelDeserializer(data=request_data)
        # raise_exception=True：当校验失败，马上终止当前视图方法，抛异常返回给前台
        book_ser.is_valid(raise_exception=True)  # 检验是否合格 raise_exception=True必填的
        book_obj = book_ser.save()  # 保存得到一个对象
        return Response({
            'status': 200,
            'msg': 0,
            'results': serializers.BookModelSerializer(book_obj).data
        })
