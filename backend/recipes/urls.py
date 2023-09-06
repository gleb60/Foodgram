from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import RecipeViewSet, TagsViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
