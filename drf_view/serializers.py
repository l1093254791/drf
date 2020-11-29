from rest_framework import serializers, exceptions
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, ListSerializer

from pimordial_drf import models


class BookListSerializer(ListSerializer):
    def update(self, instance, validated_data):
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance


class BookModelSerializer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = ('name', 'price', 'img', 'author_list', 'publish_name', 'publish', 'authors')

        extra_kwargs = {
            'name': {
                'required': True,
                'min_length': 1,
                'error_messages': {
                    'required': '必填项',
                    'min_length': '太短',
                }
            },
            'publish': {
                'write_only': True
            },
            'authors': {
                'write_only': True
            },
            'img': {
                'read_only': True,
            },
            'author_list': {
                'read_only': True,
            },
            'publish_name': {
                'read_only': True,
            }
        }
        list_serializer_class = BookListSerializer

    def validate_name(self, value):
        # 书名不能包含 g 字符
        if 'g' in value.lower():
            raise ValidationError('该g书不能出版')
        return value

    def validate(self, attrs):
        publish = attrs.get('publish')
        name = attrs.get('name')
        if models.Book.objects.filter(name=name, publish=publish):
            raise ValidationError({'book': '该书已存在'})
        return attrs
