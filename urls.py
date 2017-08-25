from django.conf.urls import include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from contents import views

router = DefaultRouter()
router.register(r'series', views.SeriesViewSet)
router.register(r'post', views.PostViewSet)
router.register(r'npost', views.NewPostViewSet)
router.register(r'postmapping', views.SeriesPostMappingViewSet)
router.register(r'postlink', views.PostLinkViewSet)

urlpatterns = [
    url(r'^contents/', include(router.urls)),
]
