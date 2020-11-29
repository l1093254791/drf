from rest_framework import serializers, exceptions
from django.conf import settings

# DateTimeField与DateField（2020-11-22T16:14:46.107960Z）显示年月日时分秒
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer

from pimordial_drf import models


# 重点：ListSerializer与ModelSerializer建立关联的是： 在ModelSerializer的Meta类中设置   list_serializer_class
class V2BookListSerializer(ListSerializer):
    def update(self, instance, validated_data):  # print(instance)  # 要更新的对象们
        # print(validated_data)  # 更新的对象对应的数据们
        # print(self.child)  # 服务的模型序列化类 - V2BookModelSerializer
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance


class V2BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 序列化关联的model类
        model = models.Book
        list_serializer_class = V2BookListSerializer
        # 参与序列化的字段  —— 没有默认值的字段必须序列化，为其传值
        fields = ('name', 'price', 'img', 'author_list', 'publish_name', 'publish', 'authors')
        # extra_kwargs 用来完成反序列化字段的 系统校验规则
        # write_only：只反序列化
        # read_only：只序列化
        # 自定义字段默认只序列化(read_only)
        # 如果字段没设置write_only或者read_only，那么该字段可以序列化和反序列化
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

    # 局部钩子校验单个字段  validate_字段名
    def validate_name(self, value):  # value是字段name的值
        # 书名不能包含 g 字符
        if 'g' in value.lower():
            raise ValidationError('该g书不能出版')
        return value

    # 全局钩子
    def validate(self, attrs):
        publish = attrs.get('publish')  # publish如果是外键字段，这个就是publish对象
        name = attrs.get('name')
        if models.Book.objects.filter(name=name, publish=publish):
            raise ValidationError({'book': '该书已存在'})
        return attrs


class PublishModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publish
        fields = ('name', 'address')


class BookModelSerializer(serializers.ModelSerializer):
    # 1.还可以自定义设置序列化字段，但是必须在fields中声明,在fields中写publish_address
    # publish_address = serializers.SerializerMethodField
    #
    # def get_publish_address(self, obj):
    #     return obj.Publish.address

    # 2. 自定义连表深度---子序列化方式
    publish = PublishModelSerializer

    class Meta:
        # 序列化关联的model类
        model = models.Book
        # 参与序列化的字段
        fields = ('name', 'price', 'img', 'author_list', 'publish_name', 'publish')


class BookModelDeserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        # 没有默认值的字段必须序列化，为其传值
        fields = ('name', 'price', 'img', 'publish', 'authors')
        # extra_kwargs 用来完成反序列化字段的 系统校验规则
        extra_kwargs = {
            'img': {
                'required': True,  # 设置img字段必填
                'min_length': 10,
                'error_messages': {
                    'required': '必填项',
                    'min_length': '最少输入10位'
                }
            }
        }

        # 局部钩子校验单个字段  validate_字段名
        def validate_name(self, value):  # value是字段name的值
            # 书名不能包含 g 字符
            if 'g' in value.lower():
                raise ValidationError('该g书不能出版')
            return value

        # 全局钩子
        def validate(self, attrs):
            publish = attrs.get('publish')  # publish如果是外键字段，这个就是publish对象
            name = attrs.get('name')
            if models.Book.objects.filter(name=name, publish=publish):
                raise ValidationError({'book': '该书已存在'})
            return attrs

        # 注意：ModelSerializer类已经帮我们实现了 create 与 update 方法,不需要写create就能创建


'''
方式一：
    created_time = serializers.DateTimeField(format="%Y-%m-%d - %H:%M:%S")
方式二：
    REST_FRAMEWORK = {
        'DATETIME_FORMAT': "%Y-%m-%d - %H:%M:%S",
    }
方式三：
    views中
         def list(self, request, *args, **kwargs):
            response = super().list(request, *args, **kwargs)
            response.data['results'] = handle_env(response.data['results'])
            return response
    定义
        import re
        def handle_env(datas):
            datas_list = []
            for item in datas:
                mtch = re.search(r'(.*)T(.*)\..*?', item['created_time'])
                # 时间格式化
                item['created_time'] = mtch.group(1) + ' ' + mtch.group(2)
                datas_list.append(item)
            return datas_list

'''


# 序列化
class UserSerializer(serializers.Serializer):  # 创建一个序列化类
    name = serializers.CharField()
    phone = serializers.CharField()
    sex = serializers.IntegerField()
    icon = serializers.ImageField()
    created_time = serializers.DateTimeField()
    # created_time = serializers.DateTimeField(format="%Y-%m-%d - %H:%M:%S")

    # 自定义序列化属性
    '''
    属性名随意，值由固定的命名规范方法提供
    def get_属性名(self, 参与序列化的model对象):
        返回值就是自定义序列化属性的值
    '''

    gender = serializers.SerializerMethodField()

    def get_gender(self, obj):
        # choice类型的解释型值 get_字段_display() 来访问
        return obj.get_sex_display()

    icon1 = serializers.SerializerMethodField()

    def get_icon1(self, obj):
        # settings.MEDIA_URL: 自己配置的 /media/，给后面高级序列化与视图类准备的
        # obj.icon不能直接作为数据返回，因为内容虽然是字符串，但是类型是ImageFieldFile类型
        return '%s%s%s' % (r'http://127.0.0.1:8000', settings.MEDIA_URL, str(obj.icon))


# 反序列化
class UserDeserializer(serializers.Serializer):
    # 1) 哪些字段必须反序列化
    # 2) 字段都有哪些安全校验
    # 3) 哪些字段需要额外提供校验  钩子函数
    # 4) 哪些字段间存在联合校验
    # 注：反序列化字段都是用来入库的，不会出现自定义方法属性，会出现可以设置校验规则的自定义属性,不入数据库的
    name = serializers.CharField(
        max_length=64,
        min_length=3,

        error_messages={
            'max_length': '太长',
            'min_length': '太短'
        }
    )
    pwd = serializers.CharField()
    phone = serializers.CharField(required=False)
    sex = serializers.IntegerField(required=False)
    # 自定义有校验规则的反序列化字段,例如确认密码字段re_pwd
    re_pwd = serializers.CharField(required=True)

    # 局部钩子：validate_要校验的字段名(self, 当前要校验字段的值)
    # 校验规则：校验通过返回原值，校验失败，抛出异常
    def validate_name(self, value):
        if 'g' in value.lower():
            raise exceptions.ValidationError('名字非法')
        return value

    # 全局钩子：validate(self, 通过系统与局部钩子校验之后的所有数据)
    def validate(self, attrs):  # attrs是字典格式
        pwd = attrs.get('pwd')
        re_pwd = attrs.pop('re_pwd')  # 因为re_pwd不需要存入数据库，所以在全局钩子校验中删除掉这个字段
        if pwd != re_pwd:
            raise exceptions.ValidationError({'pwd&re_pwd': '两次密码不一致'})
        return attrs

    # 要完成新增，必须重写create方法，validated_data是校验的数据
    def create(self, validated_data):
        # 尽量在所有校验规则完毕之后，数据可以直接入库
        return models.User.objects.create(**validated_data)
 