from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Ingredient, Recipe, RecipeFavorite,
                            RecipeIngredient, ShoppingCart, Tag)
from recipes.pagination import RecipesResultsPagination
from recipes.permissions import IsOwnerOrReadOnly
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import Subscription, User

from api.filters import RecipeFilter
from api.serializers import (FavoriteDeleteSerializer, FavoriteSerializer,
                             IngredientsSerializer, RecipeGetSerializer,
                             RecipePostPatchDelSerializer,
                             ShoppingChartSerializer, TagSerializer)

from .serializers import SubscribeSerializer, SubscriptionSerializer


class SubscriptionView(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        authors = User.objects.filter(subscribing__user=user)
        object = self.paginate_queryset(authors)
        serializer = SubscriptionSerializer(
            object,
            many=True,
            context={'request': request}
        )

        return self.get_paginated_response(serializer.data)


class SubscribeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['post', 'delete']

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def subscribe(self, request, pk):
        user = request.user
        data = {
            'author': pk,
            'user': user.pk,
        }
        serializer = SubscribeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def unsubscribe(self, request, pk):
        user = request.user
        subscribe = Subscription.objects.filter(author=pk, user=user)
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsOwnerOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = RecipesResultsPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeGetSerializer

        return RecipePostPatchDelSerializer


class ShoppingCartViewSet(ModelViewSet):
    # queryset = ShoppingCart.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        queryset = ShoppingCart.objects.filter(user=current_user)
        return queryset

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                    recipe_buy=recipe,
                    user=user,
            ).exists():
                raise ValidationError('Рецепт уже в списке покупок.')
            ShoppingCart.objects.create(
                recipe_buy=recipe,
                user=user,
            )
            serializer = ShoppingChartSerializer(recipe)

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            shopping_cart = get_object_or_404(
                ShoppingCart,
                recipe_buy=recipe,
                user=user,
            )
            shopping_cart.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

    def download_shopping_cart(self, request):
        ingredient_list = 'Ваш список ингредиентов: '
        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__shopping_cart__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
        )

        for ingredient in ingredients:
            ingredient_list += (
                f"\n{ingredient['ingredient__name']}"
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['amount']}")

        return HttpResponse(ingredient_list, content_type='application')


class TagsViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class IngredientsViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = None
    permission_classes = [AllowAny]
    search_fields = ('^name',)


class FavoriteViewSet(ModelViewSet):
    queryset = RecipeFavorite.objects.all()
    permission_classes = [IsAuthenticated]

    def create_favorite(self, request, favorite_id):
        user = request.user
        data = {
            'favorite_recipe': favorite_id,
            'user': user.id,
        }

        serializer = FavoriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_favorite(self, request, favorite_id):
        user = request.user

        data = {
            'favorite_recipe': favorite_id,
            'user': user.id,
        }
        serializer = FavoriteDeleteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        subscribe = RecipeFavorite.objects.filter(
            favorite_recipe=favorite_id,
            user=user,
        )
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
