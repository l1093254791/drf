from rest_framework.views import APIView
from rest_framework.response import Response


class Test(APIView):
    # 局部渲染配置
    # renderer_classes = [JSONRenderer]

    # 局部解析类配置,post提交数据只能解析json格式数据
    # parser_classes = [JSONParser,FormParser]   #如果[]为空，那么就相当于没有设置解析类型
    def get(self, request, *args, **kwargs):
        # url拼接的参数
        print(request._request.GET)  # 二次封装方式
        print(request.GET)  # 兼容
        print(request.query_params)  # 拓展
        print(request.data)
        return Response('drf get ok')

    def post(self, request, *args, **kwargs):
        # 所有请求方式携带的数据包
        print(request._request.POST)  # 二次封装方式
        print(request.POST)  # 兼容
        print(request.data)  # 拓展，兼容性最强，三种传参方式都可以：form-data,urlencoding,json
        print(request.query_params)
        return Response('drf post ok')