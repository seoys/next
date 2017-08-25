from django.db import models
from django_api_standard import const
from django_api_standard.models import fields
from django_api_standard.models.base import DeletedModelMixin
from django_api_standard.models.base import InsertTimestampModelMixin


class Series(InsertTimestampModelMixin, DeletedModelMixin):
    """
    시리즈 테이블
    """
    series_no = models.BigAutoField(
        primary_key=True, help_text='시리즈 고유번호', verbose_name='시리즈 고유번호'
    )
    list_no = models.BigDecimalField(
        help_text='리스트 고유번호', verbose_name='리스트 고유번호'
    )
    series_title = models.CharField(
        max_length=100, help_text='타이틀', verbose_name='타이틀'
    )
    apply_start_timestamp = models.DateTimeField(
        help_text='적용기간 시작일', verbose_name='적용기간 시작일'
    )
    apply_end_timestamp = models.DateTimeField(
        help_text='적용기간 종료일', verbose_name='적용기간 종료일'
    )
    is_apply_end = fields.DomTFField(
        default=const.FALSE, help_text='종료일 설정 구분',
        verbose_name='종료일 설정 구분'
    )
    is_use = fields.DomTFField(
        default=const.FALSE, help_text='사용구분', verbose_name='사용구분'
    )

    class Meta:
        managed = False
        db_table = 'contents\".\"t_series'
        ordering = ['-series_no']


class Post(InsertTimestampModelMixin, DeletedModelMixin):
    """
    포스트 테이블
    """
    POST_TYPE_CHOICE = (
        ('default', 'default'),
        ('video', 'video'),
        ('showcase', 'showcase'),
        ('pt', 'pt'),
        ('html', 'html'),
    )

    ADD_ON_TYPE_CHOICE = (
        ('only', '단독'),
        ('first', '선발매'),
        ('gift', '사은품'),
        ('comment', '코멘트'),
    )

    VIDEO_TYPE_CHOICE = (
        ('youtube', 'youtube'),
        ('vimeo', 'vimeo'),
    )

    post_no = models.BigAutoField(
        primary_key=True, help_text='포스트 고유번호', verbose_name='포스트 고유번호'
    )
    post_type = models.CharField(
        max_length=10, choices=POST_TYPE_CHOICE, default=POST_TYPE_CHOICE[0][0],
        help_text='포스트 타입', verbose_name='포스트 타입'
    )
    item_no = models.BigDecimalField(
        blank=True, null=True, help_text='상품코드 고유번호',
        verbose_name='상품코드 고유번호'
    )
    view_start_timestamp = models.DateTimeField(
        help_text='노출기간 시작일', verbose_name='노출기간 시작일'
    )
    view_end_timestamp = models.DateTimeField(
        help_text='노출기간 종료일',
        verbose_name='노출기간 종료일')
    is_view_end = fields.DomTFField(
        default=const.FALSE, help_text='종료일 설정 구분',
        verbose_name='종료일 설정 구분'
    )
    add_on_type = models.CharField(
        max_length=30, blank=True, null=True, choices=ADD_ON_TYPE_CHOICE,
        help_text='추가기능 구분', verbose_name='추가기능 구분'
    )
    sale_value = models.DecimalField(
        blank=True, null=True, help_text='할인율', verbose_name='할인율'
    )
    apply_start_timestamp = models.DateTimeField(
        blank=True, null=True, help_text='응모기간 시작일',
        verbose_name='응모기간 시작일'
    )
    apply_end_timestamp = models.DateTimeField(
        blank=True, null=True, help_text='응모기간 종료일',
        verbose_name='응모기간 종료일'
    )
    is_apply_end = fields.DomTFField(
        default=const.FALSE, help_text='응모기간 종료일 설정 구분',
        verbose_name='응모기간 종료일 설정 구분'
    )
    post_title = models.CharField(
        max_length=100, blank=True, null=True, help_text='타이틀',
        verbose_name='타이틀'
    )
    post_text = models.CharField(
        max_length=300, blank=True, null=True, help_text='포스트 설명',
        verbose_name='포스트 설명'
    )
    is_text = fields.DomTFField(
        max_length=1, help_text='텍스트 노출여부', verbose_name='텍스트 노출여부'
    )
    video_type = models.CharField(
        max_length=10, blank=True, null=True, choices=VIDEO_TYPE_CHOICE,
        help_text='영상 타입', verbose_name='영상 타입'
    )
    video_url = models.URLField(
        max_length=100, blank=True, null=True, help_text='영상 URL',
        verbose_name='영상 URL'
    )
    pc_url = models.URLField(
        max_length=100, blank=True, null=True, help_text='PC내용 ',
        verbose_name='PC내용 '
    )
    mobile_url = models.URLField(
        max_length=100, blank=True, null=True, help_text='Mobile내용',
        verbose_name='Mobile내용'
    )
    manager_name = models.CharField(
        max_length=30, help_text='담당자명', verbose_name='담당자명'
    )
    gift_no = models.BigDecimalField(
        help_text='사은품 고유번호', verbose_name='사은품 고유번호'
    )

    video_running_time = models.DecimalField(
        help_text='비디오 런닝 타임', verbose_name='비디오 런닝 타임'
    )

    class Meta:
        managed = False
        db_table = 'contents\".\"t_post'
        ordering = ['-post_no']


