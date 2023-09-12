from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (
    RecipesViewSet, TagsViewSet, IngredientsViewSet, FavoriteView,
)

router = DefaultRouter()
router.register(r'recipes', RecipesViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:favorite_id>/favorite/', FavoriteView.as_view()),
]
