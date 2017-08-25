import django_filters
from rest_framework import filters
from contents.models.model import Series
from contents.models.model import Post
from contents.models.model import SeriesPostMapping


class SeriesFilter(filters.FilterSet):
    """
    시리즈 필터
    """
    title = django_filters.CharFilter(
        name='series_title', lookup_expr='contains')

    class Meta:
        model = Series
        fields = [
            'series_title',
            'list_no'
        ]


class PostFilter(filters.FilterSet):
    """
    포스트 필터
    """
    post_title = django_filters.CharFilter(
        name='post_title', lookup_expr='contains'
    )
    manager_name = django_filters.CharFilter(
        name='manager_name', lookup_expr='contains'
    )
    post_type = django_filters.ChoiceFilter(
        choices=Post.POST_TYPE_CHOICE, name='post_type', lookup_expr='contains'
    )
    post_text = django_filters.CharFilter(
        name='post_text', lookup_expr='contains'
    )

    class Meta:
        model = Post
        fields = [
            'post_title',
            'manager_name',
            'post_type',
            'post_text'
        ]


class PostMappingFilter(filters.FilterSet):
    """
    포스트 맵핑 필터
    """
    series_no = django_filters.CharFilter(
        name='series_no', lookup_expr='icontains'
    )

    class Meta:
        model = SeriesPostMapping
        fields = [
            'series_no'
        ]
