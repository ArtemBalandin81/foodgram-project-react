from django.conf.urls import url
from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet, SubscribeViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users/subscriptions', FollowViewSet, basename='follow')
router_v1.register(r'users', UserViewSet, basename='users')


app_name = 'users'
urlpatterns = [
    path('', include(router_v1.urls)),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    path('users/<int:user_id>/subscribe/', SubscribeViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    }), name='subscribe'),
]
