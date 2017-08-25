import logging
from django.db import transaction
from django_api_standard import const
from django_api_standard.utils.datetime import get_datetime
from django_api_standard.serializers.fields import DomTFField
from rest_framework import serializers
from contents.models import model
from contents.serializers import base

logger = logging.getLogger('service')
logging.basicConfig(level=logging.DEBUG)


class CreateSeriesSerializers(base.SeriesSerializer):
    """
     시리즈 기본정보
     """
    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related()
        return queryset


class DetailSeriesSerializers(base.SeriesSerializer):
    """
    시리즈 > 연결된 포스트 리스트
    """
    post_count = serializers.SerializerMethodField()

    def get_post_count(self, obj):
        """
        연결된 포스트 총 수량
        """
        return model.SeriesPostMapping.objects.filter(
            series_no=obj.pk
        ).count()

    @transaction.atomic()
    def update(self, instance, validated_data):
        return instance

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related()
        return queryset

    class Meta:
        model = model.Series
        fields = (
            'series_no', 'list_no', 'series_title', 'apply_start_timestamp',
            'apply_end_timestamp', 'is_apply_end', 'is_use', 'insert_timestamp',
            'is_deleted', 'post_count'
        )


class ModifyPostSerializers(serializers.ModelSerializer):
    post_no = serializers.DecimalField(
        help_text='포스트고유번호'
    )
    link_type = serializers.CharField(
        min_length=1, max_length=30, help_text='링크타입구분'
    )
    link_title = serializers.CharField(
        min_length=1, max_length=100, help_text='타이틀명'
    )
    align_no = serializers.DecimalField(
        help_text='정렬순서'
    )

    class Meta:
        model = model.PostLink
        fields = (
            "post_no", "link_type", "link_title", "align_no"
        )


class DetailPostSerializers(base.PostSerializer):
    """
    포스트 > 포스트 기본정보 호출
    """
    post_no = serializers.DecimalField(
        read_only=False, write_only=True
    )
    related_post_link = base.PostLinkSerializer(
        many=True
    )
    post_image = serializers.SerializerMethodField()
    add_on_type = serializers.SerializerMethodField()
    header_info = serializers.SerializerMethodField()

    def get_link_type(self, obj):
        return obj.link_type

    def get_header_info(self, obj):
        post_type = obj.post_type
        dic = {}

        if post_type == 'default':
            dic['table_type'] = 'header_default'
            dic['cover_image'] = ''
            dic['is_text'] = obj.is_text
            dic['color_group'] = 'white'
        elif post_type == 'video':
            dic['table_type'] = 'header_video'
            dic['video_type'] = obj.video_type
            dic['video_url'] = obj.video_url
            dic['video_running_time'] = obj.video_running_time
            dic['image'] = dict(
                path="http://image.29cm.co.kr/contents/brand/201607/"
                     "20160729182121.jpg?cmd=thumb&width=300&height=300",
                ratio_w=1,
                ratio_h=1,
                width=800,
                height=600
            )
        elif post_type == 'html':
            dic['table_type'] = 'header_html'

        return dic

    def get_post_image(self, obj):
        """
        (임시) 썸네일 이미지
        """
        return dict(
            list_type=dict(
                path="http://image.29cm.co.kr/contents/brand/201607/"
                     "20160729182121.jpg?cmd=thumb&width=300&height=300",
                ratio_w=1,
                ratio_h=1,
                width=800,
                height=600
            ),
            banner_type=dict(
                path="http://image.29cm.co.kr/contents/brand/201607/"
                     "20160729182121.jpg?cmd=thumb&width=300&height=300",
                ratio_w=1,
                ratio_h=1,
                width=1200,
                height=800
            )
        )

    def get_add_on_type(self, obj):
        """
        (임시) 추가기능
        """
        return dict(
            benefits=obj.add_on_type,
            apply_start_timestamp=obj.apply_start_timestamp,
            apply_end_timestamp=obj.apply_end_timestamp,
            sale_value=obj.sale_value,
            is_apply_end=obj.is_apply_end,
            gift_no=obj.gift_no,
        )

    @transaction.atomic()
    def update(self, instance, validated_data):
        try:
            post_no = validated_data['post_no']
            video_type = validated_data['video_type']
            video_url = validated_data['video_url']
            related_post_link = validated_data['related_post_link']
        except ValueError as e:
            raise KeyError from e
        else:
            model.Post.objects.filter(post_no=post_no).update(
                video_type=video_type, video_url=video_url)

            for item in related_post_link:
                post_link_obj = model.Post.objects.get(pk=item["post_no"])
                post_link_dic = {
                    "post_no": post_link_obj,
                    "link_type": item["link_type"],
                    "link_title": item["link_title"],
                    "align_no": item["align_no"],
                    "is_deleted": "F",
                    "type_no": 0
                }
                model.PostLink.objects.create(**post_link_dic)

        return instance

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related()
        return queryset

    class Meta:
        model = model.Post
        fields = (
            'post_no', 'post_type', 'item_no', 'post_image',
            'view_start_timestamp', 'view_end_timestamp', 'is_view_end',
            'post_title', 'post_text', 'add_on_type', 'video_type', 'video_url',
            'header_info', 'related_post_link'
        )


