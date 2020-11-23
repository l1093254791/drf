# -*- coding: utf-8 -*_ #
from . import views
from django.urls import path, re_path
from .views import test, users

urlpatterns = [
    path('test/', test.Test.as_view()),

    path('users/', users.User.as_view()),
    re_path(r'^users/(?P<pk>.*)/$', users.User.as_view()),
]
