from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import RecipeViewSet, TagsViewSet, IngredientsViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
