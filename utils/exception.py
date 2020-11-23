from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status


def exception_handler(exc, context):
    # 1.先让drf的exception_handler做基础处理,拿到返回值
    # 2.若有返回值则drf处理了,若返回值为空说明drf没处理,需要我们手动处理
    response = drf_exception_handler(exc, context)
    print(exc)  # 错误内容 'NoneType' object has no attribute 'title'
    print(context)
    # {'view': <api.views.Book object at 0x000001BBBCE05B00>, 'args': (), 'kwargs': {'pk': '3'}, 'request': <rest_framework.request.Request object at 0x000001BBBCF33978>}
    print(response)
    # 返回值为空,做二次处理
    if response is None:
        print('%s - %s - %s' % (context['view'], context['request'].method, exc))
        # <api.views.Book object at 0x00000242DC316940> - GET - 'NoneType' object has no attribute 'title'
        return Response({
            'detail': '服务器错误'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)
    return response
