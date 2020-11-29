# -*- coding: utf-8 -*_ #
from . import views
from django.urls import path, re_path
from .views import test, users, books, v2books

urlpatterns = [
    path('test/', test.Test.as_view()),

    path('users/', users.User.as_view()),
    re_path(r'^users/(?P<pk>.*)/$', users.User.as_view()),
    # 书籍
    path('books/', books.Book.as_view()),
    re_path(r'^books/(?P<pk>.*)/$', books.Book.as_view()),
    # 出版社
    path('publish/', books.Publish.as_view()),
    re_path(r'^publish/(?P<pk>.*)/$', books.Publish.as_view()),

    path('v2books/', v2books.V2Book.as_view()),
    re_path(r'^v2books/(?P<pk>.*)/$', v2books.V2Book.as_view()),
]
