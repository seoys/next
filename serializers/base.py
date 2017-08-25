from django_api_standard import const
from django_api_standard.serializers.fields import DomTFField
from django_api_standard.utils.datetime import get_datetime
from rest_framework import serializers
from contents.models.model import Post
from contents.models.model import PostLink
from contents.models.model import PostText
from contents.models.model import PostTypeMapping
from contents.models.model import Series
from contents.models.model import SeriesPostMapping


class PostTypeMappingSerializer(serializers.ModelSerializer):
    """
    포스트 타입별 모듈 매핑 시리얼라이즈
    """
    type_no = serializers.IntegerField(
        read_only=True, help_text='포스트 타입 매핑'
    )
    table_type = serializers.CharField(
        min_length=None, max_length=30, help_text='테이블 타입별 명칭'
    )
    types_seq_no = serializers.IntegerField(
        help_text='테이블 타입별 고유번호'
    )
    insert_timestamp = serializers.DateTimeField(
        help_text='등록일', default=get_datetime
    )
    updated_timestamp = serializers.DateTimeField(
        help_text='수정일'
    )
    align_no = serializers.IntegerField(
        help_text='정렬 순서'
    )
    is_deleted = DomTFField(
        help_text='삭제구분', default=const.FALSE,
    )

    class Meta:
        model = PostTypeMapping
        fields = '__all__'


class PostLinkSerializer(serializers.ModelSerializer):
    link_no = serializers.IntegerField(
        read_only=True, help_text='링크타입 고유번호'
    )
    type_no = serializers.IntegerField(
        help_text='포스트타입고유번호'
    )
    post_no = serializers.IntegerField(
        help_text='포스트고유번호', write_only=True
    )
    link_contents = serializers.CharField(
        min_length=1, max_length=1000, help_text='설명'
    )
    link_url = serializers.CharField(
        min_length=1, max_length=100, help_text='링크URL'
    )
    is_deleted = DomTFField(
        help_text='삭제구분', default=const.FALSE,
    )
    align_no = serializers.IntegerField(
        help_text='정렬순서'
    )

    table_type = serializers.SerializerMethodField("get_link_type")
    item_no = serializers.SerializerMethodField("get_link_title")

    def get_link_type(self, obj):
        return obj.link_type

    def get_link_title(self, obj):
        return obj.link_title

    class Meta:
        model = PostLink
        fields = (
            "link_no", "type_no", "post_no", "link_contents", "link_url",
            "is_deleted", "align_no", "table_type", "item_no"
        )



class PostSerializer(serializers.ModelSerializer):
    """
    포스트 Serializer    
    """
    post_no = serializers.IntegerField(
        read_only=True, help_text='포스트 고유번호'
    )
    post_type = serializers.ChoiceField(
        choices=Post.POST_TYPE_CHOICE, help_text='포스트 타입'
    )
    item_no = serializers.IntegerField(
        read_only=True, help_text='상품코드 고유번호'
    )
    view_start_timestamp = serializers.DateTimeField(
        help_text='노출기간 시작일'
    )
    view_end_timestamp = serializers.DateTimeField(
        help_text='노출기간 종료일'
    )
    is_view_end = DomTFField(
        help_text='종료일 설정 구분', default=const.TRUE
    )
    post_title = serializers.CharField(
        min_length=1, max_length=100, help_text='타이틀'
    )
    post_text = serializers.CharField(
        min_length=1, max_length=1000, help_text='포스트 설명'
    )
    is_text = serializers.CharField(
        help_text='텍스트 노출여부', default=const.FALSE
    )
    video_type = serializers.ChoiceField(
        choices=Post.VIDEO_TYPE_CHOICE, help_text='영상 타입'
    )
    video_url = serializers.URLField(
        max_length=100, min_length=1, help_text='영상 URL'
    )
    pc_url = serializers.URLField(
        max_length=100, min_length=1, help_text='PC 내용'
    )
    mobile_url = serializers.URLField(
        max_length=100, min_length=1, help_text='Mobile 내용'
    )
    insert_timestamp = serializers.DateTimeField(
        help_text='등록일', read_only=True, default=get_datetime
    )
    is_deleted = DomTFField(
        help_text='삭제 구분', default=const.FALSE
    )
    manager_name = serializers.CharField(
        min_length=1, max_length=30, help_text='담당자명'
    )
    is_apply_end = DomTFField(
        help_text='종료일 구분', default=const.FALSE
    )
    gift_no = serializers.IntegerField(
        help_text='사은품 고유번호'
    )
    video_running_time = serializers.IntegerField(
        help_text='비디오 런링타임'
    )
    post_type_list = PostTypeMappingSerializer(
        required=False, many=True
    )

    post_link_list = PostLinkSerializer(
        required=False, many=True
    )

    class Meta:
        model = Post
        fields = (
            'post_no',
            'post_type',
            'item_no',
            'view_start_timestamp',
            'view_end_timestamp',
            'is_view_end',
            'post_title',
            'post_text',
            'is_text',
            'video_type',
            'video_url',
            'pc_url',
            'mobile_url',
            'insert_timestamp',
            'is_deleted',
            'manager_name',
            'is_apply_end',
            'gift_no',
            'video_running_time',
            'post_type_list',
            'post_link_list'
        )