class SeriesPostMapping(InsertTimestampModelMixin, DeletedModelMixin):
    """
    시리즈와 포스트 맵핑 테이블
    """
    connect_no = models.BigAutoField(
        primary_key=True, help_text='시리즈 커넥팅 테이블 고유번호',
        verbose_name='시리즈 커넥팅 테이블 고유번호'
    )
    series_no = models.ForeignKey(
        Series, db_column='series_no', related_name="related_series",
        help_text='시리즈 고유번호', verbose_name='시리즈 고유번호'
    )
    post_no = models.ForeignKey(
        Post, db_column='post_no', related_name="related_post",
        help_text='포스트 고유번호', verbose_name='포스트 고유번호', default=None
    )

    class Meta:
        managed = False
        db_table = "contents\".\"t_series_post_mapping"
        ordering = ['-connect_no']


class PostLink(DeletedModelMixin):
    link_no = models.BigAutoField(
        primary_key=True, help_text='링크타입고유번호', verbose_name='링크타입고유번호'
    )
    type_no = models.BigDecimalField(
        help_text='포스트타입고유번호', verbose_name='포스트타입고유번호'
    )
    post_no = models.ForeignKey(
        Post, db_column='post_no', related_name='post_link_list',
        help_text='포스트고유번호', verbose_name='포스트고유번호'
    )
    link_type = models.CharField(
        max_length=30, help_text='링크타입구분', verbose_name='링크타입구분')
    link_title = models.CharField(
        max_length=100, help_text='타이틀명', verbose_name='타이틀명')
    link_contents = models.CharField(
        max_length=1000, blank=True, null=True, help_text='설명',
        verbose_name='설명'
    )
    link_url = models.CharField(
        max_length=100, help_text='링크URL', verbose_name='링크URL'
    )
    align_no = models.SmallDecimalField(
        help_text='정렬순서', verbose_name='정렬순서'
    )

    class Meta:
        managed = False
        db_table = "contents\".\"t_post_link"
        ordering = ['align_no']


class PostTypeMapping(InsertTimestampModelMixin, DeletedModelMixin):
    type_no = models.BigDecimalField(
        primary_key=True, help_text='포스트 타입 매핑', verbose_name='포스트 타입 매핑'
    )
    post_no = models.ForeignKey(
        Post, db_column='post_no', related_name='post_type_list'
    )
    table_type = models.CharField(
        max_length=30, help_text='테이블 타입별 명칭', verbose_name='테이블 타입별 명칭'
    )
    types_seq_no = models.BigDecimalField(
        help_text='테이블 타입별 고유번호', verbose_name='테이블 타입별 고유번호'
    )
    updated_timestamp = models.DateTimeField(
        help_text='수정일', verbose_name='수정일'
    )
    align_no = models.SmallDecimalField(
        help_text='정렬 순서', verbose_name='정렬 순서'
    )

    class Meta:
        managed = False
        db_table = "contents\".\"t_post_type_mapping"
        ordering = ['align_no']


class PostText(models.Model):
    """
    컨텐츠 텍스트 타입
    """
    text_no = models.BigAutoField(
        primary_key=True, help_text='텍스트 타입 고유번호',
        verbose_name='텍스트 타입 고유번호'
    )
    type_no = models.ForeignKey(
        PostTypeMapping, help_text='포스트_타입_맵핑 고유번호',
        verbose_name='포스트_타입_맵핑 고유번호'
    )
    post_no = models.BigDecimalField(
        help_text='포스트 고유번호', verbose_name='포스트 고유번호'
    )
    text_html_contents = models.CharField(
        max_length=1000, blank=True, null=True, help_text='내용 텍스트(HTML)',
        verbose_name='내용 텍스트(HTML)'
    )
    text_contents = models.CharField(
        max_length=1000, blank=True, null=True, help_text='내용 텍스트',
        verbose_name='내용 텍스트'
    )
    insert_timestamp = models.DateTimeField(
        help_text = '등록일', verbose_name='등록일'
    )
    updated_timestamp = models.DateTimeField(
        help_text = '수정일', verbose_name='수정일'
    )
    is_deleted = models.CharField(
        help_text='삭제 구분', verbose_name='삭제 구분'
    )
    text_html_title = models.CharField(
        max_length=100, blank=True, null=True, help_text='포스트 타이틀(HTML)',
        verbose_name='포스트 타이틀(HTML)'
    )
    text_title = models.CharField(
        max_length=100, blank=True, null=True, help_text='포스트 타이틀',
        verbose_name='포스트 타이틀'
    )

    class Meta:
        managed = False
        db_table = "contents\".\"t_post_text"
        ordering = ['text_no']