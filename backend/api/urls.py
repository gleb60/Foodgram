from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from recipes.views import RecipesViewSet

router = DefaultRouter()
router.register(r'recipes', RecipesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