class SeriesPostMappingSerializer(serializers.ModelSerializer):
    """
    Series & Post 연계 Serializer
    """
    connect_no = serializers.IntegerField(
        help_text='시리즈 커넥팅 테이블 고유번호'
    )
    series_no = serializers.IntegerField(
        read_only=True, help_text='포스트 타입 고유번호'
    )
    post_no = serializers.IntegerField(
        read_only=True, help_text='포스트 고유번호'
    )
    insert_timestamp = serializers.DateTimeField(
        help_text='등록일', default=get_datetime
    )
    is_deleted = DomTFField(
        help_text='삭제 구분'
    )

    class Meta:
        model = SeriesPostMapping
        read_only_fields = ('connect_no',)
        fields = "__all__"


class SeriesSerializer(serializers.ModelSerializer):
    """
    시리즈 Serializer
    """
    series_no = serializers.IntegerField(
        read_only=True, help_text='시리즈 고유번호'
    )
    list_no = serializers.IntegerField(
        help_text='리스트 고유번호'
    )
    series_title = serializers.CharField(
        min_length=None, max_length=100, help_text='타이틀'
    )
    apply_start_timestamp = serializers.DateTimeField(
        help_text='적용기간 시작일'
    )
    apply_end_timestamp = serializers.DateTimeField(
        help_text='적용기간 종료일'
    )
    is_apply_end = DomTFField(
        default=const.FALSE, help_text='종료일 설정 구분'
    )
    is_use = DomTFField(
        default=const.TRUE, help_text='사용 구분'
    )
    insert_timestamp = serializers.DateTimeField(
        help_text='등록일', default=get_datetime
    )
    is_deleted = DomTFField(
        default=const.FALSE, help_text='삭제 구분'
    )

    class Meta:
        model = Series
        read_only_fields = ('series_no',)
        fields = "__all__"



class PostTextSerializer(serializers.ModelSerializer):
    text_no = serializers.IntegerField(
        help_text='텍스트 타입 고유번호'
    )
    type_no = serializers.IntegerField(
        help_text = '포스트_타입_맵핑 고유번호'
    )
    post_no = serializers.IntegerField(
        help_text = '포스트 고유번호'
    )
    text_html_contents = serializers.CharField(
        max_length=1000, help_text='내용 텍스트(HTML)'
    )
    text_contents = serializers.CharField(
        max_length=1000, help_text='내용 텍스트'
    )
    insert_timestamp = serializers.DateTimeField(
        help_text = '등록일'
    )
    updated_timestamp = serializers.DateTimeField(
        help_text = '수정일'
    )
    is_deleted = serializers.CharField(
        help_text='삭제 구분'
    )
    text_html_title = serializers.CharField(
        max_length=100, help_text='포스트 타이틀(HTML)'
    )
    text_title = serializers.CharField(
        max_length=100, help_text='포스트 타이틀'
    )

    class Meta:
        model = PostText
        fields = (
            'text_no', 'type_no', 'post_no', 'text_html_contents',
            'text_contents', 'insert_timestamp', 'updated_timestamp',
            'is_deleted', 'text_html_title', 'text_title'
        )