class CreatePostSerializers(base.PostSerializer):
    """
    POST 기본정보
    """
    post_image = serializers.SerializerMethodField()
    heart_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    open_status = serializers.SerializerMethodField()
    add_on_type = serializers.SerializerMethodField()

    def get_post_image(self, obj):
        """
        (임시) 썸네일 이미지
        """
        return dict(
            list_type=dict(
                path="",
                ratio_w="",
                ratio_h="",
                width="",
                height=""
            ),
            banner_type=dict(
                path="",
                ratio_w="",
                ratio_h="",
                width="",
                height=""
            )
        )

    def get_add_on_type(self, obj):
        """
        (임시) 추가기능
        """
        return dict(
            benefits=obj.add_on_type,
            apply_start_timestamp=obj.apply_start_timestamp,
            apply_end_timestamp=obj.apply_end_timestamp,
            sale_value=obj.sale_value,
            is_apply_end=obj.is_apply_end,
            gift_no=obj.gift_no,
        )

    def get_heart_count(self, obj):
        """
        (임시) 하트 카운트
        """
        return 0

    def get_view_count(self, obj):
        """
        (임시) 뷰 카운트
        """
        return 0

    def get_open_status(self, obj):
        """
        글 현재 상태
        """
        # return get_diff_status(obj.apply_start_timestamp,
        #                        obj.apply_end_timestamp)

        return "F"

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related()
        return queryset

    @transaction.atomic()
    def create(self, validated_data):
        series_no = validated_data.pop('series_no')
        series_obj = model.Series.objects.get(pk=series_no)
        post = model.Post.objects.create(**validated_data)

        if not series_no:
            post_dic = {
                'series_no': series_obj,
                'post_no': post.post_no,
                'is_deleted': 'F',
            }

            model.SeriesPostMapping.objects.create(**post_dic)

        return post

    class Meta:
        model = model.Post
        fields = (
            'post_no', 'post_type', 'item_no', 'post_image',
            'view_start_timestamp', 'view_end_timestamp', 'is_view_end',
            'post_title', 'post_text', 'is_text', 'video_type', 'video_url',
            'pc_url', 'mobile_url', 'insert_timestamp', 'manager_name',
            'is_deleted', 'heart_count', 'view_count', 'open_status',
            'add_on_type', 'post_link'
        )


class ModifySeriesPostMappingSerializer(base.SeriesPostMappingSerializer):
    post_no = base.PostSerializer(
        many=False
    )
    series_no = base.Series()

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related()
        return queryset

    @transaction.atomic()
    def update(self, instance, validated_data):
        try:
            connect_no = validated_data['connect_no']
        except ValueError as e:
            raise KeyError from e
        else:
            model.SeriesPostMapping.objects.filter(connect_no=connect_no) \
                .update(is_deleted="T")

        return instance

    class Mate:
        model = model.SeriesPostMapping
        fields = "__all__"


