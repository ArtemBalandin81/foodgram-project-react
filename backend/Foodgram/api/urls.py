from django.conf.urls import url
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                    ShoppingViewSet, TagViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'recipes', RecipeViewSet, basename='ingredients')


app_name = 'api'
urlpatterns = [
    path('', include(router_v1.urls)),
    path('recipes/<int:recipe_id>/favorite/', FavoriteViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    }), name='favorite'),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    }), name='favorite'),
]
