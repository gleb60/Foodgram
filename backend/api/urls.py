from django.urls import include, path
from rest_framework import routers

from api.views import (FavoriteViewSet, IngredientsViewSet, RecipesViewSet,
                       ShoppingCartViewSet, TagsViewSet)

from .views import SubscribeViewSet, SubscriptionView

router = routers.DefaultRouter()

router.register(r'recipes', RecipesViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'ingredients', IngredientsViewSet)

urlpatterns = [
    path('users/subscriptions/', SubscriptionView.as_view()),
    path('recipes/download_shopping_cart/',
         ShoppingCartViewSet.as_view({'get': 'download_shopping_cart'}),
         name='download_shopping_cart'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/', SubscribeViewSet.as_view({
        'post': 'subscribe',
        'delete': 'unsubscribe'
    })),
    path('recipes/<int:favorite_id>/favorite/',
         FavoriteViewSet.as_view(
             {'post': 'create_favorite',
              'delete': 'delete_favorite'
              })),
]
