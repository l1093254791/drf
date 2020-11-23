"""drf_Source_code URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static, serve

from rest_framework.documentation import include_docs_urls

# 使用自动URL路由连接我们的API。
# 另外，我们还包括支持浏览器浏览API的登录URL。
urlpatterns = [
    path('admin/', admin.site.urls),
    # 接口文档
    path(r'docs/', include_docs_urls(title='接口文档')),
]

urlpatterns += [
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'', include('pimordial_django.urls')),
    path(r'', include('pimordial_drf.urls')),
    # 找图片
    re_path(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})
]
# # 找图片
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
