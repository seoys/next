from django_api_standard.pagination import DefaultLimitOffsetPagination
from django_api_standard.viewsets import ModelViewSet
from django_api_standard.viewsets import UpdateViewSet
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import list_route
from contents import filters as custom_filter
from contents.models.model import Post
from contents.models.model import PostTypeMapping
from contents.models.model import Series
from contents.models.model import PostLink
from contents.models.model import SeriesPostMapping
from contents.serializers import service
from contents.serializers import base


class SeriesViewSet(ModelViewSet):
    """
    시리즈 뷰셋
    """
    queryset = Series.objects.all().filter(is_deleted='F')
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, )
    filter_class = custom_filter.SeriesFilter

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'partial_update':
            return service.DetailSeriesSerializers
        else:
            return service.CreateSeriesSerializers

    def get_queryset(self):
        qs = Series.objects.all().filter(is_deleted='F')
        qs = self.get_serializer_class().setup_eager_loading(qs)

        return qs

    def list(self, request, *args, **kwargs):
        """
        series 리스트 
        """
        return super(SeriesViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        series 등록 
        """
        return super(SeriesViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        series 조회 
        """
        return super(SeriesViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        series 수정 
        """
        return super(SeriesViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        series 삭제 
        """
        return super(SeriesViewSet, self).destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        series 부분 수정 
        """
        return super(SeriesViewSet, self).partial_update(request,
                                                         *args, **kwargs)


class SeriesPostMappingViewSet(ModelViewSet):
    """
    시리즈 포스트 맵핑 뷰셋
    """
    queryset = SeriesPostMapping.objects.all().filter(is_deleted='F')
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, )
    filter_class = custom_filter.PostMappingFilter

    def get_serializer_class(self):
        print(self.action)
        if self.action == 'retrieve' or self.action == 'partial_update':
            return service.ModifySeriesPostMappingSerializer
        elif self.action == 'create':
            return service.CreateSeriesPostMappingSerializer
        else:
            return service.ListSeriesPostMappingSerializer

    def get_queryset(self):
        qs = SeriesPostMapping.objects.all().filter(is_deleted='F')
        qs = self.get_serializer_class().setup_eager_loading(qs)

        return qs

    def list(self, request, *args, **kwargs):
        """
        series 리스트 
        """
        return super(SeriesPostMappingViewSet, self).list(request,
                                                          *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        series 등록 
        """
        return super(SeriesPostMappingViewSet, self).create(request,
                                                            *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        series 조회 
        """
        return super(SeriesPostMappingViewSet, self).retrieve(request,
                                                              *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        series 수정 
        """
        return super(SeriesPostMappingViewSet, self).update(request,
                                                            *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        series 삭제 
        """
        return super(SeriesPostMappingViewSet, self).destroy(request,
                                                             *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        series 부분 수정 
        """
        return super(SeriesPostMappingViewSet, self).partial_update(request,
                                                                    *args, **kwargs)


class PostViewSet(ModelViewSet):
    """
    포스트 뷰셋
    """
    queryset = Post.objects.all().filter(is_deleted='F')
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, )
    filter_class = custom_filter.PostFilter

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'partial_update':
            return service.DetailPostSerializers
        else:
            return service.CreatePostSerializers

    def get_queryset(self):
        qs = Post.objects.all().filter(is_deleted='F')
        qs = self.get_serializer_class().setup_eager_loading(qs)

        return qs

    def list(self, request, *args, **kwargs):
        """
        Post 리스트
        """
        return super(PostViewSet, self).list(request, *args, **kwargs)

    # @list_route(methods=['get'], url_path='ps')
    # def app_list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     result = [
    #         {'post_info':serializer.data}
    #     ]
    #     return Response(result)

    def create(self, request, *args, **kwargs):
        """
        Post 등록
        """
        return super(PostViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Post 조회
        """
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
         Post 수정
        """
        return super(PostViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
         Post 삭제
        """
        return super(PostViewSet, self).destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
         Post 부분 수정
        """
        return super(PostViewSet, self).partial_update(request, *args, **kwargs)


class PostLinkViewSet(UpdateViewSet):
    """
     포스트 뷰셋
     """
    queryset = PostLink.objects.all().filter(is_deleted='F')
    pagination_class = DefaultLimitOffsetPagination

    def get_serializer_class(self):
        return service.ModifyPostLinkSerializer

    def get_queryset(self):
        qs = PostLink.objects.all().filter(is_deleted='F')
        qs = self.get_serializer_class().setup_eager_loading(qs)

        return qs

    def partial_update(self, request, *args, **kwargs):
        """
        포스트 링크 수정
        """
        return super(PostLinkViewSet, self).partial_update(
            request, *args, **kwargs)



class NewPostViewSet(ModelViewSet):
    # queryset = Post.objects.select_related().all()
    queryset = Post.objects.select_related().all()
    pagination_class = DefaultLimitOffsetPagination
    # filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    # filter_class = custom_filter.PostFilter

    def get_serializer_class(self):
        return service.NewPostListSerializer

    def get_queryset(self):
        qs = Post.objects.select_related().all()
        qs = self.get_serializer_class().setup_eager_loading(qs)

        return qs

    def list(self, request, *args, **kwargs):
        """
        Post 리스트
        """
        return super(NewPostViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Post 등록
        """
        return super(NewPostViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Post 조회
        """
        return super(NewPostViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
         Post 수정
        """
        return super(NewPostViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
         Post 삭제
        """
        return super(NewPostViewSet, self).destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
         Post 부분 수정
        """
        return super(NewPostViewSet, self).partial_update(request, *args, **kwargs)
