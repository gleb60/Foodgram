from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from .models import (
    Recipe, Tag, Ingredient,  RecipeFavorite, RecipeIngredient, ShoppingChart,
)


class RecipeSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'time',
            'author', 'ingredients', 'description',
            'tags', 'image'
        )
        model = Recipe


class TagSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Tag


# class IngredientSerializer(ModelSerializer):
#     author = SlugRelatedField(slug_field='username', read_only=True)
#
#     class Meta:
#         fields = ('id', 'author', 'post', 'text', 'created')
#         model = Ingredient
#         read_only_fields = ('post',)