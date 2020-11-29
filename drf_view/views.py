from rest_framework.views import APIView

from .serializers import BookModelSerializer

from pimordial_drf import models

from utils.response import APIResponse


class BookListView(APIView):
    def get(self, request):
        books_query = models.Book.objects.filter(is_deleted=False).all()
        book_ser = BookModelSerializer(instance=books_query, many=True)
        return APIResponse(results=book_ser.data)


'''
GenericAPIView是继承APIView的，使用完全兼容APIView，主要增加了操作序列化器和数据库查询的方法，作用是为下面Mixin扩展类的执行提供方法支持。通常在使用时，可以配合一个或多个Mixin扩展类
重点：GenericAPIView在APIView基础上完成了哪些事  
    1）get_queryset()：从类属性queryset中获得model的queryset数据                                   群操作就走get_queryset()方法(包括群查，群增等)
    2）get_object()：从类属性queryset中获得model的queryset数据，再通过有名分组pk确定唯一操作对象     单操作就走get_object()方法（包括单查，单增等）
    3）get_serializer()：从类属性serializer_class中获得serializer的序列化类
'''
from rest_framework.generics import GenericAPIView


class BookGenericAPIView(GenericAPIView):
    queryset = models.Book.objects.filter(is_deleted=False)
    serializer_class = BookModelSerializer

    # 自定义主键的有名分组
    # lookup_field = 'id'
    # #群查
    # def get(self, request):
    #     # books_query = models.Book.objects.filter(is_deleted=False).all()
    #     books_query = self.get_queryset()
    #     # book_ser = BookModelSerializer(instance=books_query, many=True)
    #     book_ser = self.get_serializer(instance=books_query, many=True)
    #     return APIResponse(results=book_ser.data)

    # 单查
    def get(self, request):
        # books_query = models.Book.objects.filter(is_deleted=False).all()
        books_query = self.get_object()
        # book_ser = BookModelSerializer(instance=books_query, many=True)
        book_ser = self.get_serializer(instance=books_query)
        return APIResponse(results=book_ser.data)


class BookListGenericAPIView(GenericAPIView):
    queryset = models.Book.objects.filter(is_deleted=False)
    serializer_class = BookModelSerializer

    # # 群查
    # def get(self, request, *args, **kwargs):
    #     return self.list(self, request, *args, **kwargs)

    # 单查
    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        books_query = self.get_queryset()
        book_ser = self.get_serializer(instance=books_query, many=True)
        return APIResponse(results=book_ser.data)

    def retrieve(self, request, *args, **kwargs):
        books_query = self.get_object()
        book_ser = self.get_serializer(instance=books_query)
        return APIResponse(results=book_ser.data)


from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin


class BookListMixinsAPIView(RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin,
                            GenericAPIView):
    queryset = models.Book.objects.filter(is_deleted=False)
    serializer_class = BookModelSerializer

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            response = self.retrieve(request, *args, *kwargs)
        else:
            # return self.list(request, *args, **kwargs)
            # mixins提供的list方法的响应对象是Response,想将该对象格式化为APIResponse(自己二次封装的Response类)
            response = self.list(request, *args, *kwargs)
        # response的数据都存放在response.data中
        return APIResponse(results=response.data)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, *kwargs)
        return APIResponse(results=response.data)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, *kwargs)
        return APIResponse(results=response.data)

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, *kwargs)
        return APIResponse(results=response.data)


# 工具视图
# 1）工具视图都是GenericAPIView的子类，且不同的子类继承了不同的工具类，重写了请求方法
# 2）工具视图的功能如果直接可以满足需求，只需要继承工具视图，提供queryset与serializer_class即可

from rest_framework.generics import ListCreateAPIView


class BookListCreateAPIView(ListCreateAPIView):
    queryset = models.Book.objects.filter(is_deleted=False)
    serializer_class = BookModelSerializer


# 视图集
# 1）视图集都是优先继承ViewSetMixin类，再继承一个视图类(GenericAPIView或APIView)
# GenericViewSet、ViewSet
# 2) ViewSetMixin提供了重写的as_view()方法，继承视图集的视图类，配置路由时调用as_view()必须传入 请求-函数名 映射关系字典
#       eg: url(r'v6/books/$', views.BookGenericViewSet.as_view({'get': 'my_get_list'})),
#       表示get请求会交给my_get_list视图函数处理
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


class BookGenericViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = models.Book.objects.filter(is_deleted=False)
    serializer_class = BookModelSerializer

    def my_get_list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def my_get_obj(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# GenericAPIView与APIView两大继承视图的区别
'''
1）GenericViewSet和ViewSet都继承了ViewSetMixin，as_view都可以配置 请求-函数 映射
2）GenericViewSet继承的是GenericAPIView视图类，用来完成标准的 model 类操作接口
3）ViewSet继承的是APIView视图类，用来完成不需要 model 类参与，或是非标准的 model 类操作接口
      post请求在标准的 model 类操作下就是新增接口，登陆的post不满足
      post请求验证码的接口，不需要 model 类的参与
案例：登陆的post请求，并不是完成数据的新增，只是用post提交数据，得到的结果也不是登陆的用户信息，而是登陆的认证信息
'''

# 视图集子类分析-ModelViewSet
# 拥有六大接口：单查、群查、单增、单删、单整体该、单局部改
from rest_framework.viewsets import ModelViewSet


class BookModelViewSet(ModelViewSet):
    queryset = models.Book.objects.filter(is_deleted=False)
    serializer_class = BookModelSerializer

    # 删不是数据库，而是该记录中的删除字段
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return APIResponse(201, '删除失败')
        instance.is_deleted = True
        instance.save()  # 逻辑删除
        return APIResponse(200, '删除成功')

    # def perform_destroy(self, instance):
    #     instance.delete()  # 物理删除
