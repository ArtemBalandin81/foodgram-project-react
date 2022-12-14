from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter


from djoser.views import UserViewSet
router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')


app_name = 'users'
urlpatterns = [
    path('', include(router_v1.urls)),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
