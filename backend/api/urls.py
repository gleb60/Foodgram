from django.urls import include, path
from rest_framework import routers
from users.views import SubscriptionView, SubscribeView
from recipes.views import (
    RecipesViewSet, TagsViewSet, IngredientsViewSet, FavoriteView,
)

router = routers.DefaultRouter()

router.register(r'recipes', RecipesViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'ingredients', IngredientsViewSet)

urlpatterns = [
    path('users/subscriptions/', SubscriptionView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view()),
    path('recipes/<int:favorite_id>/favorite/', FavoriteView.as_view()),
]