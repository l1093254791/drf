# -*- coding: utf-8 -*_ #
from django.conf.urls import url
from pimordial_django import views

urlpatterns = [
    url(r'^category/$', views.CategoryView.as_view()),
    url(r'^category/(?P<pk>\d+)/$', views.CategoryView.as_view())
]
