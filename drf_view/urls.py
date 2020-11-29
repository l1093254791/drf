from . import views
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('v1/books/', views.BookListView.as_view()),
    re_path(r'^v1/books/(?P<pk>.*)/$', views.BookListView.as_view()),

    path('v2/books/', views.BookGenericAPIView.as_view()),
    re_path(r'^v2/books/(?P<pk>.*)/$', views.BookGenericAPIView.as_view()),

    path('v3/books/', views.BookListGenericAPIView.as_view()),
    re_path(r'^v3/books/(?P<pk>.*)/$', views.BookListGenericAPIView.as_view()),

    path('v4/books/', views.BookListMixinsAPIView.as_view()),
    re_path(r'^v4/books/(?P<pk>.*)/$', views.BookListMixinsAPIView.as_view()),

    path('v5/books/', views.BookListCreateAPIView.as_view()),
    re_path(r'^v5/books/(?P<pk>.*)/$', views.BookListCreateAPIView.as_view()),

    # View的as_view():将get请求映射到视图类的get方法
    # ViewSet的as_view(('get': 'my_get_list'):将get请求映射到视图类的my_get_list方法
    path('v6/books/', views.BookGenericViewSet.as_view({'get': 'my_get_list'})),
    re_path(r'^v6/books/(?P<pk>.*)/$', views.BookGenericViewSet.as_view({'get': 'my_get_obj'})),

    path('v7/books/', views.BookModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^v7/books/(?P<pk>.*)/$',
            views.BookModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
                                            'delete': 'destroy'})),
]

from django.conf.urls import include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
# 所有路由与ViewSet视图类的都可以注册，会产生 '^v6/books/$' 和 '^v6/books/(?P<pk>[^/.]+)/$'
router.register('v7/books', views.BookModelViewSet)

urlpatterns += [
    # 第一种添加子列表方式
    re_path(r'^', include(router.urls)),
]
# 第二种添加子列表方式
# urlpatterns.extend(router.urls)