class CreateSeriesPostMappingSerializer(serializers.ModelSerializer):
    """
    시리즈 포스트 맵핑 시리얼라이즈
    """
    connect_no = serializers.DecimalField(
        read_only=True, help_text='시리즈 커넥팅 테이블 고유번호'
    )
    series_no = serializers.DecimalField(
        help_text='포스트 타입 고유번호', write_only=True
    )
    post_no = serializers.DecimalField(
        help_text='포스트 고유번호', write_only=True
    )
    insert_timestamp = serializers.DateTimeField(
        help_text='등록일', default=get_datetime
    )
    is_deleted = DomTFField(
        help_text='삭제 구분', default=const.FALSE,
    )

    class Meta:
        model = model.SeriesPostMapping
        read_only_fields = ('connect_no',)
        fields = "__all__"

    @transaction.atomic()
    def create(self, validated_data):
        validated_data['series_no'] = model.Series.objects.get(
            pk=validated_data.pop('series_no'))
        validated_data['post_no'] = model.Post.objects.get(
            pk=validated_data.pop('post_no'))

        return model.SeriesPostMapping.objects.create(**validated_data)


class ListSeriesPostMappingSerializer(base.SeriesPostMappingSerializer):
    """
    시리즈 리스트 시리얼라이즈
    """
    post_no = base.PostSerializer(
        many=False
    )
    series_no = base.Series()

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related()
        return queryset

    class Meta:
        model = model.SeriesPostMapping
        fields = "__all__"


class ModifyPostLinkSerializer(base.PostLinkSerializer):
    """
    포스트링크 수정 시리얼라이즈
    """
    link_no = serializers.DecimalField(
        required=True
    )
    align_no = serializers.DecimalField(
        required=True
    )
    is_deleted = serializers.CharField(
        required=True
    )

    @transaction.atomic()
    def update(self, instance, validated_data):
        try:
            callback_data = validated_data
        except ValueError as e:
            raise KeyError from e
        else:
            link_no = callback_data['link_no']
            align_no = callback_data['align_no']
            is_deleted = callback_data['is_deleted']

            model.PostLink.objects.filter(link_no=link_no).update(
                align_no=align_no, is_deleted=is_deleted)

        return instance

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related()
        return queryset

    class Meta:
        model = model.PostLink
        fields = "__all__"



class NewPostListSerializer(base.PostSerializer):
    """
    (임시) 포스트 리스트 시리얼라이즈
    """
    post_image = serializers.SerializerMethodField()
    heart_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    open_status = serializers.SerializerMethodField()
    add_on_type = serializers.SerializerMethodField()

    def get_post_image(self, obj):
        """
        (임시) 썸네일 이미지
        """
        return dict(
            list_type=dict(
                path="",
                ratio_w="",
                ratio_h="",
                width="",
                height=""
            ),
            banner_type=dict(
                path="",
                ratio_w="",
                ratio_h="",
                width="",
                height=""
            )
        )

    def get_add_on_type(self, obj):
        """
        (임시) 추가기능
        """
        return dict(
            benefits=obj.add_on_type,
            apply_start_timestamp=obj.apply_start_timestamp,
            apply_end_timestamp=obj.apply_end_timestamp,
            sale_value=obj.sale_value,
            is_apply_end=obj.is_apply_end,
            gift_no=obj.gift_no,
        )

    def get_heart_count(self, obj):
        """
        (임시) 하트 카운트
        """
        return 0

    def get_view_count(self, obj):
        """
        (임시) 뷰 카운트
        """
        return 0

    def get_open_status(self, obj):
        """
        글 현재 상태
        """
        # return get_diff_status(obj.apply_start_timestamp,
        #                        obj.apply_end_timestamp)

        return "F"

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related()
        return queryset

    class Meta:
        model = model.Post
        fields = '__all__'
