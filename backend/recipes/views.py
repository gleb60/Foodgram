from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Recipe, Tag, Ingredient, RecipeFavorite, ShoppingCart, RecipeIngredient,
)
from .pagination import RecipesResultsPagination
from .permissions import IsAuthorOrAdmin
from .serializers import (
    RecipeGetSerializer, TagSerializer, IngredientsSerializer,
    RecipePostPatchDelSerializer, FavoriteSerializer, ShoppingChartSerializer,
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

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, request, pk)
        else:
            return self.delete_recipe(ShoppingCart, request, pk)

    def add_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if model.objects.filter(
                recipe_buy=recipe,
                user=user,
        ).exists():
            raise ValidationError('Рецепт уже в списке покупок.')
        model.objects.create(
            recipe_buy=recipe,
            user=user,
            # favorite_recipe=recipe.favorite_recipe,
        )
        serializer = ShoppingChartSerializer(recipe)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        shopping_cart = get_object_or_404(model, recipe_buy=recipe, user=user)
        shopping_cart.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('get',),
        serializer_class=RecipeGetSerializer,
        permission_classes=(IsAuthenticated,),
    )
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
    pagination_class = None
    permission_classes = [AllowAny]
    search_fields = ('^name',)


class FavoriteView(APIView):
    def post(self, request, favorite_id):
        user = request.user
        data = {
            'favorite_recipe': favorite_id,
            'user': user.id,
        }
        if RecipeFavorite.objects.filter(
                favorite_recipe=favorite_id,
                user=user,
        ).exists():
            raise ValidationError('Рецепт уже в избранном.')

        serializer = FavoriteSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, favorite_id):
        user = request.user

        if not RecipeFavorite.objects.filter(
                favorite_recipe=favorite_id,
                user=user,
        ).exists():
            raise ValidationError('Такого лайка еще нет.')

        subscribe = RecipeFavorite.objects.filter(
            favorite_recipe=favorite_id,
            user=user,
        )
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
