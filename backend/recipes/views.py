from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Recipe, Tag, Ingredient, RecipeFavorite
from .pagination import RecipesResultsPagination

from .permissions import IsAuthorOrAdmin
from .serializers import (
    RecipeGetSerializer, TagSerializer, IngredientsSerializer,
    RecipePostPatchDelSerializer
)


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]
    filter_backends = (DjangoFilterBackend,)
    pagination_class = RecipesResultsPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeGetSerializer

        return RecipePostPatchDelSerializer


class TagsViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class IngredientsViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = [AllowAny]
    search_fields = ('^name',)
